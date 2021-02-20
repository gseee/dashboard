import imaplib
import email
import traceback
from config import SMTP_SERVER, FROM_EMAIL, FROM_PWD


Emails = namedtuple('Emails', "from subject")

def read_email_from_gmail():
    email_dict = {}
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]

        id_list = mail_ids[0].split()[-20:] #last 20 emails
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_dict[email_from] = email_subject

        print(email_dict)
        return email_dict

    except Exception as e:
        traceback.print_exc()
        print(str(e))


read_email_from_gmail()
