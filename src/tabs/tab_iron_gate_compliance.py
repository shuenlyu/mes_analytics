from dash import html, Input, Output, dcc, dash_table

import dash_bootstrap_components as dbc 
import plotly.express as px 
import plotly.graph_objects as go 

from utils.data import mes_compliance_df
from app import app 
from utils import base_layout, base_bar_attr

def tab_iron_gate_compliance():
    tab_layout = dbc.Row(
        class_name="tab-igc",
        children=[
            #TODO customize layout attributes
            dbc.Col(dcc.Graph(id="graph-iron-gate-analysis"),
                    class_name="tab-igc-graph"
                    ),
            dbc.Col(id="table-iron-gate-compliance", 
                    className="dbc",
                    # class_name="tab-igc-table"
                    )
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
    
    layout = base_layout
    layout.title = "Iron-Gate Analysis"
    layout.yaxis.title = "Count of WOs"
    layout.legend.title = ""
    
    fig_iron_gate_analysis.update_traces(base_bar_attr)
    fig_iron_gate_analysis.update_layout(layout)
    #TODO matrix table for iron-gate analysis
    filtered_mes_compliance_df.fillna(value={"override_by":" "}, inplace=True)
    count_wo_df = filtered_mes_compliance_df.groupby(["kit_box_date", "action_status", "override_by"])\
        .work_order_no.count().rename("wo_count").reset_index()
    
    cols = [{"name":i, "id":i} for i in count_wo_df.columns]
    cols[0]["name"] = "Date"
    cols[1]["name"] = "Status"
    cols[2]["name"] = "Override by"
    cols[3]["name"] = 'Count of WOs'
    
    print(cols)
     
    count_wo_dt = dash_table.DataTable(
        count_wo_df.to_dict("records"),
        cols,
        page_action='none', 
        style_table={'height':"80vh", "overflowY":'auto'},
        style_header={
            'fontWeight': 'bolder'
        }
    )
    
    return fig_iron_gate_analysis,  count_wo_dt 
