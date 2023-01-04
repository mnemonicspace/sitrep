import smtplib
import configparser
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl


def send_mail(text, report=""):
    # compile config from conf file
    try:
        config = get_config()
    except Exception as e:
        raise RuntimeError(e)

    # compile message from conf and provided text and optional attachment
    try:
        message = compose(config, text, report)
    except Exception as e:
        raise RuntimeError(e)

    # try smtp_ssl connection to server
    try:
        server = connect_ssl(config)

    # if ssl doesnt work, try tls
    except ssl.SSLError:
        try:
            server = connect_tls(config)
        except Exception as e:
            raise RuntimeError("Could not connect to SMTP")

    # login to server if credentials provided
    if config["user"] and config["password"]:
        try:
            server.login(config["user"], config["password"])
        except smtplib.SMTPAuthenticationError:
            raise RuntimeError("Invalid SMTP Login")

    # send message to server
    try:
        server.sendmail(config["sender"], config["receiver"], message)
    except smtplib.SMTPSenderRefused:
        raise RuntimeError("SMTP username and/or password is missing")
    
    # close connection to server
    server.quit()


def get_config():
    # read in config file
    config = configparser.ConfigParser()
    try:
        config.read("config/mailconfig.ini")
    except:
        raise RuntimeError("Could not read mailconfig.ini")

    # set credentials if provided, otherwise set to empty
    try:
        user = config["MAIL SERVER"]["user"]
        password = config["MAIL SERVER"]["password"]
    except KeyError:
        user = ""
        password = ""

    # return dict of settings from conf file
    try:
        return {
            "server": config["MAIL SERVER"]["server"],
            "port": config["MAIL SERVER"]["port"],
            "sender": config["MAIL SERVER"]["sender"],
            "receiver": config["MAIL SERVER"]["receiver"],
            "user": user,
            "password": password,
        }
    except Exception:
        raise RuntimeError("Could not parse mailconfig.ini")


def compose(config, text, attachment=""):
    # initialize message
    message = MIMEMultipart("mixed")

    # parse config file
    try:
        message["From"] = config["sender"]
        message["To"] = config["receiver"]
    except:
        raise RuntimeError("Could not compose message headers")

    message["Subject"] = f"{date.today()}-Sitrep"
    
    # add text to body
    try:
        body = MIMEText(text, "html")
        message.attach(body)
    except:
        raise RuntimeError("Could not create message body")
    
    # add attachment if provided
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

    # return message as string
    try:
        return message.as_string()
    except:
        raise RuntimeError("Could not convert message to string")

def connect_ssl(config):
    # connect to server via ssl and send ehlo
    try:
        server = smtplib.SMTP_SSL(config["server"], config["port"])
        server.ehlo()

    except ssl.SSLError:
        raise ssl.SSLError

    return server


def connect_tls(config):
    # connect to server, send ehlo and starttls
    try:
        server = smtplib.SMTP(config["server"], config["port"])
        server.ehlo()
        server.starttls()
    except Exception as e:
        raise RuntimeError(e)

    return server
