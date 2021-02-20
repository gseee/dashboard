import imaplib
import email
from config import SMTP_SERVER, FROM_EMAIL, FROM_PWD


class Email(object):

    def __init__(self, email_message):
        self.__email = email_message

    @property
    def sender(self):
        return self.__email['From']

    @property
    def date(self):
        return self.__email['Date']

    @property
    def subject(self):
        return self.__email['Subject']


class EmailParserImapClient(imaplib.IMAP4_SSL):

    def get_mail_ids(self):
        return self.search(None, 'ALL')[1][0].split()

    def iter_mails(self, mail_ids):

        first_email_id = int(mail_ids[0])
        latest_email_id = int(mail_ids[-1])

        for i in range(latest_email_id, first_email_id, -1):
            mail_content = self.fetch(str(i), '(RFC822)')[1][0][1]
            msg = email.message_from_string(str(mail_content, 'utf-8'))
            yield Email(msg)


def read_email_from_gmail(box='inbox', max_count=20):
    imap_client = EmailParserImapClient(SMTP_SERVER)
    imap_client.login(FROM_EMAIL, FROM_PWD)
    imap_client.select(box)

    all_mails_ids = imap_client.get_mail_ids()[-max_count:]

    return list(imap_client.iter_mails(all_mails_ids))
