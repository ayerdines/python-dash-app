import dash_html_components as html
import dash_core_components as dcc

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
    ], className='custom-header mb-5 noselect'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='demo-dropdown',
                        options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montreal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'}
                        ],
                        placeholder='Select a City'
                    ),
                ], className='col-sm-4 d-sm-inline-block'),
                html.Div([
                    dcc.Dropdown(
                        id='demo-dropdown',
                        options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montreal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'}
                        ],
                        placeholder='Select a City'
                    ),
                ], className='col-sm-4 d-sm-inline-block'),
                html.Div([
                    dcc.Dropdown(
                        id='demo-dropdown',
                        options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montreal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'}
                        ],
                        placeholder='Select a City'
                    ),
                ], className='col-sm-4 d-sm-inline-block'),
                dcc.Graph(
                    id='example-graph',
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
            html.Div([], className='col-sm-4')
        ], className='row')
    ], className='container pb-4')
]

