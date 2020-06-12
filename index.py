import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import datapulse, country, currency, central_bank

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


if __name__ == '__main__':
    app.run_server(debug=True)
