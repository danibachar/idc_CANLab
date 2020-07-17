import sys
import os
from .utils import build_remote_and_local_file_names
from .core.storage import upload_file

def summarize_dfs(dfs):
    remote, local = build_remote_and_local_file_names("summarize",".txt")
    print("grrrr")
    print(remote)
    sys.stdout = open(local, 'w')
    for df in dfs:
        print(df.info())
        print(df.describe(include=['object']))
        print(df.describe())
    sys.stdout.close()
    remote_url = upload_file(local, remote)
    print(remote_url)
    return remote_url
