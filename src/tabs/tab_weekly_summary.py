from dash import html, Input, Output, dcc 

import plotly.express as px 
import plotly.graph_objects as go 

import dash_bootstrap_components as dbc 

from utils.data import rcv_shp_df, wip_df, tat_df, dmr_df, otd_df
from utils import base_layout, base_bar_attr

from app import app 


def tab_weekly_summary():
    tab_layout = dbc.Row(
        children=[
            dbc.Row(
                class_name="tab-ws-row-first",
                children=[
                    dbc.Col(dcc.Graph(id="graph-weekly-shp-rcv")), 
                    dbc.Col(dcc.Graph(id='graph-weekly-wip'))
                ]
            ), 
            dbc.Row(
                class_name="tab-ws-row-second",
                children=[
                    dbc.Col(dcc.Graph(id="graph-weekly-otd")), 
                    dbc.Col(dcc.Graph(id="graph-weekly-avg-tat"))
                ]
            ), 
            dbc.Row(
                class_name="tab-ws-row-third",
                children=[
                    dbc.Col(dcc.Graph(id="graph-weekly-opened-dmrs"),width=6), 
                    dbc.Col(id="graph-shp-mes-success", width=6,class_name="graph-container"),
                    dbc.Col(html.P(id="text-total-barcodes", hidden=True),width=0),
                    dbc.Col(html.P(id="text-penetration", hidden=True),width=0),
                    dbc.Col(html.P(id="text-adherence", hidden=True),width=0)
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
        # marker = dict(color = "rgb(0,120,255)"
        **base_bar_attr
    )
    bar_shp_late = go.Bar(
        x = groupby_shp_late_df.date, 
        y = groupby_shp_late_df.total_wos,
        # width=0.4,  
        # offset = -0.4, 
        name = "SHP-Late", 
        # marker = dict(color = "rgb(250,60,0)")
        **base_bar_attr
    )
    bar_shp_ontime = go.Bar(
        x = groupby_shp_ontime_df.date, 
        y = groupby_shp_ontime_df.total_wos,
        # width=0.4,  
        # offset = -0.4, 
        name = "SHP-Ontime", 
        # marker = dict(color = "rgb(250,130,0)")
        **base_bar_attr
    )
    layout = base_layout 
    layout.title = "Weekly SHP-RCV (WOs)" 
    layout.yaxis.title = "WOs"
    layout.xaxis.title = "Date"
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
        barmode = "stack",
    )
    
    ##update layout and update traces attributes
    layout = base_layout 
    layout.title = "Weekly WIP (WOs)"
    layout.yaxis.title = "WOs"
    layout.xaxis.title = "Date"
    layout.legend.title = ""
    fig_weekly_wip.update_traces(base_bar_attr) 
    fig_weekly_wip.update_layout(layout)
     
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
    layout = base_layout 
    layout.title = "Weekly OTD%"
    layout.xaxis.title = "Date" 
    layout.yaxis.title = "OTD%"
    fig_weekly_otd.update_traces(base_bar_attr)
    fig_weekly_otd.update_layout(layout)
    
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
    layout = base_layout 
    layout.title = "Weekly Avg TAT"
    layout.xaxis.title = "Date"
    layout.yaxis.title = "Days"
    
    fig_weekly_avg_tat.update_traces(base_bar_attr)
    fig_weekly_avg_tat.update_layout(base_layout)
    
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
    layout = base_layout
    layout.title = "Weekly Opened DMRs"
    layout.xaxis.title = "Date"
    layout.yaxis.title = "Count"
    
    fig_weekly_opened_dmrs.update_traces(base_bar_attr)
    fig_weekly_opened_dmrs.update_layout(layout)
    return fig_weekly_opened_dmrs