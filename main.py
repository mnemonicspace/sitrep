import app.nhcisco as nhcisco
import app.nhpalo as nhpalo
import app.config as config
from app.nhmail import send_mail
from datetime import date, timedelta
from openpyxl import Workbook, load_workbook
import re
import xml.etree.ElementTree as ET


def main():
    # create devices
    palo_list = [
        nhpalo.Palo('DC1_VPN', config.api, '172.16.50.50'),
        nhpalo.Palo('601_VPN', config.api, '172.16.50.51')
    ]

    cisco_list = [
        nhcisco.Cisco("DC1-6807", "172.16.50.60", "cisco_ios",
                      "lab", "/Users/msexton/.ssh/lab"),
        nhcisco.Cisco("601-6807", "172.16.50.61", "cisco_ios",
                      "lab", "/Users/msexton/.ssh/lab")
    ]

    p_command = "<show><high-availability><state></state></high-availability></show>"
    c_command = "show standby brief"

    # run uptime on devices and create dict of responses
    palo_data = {dev.name: ET.fromstring(dev.ha_state().content).find(
        'result').find('group').find('local-info').find('state').text for dev in palo_list}

    cisco_data = {dev.name: re.findall(
        r"\A[^,]+?P (Active|Standby)", str(dev.send_cmd(c_command))) for dev in cisco_list}
    get_report(palo_data, cisco_data)
    changed = compare(palo_data, cisco_data)

    if len(changed) == 0:
        text = "No changes"
    else:
        text = "The following devices have changed state:\n\n" + \
            '\n'.join(changed)
    print(text)
    # send_mail(f"reports/{str(date.today())}-sitrep.xlsx", text)


def get_report(palo, cisco):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sitrep"
    ws.append(['Device Name', 'State'])

    for name, state in cisco.items():
        ws.append([name, state[0]])

    for name, state in palo.items():
        ws.append([name, state.title()])

    wb.save(f"reports/{str(date.today())}-sitrep.xlsx")


def compare(palo, cisco):
    today = date.today()
    yesterday = today - timedelta(days=1)

    changed = []

    try:
        wb = load_workbook(f"reports/{str(yesterday)}-sitrep.xlsx")
        ws = wb["Sitrep"]
    except:
        return ['Yesterday\'s sitrep not detected']

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

        if state != old_state:
            changed.append(dev)

    return changed


if __name__ == "__main__":
    main()
