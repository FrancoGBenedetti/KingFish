import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac
import dash_bootstrap_components as dbc
from datetime import datetime as dt
import datetime
from datos import *

dropdown_items = [
	dac.BoxDropdownItem(url="https://www.google.com", children="Link to google"),
	dac.BoxDropdownItem(url="#", children="item 2"),
	dac.BoxDropdownDivider(),
	dac.BoxDropdownItem(url="#", children="item 3")
]

anomaly_tab = dac.TabItem(id='anomaly_cards',

    children=[

        html.Div([
            dac.ValueBox(
            	value=anomD_lastMonth,
                subtitle="Cantidad en el último mes",
                color = "primary",
                icon = "eye",
                href = "#"
            ),
            dac.ValueBox(
              elevation = 4,
              value = anomD_lastMonth-anomD_previousMonth,
              subtitle = "Diferencia con el mes anterior",
              color = "danger",
              icon = "exclamation-circle"
            ),
            dac.ValueBox(
              value = anomA_lastMonth,
              subtitle = "Cantidad en el último mes",
              color = "warning",
              icon = "eye"
            ),
            dac.ValueBox(
              value = anomA_lastMonth-anomA_previousMonth,
              subtitle = "Diferencia con el mes anterior",
              color = "success",
              icon = "exclamation-circle"
            ),
            dac.Box(
                [
                    dac.BoxHeader(
						dac.BoxDropdown(dropdown_items),
                        collapsible = True,
                        closable = True,
                        title="Anomalías en la renta Diaria"
                    ),
                	dac.BoxBody(
                        dcc.Graph(
	                        id='box-renta_diaria',
	                        config=dict(displayModeBar=False),
	                        style={'width': '37vw'}
	                    )
                    )
                ],
                color='primary',
                solid_header=True,
                elevation=4,
                width=6
            ),
			dac.Box(
                [
                    dac.BoxHeader(
						dac.BoxDropdown(dropdown_items),
                        collapsible = True,
                        closable = True,
                        title="Anomalías en la renta Acumulada"
                    ),
                	dac.BoxBody(
                        dcc.Graph(
	                        id='box-renta_acum',
	                        config=dict(displayModeBar=False),
	                        style={'width': '37vw'}
	                    )
                    )
                ],
                color='primary',
                solid_header=True,
                elevation=4,
                width=6
            )],
            className='row'
        )

    ]
)
