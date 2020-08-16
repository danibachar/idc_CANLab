import pandas as pd
import numpy as np
import os, random, string
from datetime import datetime

from .consts import PROJECT_NAME_ENV_VAR, USERNAME_ENV_VAR

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Based on - https://gist.github.com/sainathadapa/eb3303975196d15c73bac5b92d8a210f
def anti_join(x, y, left_on, right_on):
    """Return rows in x which are not present in y"""
    ans = pd.merge(left=x, right=y, how='left', indicator=True, left_on=left_on, right_on=right_on, suffixes=('', '_y'))
    ans = ans.loc[ans._merge == 'left_only', :].drop(columns='_merge')
    return ans


def anti_join_all_cols(x, y):
    """Return rows in x which are not present in y"""
    assert set(x.columns.values) == set(y.columns.values)
    return anti_join(x, y, x.columns.tolist())


def list_all_files_in_dir(root, filter_by_file_type = ["csv"]):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(root):
        for filename in filenames:
            if filename.split(".")[-1] in filter_by_file_type:
                files.append(os.path.join(dirpath, filename))

    return files

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def build_remote_and_local_file_names(prefix, file_type):
    PROJECT = os.environ[PROJECT_NAME_ENV_VAR]
    USERNAME = os.environ[USERNAME_ENV_VAR]
    date_str = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    location = "{}/{}".format(USERNAME, PROJECT)
    file_name = "{}_{}.{}".format(prefix, date_str, file_type)
    return "{}/{}".format(location, file_name), file_name
