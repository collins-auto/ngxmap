import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html

pf = pd.read_csv("stock_heatmap.csv", index_col=0)

fig = px.treemap(pf, path=[px.Constant("All Share Index"), "Sector", "Ticker"],
                 values = "Market Cap", color = "YTD Return",
                 hover_data = {"YTD Return":":.2p", "Market Cap": ":.2f"}, color_continuous_scale='RdYlGn',
                 color_continuous_midpoint=0, 
                 range_color = [-0.5, 0.5])

# fig.data[0].textinfo = 'label+value+percent parent'
returns = pf["YTD Return"].tolist()
market_cap = pf["Market Cap"].tolist()

## store multiple lists of data in customdata
fig.data[0].customdata = np.column_stack([returns, market_cap])
fig.data[0].texttemplate = "%{label}<br>Market Cap:₦%{value}B<br>YTD Return:%{customdata[0]:.2p}"

fig.update_layout(margin = dict(l=5, r=5, t=20, b=5))

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(style={"textAlign": "center", "color": "#6bd64d"}, children='NGX ASI 2022 Summary'),
    
    html.Div(style={"textAlign": "center", "color": "#6bd64d"}, children='''
        Summary of NGX listed companies performance for 2022
    '''),
    
    dcc.Graph(figure=fig)])

app.run_server(debug=True)