# -*- coding: utf-8 -*-

import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash()
app.title = 'DASHBOARD'

server = app.server

#extarct, transform and load from data/coffees.csv
df = pd.read_csv('data/coffees.csv')
df.dropna(inplace=True)
df['coffees'] = df.coffees.astype(int)
df['timestamp'] = pd.to_datetime(df.timestamp)

colors = {'background': '#3a3e38',
          'text': 'white'}

app.layout = html.Div(children=[
    html.Div(children=[
        html.Img(src='https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo'
                     '/new-branding/dash-logo-by-plotly-stripe.png',
                 style={'height': '100px',
                        'float': 'right'}),
        html.H1('Coffees - Consumption Overview',
                style={'float': 'left',
                        'color': '#3a3e38',
                        'font-size': '40px',
                        'font-family': 'Product Sans'})
    ], style={'grid-column': '1 / -1'}),
    html.Div(children=[
        html.Div([
            html.H3(id='slider-range'),
            html.H3('TOTAL COFFEES: %s' % sum(df.coffees)),
            html.H3(id='total-coffees')
        ], style={'display': 'grid',
                  'text-align': 'center',
                  'grid-template-columns': '1fr 1fr 1fr'}),
        dcc.RangeSlider(id='timestamp-slider',
                        min=0,
                        max=len(df),
                        value=[200, 400]),
    ], style={'grid-column': '1 / -1',
              'padding-bottom': '10px'}),
    html.Div(children=[
        dcc.Graph(id='GRAPH-1'),
        dcc.Graph(id='GRAPH-2')
    ], style={'display': 'grid',
              'grid-template-rows': '300px 300px',
              'grid-template-columns': 'autofit',
              'grid-gap': '5px'}),
    html.Div(children=[
        dt.DataTable(rows=[{}],
                     row_selectable=True,
                     min_height=605,
                     sortable=True,
                     selected_row_indices=[],
                     id='table'),
        html.Div(id='selected-indexes')
    ])
], style={'padding-top': '10px',
          'padding-bottom': '10px',
          'margin-left': 'auto',
          'margin-right': 'auto',
          'padding-left': '20px',
          'padding-right': '20px',
          'font-size': '1em',
          'width': '95%',
          'font-family': 'Product Sans',
          'display': 'grid',
          'grid-template-columns': '50% 50%',
          'grid-gap': '10px'})

@app.callback(Output('table', 'rows'),
              [Input('timestamp-slider', 'value')])
def update_table(value):
    """
    For user selections, return the relevant table
    """
    global df
    mdf = df.iloc[value[0]: value[-1]]
    return mdf.to_dict('records')

@app.callback(Output('slider-range', 'children'),
              [Input('timestamp-slider', 'value')])
def update_range(value):
    """
    For user selections, return the relevant range
    """
    global df
    min, max = df.timestamp.iloc[value[0]], df.timestamp.iloc[value[-1]]
    return '{} | {}'.format(min, max)

@app.callback(Output('total-coffees', 'children'),
              [Input('timestamp-slider', 'value')])
def update_info(value):
    """
    For user selections, return the relevant range
    """
    global df
    tc = sum(df.coffees.iloc[value[0]: value[-1]])
    return '{}'.format(tc)

@app.callback(Output('GRAPH-1', 'figure'),
              [Input('timestamp-slider', 'value')])
def update_graph_1(value):
    """
    For user selections, return the coffee consumption for each contributor
    """
    global df, colors
    mdf = df.iloc[value[0]: value[-1]]
    figure={'layout': {'plot_bgcolor': colors['background'],
                       'paper_bgcolor': colors['background'],
                       'font': { 'color': colors['text'] },
                       'title': 'individual consumption'},
            'data': [{'x': [i],
                       'y': [sum(mdf[mdf.contributor==i].coffees)],
                       'type': 'bar',
                       'name': i}
                       for i in mdf.contributor.unique() ]}
    return figure

@app.callback(Output('GRAPH-2', 'figure'),
              [Input('timestamp-slider', 'value')])
def update_graph_2(value):
    """
    For user selections, return the coffee consumption per day
    """
    global df, colors
    mdf = df.iloc[value[0]: value[-1]]
    figure={'layout': {'plot_bgcolor': colors['background'],
                       'paper_bgcolor': colors['background'],
                       'font': { 'color': colors['text'] },
                       'title': 'consumption per day'},
            'data': [go.Scatter(x=list(mdf.timestamp),
                                y=list(mdf.coffees))]}
    return figure

app.css.append_css({"external_url": "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"})


if __name__ == '__main__':
    app.run_server()
