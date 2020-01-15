import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac
import dash_bootstrap_components as dbc
import dash_table
from datetime import datetime as dt
import datetime
from pyScripts.datos import *

dropdown_items = [
	dac.BoxDropdownItem(url="https://www.google.com", children="Link to google"),
	dac.BoxDropdownItem(url="#", children="item 2"),
	dac.BoxDropdownDivider(),
	dac.BoxDropdownItem(url="#", children="item 3")
]

anomaly_tab = dac.TabItem(id='anomaly_cards',

    children=[

		html.Div([
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
        ),
		html.Div([
			html.H4('Anomalías Renta Diaria'),

			dash_table.DataTable(
			id='tabla_rnt_diaria',
			style_as_list_view=True,
			style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}],
			style_header={'backgroundColor': '#f5b86e','fontWeight': 'bold'},
			style_table={'overflowX': 'scroll'},
	        columns=[
	            {'name': i, 'id': i, 'deletable': True} for i in sorted(anomD.columns)
	        ],
	        page_current=0,
			page_size=8,
	        page_action='custom',
	        sort_action='custom',
	        sort_mode='single',
	        sort_by=[]
	    )
		], className='container mt-3'),
		html.Div([
			html.H4('Anomalías Renta Acumulada'),

			dash_table.DataTable(
			id='tabla_rnt_acum',
			style_as_list_view=True,
			style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}],
			style_header={'backgroundColor': '#f5b86e','fontWeight': 'bold'},
			style_table={'overflowX': 'scroll'},
	        columns=[
	            {'name': i, 'id': i, 'deletable': True} for i in sorted(anomA.columns)
	        ],
	        page_current=0,
			page_size=8,
	        page_action='custom',
	        sort_action='custom',
	        sort_mode='single',
	        sort_by=[]
	    )
		], className='container mt-3'),
		html.Div([
		html.Div([
			#html.Div([
			dac.Box(
            [
                dac.BoxHeader(
					dac.BoxDropdown(dropdown_items),
                    collapsible = True,
                    closable = True,
                    title="Cantidad de anomalías Renta diaria"
                ),
            	dac.BoxBody(
                    dcc.Graph(
                        id='box-anomD_cont',
                        config=dict(displayModeBar=False),
                        style={'width': '36vw'}
                    )
                )
            ],
            color='primary',
            solid_header=True,
            elevation=4,
            width=6
        ),
		#], className='col-6'),

			#html.Div([
			dac.Box(
			[
				dac.BoxHeader(
					dac.BoxDropdown(dropdown_items),
					collapsible = True,
					closable = True,
					title="Cantidad de anomalías Renta acumulada"
				),
				dac.BoxBody(
					dcc.Graph(
						id='box-anomA_cont',
						config=dict(displayModeBar=False),
						style={'width': '36vw'}
					)
				)
			],
			color='primary',
			solid_header=True,
			elevation=4,
			width=6
		)
		#], className='col-6')
		], className='row')
		], className='container mt-5')
		],className='container')
    ]
)
