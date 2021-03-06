from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource,Range1d

from .core.storage import upload_file
from .utils import chunks, build_remote_and_local_file_names

def plots_by_group_and_features(df, groupping_col_name, y_name, x_name, grid_features, width=300, height=200):
  groups = df.groupby(by=[groupping_col_name])

  plots = []
  for group in groups:
    g = group[-1]
    group_col = g[groupping_col_name]
    if len(group_col) == 0:
      continue

    parsed_feature_set = set()
    group_id = groupping_col_name+"="+str(group_col.iloc[0])
    plots += _plots_array_by(g, grid_features, y_name, x_name, width, height, group_id)

  grid_count = 0
  for f in grid_features:
      grid_count += len(df[f].unique())

  remote_file_name, local_file_name = build_remote_and_local_file_names("groups_by_features","html")
  output_file(local_file_name,mode='inline')
  local_url = save(gridplot(chunks(plots, len(grid_features)*(grid_count+len(grid_features)))))
  remote_url = upload_file(local_url, remote_file_name)
  return plots, remote_url

def plot_general_avg(df, y_name, x_name, width=600, height=400):
    max_y_value = df[y_name].max()
    min_y_value = df[y_name].min()
    groupd_avg = df.groupby(by=[x_name])[y_name].mean().reset_index()
    p = figure(
    plot_width=width, plot_height=height,
    title="Avarage {}".format(y_name)
    )
    p.line(x=x_name, y=y_name, source=ColumnDataSource(groupd_avg))
    p.y_range=Range1d(min_y_value, max_y_value)
    remote_file_name, local_file_name = build_remote_and_local_file_names("general_avg","html")
    output_file(local_file_name,mode='inline')
    local_url = save(p)
    remote_url = upload_file(local_url, remote_file_name)
    return p, remote_url

def plot_general_avg_grid(df, y_name, x_name, grid_features, width=400, height=400):

  plots = _plots_array_by(df, grid_features, y_name, x_name, width, height)

  grid_count = 0
  for f in grid_features:
      grid_count += len(df[f].unique())

  remote_file_name, local_file_name = build_remote_and_local_file_names("general_avg_grid","html")
  output_file(local_file_name,mode='inline')
  local_url = save(gridplot(chunks(plots, len(grid_features))))
  remote_url = upload_file(local_url, remote_file_name)
  return plots, remote_url


def _plots_array_by(df, grid_features, y_name, x_name, width, height, group_id=""):
    max_y_value = df[y_name].max()
    min_y_value = df[y_name].min()
    plots = []
    parsed_feature_set = set()

    for i in range(len(grid_features)):
        for j in range(len(grid_features)):
            feature_name = grid_features[i]
            feature_values = df[feature_name].unique()

            other_feature_name = grid_features[j]
            other_feature_values = df[other_feature_name].unique()

            for f_val in feature_values:
                for of_val in other_feature_values:
                    fkey1 = "{} X {}".format(f_val, of_val)
                    fkey2 = "{} X {}".format(of_val, f_val)
                    if fkey1 in parsed_feature_set or fkey2 in parsed_feature_set:
                        continue
                    parsed_feature_set.add(fkey1)
                    parsed_feature_set.add(fkey2)

                    title = group_id + "_" + feature_name + "=" + str(f_val) + "/" + other_feature_name + "=" + str(of_val)
                    selector = (df[feature_name] == f_val) & (df[other_feature_name] == of_val)
                    if True not in list(selector.unique()):
                      continue
                    gg = df[selector]
                    y = gg.groupby(by=[x_name])[y_name].mean().reset_index()

                    raw_data_source = ColumnDataSource(y)
                    p = figure(
                      plot_width=width, plot_height=height,
                      title=title,
                      x_axis_label=x_name,
                      y_axis_label=y_name,
                    )
                    p.y_range=Range1d(min_y_value, max_y_value)
                    p.title.text_font_size="7px"
                    p.xaxis.axis_label_text_font_size = "7px"
                    p.yaxis.axis_label_text_font_size = "7px"
                    p.line(x=x_name, y=y_name, source=raw_data_source)
                    plots.append(p)

    return plots
