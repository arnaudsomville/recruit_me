"""Contains the definition of basemodels."""

from pathlib import Path
from pydantic import BaseModel

class EmailRecipient(BaseModel):
    """Definition of the Recipient of the email."""
    name: str
    email: str


class EmailModel(BaseModel):
    """Definition of email object."""
    recipient: EmailRecipient
    content: str
    object: str = 'Interest in Career Opportunity'
    attached_file: Path | None = None
    