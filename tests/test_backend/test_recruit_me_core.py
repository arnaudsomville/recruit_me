"""Test the recruit_me_core methods."""

import pytest
from pathlib import Path
from recruit_me.backend.recruit_me_core import RecruitMe
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