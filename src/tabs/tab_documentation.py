from dash import html, dcc 

_views_for_tabs = {
    "Weekly Summary":[
        'Reporting vw_OPS_Scorecard_RCV_SHP_Summ',
	    'Reporting vw_OPS_Scorecard_WIP_Summ',
	    'Reporting vw_OPS_Scorecard_RCV_SHP_Summ',
	    'Reporting vw_OPS_Scorecard_TAT_Summ',
	    'Reporting vw_OPS_Scorecard_DMR_Opened',
	    'Reporting vw_OPS_Scorecard_MES_PROC_Summ',
        'Reporting vw_OPS_Scorecard_eTraveler_Status'
    ],
    "MES Analytics":[
    	'Reporting vw_OPS_Scorecard_MES_PROC_Summ',
    	'Reporting vw_OPS_Scorecard_MES_WAIT_Summ',
    	'Reporting vw_OPS_Scorecard_MES_RCV_Summ',
    	'Reporting vw_OPS_Scorecard_MES_SHP_Summ',
    	'Reporting vw_OPS_Scorecard_RCV_Summ',
    	'Reporting vw_OPS_Scorecard_SHP_Summ',
        'Reporting vw_OPS_Scorecard_eTraveler_Status'
    ],
    "Iron-Gate Compliance":[
        'Reporting vw_OPS_Scorecard_MES_COMPLIANCE_Summ'
    ],
    "Comparison":[
        'Reporting vw_OPS_Scorecard_MES_COMPLIANCE_Summ',
        'Reporting vw_OPS_Scorecard_MES_SHP_Summ',
        'Reporting vw_Ops_Scorecard_eTraveler_Status'        
    ]
}

def _generate_markdown(tab_views:dict)-> dcc.Markdown:
    """Generate markdown text for tab_views"""
    res = ''
    for k, v in tab_views.items():
        res += f"###### {k} \n"
        for view in v:
            res += f"- {view} \n"
        res += "\n"
    return res

_markdown_text = _generate_markdown(_views_for_tabs) 

def tab_documentation():
    """build tab comparison with MarkDown 
    """
    return html.Div(
        children=[
           dcc.Markdown(_markdown_text) 
        ]
    )