"""File managing the dataframe that keeps in memory the email sent."""

from datetime import datetime
import os
from pathlib import Path
import warnings
import pandas as pd

from recruit_me.models.data_models import AnswerType, DataframeEntryModel, EmailRecipient
from recruit_me.utils.configuration import MainConfig

def add_entry_to_dataframe(data: DataframeEntryModel, dataframe: pd.DataFrame)->pd.DataFrame:
    """Add an entry to the Dataframe managing the sent emails. If the entry already exist, it will increment the amount of email sent.

    Args:
        data (DataframeEntryModel): data to add.

    Returns:
        pd.DataFrame: Updated dataframe.

    """
    if data.recipient.email in dataframe["recipient_email"].values:
        if data.recipient.email in dataframe["recipient_email"].values:
            dataframe.loc[dataframe["recipient_email"] == data.recipient.email, "last_sent"] = data.last_sent.isoformat()
            dataframe.loc[dataframe["recipient_email"] == data.recipient.email, "amount_of_email_sent"] += 1
    else:
        new_row = pd.DataFrame([data.to_dict()])
        dataframe = pd.concat([dataframe, new_row], ignore_index=True)
    return dataframe

def retrieve_dataframe() -> pd.DataFrame:
    """Retrieve the dataframe from file.

    Returns:
        pd.DataFrame: Retrieved Dataframe.
    """
    expected_columns = DataframeEntryModel(
        first_sent=datetime.now(),
        last_sent=datetime.now(),
        recipient=EmailRecipient(name="Test", email="test@example.com", company="TestCompany"),
        answer=AnswerType.WAITING,
        amount_of_email_sent=0
    ).to_dict().keys()
    dataframe_save_file = Path.home().joinpath(f'{MainConfig().home_folder}/saved_sent_email_data.csv')
    if dataframe_save_file.exists():
        dataframe = pd.read_csv(dataframe_save_file)
        if set(dataframe.columns) == set(expected_columns):
            return dataframe
        else:
            print(dataframe.index)
            os.remove(str(dataframe_save_file))
            warnings.warn("Corrupted Dataframe save. Removing file.")
            return pd.DataFrame(columns=expected_columns)
        
    
    else:
        #Dynamic retrieval of DataframeEntryModel columns to avoid useless future modifications.
        return pd.DataFrame(columns=expected_columns)

def save_dataframe(dataframe: pd.DataFrame) -> bool:
    """Save the dataframe in the home folder.

    Args:
        dataframe (pd.DataFrame): Dataframe that keeps in memory the email sent.

    Returns:
        bool: True if everything went well.
    """
    try:
        dataframe_save_file = Path.home().joinpath(f'{MainConfig().home_folder}/saved_sent_email_data.csv')
        dataframe.to_csv(dataframe_save_file, index=False)
        return True
    except Exception as e:
        print(f"Error saving DataFrame: {e}")
        return False

if __name__ == '__main__': #pragma: no-cover
    dataframe_entries = [
        DataframeEntryModel(
            first_sent=datetime(2023, 1, 1, 10, 0),
            last_sent=datetime(2023, 1, 2, 15, 30),
            recipient=EmailRecipient(
                name="Homer Simpson",
                email="homer@duffbrewery.com",
                company="Duff Brewery",
                position="Nuclear Safety Inspector"
            ),
            answer=AnswerType.WAITING,
            amount_of_email_sent=3
        ),
        DataframeEntryModel(
            first_sent=datetime(2023, 1, 5, 9, 0),
            last_sent=datetime(2023, 1, 6, 11, 0),
            recipient=EmailRecipient(
                name="Tony Stark",
                email="ironman@starkindustries.com",
                company="Stark Industries",
                position="CEO"
            ),
            answer=AnswerType.ACCEPTED,
            amount_of_email_sent=2
        ),
        DataframeEntryModel(
            first_sent=datetime(2023, 1, 10, 8, 0),
            last_sent=datetime(2023, 1, 12, 16, 45),
            recipient=EmailRecipient(
                name="Rick Sanchez",
                email="rick@interdimensionalmail.com",
                company="Interdimensional Inc.",
                position="Mad Scientist"
            ),
            answer=AnswerType.REFUSED,
            amount_of_email_sent=4
        ),
        DataframeEntryModel(
            first_sent=datetime(2023, 1, 15, 14, 0),
            last_sent=datetime(2023, 1, 15, 18, 0),
            recipient=EmailRecipient(
                name="Sherlock Holmes",
                email="sherlock@bakerstreet.com",
                company="Baker Street Detective Agency",
                position="Consulting Detective"
            ),
            answer=AnswerType.WAITING,
            amount_of_email_sent=1
        ),
        DataframeEntryModel(
            first_sent=datetime(2023, 1, 20, 13, 0),
            last_sent=datetime(2023, 1, 21, 17, 30),
            recipient=EmailRecipient(
                name="Darth Vader",
                email="darth@empire.com",
                company="Galactic Empire",
                position="Sith Lord"
            ),
            answer=AnswerType.REFUSED,
            amount_of_email_sent=5
        )
    ]
    dataframe = pd.DataFrame(data=[data.to_dict() for data in dataframe_entries])
    assert save_dataframe(dataframe)

    additional_data = DataframeEntryModel(
        first_sent=datetime(2023, 1, 20, 13, 0),
        last_sent=datetime(2023, 1, 21, 17, 30),
        recipient=EmailRecipient(
            name="Mickey Mouse",
            email="mickey@disney.com",
            company="Disney Inc",
            position="CEO"
        ),
        answer=AnswerType.ACCEPTED,
        amount_of_email_sent=50
    )
    dataframe = retrieve_dataframe()
    dataframe = add_entry_to_dataframe(additional_data, dataframe)
    save_dataframe(dataframe)