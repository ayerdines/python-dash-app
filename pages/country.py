import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import os


df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/sample.csv')
country_list=sorted(['AUD', 'CAD', 'CNH', 'EUR', 'JPY', 'MXN', 'NZD', 'NOK', 'SGD', 'ZAR', 'SEK', 'CHF', 'TRY', 'GBP', 'USD'])




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
                html.Label(['Country',
                            dcc.Dropdown(
                                id='country_dropdown',
                                options=[
                                        {'label':country, 'value':country} for country in country_list
                                ],
                                clearable=False,
                                value='AUD',
                                style={'marginTop': 4}
                            ),
                            ], className='col-sm-5 d-sm-inline-block align-top'),
                html.Label(['Sector',
                            dcc.Dropdown(
                                id='sector_dropdown',
                                options=[
                                    {'label': 'Economic Activity', 'value': 'Economic Activity'},
                                    {'label': 'Inflation', 'value': 'Inflation'}
                                ],
                                clearable=False,
                                value='Economic Activity',
                                style={'marginTop': 4}
                            ),
                            ], className='col-sm-5 d-sm-inline-block align-top'),
                html.Label(['Data',
                            dcc.Dropdown(
                                id='data_dropdown',
                                clearable=False,
                                style={'marginTop': 4}
                            ),
                            ], className='col-sm-6 d-sm-inline-block align-top'),
                dcc.Graph(
                    id='pulse_sector_graph',
                    figure={
                        'data': [
                        ],
                        'layout': dict(
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Data-Pulse'},
                            margin={'l': 10, 'b': 40, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    },
                    style={'marginTop': 10}
                )
            ], className='col-sm-8'),
            html.Div([
                html.Div("Economic Data Release Details", className='mb-4 text-center'),
                dash_table.DataTable(
                    id='release_table_country',
                    columns=([
                        {'id': 'release_date', 'name': 'Release_Date'},
                        {'id': 'country', 'name': 'Country'},
                        {'id': 'data_name', 'name': 'Data_Name'},
                        {'id': 'sector', 'name': 'Sector'},
                        {'id': 'reading', 'name': 'Reading'},
                        {'id': 'contribution', 'name': 'Contribution'}
                    ]),
                        style_data_conditional=[
                            {
                                'if': {
                                    'column_id': 'contribution',
                                    'filter_query': '{contribution} > 0'
                                },
                                'backgroundColor': 'green',
                                'color': 'white',
                            },
                            {
                                'if': {
                                    'column_id': 'contribution',
                                    'filter_query': '{contribution} < 0'
                                },
                                'backgroundColor': 'red',
                                'color': 'white',
                            },
                        ],
                ),
                dcc.Graph(
                    figure=dict(
                        layout=dict(
                            showlegend=True,
                            legend={'x': 0, 'y': 1}
                        )
                    ),
                    style={'height': 400,'width':600},
                    id='data_ts'
                )
            ], className='col-sm-4')
        ], className='row')
    ], className='container pb-4')
]
