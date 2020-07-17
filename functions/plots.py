from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource

from .storage import upload_file
from .utils import chunks, build_remote_and_local_file_names

def plots_by_group_and_features(df, groupping_col_name, y_name, x_name, grid_features, width=200, height=200):
  # print("Groupping by - ",groupping_col_name)
  # print("y value by - ", y_name)
  # print("x value by - ",x_name)
  # print("feature matrix - ",grid_features)
  groups = df.groupby(by=[groupping_col_name])

  plots = []
  for group in groups:
    g = group[-1]
    _grid_features = grid_features.copy()
    group_col = g[groupping_col_name]
    if len(group_col) == 0:
      continue
    group_id = groupping_col_name+"="+str(group_col.iloc[0])
    for feature_name in _grid_features:
      feature_values = g[feature_name].unique()
      _grid_features.remove(feature_name)
      for f_val in feature_values:
        for other_feature_name in _grid_features:
          other_feature_values = g[other_feature_name].unique()
          for of_val in other_feature_values:
            title = group_id + "_" + feature_name + "=\n" + str(f_val) + "/\n" + other_feature_name + "=" + str(of_val)
            selector = (g[feature_name] == f_val) & (g[other_feature_name] == of_val)
            gg = g[selector]
            y = gg.groupby(by=[x_name])[y_name].mean().reset_index()
            raw_data_source = ColumnDataSource(y)
            p = figure(
              plot_width=width, plot_height=height,
              title=title,
              title_text_font_size="10pt"
              x_axis_label=x_name,
              x_axis_label_text_font_size="5pt",
              y_axis_label=y_name,
              y_axis_label_text_font_size="5pt"
            )
            p.line(x=x_name, y=y_name, source=raw_data_source)
            plots.append(p)

  remote_file_name, local_file_name = build_remote_and_local_file_names("groups_by_features","html")
  output_file(local_file_name,mode='inline')
  local_url = save(gridplot(chunks(plots, len(groups))))
  remote_url = upload_file(local_url, remote_file_name)
  return plots, remote_url

def plot_general_avg(df, y_name, x_name, width=200, height=200):
  groupd_avg = df.groupby(by=[x_name])[y_name].mean().reset_index()
  p = figure(
    plot_width=width, plot_height=height,
    title="Avarage {}".format(y_name)
  )
  p.line(x=x_name, y=y_name, source=ColumnDataSource(groupd_avg))

  remote_file_name, local_file_name = build_remote_and_local_file_names("general_avg","html")
  output_file(local_file_name,mode='inline')
  local_url = save(p)
  remote_url = upload_file(local_url, remote_file_name)
  return p, remote_url

def plot_general_avg_grid(df, y_name, x_name, grid_features, width=200, height=200):
  plots = []
  _grid_features = grid_features.copy()
  for feature_name in _grid_features:
    feature_values = df[feature_name].unique()
    _grid_features.remove(feature_name)
    for f_val in feature_values:
      for other_feature_name in _grid_features:
        other_feature_values = df[other_feature_name].unique()
        for of_val in other_feature_values:
          title = feature_name + "=" + str(f_val) + "/" + other_feature_name + "=" + str(of_val)
          selector = (df[feature_name] == f_val) & (df[other_feature_name] == of_val)
          gg = df[selector]
          y = gg.groupby(by=[x_name])[y_name].mean().reset_index()
          raw_data_source = ColumnDataSource(y)
          p = figure(
            plot_width=width, plot_height=height,
            title=title,
            x_axis_label=x_name,
            y_axis_label=y_name
          )
          p.line(x=x_name, y=y_name, source=raw_data_source)
          plots.append(p)

  remote_file_name, local_file_name = build_remote_and_local_file_names("general_avg_grid","html")
  output_file(local_file_name,mode='inline')
  local_url = save(gridplot(chunks(plots, len(groups))))
  remote_url = upload_file(local_url, remote_file_name)
  return plots, remote_url
