import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import os

df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/sample.csv')

layout = [
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.I(className='far fa-door-open hacker-green')
                ], className='header-icon'),
                html.Div([
                    html.H1('Country Analysis', className='mb-0 text'),
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
                                id='demo-dropdown-country1',
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
                                id='demo-dropdown-country2',
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
                                id='demo-dropdown-country3',
                                options=[
                                    {'label': 'New York City', 'value': 'NYC'},
                                    {'label': 'Montreal', 'value': 'MTL'},
                                    {'label': 'San Francisco', 'value': 'SF'}
                                ],
                                style={'marginTop': 4}
                            ),
                            ], className='col-sm-4 d-sm-inline-block align-top'),
                dcc.Graph(
                    id='example-graph-country1',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                        }
                    }
                )
            ], className='col-sm-8'),
            html.Div([
                html.Div("DataTable Country", className='mb-4 text-center'),
                dash_table.DataTable(
                    id='table-country1',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                ),
                dcc.Graph(
                    figure=dict(
                        data=[
                            dict(
                                x=[1995, 1996, 1997, 1998],
                                y=[219, 146, 112, 127],
                                name='Rest of world',
                                marker=dict(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
                            dict(
                                x=[1995, 1996, 1997, 1998],
                                y=[16, 13, 10, 11],
                                name='China',
                                marker=dict(
                                    color='rgb(26, 118, 255)'
                                )
                            )
                        ],
                        layout=dict(
                            title='US Export of Plastic Scrap',
                            showlegend=True,
                            # legend=dict(
                            #     x=1,
                            #     y=1
                            # ),
                            # margin=dict(l=40, r=0, t=100, b=60)
                        )
                    ),
                    style={'height': 300, 'marginTop': 40},
                    id='my-graph-country1'
                )
            ], className='col-sm-4')
        ], className='row')
    ], className='container pb-4')
]
