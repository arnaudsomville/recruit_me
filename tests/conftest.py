"""Function used before each test."""

import csv
from datetime import datetime
from pathlib import Path
import shutil
from typing import Iterable

from confz import DataSource
import pytest

from recruit_me.models.data_models import AnswerType, DataframeEntryModel, EmailRecipient
from recruit_me.utils.configuration import MainConfig
from recruit_me.utils.home_folder_management import verify_home_folder

def create_dummy_csv() -> None:
    """Create a dummy CSV file with email data."""
    dataframe_save_file = Path.home().joinpath(f'{MainConfig().home_folder}/{MainConfig().csv_file}')
    data = [
        ["first_sent", "last_sent", "recipient_company", "recipient_name", "recipient_position", "recipient_email", "amount_of_email_sent"],
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

dummy_dataframe_entries = [
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
        ),
        DataframeEntryModel(
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
    ]

expected_columns = DataframeEntryModel(
        first_sent=datetime.now(),
        last_sent=datetime.now(),
        recipient=EmailRecipient(name="Test", email="test@example.com", company="TestCompany"),
        answer=AnswerType.WAITING,
        amount_of_email_sent=0
    ).to_dict().keys()

@pytest.fixture(scope='function', autouse=True)
def pre_test_configuration()->Iterable:
    """Function executed before each test to make sure each tests are independant of each other."""
    conf = MainConfig().model_dump()
    conf['home_folder'] = '.test_recruit_me'
    test_folder = Path.home().joinpath('.test_recruit_me')
    if test_folder.exists():
        shutil.rmtree(str(test_folder))
    with MainConfig().change_config_sources(DataSource(conf)):
        verify_home_folder()
        create_dummy_csv()
        yield
