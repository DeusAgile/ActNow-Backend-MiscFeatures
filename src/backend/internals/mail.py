from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from os import environ


def send_mail(your_message: str, mail_to: str, mail_subject: str):

    msg = MIMEMultipart()

    password = environ.get("MAIL_PASS")
    msg['From'] = environ.get("MAIL_FROM")
    msg['To'] = mail_to
    msg['Subject'] = mail_subject

    msg.attach(MIMEText(your_message, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', '465')

    server.login(msg["From"], password)

    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()

    print ("success")


