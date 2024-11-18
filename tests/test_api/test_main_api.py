"""Test for the endpoints."""

from unittest.mock import patch
from fastapi.testclient import TestClient
from pathlib import Path
from recruit_me.api.main_api import app
from recruit_me.models.data_models import AnswerType, EmailRecipient
from recruit_me.utils.configuration import MainConfig

client = TestClient(app)

def test_health_endpoint():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200}


def test_upload_template_success():
    """Test uploading a template successfully."""
    files = {"file": ("example_template.txt", b"This is a template.")}
    response = client.post("/upload_template", files=files)
    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert "Template saved as example_template.txt" in response.json()["description"]


def test_upload_template_duplicate():
    """Test uploading a duplicate template."""
    template_folder = Path.home().joinpath(f"{MainConfig().home_folder}/templates")
    template_folder.mkdir(parents=True, exist_ok=True)
    (template_folder / "example_template.txt").touch()  # Create a file beforehand

    files = {"file": ("example_template.txt", b"This is another template.")}
    response = client.post("/upload_template", files=files)
    assert response.status_code == 200
    assert response.json()["status_code"] == 409
    assert "The template already exists" in response.json()["description"]


def test_upload_template_invalid_format():
    """Test uploading a template with an invalid format."""
    files = {"file": ("invalid_template.pdf", b"This is an invalid template.")}
    response = client.post("/upload_template", files=files)
    assert response.status_code == 200
    assert response.json()["status_code"] == 400
    assert "Unauthorized file format" in response.json()["description"]


def test_upload_cv_success():
    """Test uploading a CV successfully."""
    files = {"file": ("example_cv.pdf", b"This is a CV.")}
    response = client.post("/upload_cv", files=files)
    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert "Template saved as example_cv.pdf" in response.json()["description"]


def test_upload_cv_invalid_format():
    """Test uploading a CV with an invalid format."""
    files = {"file": ("invalid_cv.txt", b"This is an invalid CV.")}
    response = client.post("/upload_cv", files=files)
    assert response.status_code == 200
    assert response.json()["status_code"] == 400
    assert "Unauthorized file format" in response.json()["description"]

def test_upload_cv_duplicate():
    """Test uploading a duplicate cv."""
    cv_folder = Path.home().joinpath(f"{MainConfig().home_folder}/cvs")
    cv_folder.mkdir(parents=True, exist_ok=True)
    (cv_folder / "example_cv.pdf").touch()  # Create a file beforehand

    files = {"file": ("example_cv.pdf", b"This is another cv.")}
    response = client.post("/upload_cv", files=files)
    assert response.status_code == 200
    assert response.json()["status_code"] == 409
    assert "The cv already exists" in response.json()["description"]

def test_get_cv_list():
    """Test retrieving the list of uploaded CVs."""
    cv_folder = Path.home().joinpath(f"{MainConfig().home_folder}/cvs")
    cv_folder.mkdir(parents=True, exist_ok=True)
    (cv_folder / "cv1.pdf").touch()
    (cv_folder / "cv2.pdf").touch()

    response = client.get("/get_cv_list")
    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert "cv1.pdf cv2.pdf" in response.json()["description"]


def test_get_template_list():
    """Test retrieving the list of uploaded templates."""
    template_folder = Path.home().joinpath(f"{MainConfig().home_folder}/templates")
    template_folder.mkdir(parents=True, exist_ok=True)
    (template_folder / "template1.txt").touch()
    (template_folder / "template2.html").touch()

    response = client.get("/get_template_list")
    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert "template1.txt template2.html" in response.json()["description"]


def test_send_email_endpoint():
    """Test the /send_email endpoint with send_email mocked."""
    email_data = {
        "email_recipient": {
            "name": "Elon Musk",
            "email": "elonmusk@spacex.com",
            "company": "SpaceX",
            "position": "CEO"
        },
        "email_object": "Join SpaceX!",
        "cv_filename": "cv.pdf",
        "cover_letter_template_filename": "cover_letter_template.txt",
        "email_template_filename": "email_template.txt"
    }

    # Mock RecruitMe.send_email
    with patch("recruit_me.api.main_api.RecruitMe.send_email", return_value=True) as mock_send_email:
        response = client.post("/send_email", json=email_data)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            'status_code': 200,
            'description': f"Email successfully sent to {email_data['email_recipient']['email']}"
        }
        mock_send_email.assert_called_once_with(
            email_recipient=EmailRecipient(**email_data["email_recipient"]),
            email_object=email_data["email_object"],
            cv_filename=email_data["cv_filename"],
            cover_letter_template_filename=email_data["cover_letter_template_filename"],
            email_template_filename=email_data["email_template_filename"]
        )

def test_download_summary_existing_file():
    """Test the /download_summary endpoint when the file exists."""
    file_path = Path.home().joinpath(f"{MainConfig().home_folder}/{MainConfig().csv_file}")
    file_path.touch()
    with (
        patch("recruit_me.api.main_api.Path.exists", return_value=True),
    ):
        response = client.get("/download_summary")
        assert response.status_code == 200


def test_download_summary_no_file():
    """Test the /download_summary endpoint when the file does not exist."""
    file_path = Path.home().joinpath(f"{MainConfig().home_folder}/{MainConfig().csv_file}")
    file_path.touch()
    with (
        patch("recruit_me.api.main_api.Path.exists", return_value=True),
    ):
        response = client.get("/download_summary")
        assert response.status_code == 200

def test_update_answer_success():
    """Test the /update_answer endpoint with a successful update."""
    
    # Préparer les données de test
    test_data = {
        "email": "test@example.com",
        "new_answer": AnswerType.ACCEPTED
    }

    # Mock de la méthode update_response_status
    with patch("recruit_me.api.main_api.RecruitMe.update_response_status") as mock_update_response_status:
        # Configurer le mock pour ne rien retourner
        mock_update_response_status.return_value = None

        # Appeler l'endpoint
        response = client.post("/update_answer", json=test_data)

        # Vérifier la réponse
        assert response.status_code == 200
        assert response.json() == {
            'status_code': 200,
            'description': 'Data updated'
        }

        # Vérifier l'appel du mock
        mock_update_response_status.assert_called_once_with(
            test_data["email"], test_data["new_answer"]
        )
def test_update_answer_failure():
    """Test the /update_answer endpoint when an error occurs."""
    
    # Préparer les données de test
    test_data = {
        "email": "test@example.com",
        "new_answer": AnswerType.ACCEPTED
    }

    # Mock de la méthode update_response_status pour qu'elle raise une exception
    with patch("recruit_me.api.main_api.RecruitMe.update_response_status") as mock_update_response_status:
        mock_update_response_status.side_effect = RuntimeError("Mocked exception")

        # Appeler l'endpoint
        response = client.post("/update_answer", json=test_data)

        # Vérifier la réponse
        assert response.json() == {
            'status_code': 500,
            'description': 'Internal error : Mocked exception'
        }

        # Vérifier l'appel du mock
        mock_update_response_status.assert_called_once_with(
            test_data["email"], test_data["new_answer"]
        )