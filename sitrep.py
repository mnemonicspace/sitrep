import devices
import smtplib
from datetime import date
import csv


def main():

    # create devices
    palo_list = {
        "vpn_dc1": devices.create("homebridge", "300.10.20.78", "linux", "ansible"),
    }

    # run uptime on devices and create dict of responses
    command = "uptime"
    data = {dev.name: dev.send_cmd(command) for dev in palo_list.values()}

    print(data)


# Function to Get uptime
def get_uptime(device):

    # create netmiko object with device attrib
    return send_cmd(device.build(), command)


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
