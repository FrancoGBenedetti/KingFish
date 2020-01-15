import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac
import dash_table
from example_plots import plot_pie, plot_bar
from pyScripts.datos import all_errors, td

dropdown_items = [
	dac.BoxDropdownItem(url="https://www.google.com", children="Link to google"),
	dac.BoxDropdownItem(url="#", children="item 2"),
	dac.BoxDropdownDivider(),
	dac.BoxDropdownItem(url="#", children="item 3")
]

validation_tab = dac.TabItem(id='validations_cards',

    children=html.Div([
			html.Div([
			dac.Box(
                [
                    dac.BoxHeader(
                        dac.BoxDropdown(dropdown_items),
                        collapsible = True,
                        closable = True,
                        title="Campos con datos Inválidos"
                    ),
                    dac.BoxBody(
                        dcc.Graph(
                            figure=plot_bar(),
                            config=dict(displayModeBar=False),
                            style={'width': '37vw'}
                        )
                    )
                ],
                color='warning',

            ),
            dac.ValueBox(
            	value=len(all_errors),
                subtitle="Errores detectados",
                color = "success",
                icon = "bug",
                href = "#"
            )
        ],className='row'),

		html.Div([
			html.H4('Errores Detectados'),

			dash_table.DataTable(
			id='errores-detectados',
			style_as_list_view=True,
			style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}],
			style_header={'backgroundColor': '#f5b86e','fontWeight': 'bold'},
			style_table={'overflowX': 'scroll'},
	        columns=[
	            {'name': i, 'id': i, 'deletable': True} for i in sorted(all_errors.columns)
	        ],
	        page_current=0,
			page_size=8,
	        page_action='custom',
	        sort_action='custom',
	        sort_mode='single',
	        sort_by=[]
	    )
		], className='container')
	],className='container')
)
