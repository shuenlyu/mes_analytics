import os 
import dash 
from dash import Dash, html, dcc 
from dash import Input, Output 

import dash_bootstrap_components as dbc 
from flask_caching import Cache 

from src.layout import build_tabs, banner, footer, global_slicer
from src.layout.composent_test import dropdown_test
from src.pages import about_page

from src.tabs import tab_documentation, tab_mes_analytics, tab_iron_gate_compliance, tab_weekly_summary

from app import app 

server = app.server

app.title = "UCT IAnalytics Platform"
app.layout = dbc.Container(
    fluid=True, 
    style={"padding":"0"},
    children=[
        dcc.Location(id="url", refresh=False),
        banner(), 
        html.Div(id="page-content", 
                 style={"display":"flex", "min-height":"100vh"}),
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
    elif pathname == "/about":
        return about_page()

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def update_tab_content(tab_selected):
    if tab_selected == "documentation":
        return tab_documentation()
    elif tab_selected == "mes-analytics":
        return tab_mes_analytics()
    elif tab_selected == "iron-gate-compliance":
        return tab_iron_gate_compliance()
    elif tab_selected == "weekly-summary":
        return tab_weekly_summary()
    else:
        return html.Div(f"Tab {tab_selected} not implemented yet!")

if __name__ == "__main__":
    print(app._callback_list)
    app.run_server(
        debug = True, 
        port=8081,
        processes=1,
        threaded=True
    )