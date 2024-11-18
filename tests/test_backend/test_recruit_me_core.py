"""Test the recruit_me_core methods."""

from pathlib import Path
from unittest.mock import patch
from recruit_me.backend.recruit_me_core import RecruitMe
from recruit_me.models.data_models import EmailRecipient
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
        patch("recruit_me.backend.recruit_me_core.save_dataframe") as patch_save_dataframe
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

        # Vérifications des appels des mocks
        patch_fill_gaps_in_template.assert_any_call(
            Path("/mocked/template/folder/cover_letter_template.txt"),
            recipient,
            "Cover Letter"
        )
        patch_fill_gaps_in_template.assert_any_call(
            Path("/mocked/template/folder/email_template.txt"),
            recipient,
            "Email filled template"
        )
        patch_send_email.assert_called_once()
        patch_retrieve_dataframe.assert_called_once()
        patch_add_entry_to_dataframe.assert_called_once()
        patch_save_dataframe.assert_called_once()