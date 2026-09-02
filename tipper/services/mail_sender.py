import smtplib
from email.mime.text import MIMEText

from models import config


class MailSend:

    SIGNATURE = '''
Mit vorzüglicher Hochachtung,

Dein Lieblingsbot AI-ntracht aka. Botrick PostBOTe
'''
    SUBJECT_SUCCESS = 'Erfolgreich Getippt'
    MESSAGE_SUCCESS = f'''Gude Patrick,

Das mit dem Tippen scheint ganz gut geklappt zu haben, sehr schön.

{SIGNATURE}
'''
    SUBJECT_FAILURE = 'Tippen fehlgeschlagen!!'
    MESSAGE_FAILURE = f'''Du... Patrick...

Ich glaube da ist was schief gelaufen beim Tippen, schau doch mal nach.

{SIGNATURE}
'''

    def __init__(self, user_mail, user_passwort, smtp_host, smtp_port, mail_to):
        conf = config.load_config()
        self.user_mail = user_mail
        self.user_passwort = user_passwort
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.mail_to = mail_to

    def send_msg(self, msg):
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.user_mail, self.user_passwort)
                server.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            print('SMTP-Login fehlgeschlagen!')
            print('Bitte E-Mail-Adresse und Passwort/App-Passwort überprüfen.')
            raise

    def success_msg(self):
        msg = MIMEText(self.MESSAGE_SUCCESS)
        msg['Subject'] = self.SUBJECT_SUCCESS
        msg['From'] = self.user_mail
        msg['To'] = self.mail_to
        self.send_msg(msg)

    def failure_msg(self):
        msg = MIMEText(self.MESSAGE_FAILURE)
        msg['Subject'] = self.SUBJECT_FAILURE
        msg['From'] = self.user_mail
        msg['To'] = self.mail_to
        self.send_msg(msg)

    def test_msg(self):
        msg = MIMEText('DIES IST EIN TEST')
        msg['Subject'] = 'TEST'
        msg['From'] = self.user_mail
        msg['To'] = self.mail_to
        self.send_msg(msg)


def main():
    conf = config.load_config()

    mail_send = MailSend(
        user_mail = conf.user.e_mail,
        user_passwort = conf.user.mail_password,
        smtp_host = conf.user.smtp_host,
        smtp_port = conf.user.smtp_port,
        mail_to = conf.daddy.e_mail
    )
    mail_send.test_msg()

if __name__ == '__main__':
    main()
