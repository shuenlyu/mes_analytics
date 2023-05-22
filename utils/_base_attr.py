import plotly.graph_objects as go 

base_bar_attr = dict(
    marker=dict(
        # line=dict(width=1, color='red'), 
        # color='rgba(10, 10, 10, 0.9)',
        opacity=1
    ),
    textposition='auto',
    texttemplate="%{y:.0f}", 
    # name='trace 0',
    # hoverinfo='all',
)

base_layout = go.Layout(
    # width=50000,
    xaxis=dict(
        autorange=True, 
        title=dict(
            text="Date"
        ),
        tickformat="%d %b",
        rangemode='normal',
        tickprefix=None, #'prefix', 
        ticksuffix=None, #'suffix'
        tickmode='auto',
        showticklabels=True,
        tickangle= 0,
        ),
    yaxis=dict(
        title=dict(
            text=None
        ),
        tickprefix=None,
        ticksuffix=None, 
        tickmode='auto',
        showticklabels=True 
    ),
    # plot_bgcolor='rgb(203, 154, 242)', 
    # paper_bgcolor='rgb(87, 209, 186)',
    margin=dict(
        t=80,
        b=60,
        l=80,
        r=40,
        pad=0,
        autoexpand=True
    ),
    title = dict(
        # text="Fig Title", 
        font=dict(
            # color='rgb(0,0,0)',
            size=24,
            family="Droid Sans"
        ),
        # pad=dict(t=5,r=1,b=1000,l=1),
        x=0,
        xref="paper", #or paper 
        xanchor="auto",
        # y=0,
        yanchor="auto",
        # yref="container"
    ),
    font=dict(
        family="Droid Sans",
        # color='rgb(32, 9, 244)',
        size=13
    ),
    modebar=dict(
        orientation='v',
        # bgcolor=
        # color=?
        #activaecolor=?
    ),
    hovermode='x',
    # bargap=0.2,
    # bargroupgap=0,
    
    legend=dict(
        title=dict(
            text=None
        ),
        # borderwidth=1,
        x=1,
        y=1,
        # bgcolor='rgb(129, 160, 232)',
        xanchor="right", 
        yanchor="bottom",
        orientation='h',
        valign='middle', 
        # bordercolor='black',
        # borderwidth=1
        # xref="paper"
    )
)