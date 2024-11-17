"""Test for the endpoints."""

from fastapi.testclient import TestClient
from pathlib import Path
from recruit_me.api.main_api import app
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