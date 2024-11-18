"""Contains the definition of basemodels."""

from datetime import datetime
from enum import StrEnum
from pathlib import Path
from pydantic import BaseModel


class EmailRecipient(BaseModel):
    """Definition of the Recipient of the email."""

    name: str
    email: str
    company: str
    position: str = "Unknown"


class EmailModel(BaseModel):
    """Definition of email object."""

    recipient: EmailRecipient
    content: str
    object: str = "Interest in Career Opportunity"
    attached_files: list[Path] = []


class AnswerType(StrEnum):
    WAITING = "WAITING"
    REFUSED = "REFUSED"
    ACCEPTED = "ACCEPTED"


class DataframeEntryModel(BaseModel):
    first_sent: datetime
    last_sent: datetime
    recipient: EmailRecipient
    answer: AnswerType
    amount_of_email_sent: int

    def to_dict(self) -> dict:
        """Convert the object into a dataframe entry dict.

        Returns:
            dict: Dataframe entry.
        """
        return {
            "first_sent": self.first_sent.isoformat(),
            "last_sent": self.last_sent.isoformat(),
            "recipient_company": self.recipient.company,
            "recipient_name": self.recipient.name,
            "recipient_position": self.recipient.position,
            "recipient_email": self.recipient.email,
            "amount_of_email_sent": self.amount_of_email_sent,
            "answer": self.answer,
        }
