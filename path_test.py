from dash import Input as in1, Output as out1 
from dash.dependencies import Input as in2, Output as out2 
print(in1 is in2, out1 is out2)

from dash import callback as call1 
from app import app 
print(app.callback is call1)

from dash import dcc
store = dcc.Store
graph = dcc.Graph 

import dash_bootstrap_components as dbc 
from dash import dcc 
print(dcc.Tabs is dbc.Tabs)