import smtplib
import configparser
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl


def send_mail(text, report=""):
    config = get_config()
    print(config)
    message = compose(config, text, report)

    try:
        server = connect_ssl(config)

    except ssl.SSLError:
        try:
            server = connect_tls(config)
        except Exception as e:
            raise RuntimeError("Could not connect to SMTP")

    if config["user"] and config["password"]:
        try:
            server.login(config["user"], config["password"])
        except smtplib.SMTPAuthenticationError:
            raise RuntimeError("Invalid SMTP Login")

    try:
        server.sendmail(config["sender"], config["receiver"], message)
    except smtplib.SMTPSenderRefused:
        raise RuntimeError("SMTP username and/or password is missing")
    server.quit()


def get_config():
    config = configparser.ConfigParser()
    config.read("config/mailconfig.ini")

    try:
        user = config["MAIL SERVER"]["user"]
        password = config["MAIL SERVER"]["password"]
    except KeyError:
        user = ""
        password = ""

    return {
        "server": config["MAIL SERVER"]["server"],
        "port": config["MAIL SERVER"]["port"],
        "sender": config["MAIL SERVER"]["sender"],
        "receiver": config["MAIL SERVER"]["receiver"],
        "user": user,
        "password": password,
    }


def compose(config, text, attachment=""):
    message = MIMEMultipart("mixed")
    message["From"] = config["sender"]
    message["To"] = config["receiver"]
    message["Subject"] = f"{date.today()}-Sitrep"
    body = MIMEText(text, "html")
    message.attach(body)
    if attachment:
        try:
            with open(attachment, "rb") as file:
                p = MIMEApplication(file.read())
                p.add_header(
                    "Content-Disposition",
                    "attachment; filename= %s" % attachment.split("/")[-1],
                )
                message.attach(p)
        except Exception as e:
            raise RuntimeError(f"Could not attach {e}")

    return message.as_string()


def connect_ssl(config):
    try:
        server = smtplib.SMTP_SSL(config["server"], config["port"])
        server.set_debuglevel(1)
        server.ehlo()

    except ssl.SSLError:
        raise ssl.SSLError

    return server


def connect_tls(config):
    try:
        server = smtplib.SMTP(config["server"], config["port"])
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
    except Exception as e:
        raise RuntimeError(e)

    return server
