
from dash import html, dcc 
import dash_bootstrap_components as dbc 

def build_tabs():
    """ build the seven different tabs """
    return html.Div(
        id = "tabs-container",
        children=[
            dcc.Tabs(
                id="tabs",
                parent_className="custom-tabs",
                value="tab-select",
                children=[
                    dcc.Tab(
                        label="Weekly Summary",
                        value="tab-select",
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
            )
        ]
    )