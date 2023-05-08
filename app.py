from dash import Dash

import dash_bootstrap_components as dbc 
from flask_caching import Cache 


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

cache = Cache(app.server, config={
    # "CACHE_TYPE": "flask_caching.backends.SimpleCache",
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "cache-directory"
})

TIMEOUT = 60
