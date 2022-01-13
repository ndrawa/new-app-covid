import pandas as pd
import random
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

range_slider = RangeSlider(start=year[0], end=year[-1], value=year[:2], step=1, title='Year')
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
    new_src = data[(data['year'] >= range_slider.value[0]) & (data['year'] <= range_slider.value[1]) & (data['country']==select.value)]
    source.data = new_src.to_dict('series')

def change_function(attr, old, new):
    filter_function()


range_slider.on_change('value', change_function)
select.on_change('value', change_function)


widgets_row = Row(select, range_slider)
layout = layout([[Div(text='<h1 style="text-align: center">Bla blae bom</h1>')],
                 [widgets_row],
                 [plot_function(country)],
                ])

curdoc().title = 'Bla bla bla'
curdoc().add_root(layout)
show(layout)