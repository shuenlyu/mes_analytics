from dash import html, Input, Output, dash_table, dcc 

import plotly.express as px  
import plotly.graph_objects as go 

import dash_bootstrap_components as dbc
from utils.data import eTraveler_df, mes_shp_df, mes_compliance_df
from utils import base_bar_attr, base_layout
import pandas as pd 
from itertools import product

from app import app 
 
def tab_comparison():
    tab_layout = dbc.Row(
        children=[
            dbc.Row(
                class_name="tab-com-row-first",
                children=[
                    dbc.Col(
                        id="table-mes-adoption-adherence", className="dbc"
                    ),
                    dbc.Col(
                        dcc.Graph(id="graph-mes-adoption-adherence"),
                    ),
                ]
            ), 
            dbc.Row(
                # class_name="tab-com-rows",
                children=[
                    dbc.Col(
                        id="table-iron-gate-violations", className="dbc"
                    ),
                    dbc.Col(
                        dcc.Graph(id="graph-iron-gate-violations")
                    ), 
                ]
            )
        ]
    )
    return tab_layout

@app.callback(
    Output("table-mes-adoption-adherence", "children"), 
    Output("graph-mes-adoption-adherence", "figure"), 
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
)
def update_mes_adoption_adherence(workyear, workweek, locations):
    workyear, workweek, locations = sorted(workyear), sorted(workweek), sorted(locations)
    
    filtered_mes_shp_df = mes_shp_df[
        mes_shp_df.work_year.isin(workyear) &\
        mes_shp_df.work_week.isin(workweek) &\
        mes_shp_df.location_name.isin(locations)
    ]
    print("update mes adoption adherence")
    print(workyear, workweek, locations)
    print(filtered_mes_shp_df)
     
    mes_barcodes_count_df = filtered_mes_shp_df.groupby(["location_name", "work_week"])\
        .mes_shp_bc.sum()\
        .rename("mes_shp_BC")\
        .reset_index()

    filtered_eTraveler_df = eTraveler_df[
        eTraveler_df.work_year.isin(workyear) &\
        eTraveler_df.work_week.isin(workweek) &\
        eTraveler_df.location_name.isin(locations) &\
        (eTraveler_df.status == "Success")
    ]
    
    eTraveler_barcodes_count_df = filtered_eTraveler_df.groupby(["location_name", "work_week"])\
        .barcode_count.sum()\
        .rename("eTraveler_BC_success")\
        .reset_index() 
    
    #data frame only with location and workweek for later use 
    index_df = pd.DataFrame(list(product(locations, workweek)), columns=["location_name", "work_week"])
    
    #left join mes_barcodes count
    index_mes_df = index_df.merge(mes_barcodes_count_df,\
        on=["location_name", "work_week"],\
        how="left")
    #left join mes etraveler df for producing adherence value 
    index_mes_eTraveler_df = index_mes_df.merge(eTraveler_barcodes_count_df,\
        on=["location_name", "work_week"],\
        how="left")
    
    ##process fill null for calculating adherence value 
    index_mes_eTraveler_df.fillna(value={"mes_shp_BC":0.00001, "eTraveler_BC_success":0}, inplace=True)
    
    ##calculate mes adherence and adoption 
    index_mes_eTraveler_df["mes_adherence"] = round(index_mes_eTraveler_df['eTraveler_BC_success']/index_mes_eTraveler_df['mes_shp_BC'] * 100)
    
    ##pre-processing for convert to pivot table 
    index_mes_eTraveler_df.work_week = index_mes_eTraveler_df.work_week.astype(str)
    # index_mes_eTraveler_df.reset_index(inplace=True)
    
    mes_adherence_df = pd.pivot(index_mes_eTraveler_df, index="location_name", columns="work_week", values="mes_adherence")
    mes_adherence_df.reset_index(inplace=True)
  
    mes_adherence_dt_columns = sorted([{"name":f"Week-{i}(%)", "id":i} for i in mes_adherence_df.columns[1:]], key=lambda x: int(x["id"]))
    mes_adherence_dt_columns.insert(0, {"name":"Sites", "id":"location_name"})
    
    mes_adherence_dt = dash_table.DataTable(
        mes_adherence_df.to_dict("records"), 
        mes_adherence_dt_columns,
        page_action='none', 
        style_table={'height':"80vh", "overflowY":'auto'},
        style_header={
            'fontWeight': 'bolder'
        }
        )
    
    ### generating figure 
    fig_mes_adherence = px.line(
        index_mes_eTraveler_df,
        x="work_week",
        y="mes_adherence",
        color="location_name",
        markers=True
    )
    trace_attr = dict(
        marker = dict(
            line=dict(width=1)
        ),
        textposition="bottom right"
    )
    fig_mes_adherence.update_traces(trace_attr)
    
    layout = go.Layout(
        # marker 
        xaxis=dict(
            title=dict(
                text="Work Week"
            )
        ), 
        yaxis=dict(
            title=dict(
                text=""
            ), 
            ticksuffix="%"
        ), 
        margin=dict(
           t=80,
           b=60,
           l=20,
           r=40,
           pad=0,
           autoexpand=True
        ),
        title=dict(
            text="MES Adoption & Adherence",
            font=dict(
                size=24,
                family="Droid Sans"
            )
        ), 
        hovermode='x', 
        legend=dict(
            title=dict(
                text=""
            )
        )   
    )
    fig_mes_adherence.update_layout(layout) 
     
    return mes_adherence_dt, fig_mes_adherence

@app.callback(
    Output("table-iron-gate-violations", "children"), 
    Output("graph-iron-gate-violations", "figure"), 
    Input("global-slicer-work-year", "value"), 
    Input("global-slicer-work-week", "value"), 
    Input("global-slicer-locations", "value")
)
def update_iron_gate_violations(workyear, workweek, locations):
    workyear, workweek, locations = sorted(workyear), sorted(workweek), sorted(locations)
    
    filtered_mes_compliance_df = mes_compliance_df[
        mes_compliance_df.work_year.isin(workyear) &\
        mes_compliance_df.work_week.isin(workweek) &\
        mes_compliance_df.location_name.isin(locations)
        # (mes_compliance_df.action_status == "Override Performed")
    ]
    count_overrides = filtered_mes_compliance_df.where(mes_compliance_df.action_status == "Override Performed")\
        .groupby(["location_name", "work_week"])\
        .action_status.count() 
    count_wo = filtered_mes_compliance_df.groupby(["location_name", "work_week"])\
        .wo_num.count() 
    
    #data frame only with location and workweek for later use 
    index_df = pd.DataFrame(list(product(locations, workweek)), columns=["location_name", "work_week"])
    index_overrides_df = index_df.merge(count_overrides, \
        on = ["location_name", "work_week"],\
        how="left")
    index_overrides_wo_df = index_overrides_df.merge(count_wo, \
        on=["location_name", "work_week"], \
        how = "left")
    # print(index_overrides_wo_df)
    ##fill null values 
    index_overrides_wo_df.fillna(value={"action_status":0, "wo_num":0.00001}, inplace=True)
    
    ## columns convert dtype from int to string 
    index_overrides_wo_df.work_week = index_overrides_wo_df.work_week.astype("str")
    index_overrides_wo_df["irongate_violations"] = round(index_overrides_wo_df.action_status/index_overrides_wo_df.wo_num * 100)
    
    iron_gate_violation_df = pd.pivot(index_overrides_wo_df, index="location_name", columns="work_week", values="irongate_violations")
    iron_gate_violation_df.reset_index(inplace=True) 
    # print(iron_gate_violation_df)
     
    iron_gate_violation_dt_columns = sorted([{"name":f'Week-{i}(%)', "id":i} for i in iron_gate_violation_df.columns[1:]], key=lambda x: int(x["id"]))
    iron_gate_violation_dt_columns.insert(0, {"name":"Sites", "id":"location_name"})
    print(iron_gate_violation_dt_columns)
     
    iron_gate_violation_dt = dash_table.DataTable(
        iron_gate_violation_df.to_dict("records"), 
        iron_gate_violation_dt_columns,
        page_action='none', 
        style_table={'height':"80vh", "overflowY":'auto'},
        style_header={
            'fontWeight': 'bolder'
        }
        )
    
    ### generating figure 
    fig_iron_gate_violation = px.bar(
        index_overrides_wo_df,
        x="work_week",
        y="irongate_violations",
        color="location_name",
        barmode="group"
    ) 

    layout = go.Layout(
        # marker 
        xaxis=dict(
            title=dict(
                text="Work Week"
            )
        ), 
        yaxis=dict(
            title=dict(
                text=""
            ), 
            ticksuffix="%"
        ), 
        margin=dict(
           t=80,
           b=60,
           l=20,
           r=40,
           pad=0,
           autoexpand=True
        ),
        title=dict(
            text="Iron-Gate Violations",
            font=dict(
                size=24,
                family="Droid Sans"
            )
        ), 
        hovermode='x', 
        legend=dict(
            title=dict(
                text=""
            )
        )   
    )
    fig_iron_gate_violation.update_traces(base_bar_attr)
    fig_iron_gate_violation.update_layout(layout)
    
    return  iron_gate_violation_dt,  fig_iron_gate_violation