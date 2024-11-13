"""Function used before each test."""

from pathlib import Path
import shutil
from typing import Iterable

from confz import DataSource
import pytest

from recruit_me.utils.configuration import MainConfig
from recruit_me.utils.home_folder_management import verify_home_folder

@pytest.fixture(scope='function', autouse=True)
def pre_test_configuration()->Iterable:
    conf = MainConfig().model_dump()
    conf['home_folder'] = '.test_recruit_me'
    test_folder = Path.home().joinpath('.test_recruit_me')
    if test_folder.exists():
        shutil.rmtree(str(test_folder))
    with MainConfig().change_config_sources(DataSource(conf)):
        verify_home_folder()
        yield
