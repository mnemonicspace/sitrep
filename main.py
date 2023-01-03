from app.device_compile import cisco_compile, palo_compile
from app.nhmail import send_mail
from datetime import date, timedelta, datetime
from openpyxl import Workbook, load_workbook
import re
import xml.etree.ElementTree as ET
import os
import logging
import sys


def main():
    
    # initiate log file
    timestamp = f"{datetime.now().month}-{datetime.now().day}-{datetime.now().year}_{datetime.now().hour}:{datetime.now().minute}"
    logging.basicConfig(filename=f"logs/{timestamp}.log", level=logging.INFO)
    
    # create devices, log errors to log file
    try:
        palo_list = palo_compile()
    except Exception as e:
        logging.error("Could not compile paloalto.ini: {e}")
        sys.exit()
    
    try:
        cisco_list = cisco_compile()
    except Exception as e:
        logging.error("Could not compile cisco.ini: {e}")
        sys.exit()

    # set command to send to cisco devices
    palo_xpath = "<show><ha><state></state></ha></state>"
    cisco_command = "show standby brief"

    # run commands on devices and create dict of responses
    palo_data = {}
    try:
        for dev in palo_list:
            palo_data[dev.name] = ET.fromstring(dev.send_xpath(palo_xpath).content).find(
            'result').find('group').find('local-info').find('state').text
    except Exception as e:
        logging.error(f"Invalid response from Palo Alto device: {e}")
        sys.exit()
    
    cisco_data = {}
    try:
        for dev in cisco_list:
            cisco_data[dev.name] = re.findall(r"\A[^,]+?P (Active|Standby)", str(dev.send_cmd(cisco_command)))
    except Exception as e:
        logging.error("Invalid response from Cisco device: {e}")
        sys.exit()

    try:
        get_report(palo_data, cisco_data)
    except Exception as e:
        logging.error("Could not generate report: {e}")
        sys.exit()
    
    try:
        changed = compare(palo_data, cisco_data)
    except Exception as e:
        logging.error("Could not compare today's data to historical data: {e}")
        

    if len(changed) == 0:
        text = "No changes"
    else:
        text = "The following devices have changed state:\n\n" + \
            '\n'.join(changed)
    print(text)
    # send_mail(f"reports/{str(date.today())}-sitrep.xlsx", text)
    logging.info(f"Completed running at {datetime.now()}")


def get_report(palo, cisco):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Sitrep"
        ws.append(['Device Name', 'State'])
    except Exception as e:
        raise RuntimeError(f"Could not initialize workbook: {e}")

    try:
        for name, state in cisco.items():
            ws.append([name, state[0]])
    except Exception as e:
       raise RuntimeError(f"Could not add Cisco data to workbook: {e}")

    try:
        for name, state in palo.items():
            ws.append([name, state.title()])
    except Exception as e:
       raise RuntimeError(f"Could not add Palo Alto data to workbook: {e}") 

    try:
        wb.save(f"{os.getcwd()}/reports/{str(date.today())}-sitrep.xlsx")
    except Exception as e:
       raise RuntimeError(f"Could not save workbook: {e}")


def compare(palo, cisco):
    today = date.today()
    yesterday = today - timedelta(days=1)

    changed = []

    try:
        wb = load_workbook(f"reports/{str(yesterday)}-sitrep.xlsx")
        ws = wb["Sitrep"]
    except Exception as e:
        logging.error("Could not open previous report: {e}") 
        return ["Yesterday\'s sitrep not detected, see log file for details"]

    try:
        for row in range(1, 10):
            dev = ws[f"A{row}"].value
            old_state = ws[f"B{row}"].value
            if dev is None or old_state is None:
                continue
            if dev in cisco:
                state = cisco[dev][0]
            elif dev in palo:
                state = palo[dev]
            else:
                continue
            if state.lower() != old_state.lower():
                changed.append(dev)
    except Exception as e:
        logging.error("Could not parse previous report: {e}") 
        return ["Could not parse yesterday\'s sitrep, see log file for details"]

    return changed


if __name__ == "__main__":
    main()
