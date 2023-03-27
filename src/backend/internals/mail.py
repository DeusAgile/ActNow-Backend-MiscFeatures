from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from os import environ


def send_mail(your_message: str, mail_to: str, mail_subject: str):

    msg = MIMEMultipart()
    # html_response = open("src/frontend/reg_mail.html")

    password = environ.get("MAIL_PASS")
    msg['From'] = environ.get("MAIL_FROM")
    msg['To'] = mail_to
    msg['Subject'] = mail_subject

    msg.attach(MIMEText(your_message, 'plain'))

    server = smtplib.SMTP('smtp.yandex.ru', '587')

    server.starttls()

    server.login(msg["From"], password)

    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()

    print ("success")


