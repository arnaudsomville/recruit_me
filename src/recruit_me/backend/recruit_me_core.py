"""Core file orchestrating calls of functions and processing."""

from datetime import datetime
from pathlib import Path

from recruit_me.backend.dataframe_manager import add_entry_to_dataframe, dataframe_to_list, retrieve_dataframe, save_dataframe, update_response_status
from recruit_me.backend.email_sender import send_email
from recruit_me.backend.template_filler import fill_gaps_in_template
from recruit_me.models.data_models import AnswerType, DataframeEntryModel, EmailModel, EmailRecipient
from recruit_me.utils.configuration import MainConfig


class RecruitMe:
    """Orchestrator of the project."""

    def __init__(self) -> None:
        """Class constructor."""
        pass

    def get_template_folder(self)->Path:
        """Retrieve the Template path.

        Returns:
            Path: Template path.
        """
        folder = Path.home().joinpath(f'{MainConfig().home_folder}/templates')
        folder.mkdir(parents=True, exist_ok=True)
        return folder
    def get_template_list(self)->list:
        """Retrieve templates list.

        Returns:
            list: List of templates.
        """
        return sorted([file.name for file in self.get_template_folder().iterdir() if file.is_file()])

    def get_cv_folder(self)->Path:
        """Retrieve the cv path.

        Returns:
            Path: Cv path.
        """
        folder = Path.home().joinpath(f'{MainConfig().home_folder}/cvs')
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def get_cv_list(self)->list:
        """Retrieve cv list.

        Returns:
            list: List of cvs.
        """
        return sorted([file.name for file in self.get_cv_folder().iterdir() if file.is_file()])
    
    def send_email(
            self,
            email_recipient: EmailRecipient,
            email_object: str,
            cv_filename: str,
            cover_letter_template_filename: str,
            email_template_filename:str,
        )->bool:
        """Function used to send email to the recipient.

        Args:
            email_recipient (EmailRecipient): details of the recipient.
            cv_filename (str): Cv filename.
            cover_letter_template_filename (str): cover letter template filename.
            email_template_filename (str): email template filename.

        Returns:
            bool: Wether the email sending worked or not.
        """
        #Verify that files exist
        if cv_filename not in self.get_cv_list():
            raise ValueError(f"Provided cv '{cv_filename}' not in file list. Imported cvs are {' '.join(map(str, self.get_cv_list()))}")
        
        if cover_letter_template_filename not in self.get_template_list():
            raise ValueError(f"Provided cover letter '{cover_letter_template_filename}' not in file list. Imported templates are {' '.join(map(str, self.get_template_list()))}")
        
        if email_template_filename not in self.get_template_list():
            raise ValueError(f"Provided email '{email_template_filename}' not in file list. Imported templates are {' '.join(map(str, self.get_template_list()))}")
        
        #Fill the templates
        filled_cover_letter_path = fill_gaps_in_template(self.get_template_folder().joinpath(cover_letter_template_filename), email_recipient, 'Cover Letter')
        filled_email_template_path = fill_gaps_in_template(self.get_template_folder().joinpath(cover_letter_template_filename), email_recipient, 'Email filled template')
        cv_path = self.get_cv_folder().joinpath(cv_filename)

        #Send the email
        with open(filled_email_template_path, 'r') as file_out:
            email_content = file_out.read()
        email_model = EmailModel(
            recipient=email_recipient,
            content=email_content,
            object= email_object,
            attached_files=[filled_cover_letter_path, cv_path]
        )
        email_sent = send_email(email_model)
        if not email_sent:
            raise RuntimeError("An error occured while sending the email.")
        
        #Add to csv save, could have used a db (even sqlite db) but seemed overkill
        entry_model = DataframeEntryModel(
            first_sent=datetime.now(),
            last_sent=datetime.now(),
            recipient=email_recipient,
            answer=AnswerType.WAITING,
            amount_of_email_sent=1
        )
        dataframe = retrieve_dataframe()
        dataframe = add_entry_to_dataframe(entry_model, dataframe)
        return save_dataframe(dataframe)

    def update_response_status(self, email:str, answer: AnswerType)->None:
        """_summary_

        Args:
            email (str): email of the recipient
            answer (AnswerType): new type of answer

        """
        dataframe = retrieve_dataframe()
        dataframe = update_response_status(email, answer, dataframe)
        save_dataframe(dataframe)
    
    def relaunch_everyone(
            self,
            email_object: str,
            cv_filename: str,
            cover_letter_template_filename: str,
            email_template_filename:str
        )->int:
        """Relaunch everyone who did not answer yet.

        Args:
            email_object (str): Object of the emails.
            cv_filename (str): Cv filename.
            cover_letter_template_filename (str): cover letter template filename.
            email_template_filename (str): email template filename.
        
        Return:
            int: number of people relaunched
        """
        dataframe = retrieve_dataframe()
        sent_email_list = dataframe_to_list(dataframe)

        people_relaunched = 0

        for email_data in sent_email_list:
            if email_data.answer != AnswerType.WAITING:
                continue
            self.send_email(
                email_data.recipient,
                email_object,
                cv_filename,
                cover_letter_template_filename,
                email_template_filename
            )
            people_relaunched += 1
        return people_relaunched