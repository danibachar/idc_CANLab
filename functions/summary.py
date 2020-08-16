import sys
import os
import pandas as pd
from .utils import build_remote_and_local_file_names
from .core.storage import upload_file

def accuracy_calculator(before_df, after_df, group_by, unique_key, features_col_names):
    before = before_df.copy()
    after = after_df.copy()
    res_before, res_after = {}, {}
    dfs = []
    def fill_res(groups, results):
        for group in groups:
          g = group[-1]
          group_col = g[group_by]
          group_id = group_by+"="+str(group_col.iloc[0])
          results[group_id] = {}
          parsed_feature_set = set()
          for first_feature_name in features_col_names:
              for second_feature_name in features_col_names:
                  if first_feature_name == second_feature_name:
                      continue
                  first_feature_values = g[first_feature_name].unique()
                  second_feature_values = g[second_feature_name].unique()
                  for f_val in first_feature_values:
                    for s_val in second_feature_values:
                        fkey1 = "{} X {}".format(f_val, s_val)
                        fkey2 = "{} X {}".format(s_val, f_val)
                        if fkey1 in parsed_feature_set or fkey2 in parsed_feature_set:
                            continue
                        parsed_feature_set.add(fkey1)
                        parsed_feature_set.add(fkey2)
                        sel = (g[first_feature_name] == f_val) & (g[second_feature_name] == s_val)
                        f = first_feature_name+"="+str(f_val)
                        s = second_feature_name+"="+str(s_val)
                        name = f+" / "+s

                        results[group_id][name] = g[sel][unique_key].nunique()
    groups_before = before.groupby(by=[group_by])
    groups_after = after.groupby(by=[group_by])
    fill_res(groups_before, res_before)
    fill_res(groups_after, res_after)


    for key, b in res_before.items():
        rrrr = {}
        a = res_after.get(key,{})
        count_before = []
        count_after = []
        accuracy = []

        for k,v in b.items():
            if v==0:
                continue
            grrrr = k.split("/")
            c1 = grrrr[0].split("=")
            name1 = c1[0]
            val1 = c1[1]
            c2 = grrrr[1].split("=")
            name2 = c2[0]
            val2 = c2[1]
            if name1 in rrrr:
                rrrr[name1].append(val1)
            else:
                rrrr[name1] = [val1]

            if name2 in rrrr:
                rrrr[name2].append(val2)
            else:
                rrrr[name2] = [val2]
            af = a.get(k,0)
            count_before.append(v)
            count_after.append(af)
            acc = af/v
            accuracy.append(acc)

        rrrr["participant"] = [key]*len(count_before)
        rrrr["count_before"] = count_before
        rrrr["count_after"] = count_after
        rrrr["accuracy"] = accuracy
        try:
            dfs.append(pd.DataFrame(rrrr))
        except Exception as e:
            pass

    remote, local = build_remote_and_local_file_names("accuracy","csv")
    pd.concat(dfs).to_csv(local)
    return upload_file(local, remote)


def info_dfs(dfs):
    remote, local = build_remote_and_local_file_names("info","txt")
    f =  open(local, 'w')
    weak_stdout = sys.stdout
    sys.stdout = f
    for df in dfs:
        print(df.info())
        print("Null/Nan Values\nPlease note, Null/Nan values could indicate a problem with your data")
        print("On the left you will see the relevant column name, and on the right the amount of Null/Nan rows for that column")
        print(df.isnull().sum())
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
