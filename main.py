import pandas as pd
import random
from bokeh.io import output_file, show
from bokeh.layouts import gridplot, layout
from bokeh.palettes import Category20
from bokeh.plotting import figure, curdoc
from bokeh.models import (ColumnDataSource, CDSView, GroupFilter, DataTable,
                          TableColumn, Column, Row, Div, HoverTool, Select)


data = pd.read_csv('data_clean.csv')
data['status'].unique()
data.sort_values(by='year', ascending=True, inplace=True)

status = sorted(list(data.status.unique()))

type_select= Select(title="Status", value=status[0], options=status)
df = data[data['status']==type_select.value]
source = ColumnDataSource(data=df)

# TABLE
# Creating the list of columns:
columns = [
        TableColumn(field="status", title="Status")
    ]
# Initializing the table:
table = DataTable(source=source, columns=columns, height=500)

# PLOT
def plot_function(tickers):
    # Getting some colors:
    colors = list(Category20.values())[17]
    random_colors = []
    for c in range(len(tickers)):
        random_colors.append(random.choice(colors))

    # Create the hovertool:
    TOOLTIPS = HoverTool(tooltips=[    ('year', '$@{year}'),
                #    ('AvgPrice', '$@{AveragePrice}'),
                #    ('Total Volume', '$@{TotalVolume}'),
                   ('Life Expectancy', '$@{life expectancy}')],
                         formatters={'$x': 'datetime'})

    # Create the figure to store all the plot lines in:
    p = figure(x_axis_type='datetime', width=1000, height=500)

    # Loop through the tickers and colors and create plot line for each:
    for t, rc in zip(tickers, random_colors):
        view = CDSView(source=source, filters=[GroupFilter(column_name='country', group=t)])
        p.scatter(x='year', y='life expectancy', source=source, view=view, line_color=rc, line_width=4)
        p.line(x='year', y='life expectancy', source=source, view=view, line_color=rc, line_width=4)

    # Add the hovertool to the figure:
    p.add_tools(TOOLTIPS)
    return p

p = plot_function(status)

def text_function(attr, old, new):
    new_text = new
    old_text = old
    text_data = pd.read_json('text_data.json')

def filter_function():
    # Filter the data according to the widgets:
    new_src = data[(data['status']==type_select.value)]

    # Replace the data in the current data source with the new data:
    source.data = new_src.to_dict('series')

def change_function(attr, old, new):
    filter_function()

type_select.on_change('value', change_function)

# Header
title = Div(text='<h1 style="text-align: center">Bla blae</h1>')

# widgets_col = Column(month_slider, year_slider)
widgets_row = Row(type_select)
layout = layout([[title],
                 [widgets_row],
                 [p]
                ])
curdoc().title = 'Bla bla'
curdoc().add_root(layout)