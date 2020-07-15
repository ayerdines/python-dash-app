import dash_html_components as html
import dash_core_components as dcc
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Sign
from dash.dependencies import Input, Output,State
import os
import sys
import dash_table
import pandas as pd
import numpy as np

sys.path.append(r"C:\Git\python-dash-app\tools")
import App_backend_bin

'''All the pre-loaded data for page'''

conn_str=('Driver={SQL Server Native Client 11.0};'
                      'Server=LON-FWANG-02;'
                      'Database=macro_dash_database;'
                      'Trusted_Connection=yes;'
                      'autocommit=False')


countries=['AUD', 'CAD', 'EUR', 'JPY', 'MXN', 'NZD', 'NOK', 'SGD', 'ZAR', 'SEK', 'CHF','CNH', 'TRY', 'GBP', 'USD']

'''All the page layout codes'''

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
                html.Label(['Currency One:',
                            dcc.Dropdown(
                                id='currency1-dropdown',
                                options=[{'label':country, 'value':country} for country in np.sort(countries)],
                                style={'marginTop': 4},
                                value='EUR',
                                clearable=False
                            ),
                            ], className='col-sm-4 d-sm-inline-block align-top'),
                html.Label(['Currency Two:',
                            dcc.Dropdown(
                                id='currency2-dropdown',
                                options=[{'label':country, 'value':country} for country in np.sort(countries)],
                                style={'marginTop': 4},
                                value='USD',
                                clearable=False
                            ),
                            ], className='col-sm-4 d-sm-inline-block align-top'),
                html.Label(['Pulse Moving Avg (days)',
                            dcc.Input(
                                id="mov_avg",
                                type="number",
                                placeholder="30",
                                value="21"
                                # style={'margin': '30px 20px 0px 65px'}
                                ),
                            ], className='col-sm-4 d-sm-inline-block align-top'),
                dcc.Graph(
                    id='pulse_main_graph',
                    figure={
                        'data': [
                        ],
                        'layout': dict(
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Data-Pulse (Net)'},
                            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    },
                    style={'marginTop': 40}
                ),
                # dcc.Graph(
                #     id='example-graph-currency1',
                #     figure={
                #         'data': [
                #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                #         ],
                #         'layout': {
                #             'title': 'Dash Data Visualization'
                #         }
                #     },
                #     style={'marginTop': 40}
                # )
            ], className='col-sm-8'),
            html.Div([
                html.Div("Data Releases", className='mb-4 text-center'),
                dash_table.DataTable(
                    id='release_table',
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
                html.Div(children='Top Movers',style={
                    'fontSize': 24}, className='my-4 text-center'),
                dash_table.DataTable(
                    id='top_movers',
                    sort_action='native',
                    row_selectable="single",
                    style_cell={'fontSize':14, 'font-family':'Cambria'} ,
                    style_header={
                        'fontWeight': 'bold',
                        'border':'1px solid black'},
                    # fixed_rows={'headers': True},
                    columns=[
                        {'id': 'ticker', 'name': 'Currency'},
                        {'id': 'price', 'name': 'Last Close'},
                        {'id': 'st_chng', 'name': '1 Day Change', 'type': 'numeric','format': FormatTemplate.percentage(2).sign(Sign.positive)},
                        {'id': 'lt_chng', 'name': '1 Week Change','type': 'numeric','format': FormatTemplate.percentage(2).sign(Sign.positive)}
                    ],
                    style_data_conditional=[
                        {
                            'if': {
                                'column_id': 'st_chng',
                                'filter_query': '{st_chng} > 0'
                            },
                            'color': 'green',
                        },
                        {
                            'if': {
                                'column_id': 'st_chng',
                                'filter_query': '{st_chng} < 0'
                            },
                            'color': 'red',
                        },
                        {
                            'if': {
                                'column_id': 'lt_chng',
                                'filter_query': '{lt_chng} > 0'
                            },
                            'color': 'green',
                        },
                        {
                            'if': {
                                'column_id': 'lt_chng',
                                'filter_query': '{lt_chng} < 0'
                            },
                            'color': 'red',
                        },
                    ],
                    data=App_backend_bin.top_mover_tbl(conn_str,1,5,15).to_dict('records'),
                ),
            ], className='col-sm-4')
        ], className='row')
    ], className='container pb-4')
]
