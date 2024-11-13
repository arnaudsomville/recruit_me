"""Verify the integrity of home folder."""

from pathlib import Path
import shutil


def verify_home_folder()->None:
    """Create the home folder if needed with all the needed resources."""
    home_folder = Path.home().joinpath('.recruit_me')
    home_folder.mkdir(parents=True, exist_ok=True)

    conf_file = home_folder.joinpath('configuration.yaml')
    if not conf_file.exists():
        shutil.copy(Path(__file__).parents[1].joinpath('configuration_template.yaml'),conf_file)

if __name__ == '__main__': #pragma: no-cover
    verify_home_folder()