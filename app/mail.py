import smtplib
import configparser
from datetime import date
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
import ssl

def send_mail(report, text):
    config = configparser.ConfigParser()
    config.read('config/mailconfig.ini')
    
    SERVER = config['MAIL SERVER']['server']
    PORT = config['MAIL SERVER']['port']
    sender = config['MAIL SERVER']['sender']
    receiver =config['MAIL SERVER']['receiver']
    try:
        user = config['MAIL SERVER']['user']
        password = config['MAIL SERVER']['password']
    except KeyError:
        user = ''
        password = ''
        
    message = MIMEMultipart('mixed')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = f"{date.today()}-Sitrep"
    body = MIMEText(text, 'html')
    message.attach(body)
    
    try:
        print(report.split("\\")[-1])
        with open(report, "rb") as attachment:
            p = MIMEApplication(attachment.read())	
            p.add_header('Content-Disposition', "attachment; filename= %s" % report.split("/")[-1]) 
            message.attach(p)
    except Exception as e:
        raise RuntimeError(f"Could not attach {e}")
    
    msg_full = message.as_string()
    
    try:    
        with smtplib.SMTP_SSL(SERVER, PORT) as server:
            server.ehlo()
            if user and password:
                try:
                    server.login(user, password)
                except smtplib.SMTPAuthenticationError:
                    raise RuntimeError("Invalid SMTP Login")
            try:
                server.sendmail(sender, receiver, msg_full)
            except smtplib.SMTPSenderRefused:
                    raise RuntimeError("SMTP username and/or password is missing")
            server.quit()
    
    except ssl.SSLError:
        with smtplib.SMTP(SERVER, PORT) as server:
            server.ehlo()
            server.starttls()
            if user and password:
                try:
                    server.login(user, password)
                except smtplib.SMTPAuthenticationError:
                    raise RuntimeError("Invalid SMTP Login")
            try:
                server.sendmail(sender, receiver, msg_full)
            except smtplib.SMTPSenderRefused:
                    raise RuntimeError("SMTP username and/or password is missing")
            server.quit()