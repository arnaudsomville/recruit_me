"""Test the template filler."""

from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from confz import DataSource
from jinja2 import TemplateNotFound
import pytest
from recruit_me.backend.template_filler import fill_gaps_in_template
from recruit_me.models.data_models import EmailRecipient
from recruit_me.utils.configuration import MainConfig


def test_txt_filling_nominal()->None:
    """Test the template filling with txt file."""
    conf = MainConfig().model_dump()
    conf['user']['name'] = 'Jane Smith'
    conf['user']['email'] = 'janesmith@example.com'

    recipient=EmailRecipient(
        name='John Doe',
        email='johndoe@example.com',
        company='Example Corp',
        position='Software Engineer'
    )
    
    with (
        patch("recruit_me.backend.template_filler.datetime") as mock_datetime,
        MainConfig().change_config_sources(DataSource(conf))
    ):
        mock_datetime.now.return_value = datetime(2023, 11, 13)
        template_folder = Path(__file__).parent.joinpath('templates_for_tests')
        output_file: Path = fill_gaps_in_template(template_folder.joinpath('template_for_test.txt'),recipient)
        assert output_file.exists()
        with open(output_file, 'r') as file_out, open(template_folder.joinpath('expected_filled_template_for_test.txt'), 'r') as expected_file:
            output_content = file_out.read()
            expected_content = expected_file.read()
            assert output_content == expected_content, "The filled template does not match the expected output."

def test_txt_filling_no_file()->None:
    """Test the template filling with txt file."""
    conf = MainConfig().model_dump()
    conf['user']['name'] = 'Jane Smith'
    conf['user']['email'] = 'janesmith@example.com'

    recipient=EmailRecipient(
        name='John Doe',
        email='johndoe@example.com',
        company='Example Corp',
        position='Software Engineer'
    )
    
    with pytest.raises(TemplateNotFound):
        template_folder = Path(__file__).parent.joinpath('templates_for_tests')
        fill_gaps_in_template(template_folder.joinpath('I_do_not_exist.txt'),recipient)
