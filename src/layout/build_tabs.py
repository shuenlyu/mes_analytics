
from dash import html, dcc 
import dash_bootstrap_components as dbc 
from .global_slicer import global_slicer
from .banner import banner
from .footer import footer
from .composent_test import dropdown_test

def build_tabs():
    """ build the seven different tabs """
    return html.Div(
        id = "tabs-container",
        className="dbc",
        children=[
            banner(),
            dcc.Tabs(
                id="tabs",
                parent_className="custom-tabs",
                value="weekly-summary",
                children=[
                    dcc.Tab(
                        label="Weekly Summary",
                        value="weekly-summary",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="mes-analytics",
                        label="MES Analytics",
                        value="mes-analytics",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        # disabled=True,
                    ),
                    dcc.Tab(
                        id="iron-gate-compliance",
                        label="Iron-Gate Compliance",
                        value="iron-gate-compliance",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        # disabled=True, 
                    ),
                    dcc.Tab(
                        id="comparison",
                        label="Comparison",
                        value="comparison", 
                        className="custom-tab--selected",
                        # disable=True,
                    ),
                    dcc.Tab(
                        id="documentation",
                        label="Documentation",
                        value="documentation", 
                        className="custom-tab--selected",
                        # disable=True,
                    ),
                ]
            ),
            html.Div(
                id="tab-content-containers",
                children=[global_slicer(),
                          html.Hr(),
                          html.Div(id="tab-content")
                    
                ]
            ),
            footer()
        ]
    )