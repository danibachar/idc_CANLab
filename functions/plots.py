import bokeh.plotting
from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
from bokeh.io import output_notebook
import .storage

def plots_by_group_and_features(df, groupping_col_name, y_name, x_name, grid_features):
  print("Groupping by - ",groupping_col_name)
  print("y value by - ", y_name)
  print("x value by - ",x_name)
  print("feature matrix - ",grid_features)
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
            title = group_id + "_" + feature_name + "=" + str(f_val) + "/" + other_feature_name + "=" + str(of_val)
            selector = (g[feature_name] == f_val) & (g[other_feature_name] == of_val)
            gg = g[selector]
            y = gg.groupby(by=[x_name])[y_name].mean().reset_index()
            raw_data_source = ColumnDataSource(y)
            p = figure(
              plot_width=400, plot_height=400,
              title=title,
              x_axis_label=x_name,
              y_axis_label=y_name
            )
            p.line(x=x_name, y=y_name, source=raw_data_source)
            plots.append(p)

    
  return plots

def plot_general_avg(df, y_name, x_name):
  groupd_avg = df.groupby(by=[x_name])[y_name].mean().reset_index()
  p = figure(
    plot_width=400, plot_height=400,
    title="Avarage {}".format(y_name)
  )
  p.line(x=x_name, y=y_name, source=ColumnDataSource(groupd_avg))
  return p

def plot_general_avg_grid(df, y_name, x_name, grid_features):
  plots = []
  # groupd_avg = df.groupby(by=[x_name])[y_name].mean().reset_index()
  _grid_features = grid_features.copy()
  # group_id = groupping_col_name+"="+str(g[groupping_col_name].iloc[0])
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
            plot_width=400, plot_height=400,
            title=title,
            x_axis_label=x_name,
            y_axis_label=y_name
          )
          p.line(x=x_name, y=y_name, source=raw_data_source)
          plots.append(p)
  return plots
