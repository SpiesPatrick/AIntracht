import smtplib
from email.mime.text import MIMEText


class MailSend:

    def __init_(self):


    msg = MIMEText("Hallo, das ist ein Test von Python")
    msg["Subject"] = "Test Mail"
    msg["From"] = "deinname@gmx.de"
    msg["To"] = "empfaenger@mail.de"

    with smtplib.SMTP("mail.gmx.net", 587) as server:
        server.starttls()
        server.login("deinname@gmx.de", "DEIN_PASSWORT")
        server.send_message(msg)

    print("Mail wurde verschickt (hoffentlich 😄)")


    def success_msg():
        msg = MIMEText("Hallo, das ist ein Test von Python")
        msg["Subject"] = "Test Mail"
        msg["From"] = "deinname@gmx.de"
        msg["To"] = "empfaenger@mail.de"

    def failure_msg():
        msg = MIMEText("Hallo, das ist ein Test von Python")
        msg["Subject"] = "Test Mail"
        msg["From"] = "deinname@gmx.de"
        msg["To"] = "empfaenger@mail.de"

    # def test_msg():
