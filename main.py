from app.device_compile import cisco_compile, palo_compile
from app.mail import send_mail
from datetime import date, timedelta, datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
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
        logging.error(f"Could not compile paloalto.ini: {e}")
        sys.exit()
    
    try:
        cisco_list = cisco_compile()
    except Exception as e:
        logging.error(f"Could not compile cisco.ini: {e}")
        sys.exit()

    # set command to send to cisco devices
    palo_xpath = "<show><high-availability><state></state></high-availability></show>"
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
        logging.error(f"Invalid response from Cisco device: {e}")
        sys.exit()

    # user responses to create spreadsheet report
    try:
        report = get_report(palo_data, cisco_data)
    except Exception as e:
        logging.error(f"Could not generate report: {e}")
        sys.exit()
    
    # compare results to previous day to see if anything changed
    try:
        changed = compare(palo_data, cisco_data)
    except Exception as e:
        logging.error(f"Could not compare today's data to historical data: {e}")
        
    # generate the text for the email message
    if len(changed) == 0:
        text = "No devices have changed state from the previous day"
    else:
        text = "The following devices have changed state:\n\n" + \
            '\n'.join(changed)
    
    # log result to log file as well
    logging.info(text)

    # send report via mail
    try:
        send_mail(text, report)
    except Exception as e:
        logging.error(f"Could not send mail: {e}")

    # log completion to log file if successful
    logging.info(f"Completed running at {datetime.now()}")


def get_report(palo, cisco):
    # open new excel sheet and add headers
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Sitrep"
        ws.append(['Device Name', 'State'])
        c = ws['A1':'A2']
        c.font = Font(bold=True)
        c.style = '40 % - Accent1'
    except Exception as e:
        raise RuntimeError(f"Could not initialize workbook: {e}")

    # add all devices and their states to spreadsheet
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

    # save the excel sheet with todays date to the /reports directory
    try:
        report = f"{os.getcwd()}/reports/{str(date.today())}-sitrep.xlsx"
        wb.save(report)
    except Exception as e:
       raise RuntimeError(f"Could not save workbook: {e}")
   
    # return the report file path
    return report


def compare(palo, cisco):
    # get yesterday's date
    today = date.today()
    yesterday = today - timedelta(days=1)

    # initiate list of changed devices
    changed = []

    # try to open the report from the previous day
    try:
        wb = load_workbook(f"reports/{str(yesterday)}-sitrep.xlsx")
        ws = wb["Sitrep"]
    except Exception as e:
        logging.error("Could not open previous report: {e}") 
        return ["Yesterday\'s sitrep not detected, see log file for details"]

    # compare each device state to the previous day's state
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
        logging.error(f"Could not parse previous report: {e}") 
        return ["Could not parse yesterday\'s sitrep, see log file for details"]

    # return the list of devices that changed state
    return changed


if __name__ == "__main__":
    main()
