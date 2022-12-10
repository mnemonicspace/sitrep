import devices
import smtplib
from datetime import date, timedelta
from openpyxl import Workbook, load_workbook


def main():

    # create devices
    palo_list = [
        devices.create("DC1-VPN", "10.10.20.78", "linux",
                       "ansible", "/Users/msexton/.ssh/ansible"),
    ]

    cisco_list = [
        devices.create("DC1-6807", "10.10.10.53", "linux",
                       "ansible", "/Users/msexton/.ssh/ansible"),
        # devices.create("601-6807", "10.1.11.131", "paloalto_panos", "admin")
    ]

    p_command = "uptime"
    c_command = "uptime"

    # run uptime on devices and create dict of responses
    palo_data = {dev.name: dev.send_cmd(p_command) for dev in palo_list}

    cisco_data = {dev.name: dev.send_cmd(c_command) for dev in cisco_list}

    get_report(palo_data, cisco_data)
    changed = compare(palo_data, cisco_data)

    if len(changed) == 0:
        text = "No changes"
    else:
        text = "The following devices have changed state:\n\n" + \
            '\n'.join(changed)

    print(text)


def get_report(palo, cisco):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sitrep"
    ws.append(['Device Name', 'State'])

    for name, state in cisco.items():
        ws.append([name, state])

    for name, state in palo.items():
        ws.append([name, state])

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
        state = ws[f"B{row}"].value

        if dev is None or state is None:
            continue

        if dev in cisco:
            old_state = cisco[dev]
        elif dev in palo:
            old_state = palo[dev]
        else:
            continue

        if state != old_state:
            changed.append(dev)

    return changed


# def send_mail(report, text):
#     SERVER = "smtp.novanthealth.org"
#
#     FROM = 'nse_sitrep@novanthealth.org'
#
#     TO = ["cpsnse@novanthealth.org"] # must be a list
#
#     SUBJECT = "Sitrep {date.today()}"
#
#     TEXT = MIMEText(text, html)
#
#     # Prepare actual message
#
#     message = """\
#     From: %s
#     To: %s
    # Subject: %s
    #
    # %s
    # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    #
    # # Send the mail
#
#     server = smtplib.SMTP(SERVER)
#     server.sendmail(FROM, TO, message)
#     server.quit()
if __name__ == "__main__":
    main()
