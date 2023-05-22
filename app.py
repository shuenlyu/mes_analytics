from dash import Dash

import dash_bootstrap_components as dbc 
from flask_caching import Cache 
from dash_bootstrap_templates import load_figure_template

"""
theme list: 
    dark: "cyborg", "darkly", 
full list : ['BOOTSTRAP', 'CERULEAN', 'COSMO', 'CYBORG', 'DARKLY', 'FLATLY',\
    'GRID', 'JOURNAL', 'LITERA', 'LUMEN', 'LUX', 'MATERIA', 'MINTY', 'MORPH',\
    'PULSE', 'QUARTZ', 'SANDSTONE', 'SIMPLEX', 'SKETCHY', 'SLATE', 'SOLAR', \
    'SPACELAB', 'SUPERHERO', 'UNITED', 'VAPOR', 'YETI', 'ZEPHYR']
"""
# # template = "VAPOR"
template = "SOLAR"
# template = "SLATE" #"SUPERHERO"
# template = "VAPOR"
# template = "SUPERHERO"
#set up theme template
theme_template = getattr(dbc.themes, template)
#set up figure template

#adding styling for dash table 
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css" 

figure_template = load_figure_template(template.lower())

app = Dash(__name__, external_stylesheets=[theme_template])

cache = Cache(app.server, config={
    # "CACHE_TYPE": "flask_caching.backends.SimpleCache",
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "cache-directory"
})

TIMEOUT = 60000
