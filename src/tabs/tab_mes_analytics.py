from dash import html, dcc, Input, Output

from dash import dash_table 
import plotly.express as px
import plotly.graph_objects as go 

import dash_bootstrap_components as dbc 

from app import app 
from utils.data import mes_proc_df, mes_wait_df, eTraveler_df, mes_shp_df, shp_df
from utils import base_layout, base_bar_attr





#TODO extract the common filter or aggregation parts here
def tab_mes_analytics():
    tab_layout = dbc.Row(
        class_name="tab-ma",
        children=[
            dbc.Row(
                class_name="tab-ma-row-first",
                children=[
                    dbc.Col(
                        id="graph-shp-mes-success",
                        class_name="graph-container",
                        width=10
                    ),
                    dbc.Col(
                        class_name="mes-ma-card",
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H6("Total BC Shipped", className="card-title"),
                                        html.P(id="text-total-barcodes", className="card-content")
                                    ]
                                ),
                                class_name="mes-ma-cards"
                            ),
                            dbc.Card( 
                                dbc.CardBody(
                                    [
                                        html.H6("Penetration", className="card-title"),
                                        html.P(id="text-penetration", className="card-content")
                                    ]
                                ),
                                class_name="mes-ma-cards"
                            ),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H6("Adherence", className="card-title"),
                                        html.P(id="text-adherence", className="card-content")
                                    ]
                                ),
                                class_name="mes-ma-cards"
                            ),
                            ]
                        )
                ]
            ), 
            dbc.Row(
                class_name="tab-ma-row-second",
                children=[
                    dbc.Col(dcc.Graph(id="graph-weekly-process-time")),
                    dbc.Col(dcc.Graph(id="graph-weekly-wait-time")),
                ]
            ),
            dbc.Row(
                dbc.Col(dcc.Graph(id="graph-weekly-proc-wait-time")),
                class_name='tab-ma-row-third'
                
            )
            
        ]
    )
    return tab_layout 

#chart 
@app.callback(
    Output("graph-shp-mes-success", "children"),
    Output("text-total-barcodes", "children"), 
    Output('text-penetration', "children"), 
    Output("text-adherence", "children"), 
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
)
def update_shp_mes_success(workyear, workweek, locations):
    #total shp barcodes 
    filtered_shp_df = shp_df[
        shp_df.work_year.isin(workyear) & \
        shp_df.work_week.isin(workweek) & \
        shp_df.location_name.isin(locations)
        
    ]
    total_shp_barcodes = filtered_shp_df.groupby(['date']).total_barcodes.sum() 
    total_shp_barcodes_sum = total_shp_barcodes.sum() 
    # print(filtered_shp_df, total_shp_barcodes) 
    #total mes shp barcodes
    filtered_mes_shp_df = mes_shp_df[
        mes_shp_df.work_year.isin(workyear) & \
        mes_shp_df.work_week.isin(workweek) & \
        mes_shp_df.location_name.isin(locations)
    ]
    total_mes_shp_barcodes = filtered_mes_shp_df.groupby(["date"]).mes_shp_bc.sum()
    total_mes_shp_barcodes_sum = total_mes_shp_barcodes.sum() 
    
    #etravaler success 
    filtered_eTraveler_df = eTraveler_df[
        eTraveler_df.work_year.isin(workyear) & \
        eTraveler_df.work_week.isin(workweek) & \
        eTraveler_df.location_name.isin(locations) & \
        (eTraveler_df.status == "Success")
    ]
    total_eTravler_barcodes = filtered_eTraveler_df.groupby(["date"]).barcode_count.sum() 
    total_eTravler_barcodes_sum = total_eTravler_barcodes.sum() 
    
    bar_shp = go.Bar(
        x=total_shp_barcodes.index, 
        y=total_shp_barcodes,
        name="Total SHP",
        **base_bar_attr 
    )
    bar_mes_shp = go.Bar(
        x=total_mes_shp_barcodes.index, 
        y=total_mes_shp_barcodes, 
        name="MES SHP",
        **base_bar_attr
    ) 
    bar_mes_success = go.Bar(
        x=total_eTravler_barcodes.index, 
        y=total_eTravler_barcodes, 
        name="MES Success", 
        **base_bar_attr 
    )
    print(total_shp_barcodes)
    layout = base_layout 
    layout.title = "Total SHP VS MES Success"
    layout.yaxis.title = "Barcodes"
    layout.xaxis.title = "Date"
    
    fig = go.Figure(
        data=[bar_shp, bar_mes_shp, bar_mes_success],
        layout=layout
    )
    graph_width = max(1000, \
        max(len(total_shp_barcodes),\
        len(total_eTravler_barcodes),\
        len(total_mes_shp_barcodes)) * 45)
    print("graph len of mes-rcv-shp: ", graph_width)
     
    graph_comp = dcc.Graph(
        figure=fig,
        # responsive=True,
        # style={"width":graph_width}
    )
    
    # print(total_shp_barcodes_sum, total_mes_shp_barcodes_sum, total_eTravler_barcodes_sum) 
    text_total_shp_barcodes = f"{total_shp_barcodes_sum:.0f}"
    text_penetration = f"{total_mes_shp_barcodes_sum/total_shp_barcodes_sum * 100: .0f}%"
    text_adherence = f"{total_eTravler_barcodes_sum/total_mes_shp_barcodes_sum * 100: .0f}%"
    
    return graph_comp, text_total_shp_barcodes, text_penetration, text_adherence 



@app.callback(
    Output("graph-weekly-process-time", "figure"),
    Output("graph-weekly-wait-time", "figure"),
    Output("graph-weekly-proc-wait-time", "figure"),
    # Output("table_test", "children"),
    Input("global-slicer-work-year", "value"),
    Input("global-slicer-work-week", "value"),
    Input("global-slicer-locations", "value")
)
def update_weekly_process_time(workyear, workweek, locations):
    ##weekly process time 
    ## filter based on the slicers workyear, workweek, locations 
    filtered_mes_proc_df = mes_proc_df[
        mes_proc_df.work_year.isin(workyear) &\
        mes_proc_df.work_week.isin(workweek) & \
        mes_proc_df.location_name.isin(locations)
        ]
    sum_proc_time = filtered_mes_proc_df.groupby(["date"]).prochours.sum()
    
    bar_process_time = go.Bar(
        x=sum_proc_time.index, 
        y=sum_proc_time, 
        name="ProcTime",
        **base_bar_attr
    )

    layout_process_time = base_layout
     
    fig_process_time = go.Figure(
        data=[bar_process_time],
        layout=layout_process_time
    )
    
    #weekly wait time 
    filtered_mes_wait_df = mes_wait_df[
        mes_wait_df.work_year.isin(workyear) & \
        mes_wait_df.work_week.isin(workweek) & \
        mes_wait_df.location_name.isin(locations)
    ]
    sum_wait_time = filtered_mes_wait_df.groupby(["date"]).prochours.sum()
    bar_wait_time = go.Bar(
        x=sum_wait_time.index, 
        y=sum_wait_time, 
        name="WaitTime",
        **base_bar_attr
    )
    layout_wait_time = go.Layout(
        title="Weekly Idle Time", 
        yaxis_title = "Hours", 
        xaxis=dict(title="Date", tickformat="%d %b")
    )
    fig_wait_time = go.Figure(
        data=[bar_wait_time], 
        layout=layout_wait_time
    )
    layout_process_wait_time = base_layout
    layout_process_wait_time.title = "Weekly Process VS Idle Time"
    layout_process_wait_time.yaxis.title = "Hours"
    layout_process_wait_time.xaxis.title = "Date"
     
    fig_process_wait_time = go.Figure(
        data=[bar_process_time, bar_wait_time],
        layout=layout_process_wait_time
    )
   
    
    return fig_process_time, fig_wait_time, fig_process_wait_time
     
