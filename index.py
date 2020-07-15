import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import pyodbc
from app import app
from pages import datapulse, country, currency, central_bank

# sys.path.append(r"C:\Git\python-dash-app\tools")
import App_backend_bin

conn_str=('Driver={SQL Server Native Client 11.0};'
                      'Server=LON-FWANG-02;'
                      'Database=macro_dash_database;'
                      'Trusted_Connection=yes;'
                      'autocommit=False')

conn = pyodbc.connect(conn_str)

'''Grab all the required data from database. All calculation is based off these instead of making a new DB query'''

release_data=pd.read_sql("""
                        SELECT a.release_date,country,data_name,
                            CASE WHEN sector in ('Survey','Housing','Growth','Employment') THEN 'Activity' else 'Inflation' END  as sector ,reading,round(pulse_cont_delta,1) as contribution
                        FROM macro_dash_database.dbo.pulse_score a
                        WHERE a.release_flag=1
                        order by a.release_date
                        """,conn)

data_ts=App_backend_bin.bday_econ_ts(conn_str)

activity_df=App_backend_bin.bday_pulse(conn_str,sector=['Growth','Survey','Housing','Employment']).reset_index(level=['country','currency'])
inflation_df=App_backend_bin.bday_pulse(conn_str,sector=['Inflation']).reset_index(level=['country','currency'])

price = pd.read_sql("select * from dbo.prices order by effective_date",conn)

pulse=App_backend_bin.bday_pulse(conn_str)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav([
        html.Div([
            html.Div([
                html.A([
                    html.Img(width=135, src='/assets/company-logo.png', alt='TheGreatCompany', className='logo')
                ], href='/')
            ], className='navbar-brand'),
            html.Ul([
                html.Li([
                    html.A([
                        html.I('', className='fa fa-bars fa-lg', **{'aria-hidden': True})
                    ], id='sidebarCollapse', className='collapse-button', href='#menu-toggle')
                ], className='nav-item')
            ], className='navbar-nav navbar-right options'),
            html.Div([
                html.Ul([
                    html.Li([
                        html.A('Login', className='nav-link', href='/login')
                    ], className='nav-item'),
                    html.Li([
                        html.A('Signup', className='nav-link', href='/signup')
                    ], className='nav-item')
                ], className='navbar-nav navbar-right options vertical-align-custom')
            ],
                className='collapse navbar-collapse justify-content-end', id='navbarSupportedContent'
            )
        ], className='container-fluid')
    ],
        className='navbar navbar-expand-sm navbar-dark navbar-colour',
    ),
    html.Div([
        html.Div([
            html.Ul([
                html.Li([
                    dcc.Link("Datapulse Summary", className='nav-link', href='/datapulse-summary')
                ],
                    className='nav-item indent-item'
                ),
                html.Li([
                    dcc.Link("Country Analysis", className='nav-link', href='/country-analysis')
                ],
                    className='nav-item indent-item'
                ),
                html.Li([
                    dcc.Link("Currency Analysis", className='nav-link', href='/currency-analysis')
                ],
                    className='nav-item indent-item'
                ),
                html.Li([
                    dcc.Link("Central Bank Analysis", className='nav-link', href='/central-bank-analysis')
                ],
                    className='nav-item indent-item'
                )
            ],
                className='sidebar-nav'
            )
        ], id='sidebar-wrapper'),
        html.Div(datapulse.layout, id='page-content-wrapper'),
    ],
        id='wrapper',
        className='toggled'
    )
])


@app.callback(Output('page-content-wrapper', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/datapulse-summary':
        return datapulse.layout
    elif pathname == '/country-analysis':
        return country.layout
    elif pathname == '/currency-analysis':
        return currency.layout
    elif pathname == '/central-bank-analysis':
        return central_bank.layout
    else:
        return datapulse.layout

'''All the components interactions are below '''


@app.callback(
    Output('pulse_main_graph', 'figure'),
    [Input('currency1-dropdown', 'value'),
     Input('currency2-dropdown', 'value'),
     Input('mov_avg', 'value')
     ])

def update_pulse_main_graph(currency1,currency2,mov_avg):
    global pulse, price

    if not isinstance(mov_avg,int):
        mov_avg=30

    cds=App_backend_bin.pulse_graph(pulse,price,currency1,currency2,int(mov_avg),252)

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]],
                              shared_xaxes=True,
                              vertical_spacing=0.01
                              )

    net_pulse = go.Scatter(
        x=cds.index,
        y=cds.Pulse_net,
        name='DataPulse(Net)',
        mode = 'lines+markers'
    )

    pulse_avg = go.Scatter(
        x=cds.index,
        y=cds.average,
        name='Pulse Average',
        yaxis='y1',
        marker_color='black'
    )

    spot_price = go.Scatter(
        x=cds.index,
        y=cds.rate,
        name=currency1+currency2+' Spot',
        yaxis='y2',
        marker_color='red'
    )

    fig.add_trace(net_pulse, row=1, col=1,secondary_y=False)
    fig.add_trace(pulse_avg, row=1, col=1,secondary_y=False)
    fig.add_trace(spot_price, row=1, col=1,secondary_y=True)

    fig['layout'].update(
            legend=dict(x=0,y=1),
            yaxis={'showgrid': False}
            )

    return fig

'''Callback that updates the pulse_main_graph from the top_mover table'''

@app.callback(
    [Output('currency1-dropdown', 'value'),
     Output('currency2-dropdown','value')
     ],
    [Input('top_movers', 'data'),
     Input('top_movers', 'selected_rows')
     ])

def update_currency_dropdowns(data,selected_rows):
    try:
        currency1=data[selected_rows[0]]['ticker'][:3]
        currency2=data[selected_rows[0]]['ticker'][3:]
    except:
        currency1='EUR'
        currency2='USD'

    return currency1, currency2

@app.callback(
    Output('release_table', 'data'),
    [Input('currency1-dropdown', 'value'),
     Input('currency2-dropdown', 'value'),
     Input('pulse_main_graph', 'hoverData')
     ])

def update_release_data(ccy1,ccy2,graph_data):
    global release_data

    try:
        hover_date=graph_data['points'][0]['x']
    except:
        hover_date='01/01/2010'

    hover_data=release_data[((release_data["country"]==ccy1) | (release_data['country']==ccy2)) &(release_data['release_date']==hover_date)]

    hover_data['release_date']= hover_data['release_date'].dt.date
    hover_data = hover_data.to_dict('records')

    return hover_data

'''#####################Callbacks for the Country page###################################'''

@app.callback(
    Output('data_dropdown', 'options'),
    [Input('country_dropdown', 'value'),
     Input('sector_dropdown', 'value')]
)

def update_data_dropdown(country,sector):

    options=App_backend_bin.data_dropdown(conn_str,country,sector)

    return  [{'label':data, 'value':data} for data in options]

@app.callback(
    Output('pulse_sector_graph', 'figure'),
    [Input('country_dropdown', 'value')
     ])

def update_pulse_sector_graph(country):

    global activity_df,inflation_df

    cds_activity=activity_df[activity_df.currency==country].tail(730)
    cds_inflation=inflation_df[inflation_df.currency==country].tail(730)

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]],
                              shared_xaxes=True,
                              vertical_spacing=0.01
                              )

    pulse = go.Scatter(
        x=cds_activity.index,
        y=cds_activity.Pulse,
        name=country+' Activity Pulse',
        mode = 'lines'
    )

    sector = go.Scatter(
        x=cds_inflation.index,
        y=cds_inflation.Pulse,
        name=country+' Inflation Pulse',
        mode = 'lines'
    )

    fig.add_trace(pulse, row=1, col=1,secondary_y=False)
    fig.add_trace(sector, row=1, col=1,secondary_y=True)

    fig['layout'].update(
            title={
                'text': country+' Data Pulse',
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            legend=dict(x=0,y=1),
            yaxis={'showgrid': False}
            )


    return fig

@app.callback(
    Output('release_table_country', 'data'),
    [Input('country_dropdown', 'value'),
     Input('pulse_sector_graph', 'hoverData')
     ])

def update_release_data(country,graph_data):
    global release_data

    try:
        hover_date=graph_data['points'][0]['x']
    except:
        hover_date='01/01/2010'

    hover_data=release_data[((release_data["country"]==country)) &(release_data['release_date']==hover_date)]

    hover_data['release_date']= hover_data['release_date'].dt.date
    hover_data = hover_data.to_dict('records')

    return hover_data

@app.callback(
    Output('data_ts', 'figure'),
    [Input('data_dropdown', 'value'),
     Input('country_dropdown','value')
     ])

def update_data_ts(data_name,country):
    cds=data_ts[(data_ts['currency']==country) & (data_ts ['data_name']==data_name)]

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]],
                              shared_xaxes=False,
                              vertical_spacing=0.01
                              )
    data = go.Scatter(
        x=cds['business day'],
        y=cds.value,
        name=data_name,
        mode = 'lines'
    )

    fig.add_trace(data, row=1, col=1,secondary_y=True)

    fig['layout'].update(
            yaxis={'showgrid': False},
            xaxis={'automargin': False},
                title={
                    'text': data_name,
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'}
            )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
