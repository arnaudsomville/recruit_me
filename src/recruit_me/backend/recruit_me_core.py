"""Core file orchestrating calls of functions and processing."""

from pathlib import Path

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
        return [file.name for file in self.get_template_folder().iterdir() if file.is_file()]

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
        return [file.name for file in self.get_cv_folder().iterdir() if file.is_file()]