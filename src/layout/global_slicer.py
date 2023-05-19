from dash import html, dcc 
import dash_bootstrap_components as dbc 

from utils.data import slicer_location, slicer_work_week, slicer_work_year

init_location = slicer_location
init_work_week = sorted(slicer_work_week)[-4:]
init_work_year = sorted(slicer_work_year)[-1:]

def global_slicer():
    """build global slicers/filters here for all the tabs 
    """
    slicers = dbc.Row(
        align="start",
        children=[
            dbc.Col(
                children=[
                    dbc.Stack(
                        direction="vertical",
                        children=[
                            html.Label(["Work Year"]),
                            dcc.Dropdown(
                                id="global-slicer-work-year",
                                options=slicer_work_year,
                                value=init_work_year,
                                multi=True,
                                placeholder="select a work year"
                            )
                        ],
                        gap=1
                    ) 
                ], 
                align="start",
                width=2
            ), 
            dbc.Col(
                children=[
                    dbc.Stack(
                        direction="vertical",
                        children=[
                            html.Label(["Work Week"]),
                            dcc.Dropdown(
                                id="global-slicer-work-week",
                                options = slicer_work_week,
                                value = init_work_week,
                                multi = True,
                                placeholder="select a work week"

                           )
                       ],
                       gap = 1
                    )
                ],
                width=4,
                align="start"
            ), 
            dbc.Col(
                children=[
                    dbc.Stack(
                        direction="vertical",
                        children=[
                            html.Label(["Locations"]),
                            dcc.Dropdown(
                                id="global-slicer-locations",
                                options = slicer_location, 
                                value = init_location,
                                multi=True,
                                placeholder="select a location",
                                # style={"width":"13rem", "display": "inline"}
                            )
                        ],
                        gap=1
                    )
                ],
                width=6,
                align="start"
            )
        ]
    )
    print(init_work_week)
    print(init_location)
    print(init_work_year)
    return slicers