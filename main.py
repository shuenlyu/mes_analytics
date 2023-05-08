import os 
import dash 
from dash import Dash, html, dcc 
from dash import Input, Output 

import dash_bootstrap_components as dbc 
from flask_caching import Cache 

from src.layout import build_tabs, banner, footer, global_slicer
from src.layout.composent_test import dropdown_test

from app import app 

server = app.server

app.title = "UCT IAnalytics Platform"
app.layout = dbc.Container(
    fluid=True, 
    style={"padding":"0"},
    children=[
        dcc.Location(id="url", refresh=False),
        banner(), 
        html.Div(id="page-content"),
        global_slicer(),
        dropdown_test(),
        footer()
    ]
) 


#pages control 
@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        return build_tabs() 


if __name__ == "__main__":
    print(app._callback_list)
    app.run_server(
        debug = True, 
        port=8081,
        processes=1,
        threaded=True
    )