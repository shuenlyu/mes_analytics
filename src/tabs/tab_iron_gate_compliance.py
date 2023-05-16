from dash import html, Input, Output, dcc, dash_table

import dash_bootstrap_components as dbc 
import plotly.express as px 
import plotly.graph_objects as go 

from utils.data import mes_compliance_df
from app import app 

def tab_iron_gate_compliance():
    tab_layout = dbc.Row(
        children=[
            #TODO customize layout attributes
            dbc.Col(dcc.Graph(id="graph-iron-gate-analysis")),
            dbc.Col(id="table-iron-gate-compliance")
        ]
    )
    return tab_layout

@app.callback(
    Output("graph-iron-gate-analysis", "figure"), 
    Output("table-iron-gate-compliance", "children"),
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
) 
def update_tab_iron_gate_compliance(workyear, workweek, locations):
    filtered_mes_compliance_df = mes_compliance_df[
        mes_compliance_df.work_year.isin(workyear) & \
        mes_compliance_df.work_week_rw.isin(workweek) & \
        mes_compliance_df.location_name.isin(locations)
    ]
    
    wo_count_date_status = filtered_mes_compliance_df.\
        groupby(["kit_box_date", "action_status"]).\
        wo_num.count().rename("wo_count").reset_index() 
    
    fig_iron_gate_analysis = px.bar(
        wo_count_date_status, 
        x = 'kit_box_date', 
        y = "wo_count", 
        color="action_status"
    )
    #TODO matrix table for iron-gate analysis
    filtered_mes_compliance_df.fillna(value={"override_by":" "}, inplace=True)
    count_wo_df = filtered_mes_compliance_df.groupby(["kit_box_date", "action_status", "override_by"])\
        .work_order_no.count().rename("wo_count").reset_index()
    
    count_wo_dt = dash_table.DataTable(
        count_wo_df.to_dict("records"),
        [{"name":i, "id":i} for i in count_wo_df.columns]
    )
    
    return fig_iron_gate_analysis,  count_wo_dt 
