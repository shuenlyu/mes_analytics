from dash import html, dcc, Input, Output, callback 
import dash_bootstrap_components as dbc 

def dropdown_test():
    return dbc.Row(
        children=[
            html.Div(id="slicer-workyear-v"),
            html.Div(id="slicer-workweek-v"),
            html.Div(id="slicer-locations-v")
        ]
    )

@callback(
    Output('slicer-workyear-v', 'children'),
    Output('slicer-workweek-v', 'children'),
    Output('slicer-locations-v', 'children'),
    Input('global-slicer-work-year', 'value'),
    Input('global-slicer-work-week', "value"),
    Input("global-slicer-locations", "value")
)
def update_output(workyear, workweek, locations):
   return f"Selected workyear:{workyear}",\
       f"Selected workweek: {workweek}", \
           f"Selected locations: {locations}" 