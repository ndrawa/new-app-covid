import pandas as pd
import numpy as np
import random
from datetime import datetime as dt
from bokeh.io import output_file, show
from bokeh.layouts import gridplot, layout
from bokeh.palettes import Category20
from bokeh.plotting import figure, curdoc
from bokeh.models import (ColumnDataSource, CDSView , GroupFilter, DataTable,
                          TableColumn , Row, Div, HoverTool, Select, Panel, Tabs, RangeSlider)
from bokeh.io import output_file, show

data = pd.read_csv('data_clean.csv')
data['country'].unique()
data.sort_values(by='year', ascending=True, inplace=True)

country = sorted(list(data.country.unique()))
year = sorted(list(data.year.unique()))

range_slider = RangeSlider(start=year[0], end=year[-1], value=year[:2], step=1, title='Month')
select= Select(title="Country", value=country[0], options=country)

df = data[(data['year'] >= range_slider.value[0]) & (data['year'] <= range_slider.value[1]) & data['country']==select.value] 
source = ColumnDataSource(data=df)

columns = [
        TableColumn(field="country", title="Country")
    ]

table = DataTable(source=source, columns=columns, height=500)


def plot_function(tickers):
    colors = list(Category20.values())[12]
    random_colors = []
    for c in range(len(tickers)):
        random_colors.append(random.choice(colors))

    TOOLTIPS = HoverTool(tooltips=[
                    ('Year', '$@{year}'),
                    ('Life Expectancy', '$@{life expectancy}'),
                    ('Country', '$@{country}')
                    ])

    p = figure(width=1000, height=500)

    for t, rc in zip(tickers, random_colors):
        view = CDSView(source=source, filters=[GroupFilter(column_name='country', group=t)])
        p.line(x='year', y='life expectancy', source=source, view=view, line_color=rc, line_width=4)

    p.add_tools(TOOLTIPS)
    return p

def text_function(attr, old, new):
    new_text = new
    old_text = old
    text_data = pd.read_json('text_data.json')

def filter_function():
    new_src = data[(data['country']==select.value)]
    source.data = new_src.to_dict('series')

def change_function(attr, old, new):
    filter_function()

def tabs(data):
    x = data[data['country']=='Afghanistan']['year']
    y = data[data['country']=='Afghanistan']['life expectancy']

    p1 = figure(width=1000, height=500)
    p1.circle(x, y, size=20, color="navy", alpha=0.5)
    tab1 = Panel(child=p1, title="circle")

    p2 = figure(width=1000, height=500)
    p2.line(x, y, line_width=3, color="navy", alpha=0.5)
    tab2 = Panel(child=p2, title="line")

    return Tabs(tabs=[tab1, tab2])

range_slider.on_change('value', change_function)
select.on_change('value', change_function)

title = Div(text='<h1 style="text-align: center">Bla blae</h1>')

widgets_row = Row(select, range_slider)
layout = layout([[title],
                 [widgets_row],
                 [plot_function(country)],
                #  [tabs(data)]
                ])
curdoc().title = 'Bla bla'
curdoc().add_root(layout)
show(layout)