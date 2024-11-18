"""Configuration of the project."""

import os
from pathlib import Path
from typing import ClassVar
import warnings
from confz import ConfigSource, BaseConfig, EnvSource, FileSource
from confz.base_config import BaseConfigMetaclass

_DEFAULT_CONF_FILE_PATH = Path.home().joinpath('.recruit_me/configuration.yaml')
_TEMPLATE_CONF_FILE_PATH = Path(__file__).parents[1].joinpath('configuration_template.yaml')
_CONF_FILE_ENV_VAR_NAME = 'RECRUIT_ME_CONF_FILE_PATH'

def get_config_file_path() -> Path:
    """Get configuration file path.

    If the env var is set MPC_CONF_FILE_PATH, it reads the CONF_FILE from there.
    Otherwise, it uses the default path in _DEFAULT_CONF_FILE_PATH

    """
    path = Path(os.getenv(_CONF_FILE_ENV_VAR_NAME, _DEFAULT_CONF_FILE_PATH))
    if path.exists():
        return path
    elif _TEMPLATE_CONF_FILE_PATH.exists():
        warnings.warn("Warning : Template configuration loaded : No configuration file found, verify the _CONF_FILE_ENV_VAR_NAME env variable or the .recruit_me home folder.")
        return _TEMPLATE_CONF_FILE_PATH
    else:
        raise FileNotFoundError("Error : No configuration found, even the template !")

class EmailConf(BaseConfig, metaclass=BaseConfigMetaclass):
    """Configuration model for user."""

    name: str
    email: str
    password: str
    smtp_server: str
    smtp_port: int


class MainConfig(BaseConfig, metaclass=BaseConfigMetaclass):
    """Configuration of the project."""

    user: EmailConf
    home_folder: str
    csv_file: str

    CONFIG_SOURCES: ClassVar[list[ConfigSource]] = [
        FileSource(file=get_config_file_path()),
        EnvSource(prefix='CONF_', allow_all=True, nested_separator='__'),
    ]


if __name__ == '__main__':  # pragma: no cover
    print(MainConfig())