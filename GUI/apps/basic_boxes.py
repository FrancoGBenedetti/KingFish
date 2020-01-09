import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac
from datetime import datetime as dt
import datetime
from example_plots import plot_rnt_diaria, indicator
from datos import *

basic_boxes_tab = dac.TabItem(id='content_basic_boxes',

    children=html.Div(
        [
            dac.SimpleBox(
            	style = {'height': "600px"},
                title = "Box 1",
                children=[
                    dcc.Graph(
                        id='box-graph',
                        config=dict(displayModeBar=False),
                        style={'width': '38vw'}
                    )
                ]
            ),
            dac.SimpleBox(
            	style = {'height': "600px"},
                title = "Box 2",
                children=[
                    dcc.Graph(
                        figure=indicator(anomD_lastMonth, anomD_previousMonth, 'Anomalías Renta Acumulada útlimo mes'),
                        config=dict(displayModeBar=False),
                        style={'width': '38vw'}
                    )
                ]
            )
        ],
        className='row'
    )
)
