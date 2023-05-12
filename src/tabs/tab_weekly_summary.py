from dash import html, Input, Output, dcc 

import plotly.express as px 
import plotly.graph_objects as go 

import dash_bootstrap_components as dbc 

from utils.data import rcv_shp_df, wip_df, tat_df, dmr_df, otd_df

from app import app 


def tab_weekly_summary():
    tab_layout = dbc.Row(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(dcc.Graph(id="graph-weekly-shp-rcv")), 
                    dbc.Col(dcc.Graph(id='graph-weekly-wip'))
                ]
            ), 
            dbc.Row(
                children=[
                    dbc.Col(dcc.Graph(id="graph-weekly-otd")), 
                    dbc.Col(dcc.Graph(id="graph-weekly-avg-tat"))
                ]
            ), 
            dbc.Row(
                children=[
                    dbc.Col(dcc.Graph(id="graph-weekly-opened-dmrs")), 
                    dbc.Col(
                        children=[
                            #this graph is created by the callback function in tab_mes_analytics.py 
                            dcc.Graph(id="graph-shp-mes-success"),
                            html.P(id="text-total-barcodes", hidden=True),
                            html.P(id="text-penetration", hidden=True),
                            html.P(id="text-adherence", hidden=True)
                ])
                ]
            )
        ]
    )
    return tab_layout

@app.callback(
    Output('graph-weekly-shp-rcv', 'figure'), 
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
)
def update_graph_weekly_shp_rcv(workyear, workweek, locations):
    filtered_rcv_shp_df = rcv_shp_df[
        rcv_shp_df.work_year.isin(workyear) & \
        rcv_shp_df.work_week.isin(workweek) & \
        rcv_shp_df.location_name.isin(locations)
    ]
    
    filtered_rcv_df = filtered_rcv_shp_df[filtered_rcv_shp_df.event_type == "RCV"]
    filtered_shp_df = filtered_rcv_shp_df[filtered_rcv_shp_df.event_type == "SHP"]
    
    filtered_shp_late_df = filtered_shp_df[filtered_shp_df.late_ontime == "Late"]
    filtered_shp_ontime_df = filtered_shp_df[filtered_shp_df.late_ontime == "On Time"]
    
    groupby_rcv_df = filtered_rcv_df.groupby("date").total_wos.sum().reset_index() 
    groupby_shp_late_df = filtered_shp_late_df.groupby("date").total_wos.sum().reset_index() 
    groupby_shp_ontime_df = filtered_shp_ontime_df.groupby("date").total_wos.sum().reset_index()
    
    bar_rcv = go.Bar(
        x=groupby_rcv_df.date, 
        y = groupby_rcv_df.total_wos,
        # base = 0,
        # width = 0.4, 
        # offset = 0.0, 
        name = "RCV", 
        marker = dict(color = "rgb(0,120,255)")
    )
    bar_shp_late = go.Bar(
        x = groupby_shp_late_df.date, 
        y = groupby_shp_late_df.total_wos,
        # width=0.4,  
        # offset = -0.4, 
        name = "SHP-Late", 
        marker = dict(color = "rgb(250,60,0)")
    )
    bar_shp_ontime = go.Bar(
        x = groupby_shp_ontime_df.date, 
        y = groupby_shp_ontime_df.total_wos,
        # width=0.4,  
        # offset = -0.4, 
        name = "SHP-Ontime", 
        marker = dict(color = "rgb(250,130,0)")
    )
    
    layout = go.Layout(
        title = "Weekly SHP-RCV (WOs)", 
        yaxis=dict(title="WOs"), 
        xaxis=dict(title="Date")
    )
    # groupby_shp_df = filtered_shp_df.groupby(["date", "late_ontime"]).total_wos.sum().reset_index()
    # fig_weekly_shp_rcv = px.bar(
    #     groupby_shp_df, 
    #     x = "date", 
    #     y = "total_wos", 
    #     color = "late_ontime",
    #     barmode = "stack"
    # )
    
    # fig_weekly_shp_rcv.add_trace(
    #     go.Bar(
    #         x = groupby_rcv_df.date, 
    #         y = groupby_rcv_df.total_wos, 
    #         name="RCV",
    #         base=0,  
    #         # offset=0.0
    #     )
    # )
    # fig_weekly_shp_rcv.update_layout(barmode="group")
    fig_weekly_shp_rcv = go.Figure(
        data = [bar_rcv, bar_shp_late, bar_shp_ontime],
        # data = [bar_shp_late],
        layout=layout
    )
    
    return fig_weekly_shp_rcv

@app.callback(
    Output("graph-weekly-wip", "figure"),
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
)
def update_graph_weekly_wip(workyear, workweek, locations):
    filtered_wip_df = wip_df[
        wip_df.work_year.isin(workyear) &\
        wip_df.work_week.isin(workweek) &\
        wip_df.location_name.isin(locations)
    ]
    
    wo_df = filtered_wip_df.groupby(["date", "late_ontime"]).total_wos.sum().reset_index() 
    fig_weekly_wip = px.bar(
        wo_df, 
        x = "date", 
        y = "total_wos", 
        color = "late_ontime", 
        barmode = "stack"
    )
     
    return fig_weekly_wip


@app.callback(
    Output("graph-weekly-otd", "figure"), 
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
)
def update_graph_weekly_otd(workyear, workweek, locations):
    filtered_otd_df = otd_df[
        otd_df.work_year.isin(workyear) & \
        otd_df.work_week.isin(workweek) & \
        otd_df.location_name.isin(locations) 
    ]
    avg_otd_df = filtered_otd_df.groupby(["date"]).otd.mean().reset_index() 
    # print(avg_otd_df)
    
    fig_weekly_otd = px.bar(
        avg_otd_df, 
        x = "date", 
        y = "otd"
    )
    return fig_weekly_otd

@app.callback(
    Output("graph-weekly-avg-tat", "figure"),
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
)
def update_graph_weekly_avg_tat(workyear, workweek, locations):
    filtered_tat_df = tat_df[
        tat_df.work_year.isin(workyear) & \
        tat_df.work_week.isin(workweek) & \
        tat_df.location_name.isin(locations)
    ]
    late_ontime_df = filtered_tat_df.groupby(["date", "late_ontime"]).\
        avg_tat_days.sum().reset_index() 
    
    fig_weekly_avg_tat = px.bar(
        late_ontime_df, 
        x = "date", 
        y = "avg_tat_days", 
        color = "late_ontime",
        barmode="group"
    )
    return fig_weekly_avg_tat

@app.callback(
    Output("graph-weekly-opened-dmrs", "figure"),
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
)
def update_graph_weekly_opened_dmrs(workyear, workweek, locations):
    filtered_dmr_df = dmr_df[
       dmr_df.work_year.isin(workyear) & \
       dmr_df.work_week.isin(workweek) & \
       dmr_df.location_name.isin(locations)
    ]
    problem_category_df = filtered_dmr_df.groupby(["dateopened", "problemcategory"]).\
        dmr_count.sum().reset_index() 
    # print(problem_category_df)
    fig_weekly_opened_dmrs = px.bar(
        problem_category_df, 
        x = "dateopened", 
        y = "dmr_count", 
        color = "problemcategory"
    )
    return fig_weekly_opened_dmrs