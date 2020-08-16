import sys
import os
import pandas as pd

from .utils import build_remote_and_local_file_names
from .core.storage import upload_file

def save_locally_and_update(df, original_dfs=None, cleaning_dfs=None):
    original_files_urls = []
    if original_dfs:
        for key, val in original_dfs.items():
          remote, local = build_remote_and_local_file_names(key,"csv")
          val.to_csv(local, index=False)
          original_files_urls += [upload_file(local, remote),]

    cleaning_files_urls = []
    if cleaning_dfs:
        for key, val in cleaning_dfs.items():
          remote, local = build_remote_and_local_file_names(key,"csv")
          val.to_csv(local, index=False)
          cleaning_files_urls += [upload_file(local, remote),]

    remote, local = build_remote_and_local_file_names("primary","csv")
    df.to_csv(local, index=False)
    primary_file_urls = [upload_file(local, remote),]

    return original_files_urls, cleaning_files_urls, primary_file_urls
