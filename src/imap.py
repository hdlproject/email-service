import imaplib
import email
from email.header import decode_header
import webbrowser
import os


class IMAP:
    def __init__(self):
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")

    def login(self, username: str, password: str):
        self.imap.login(username, password)

    @staticmethod
    def clean(text):
        return "".join(c if c.isalnum() else "_" for c in text)

    def read_latest(self):
        status, messages = self.imap.select("INBOX")

        number_of_emails = int(messages[0])

        res, msg = self.imap.fetch(str(number_of_emails), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                print("Subject:", subject)

                sender, encoding = decode_header(msg.get("From"))[0]
                if isinstance(sender, bytes):
                    sender = sender.decode(encoding)
                print("From:", sender)

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        try:
                            body = part.get_payload(decode=True).decode()

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                print("Body:", body)
                            elif "attachment" in content_disposition:
                                filename = part.get_filename()

                                if filename:
                                    folder_name = self.clean(subject)
                                    if not os.path.isdir(folder_name):
                                        os.mkdir(folder_name)

                                    filepath = os.path.join(folder_name, filename)
                                    open(filepath, "wb").write(part.get_payload(decode=True))
                        except:
                            pass

                else:
                    content_type = msg.get_content_type()

                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        print("Body:", body)
                    elif content_type == "text/html":
                        folder_name = self.clean(subject)
                        if not os.path.isdir(folder_name):
                            os.mkdir(folder_name)

                        filename = "index.html"
                        filepath = os.path.join(folder_name, filename)
                        open(filepath, "w").write(body)

                        webbrowser.open(filepath)
