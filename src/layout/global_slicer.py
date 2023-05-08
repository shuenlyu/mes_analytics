from dash import html, dcc 
import dash_bootstrap_components as dbc 

from utils.data import slicer_location, slicer_work_week, slicer_work_year

def global_slicer():
    """build global slicers/filters here for all the tabs 
    """
    slicers = dbc.Row(
        align="start",
        children=[
            dbc.Col(
                children=[
                    dbc.Stack(
                        children=[
                            html.Label(["Work Year"]),
                            dcc.Dropdown(
                                id="global-slicer-work-year",
                                options=slicer_work_year,
                                value=slicer_work_year,
                                multi=True
                            )
                        ],
                        direction = "horizontal",
                        gap=2
                    ) 
                ], 
                align="center",
                width="3"
            ), 
            dbc.Col(
                children=[
                    dbc.Stack(
                       children=[
                           html.Label(["Work Week"]),
                           dcc.Dropdown(
                                id="global-slicer-work-week",
                                options = slicer_work_week,
                                value = slicer_work_week,
                                multi = True

                           )
                       ],
                       direction = "horizontal", 
                       gap = 2
                    )
                ],
                width=3,
                align="center"
            ), 
            dbc.Col(
                children=[
                    dbc.Stack(
                        children=[
                            html.Label(["Locations"]),
                            dcc.Dropdown(
                                id="global-slicer-locations",
                                options = slicer_location, 
                                value = slicer_location,
                                multi=True
                            )
                        ],
                        direction = "horizontal", 
                        gap=2
                    )
                ],
                width=6,
                align="center"
            )
        ]
    )
    return slicers