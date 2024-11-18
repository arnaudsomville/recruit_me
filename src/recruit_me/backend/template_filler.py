"""File used to fill gaps in the templates provided by the user."""

from datetime import datetime
from pathlib import Path
import uuid
from jinja2 import Environment, FileSystemLoader

from recruit_me.models.data_models import EmailRecipient
from recruit_me.utils.configuration import MainConfig

def fill_gaps_in_template(template_path: Path, email_recipient_data: EmailRecipient, output_file_name: str | None = None)->Path:
    """Fill the gaps 

    Args:
        template (Path): Path of the template used.
        email_recipient_data (Path): Data of the recipient of the email.

    Returns:
        Path: Path to a file containing the text of the template filled with correct data.
    """
    extension = template_path.suffix[1:]
    if output_file_name is None:
        output_file_name = template_path.name.replace(f'.{extension}', '')
    env = Environment(loader=FileSystemLoader(template_path.parent), autoescape=True)
    template = env.get_template(str(template_path.name))
    output = template.render(get_meta_data(email_recipient_data))
    output_folder = Path.home().joinpath(f"{MainConfig().home_folder}/outputs/templates/{str(template_path.name.replace(f'.{extension}', ''))}/{str(uuid.uuid4())}")
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder.joinpath(f'{str(output_file_name)}.{extension}')
    with open(output_file, 'w') as file:
        file.write(output)
    return output_file

def get_meta_data(email_recipient_data: EmailRecipient)->dict[str, str]:
    """Retrieve Metadata to be used by jinja2.

    Args:
        email_recipient_data (Path): Data of the recipient of the email.

    Returns:
        dict[str, str]: Meta data for jinja2.
    """
    return {
        "recipient_name": email_recipient_data.name,
        "recipient_email": email_recipient_data.email,
        "recipient_company": email_recipient_data.company,
        "recipient_position": email_recipient_data.position,
        "sender_name": MainConfig().user.name,
        "sender_email": MainConfig().user.email,
        "current_date": datetime.now().strftime("%d/%m/%Y"),
    }

if __name__ == '__main__':
    recipient=EmailRecipient(
        name='Elon Musk',
        email='elonmusk@real_email.com',
        company='SpaceX',
        position='CEO'
    )
    fill_gaps_in_template(Path.home().joinpath('.recruit_me/template_examples/template_cover_letter.txt'),recipient)