"""Test the dataframe manager."""

import csv
from datetime import datetime
import os
from pathlib import Path
import shutil
import pandas.testing as pdt
import pandas as pd
from recruit_me.backend.dataframe_manager import add_entry_to_dataframe, retrieve_dataframe, save_dataframe
from recruit_me.models.data_models import AnswerType, DataframeEntryModel, EmailRecipient
from recruit_me.utils.configuration import MainConfig
from tests.conftest import dummy_dataframe_entries, expected_columns


def test_retrieve_dataframe_nominal() -> None:
    """Test that the retrieved dataframe is correct (before each test a dummy dataframe is created)."""
    expected_dataframe = pd.DataFrame(data=[data.to_dict() for data in dummy_dataframe_entries])
    retrieved_df = retrieve_dataframe()
    pdt.assert_frame_equal(retrieved_df, expected_dataframe)

def test_retrieve_dataframe_no_file()->None:
    """Test that the dataframe retrieval if the file does not exist (before each test a dummy dataframe is created)."""
    dataframe_save_file = Path.home().joinpath(f'{MainConfig().home_folder}/saved_sent_email_data.csv')
    os.remove(dataframe_save_file)
    retrieved_df = retrieve_dataframe()
    print(retrieved_df)
    expected_dataframe = pd.DataFrame(columns=expected_columns)
    pdt.assert_frame_equal(retrieved_df, expected_dataframe)

def test_retrieve_dataframe_wrong_column()->None:
    """Test that the dataframe retrieval if the file does not exist (before each test a dummy dataframe is created)."""
    dataframe_save_file = Path.home().joinpath(f'{MainConfig().home_folder}/saved_sent_email_data.csv')
    data = [
        ["first_sent", "last_sent", "recipient_company_Incorrect_name", "recipient_name", "recipient_position", "recipient_email", "amount_of_email_sent"],
        ["2023-01-01T10:00:00", "2023-01-02T15:30:00", "Duff Brewery", "Homer Simpson", "Nuclear Safety Inspector", "homer@duffbrewery.com", 3],
        ["2023-01-05T09:00:00", "2023-01-06T11:00:00", "Stark Industries", "Tony Stark", "CEO", "ironman@starkindustries.com", 2],
        ["2023-01-10T08:00:00", "2023-01-12T16:45:00", "Interdimensional Inc.", "Rick Sanchez", "Mad Scientist", "rick@interdimensionalmail.com", 4],
        ["2023-01-15T14:00:00", "2023-01-15T18:00:00", "Baker Street Detective Agency", "Sherlock Holmes", "Consulting Detective", "sherlock@bakerstreet.com", 1],
        ["2023-01-20T13:00:00", "2023-01-21T17:30:00", "Galactic Empire", "Darth Vader", "Sith Lord", "darth@empire.com", 5],
        ["2023-01-20T13:00:00", "2023-01-21T17:30:00", "Disney Inc", "Mickey Mouse", "CEO", "mickey@disney.com", 50]
    ]

    with open(dataframe_save_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data) #type: ignore

    retrieved_df = retrieve_dataframe()
    expected_dataframe = pd.DataFrame(columns=expected_columns)
    pdt.assert_frame_equal(retrieved_df, expected_dataframe)

def test_save_dataframe_not_nominal()->None:
    """Test the saving of Dataframe if not nominal."""
    home_path = Path.home().joinpath(f'{MainConfig().home_folder}')
    shutil.rmtree(home_path)

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

    assert not save_dataframe(dataframe)

def test_save_dataframe_nominal()->None:
    """Test the saving of Dataframe."""
    dataframe_save_file = Path.home().joinpath(f'{MainConfig().home_folder}/saved_sent_email_data.csv')
    os.remove(dataframe_save_file)

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
    expected_dataframe = pd.DataFrame(data=[data.to_dict() for data in dataframe_entries])
    retrieved_df = retrieve_dataframe()
    pdt.assert_frame_equal(retrieved_df, expected_dataframe)


def test_add_entry_to_dataframe_nominal()->None:
    """Test the addition of data to the dataframe."""
    retrieved_base_df = retrieve_dataframe()
    
    added_data = DataframeEntryModel(
        first_sent=datetime(2023, 1, 15, 14, 0),
        last_sent=datetime(2023, 1, 15, 18, 0),
        recipient=EmailRecipient(
            name="Spongebob",
            email="spongebob@underthesea.com",
            company="Krusty Krab",
            position="French fries cook"
        ),
        answer=AnswerType.REFUSED,
        amount_of_email_sent=1
    )

    #Test case nominal
    new_dummy_list = dummy_dataframe_entries.copy()
    new_dummy_list.append(added_data)
    expected_dataframe_1 = pd.DataFrame(data=[data.to_dict() for data in new_dummy_list])
    
    retrieved_df = add_entry_to_dataframe(added_data, retrieved_base_df)
    pdt.assert_frame_equal(retrieved_df, expected_dataframe_1)

def test_add_entry_to_dataframe_existing_row()->None:
    """Test the addition of data to the dataframe if the row already exist (change the date of last sent email and )."""
    retrieved_base_df = retrieve_dataframe()
    
    added_data = DataframeEntryModel(
        first_sent=datetime(2023, 1, 5, 9, 0),
        last_sent=datetime(2024, 1, 6, 11, 0),
        recipient=EmailRecipient(
            name="Tony Stark",
            email="ironman@starkindustries.com",
            company="Stark Industries",
            position="CEO"
        ),
        answer=AnswerType.ACCEPTED,
        amount_of_email_sent=2
    )

    #Test case nominal
    new_dummy_list = dummy_dataframe_entries.copy()
    new_dummy_list[1].amount_of_email_sent = 3
    new_dummy_list[1].last_sent=datetime(2024, 1, 6, 11, 0)
    expected_dataframe = pd.DataFrame(data=[data.to_dict() for data in new_dummy_list])
    
    retrieved_df = add_entry_to_dataframe(added_data, retrieved_base_df)
    pdt.assert_frame_equal(retrieved_df, expected_dataframe)