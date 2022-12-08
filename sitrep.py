import devices
import smtplib
from datetime import date
import csv


def main():

    # create devices
    palo_list = [
        devices.create("DC1-VPN", "10.1.14.131", "paloalto_panos", "admin"),
        devices.create("601-VPN", "10.1.11.131", "paloalto_panos", "admin")
    ]

    cisco_list = [
        devices.create("DC1-6807", "10.1.14.131", "paloalto_panos", "admin"),
        devices.create("601-6807", "10.1.11.131", "paloalto_panos", "admin")
    ]

    p_command = "show system high-availability state"
    c_command = "show standby brief"

    # run uptime on devices and create dict of responses
    palo_data = {dev.name: dev.send_cmd(p_command) for dev in palo_list}

    cisco_data = {dev.name: dev.send_cmd(c_command) for dev in cisco_list}


def get_report(palo, cisco):
    with open(f"{date.today}.csv", 'w') as file:
        writer = csv.DictWriter(file, fieldnames=["Device", "State"])
        writer.writeheader()
        writer.writerow(palo)
        writer.writerow(cisco)


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
