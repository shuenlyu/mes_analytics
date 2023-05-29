from dash import Dash

import dash_bootstrap_components as dbc 
from flask_caching import Cache 
from dash_bootstrap_templates import load_figure_template
from utils.style import tab_20
import plotly.io as pio 

"""
theme list: 
    dark: "cyborg", "darkly", 
full list : ['BOOTSTRAP', 'CERULEAN', 'COSMO', 'CYBORG', 'DARKLY', 'FLATLY',\
    'GRID', 'JOURNAL', 'LITERA', 'LUMEN', 'LUX', 'MATERIA', 'MINTY', 'MORPH',\
    'PULSE', 'QUARTZ', 'SANDSTONE', 'SIMPLEX', 'SKETCHY', 'SLATE', 'SOLAR', \
    'SPACELAB', 'SUPERHERO', 'UNITED', 'VAPOR', 'YETI', 'ZEPHYR']
"""
# # template = "VAPOR"
# template = "SOLAR"
# template = "SLATE" #"SUPERHERO"
# template = "SUPERHERO"
#set up theme template
template = "VAPOR"
theme_template = getattr(dbc.themes, template)

#adding styling for dash table, and other core components
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css" 

#load template for figures according to the theme
load_figure_template(template.lower())

colorway = pio.templates[template.lower()].layout.colorway + tab_20
#put more color for template colorway 
pio.templates[template.lower()].layout.colorway = colorway  

TIMEOUT = 60000
# REQUESTs_PATHNAME_PREFIX = "/"
REQUESTs_PATHNAME_PREFIX = "/mes_analytics/"

app = Dash(__name__, 
    requests_pathname_prefix=REQUESTs_PATHNAME_PREFIX,\
    external_stylesheets=[theme_template])

cache = Cache(app.server, config={
    # "CACHE_TYPE": "flask_caching.backends.SimpleCache",
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "cache-directory"
})

