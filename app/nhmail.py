from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import date, timedelta
import smtplib

def send_mail(report, text):
    SERVER = 'smtp.novanthealth.org'
    PORT = 443

    msg = MIMEMultipart()
    body_part = MIMEText(text, 'plain')
    msg['Subject'] = f"Sitrep {date.today()}"
    msg['From'] = 'nse_sitrep@novanthealth.org'
    msg['To'] = 'cpsnse@novanthealth.org'
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    with open(report, 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=report))

    # Create SMTP object
    smtp_obj = smtplib.SMTP(SERVER, PORT)

    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()