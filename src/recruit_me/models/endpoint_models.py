"""File containing the base models used in rest api endpoints."""

from pydantic import BaseModel
from recruit_me.models.data_models import EmailRecipient

default_email_recipient = EmailRecipient(
    name='Elon Musk',
    email='elonmusk@real_email.com',
    company='SpaceX',
    position='CEO'
),

class EmailSendingEndpointModel(BaseModel):
    """Model used for the send_email endpoint"""
    email_recipient: EmailRecipient = default_email_recipient
    email_object: str = 'Interest in Career Opportunity'
    cv_filename: str = 'my_cv.pdf'
    cover_letter_template_filename: str = 'my_cover_letter_template.txt'
    email_template_filename:str = 'my_email_template.txt'