import pandas as pd
import numpy as np
import os, random, string

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Based on - https://gist.github.com/sainathadapa/eb3303975196d15c73bac5b92d8a210f
def anti_join(x, y, left_on, right_on):
    """Return rows in x which are not present in y"""
    ans = pd.merge(left=x, right=y, how='left', indicator=True, left_on=left_on, right_on=right_on)
    ans = ans.loc[ans._merge == 'left_only', :].drop(columns='_merge')
    return ans


def anti_join_all_cols(x, y):
    """Return rows in x which are not present in y"""
    assert set(x.columns.values) == set(y.columns.values)
    return anti_join(x, y, x.columns.tolist())


def list_all_files_in_dir(root):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(root):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))

    return files

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
