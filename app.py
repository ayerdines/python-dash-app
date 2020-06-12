import dash


external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
                        'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']
external_scripts = ['https://code.jquery.com/jquery-3.5.1.min.js']

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets,
                external_scripts=external_scripts)
server = app.server
