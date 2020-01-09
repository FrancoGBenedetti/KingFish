import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac
from example_plots import plot_pie, plot_bar
from datos import all_errors

dropdown_items = [
	dac.BoxDropdownItem(url="https://www.google.com", children="Link to google"),
	dac.BoxDropdownItem(url="#", children="item 2"),
	dac.BoxDropdownDivider(),
	dac.BoxDropdownItem(url="#", children="item 3")
]

validation_tab = dac.TabItem(id='validations_cards',

    children=html.Div(
        [
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
                            style={'width': '38vw'}
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
            ),
            dac.UserCard(
              src = "https://adminlte.io/themes/AdminLTE/dist/img/user1-128x128.jpg",
              color = "info",
              title = "User card type 1",
              subtitle = "a subtitle here",
              elevation = 4,
              children="Any content here"
            ),
            dac.UserCard(
              type = 2,
              src = "https://adminlte.io/themes/AdminLTE/dist/img/user7-128x128.jpg",
              color = "success",
              image_elevation = 4,
              title = "User card type 2",
              subtitle = "a subtitle here",
              children="Any content here"
            )
        ],
        className='row'
    )
)
