"""Test the email finder."""

from pathlib import Path
import smtplib
import uuid
from unittest.mock import patch

from recruit_me.backend.email_sender import send_email
from recruit_me.models.data_models import EmailModel, EmailRecipient
from recruit_me.utils.configuration import MainConfig

def test_email_sending_nominal_no_file()->None:
    """Test email sending in nominal case."""
    email = EmailModel(
        recipient=EmailRecipient(
            name='Elon Musk',
            email='elonmusk@real_email.com',
            company='SpaceX',
            position='CEO'
        ),
        content="Recruit me plz",
    )
    with (
        patch.object(smtplib.SMTP, 'starttls', return_value = None),
        patch.object(smtplib.SMTP, 'login', return_value = None),
        patch.object(smtplib.SMTP, 'send_message', return_value = None),
    ):
        assert send_email(email)

def test_email_sending_nominal_with_file()->None:
    """Test email sending in nominal case."""

    #Creation of a fake pdf
    attached_file = [Path.home().joinpath(f"{MainConfig().home_folder}/{uuid.uuid4()}.pdf")]
    with open(attached_file[0], 'wb') as f:
        f.write(b"%PDF-1.4\n")
        f.write(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
        f.write(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
        f.write(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n")
        f.write(b"4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(This is a PDF file) Tj\nET\nendstream\nendobj\n")
        f.write(b"xref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000079 00000 n \n0000000174 00000 n \n0000000317 00000 n \n")
        f.write(b"trailer\n<< /Root 1 0 R /Size 5 >>\nstartxref\n385\n%%EOF")
    
    email = EmailModel(
        recipient=EmailRecipient(
            name='Elon Musk',
            email='elonmusk@real_email.com',
            company='SpaceX',
            position='CEO'
        ),
        content="Recruit me plz",
        attached_files=attached_file
    )
    with (
        patch.object(smtplib.SMTP, 'starttls', return_value = None),
        patch.object(smtplib.SMTP, 'login', return_value = None),
        patch.object(smtplib.SMTP, 'send_message', return_value = None),
    ):
        assert send_email(email)


def test_email_sending_not_nominal_file_does_not_exist()->None:
    """Test email sending if file does not exist."""
    email = EmailModel(
        recipient=EmailRecipient(
            name='Elon Musk',
            email='elonmusk@real_email.com',
            company='SpaceX',
            position='CEO'
        ),
        content="Recruit me plz",
        attached_files=[Path.home().joinpath(f"{MainConfig().home_folder}/{uuid.uuid4()}.pdf")] #Does not exist
    )
    assert not send_email(email)

def test_email_sending_not_nominal_error()->None:
    """Test email sending if file does not exist."""
    email = EmailModel(
        recipient=EmailRecipient(
            name='Elon Musk',
            email='elonmusk@real_email.com',
            company='SpaceX',
            position='CEO'
        ),
        content="Recruit me plz",
    )
    def error_fct()->None:
        """Raise an error for the purpose of this test.

        Raises:
            RuntimeError: Error for the mock.
        """
        raise RuntimeError("An error occured sending the email")
    with (
        patch.object(smtplib.SMTP, 'starttls', return_value = None),
        patch.object(smtplib.SMTP, 'login', return_value = None),
        patch.object(smtplib.SMTP, 'send_message', side_effect=error_fct),
    ):
        assert not send_email(email)