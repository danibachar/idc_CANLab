import sys
import os
import pandas as pd
from .utils import build_remote_and_local_file_names
from .core.storage import upload_file

def info_dfs(dfs):
    remote, local = build_remote_and_local_file_names("info","txt")
    f =  open(local, 'w')
    weak_stdout = sys.stdout
    sys.stdout = f
    for df in dfs:
        print(df.info())
        for col in df.columns:
            u = df[col].unique()
            print("{} has {} unique values".format(col, len(u)))
            print("unique value = {}".format(u))
    sys.stdout = weak_stdout
    f.close()

    remote_url = upload_file(local, remote)
    return remote_url

def describe_dfs(dfs):
    urls = []
    for df in dfs:
        remote, local = build_remote_and_local_file_names("descibe","csv")
        f1, f2,f3 = "object_"+local, "category_"+local, "numeric_"+local
        f4, f5, f6 = "object_"+remote, "category_"+remote, "numeric_"+remote
        try:
            df.describe(include=['object']).to_csv(f1)
            urls += [upload_file(f1, f4),]
        except Exception as e:
            pass
        try:
            df.describe(include=['category']).to_csv(f2)
            urls += [upload_file(f2, f5),]
        except Exception as e:
            pass
        try:
            df.describe().to_csv(f3)
            urls += [upload_file(f3, f6)]
        except Exception as e:
            pass

    return urls
