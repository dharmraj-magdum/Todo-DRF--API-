from django.core.mail import EmailMessage
import os


class Util:
    @staticmethod
    def sendEmail(data):
        subject = data["subject"]
        body = data["body"]
        sender = os.environ.get('EMAIL_FROM')
        to = []
        to.append(data["to"])
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=sender,
            to=to,
        )
        # now email object created just send it
        email.send()
