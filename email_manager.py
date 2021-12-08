import smtplib # sending and formatting email    - |
from email.mime.multipart import MIMEMultipart # - |
from email.mime.text import MIMEText #  -  -  -  - |

import os # env variables
import datetime # system time for record keeping


class EmailManager():
    def __init__(self, frum="", to="", server="", port="", passwd=""):
        self.now = datetime.datetime.now() # maybe should add default value...?
        self.frum = frum or os.environ["FROM"]
        self.to = to or os.environ["TO"]
        self.server = server or os.environ["MAIL_SERVER"]
        self.port = port or os.environ["MAIL_PORT"]
        self.passwd = passwd or os.environ["MAIL_PW"]

    def send_email(self, content):
        msg = MIMEMultipart()
        msg["Subject"] = f"Top News Stories [Automated Email] {str(self.now.month)}-{str(self.now.day)}-{str(self.now.year)}"
        msg["From"] = self.frum
        msg["To"] = self.to

        msg.attach(MIMEText(content, "html"))

        print("Initializing Server...")

        server = smtplib.SMTP(self.server, self.port)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(self.frum, self.passwd)
        server.sendmail(self.frum, self.to, msg.as_string())

        print("Email Sent...")

        server.quit()