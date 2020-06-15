import dash_html_components as html
import dash_core_components as dcc
import os

import dash_table
import pandas as pd

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw'
                 '/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

dt = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/sample.csv')

layout = [
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.I(className='far fa-door-open hacker-green')
                ], className='header-icon'),
                html.Div([
                    html.H1('Currency Analysis', className='mb-0 text'),
                    html.Span('Search for a particular security topic to learn about.', className='faded')
                ], className='header-title')
            ], className='page-header')
        ], className='container p-4')
    ], className='custom-header mb-4 noselect'),
    html.Div([
        html.Div([
            html.Div([
                html.Label(['Select a City:',
                            dcc.Dropdown(
                                id='demo-dropdown-currency1',
                                options=[
                                    {'label': 'New York City', 'value': 'NYC'},
                                    {'label': 'Montreal', 'value': 'MTL'},
                                    {'label': 'San Francisco', 'value': 'SF'}
                                ],
                                style={'marginTop': 4}
                            ),
                            ], className='col-sm-4 d-sm-inline-block align-top'),
                html.Label(['Select a City:',
                            dcc.Dropdown(
                                id='demo-dropdown-currency2',
                                options=[
                                    {'label': 'New York City', 'value': 'NYC'},
                                    {'label': 'Montreal', 'value': 'MTL'},
                                    {'label': 'San Francisco', 'value': 'SF'}
                                ],
                                style={'marginTop': 4}
                            ),
                            ], className='col-sm-4 d-sm-inline-block align-top'),
                html.Label(['Select a City:',
                            dcc.Dropdown(
                                id='demo-dropdown-currency3',
                                options=[
                                    {'label': 'New York City', 'value': 'NYC'},
                                    {'label': 'Montreal', 'value': 'MTL'},
                                    {'label': 'San Francisco', 'value': 'SF'}
                                ],
                                style={'marginTop': 4}
                            ),
                            ], className='col-sm-4 d-sm-inline-block align-top'),
                dcc.Graph(
                    id='life-exp-vs-gdp-currency',
                    figure={
                        'data': [
                            dict(
                                x=df[df['continent'] == i]['gdp per capita'],
                                y=df[df['continent'] == i]['life expectancy'],
                                text=df[df['continent'] == i]['country'],
                                mode='markers',
                                opacity=0.7,
                                marker={
                                    'size': 15,
                                    'line': {'width': 0.5, 'color': 'white'}
                                },
                                name=i
                            ) for i in df.continent.unique()
                        ],
                        'layout': dict(
                            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                            yaxis={'title': 'Life Expectancy'},
                            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    },
                    style={'marginTop': 40}
                ),
                dcc.Graph(
                    id='example-graph-currency1',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                        }
                    },
                    style={'marginTop': 40}
                )
            ], className='col-sm-8'),
            html.Div([
                html.Div("DataTable Country", className='mb-4 text-center'),
                dash_table.DataTable(
                    id='table-currency1',
                    columns=[{"name": i, "id": i} for i in dt.columns],
                    data=dt.to_dict('records'),
                ),
                html.Div("DataTable Country", className='my-4 text-center'),
                dash_table.DataTable(
                    id='table-currency2',
                    columns=[{"name": i, "id": i} for i in dt.columns],
                    data=dt.to_dict('records'),
                ),
            ], className='col-sm-4')
        ], className='row')
    ], className='container pb-4')
]

