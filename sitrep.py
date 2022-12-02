import devices
import netmiko
import smtplib
from datetime import date
import csv


def main():

    # create devices
    dev_list = {
        "vpn_dc1": devices.create("vpn_dc1", "10.10.20.78", "linux", "ansible"),
    }

    # run function on devices and create dict of responses
    data = {dev.name: get_info(dev) for dev in dev_list.values()}

    print(data)

# Function to Get System Info


def get_info(device):
    # create netmiko object with device attrib
    working_dev = device.build()

    # Netmiko run command
    with netmiko.ConnectHandler(**working_dev) as net_connect:
        return net_connect.send_command("uptime")


# def send_mail(report):
#     SERVER = "localhost"
#
#     FROM = 'nse@novanthealth.org'
#
#     TO = ["cpsnse@novanthealth.org"] # must be a list
#
#     SUBJECT = "Sitrep {date.today()}"
#
#     TEXT = "This message was sent with Python's smtplib."
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
#     server = smtplib.SMTP('myserver')
#     server.sendmail(FROM, TO, message)
#     server.quit()


if __name__ == "__main__":
    main()
