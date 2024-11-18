"""Test the recruit_me_core methods."""

from datetime import datetime
from pathlib import Path
from unittest.mock import mock_open, patch

import pandas as pd
from recruit_me.backend.recruit_me_core import RecruitMe
from recruit_me.models.data_models import AnswerType, DataframeEntryModel, EmailRecipient
from recruit_me.utils.configuration import MainConfig


def test_get_template_folder_creates_folder():
    """Test that get_template_folder creates and returns the correct path."""
    rm = RecruitMe()
    folder = rm.get_template_folder()

    # Assertions
    assert folder.exists()
    assert folder.is_dir()
    assert folder == Path.home().joinpath(f"{MainConfig().home_folder}/templates")

def test_get_template_list_returns_files():
    """Test that get_template_list returns a list of template files."""
    rm = RecruitMe()
    template_folder = rm.get_template_folder()

    # Créer des fichiers dans le dossier des templates
    (template_folder / "template1.txt").touch()
    (template_folder / "template2.html").touch()
    (template_folder / "not_a_template").mkdir()

    # Appel de la méthode
    templates = rm.get_template_list()

    # Assertions
    assert len(templates) == 2
    assert "template1.txt" in templates
    assert "template2.html" in templates

def test_get_cv_folder_creates_folder():
    """Test that get_cv_folder creates and returns the correct path."""
    rm = RecruitMe()
    folder = rm.get_cv_folder()

    # Assertions
    assert folder.exists()
    assert folder.is_dir()
    assert folder == Path.home().joinpath(f"{MainConfig().home_folder}/cvs")

def test_get_cv_list_returns_files():
    """Test that get_cv_list returns a list of CV files."""
    rm = RecruitMe()
    cv_folder = rm.get_cv_folder()

    # Créer des fichiers dans le dossier des CVs
    (cv_folder / "cv1.pdf").touch()
    (cv_folder / "cv2.docx").touch()
    (cv_folder / "not_a_cv").mkdir()

    # Appel de la méthode
    cvs = rm.get_cv_list()

    # Assertions
    assert len(cvs) == 2
    assert "cv1.pdf" in cvs
    assert "cv2.docx" in cvs


def test_send_email_success():
    """Test send_email method with all external calls mocked."""

    # Préparer les données de test
    recipient = EmailRecipient(
        name="Elon Musk",
        email="elonmusk@spacex.com",
        company="SpaceX",
        position="CEO"
    )
    email_object = "Join SpaceX!"
    cv_filename = "cv.pdf"
    cover_letter_template_filename = "cover_letter_template.txt"
    email_template_filename = "email_template.txt"

    # Instancier la classe RecruitMe
    recruit_me = RecruitMe()

    # Mock des appels externes
    with (
        patch.object(RecruitMe, "get_cv_list", return_value=["cv.pdf"]),
        patch.object(RecruitMe, "get_template_list", return_value=["cover_letter_template.txt", "email_template.txt"]),
        patch.object(RecruitMe, "get_template_folder", return_value=Path("/mocked/template/folder")),
        patch.object(RecruitMe, "get_cv_folder", return_value=Path("/mocked/cv/folder")),
        patch("recruit_me.backend.recruit_me_core.fill_gaps_in_template") as patch_fill_gaps_in_template,
        patch("recruit_me.backend.recruit_me_core.send_email") as patch_send_email,
        patch("recruit_me.backend.recruit_me_core.retrieve_dataframe") as patch_retrieve_dataframe,
        patch("recruit_me.backend.recruit_me_core.add_entry_to_dataframe") as patch_add_entry_to_dataframe,
        patch("recruit_me.backend.recruit_me_core.save_dataframe") as patch_save_dataframe,
        patch("builtins.open", mock_open(read_data="Mocked email content"))
    ):
        # Configurer les mocks qui ne sont pas dans les patch.object fixes
        patch_fill_gaps_in_template.return_value = Path("/mocked/outputs/mocked.txt")
        patch_send_email.return_value = True
        patch_retrieve_dataframe.return_value = []
        patch_add_entry_to_dataframe.return_value = []
        patch_save_dataframe.return_value = True

        # Appeler la méthode sous test
        result = recruit_me.send_email(
            email_recipient=recipient,
            email_object=email_object,
            cv_filename=cv_filename,
            cover_letter_template_filename=cover_letter_template_filename,
            email_template_filename=email_template_filename
        )

        # Assertions
        assert result is True

def test_update_response_status():
    """Test the update_response_status method with mocked external functions."""

    # Préparer les données de test
    email = "test@example.com"
    answer = AnswerType.ACCEPTED

    # Instancier la classe RecruitMe
    recruit_me = RecruitMe()

    # Mock des appels externes
    with (
        patch("recruit_me.backend.recruit_me_core.retrieve_dataframe") as mock_retrieve_dataframe,
        patch("recruit_me.backend.recruit_me_core.update_response_status") as mock_update_response_status,
        patch("recruit_me.backend.recruit_me_core.save_dataframe") as mock_save_dataframe,
    ):
        # Configurer les retours des mocks
        mock_dataframe = "Mocked DataFrame"
        mock_retrieve_dataframe.return_value = mock_dataframe
        mock_update_response_status.return_value = mock_dataframe

        # Appeler la méthode sous test
        recruit_me.update_response_status(email, answer)

        # Vérifier les appels des mocks
        mock_retrieve_dataframe.assert_called_once()
        mock_update_response_status.assert_called_once_with(email, answer, mock_dataframe)
        mock_save_dataframe.assert_called_once_with(mock_dataframe)

def test_relaunch_everyone():
    """Test the relaunch_everyone method, ensuring only unanswered emails are resent."""
    
    # Prepare test data
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
            amount_of_email_sent=1
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
            amount_of_email_sent=1
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
            answer=AnswerType.WAITING,
            amount_of_email_sent=2
        )
    ]

    # Create the dataframe to mock retrieve_dataframe
    expected_dataframe = pd.DataFrame(data=[data.to_dict() for data in dummy_dataframe_entries])

    # Mock retrieve_dataframe and send_email
    with patch("recruit_me.backend.recruit_me_core.retrieve_dataframe", return_value=expected_dataframe), \
         patch.object(RecruitMe, "send_email") as mock_send_email:

        # Create the RecruitMe instance
        recruit_me = RecruitMe()

        # Call the method
        recruit_me.relaunch_everyone(
            email_object="Reminder: Opportunity",
            cv_filename="cv.pdf",
            cover_letter_template_filename="cover_letter_template.txt",
            email_template_filename="email_template.txt"
        )

        # Ensure send_email was called only for entries with AnswerType.WAITING
        assert mock_send_email.call_count == 2
        mock_send_email.assert_any_call(
            dummy_dataframe_entries[0].recipient,
            "Reminder: Opportunity",
            "cv.pdf",
            "cover_letter_template.txt",
            "email_template.txt"
        )
        mock_send_email.assert_any_call(
            dummy_dataframe_entries[2].recipient,
            "Reminder: Opportunity",
            "cv.pdf",
            "cover_letter_template.txt",
            "email_template.txt"
        )