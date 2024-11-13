"""Contains functions for email sending."""

from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import warnings

from recruit_me.models.data_models import EmailModel, EmailRecipient
from recruit_me.utils.configuration import MainConfig

def send_email(email_data: EmailModel) -> bool:
    """Function used to send an email

    Args:
        email_data (EmailModel): Email data containing content and attachment.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = MainConfig().user.email
        msg['To'] = email_data.recipient.email
        msg['Subject'] = email_data.object

        msg['Disposition-Notification-To'] = MainConfig().user.email
        msg['Return-Receipt-To'] = MainConfig().user.email

        msg.attach(MIMEText(email_data.content, 'plain'))

        if len(email_data.attached_files)>0:
            for attached_file in email_data.attached_files:
                if not attached_file.exists():
                    raise FileNotFoundError("The attachement file does not exist.")
                with open(attached_file, 'rb') as attachment_file:
                    filename = attached_file.name
                    part = MIMEApplication(attachment_file.read(), Name=filename)
                    part['Content-Disposition'] = f'attachment; filename="{filename}"'
                    msg.attach(part)

        with smtplib.SMTP(MainConfig().user.smtp_server, MainConfig().user.smtp_port) as server:
            server.starttls()  # Sécurise la connexion
            server.login(MainConfig().user.email, MainConfig().user.password)
            server.send_message(msg)
        return True
    except Exception as e:
        warnings.warn(f"Problem occurred when sending email: {e}")
        return False
    
if __name__ == '__main__': #pragma: no-cover
    email = EmailModel(
        recipient=EmailRecipient(
            name='Stéphane',
            email='arnaudsomville@hotmail.fr',
            company='Tesla'
        ),
        content="Recruit me plz",
        attached_files=[Path.home().joinpath(f"{MainConfig().home_folder}/test.pdf")]
    )
    send_email(email)