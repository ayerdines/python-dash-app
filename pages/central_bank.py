from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html

layout = [
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.I(className='far fa-door-open hacker-green')
                ], className='header-icon'),
                html.Div([
                    html.H1('Central Bank Meeting Analysis', className='mb-0 text'),
                    html.Span('Search for a particular security topic to learn about.', className='faded')
                ], className='header-title')
            ], className='page-header')
        ], className='container p-4')
    ], className='custom-header mb-4 noselect'),
    html.Div([
        html.Div([
            html.Div([
                html.Label(['Date of Start:',
                            dcc.DatePickerSingle(
                                id='date-picker-single1',
                                date=datetime(1997, 5, 10)
                            ),
                            ], className='col-sm-4 d-sm-inline-block'),
                html.Label(['Date of End:',
                            dcc.DatePickerSingle(
                                id='date-picker-single2',
                                date=datetime(1997, 5, 10),
                            ),
                            ], className='col-sm-4 d-sm-inline-block'),
                html.Label(['Select a City:',
                            dcc.Dropdown(
                                id='demo-dropdown-central',
                                options=[
                                    {'label': 'New York City', 'value': 'NYC'},
                                    {'label': 'Montreal', 'value': 'MTL'},
                                    {'label': 'San Francisco', 'value': 'SF'}
                                ],
                                style={'marginTop': 4}
                            ),
                            ], className='col-sm-4 d-sm-inline-block align-top'),
                dcc.Graph(
                    id='example-graph-central1',
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
            ], className='col-sm-6'),
            html.Div([
                dcc.Input(
                    id="input_text1",
                    type="text",
                    placeholder="input type text",
                    style={'margin': '30px 20px 0px 65px'}
                ),
                dcc.Input(
                    id="input_text2",
                    type="text",
                    placeholder="input type text",
                ),
                dcc.Graph(
                    id='example-graph-central2',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                        }
                    },
                    style={'marginTop': 20}
                ),
                dcc.Graph(
                    id='example-graph-central3',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                        }
                    },
                )
            ], className='col-sm-6')
        ], className='row')
    ], className='container pb-1')
]

