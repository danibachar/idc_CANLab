import sys
import os
import pandas as pd

from .utils import build_remote_and_local_file_names
from .core.storage import upload_file

def save_locally_and_update(df, original_dfs, cleaning_dfs):
  urls = []
  for key, val in original_dfs.items():
      remote, local = build_remote_and_local_file_names("original","csv")
      val.to_csv(local, index=False)
      urls += [upload_file(local, remote),]

  for key, val in cleaning_dfs.items():
      remote, local = build_remote_and_local_file_names("clean","csv")
      val.to_csv(local, index=False)
      urls += [upload_file(local, remote),]

  remote, local = build_remote_and_local_file_names("primary","csv")
  df.to_csv(local, index=False)
  urls += [upload_file(local, remote),]

  return urls
