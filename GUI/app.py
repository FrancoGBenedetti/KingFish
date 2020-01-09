from datos import *
import dash
from dash.dependencies import Input, Output

import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac

from dash.exceptions import PreventUpdate

from apps.cards import anomaly_tab
from apps.validations_cards import validation_tab
from apps.tab_cards import tab_cards_tab
from apps.basic_boxes import basic_boxes_tab
from apps.value_boxes import value_boxes_tab

from example_plots import plot_rnt_diaria, plot_rnt_acum

# =============================================================================
# Dash App and Flask Server
# =============================================================================
app = dash.Dash(__name__)
server = app.server
app.title = 'Antarctic Validaciones'

# =============================================================================
# Dash Admin Components
# =============================================================================
# Navbar
right_ui = dac.NavbarDropdown(
	badge_label = "!",
    badge_color= "danger",
    src = "https://quantee.ai",
	header_text="2 Items",
    children= [
		dac.NavbarDropdownItem(
			children = "message 1",
			date = "today"
		),
		dac.NavbarDropdownItem(
			children = "message 2",
			date = "yesterday"
		),
	]
)

navbar = dac.Navbar(color = "white",
                    text="Menú",
                    children=right_ui)

# Sidebar
subitems = [dac.SidebarMenuSubItem(id='tab_gallery_1',
                            label='Gallery 1',
                            icon='arrow-circle-right',
                            badge_label='Soon',
                            badge_color='success'),
			dac.SidebarMenuSubItem(id='tab_gallery_2',
                            label='Gallery 2',
                            icon='arrow-circle-right',
                            badge_label='Soon',
                            badge_color='success')
            ]

sidebar = dac.Sidebar(
	dac.SidebarMenu(
		[
			dac.SidebarMenuItem(id='tab_tab_cards', label='Inicio', icon='home'),
			dac.SidebarHeader(children="Dashboards"),
			dac.SidebarMenuItem(id='tab_anomaly', label='Detección Anomalías', icon='eye'),
            dac.SidebarMenuItem(id='tab_validations', label='Validaciones', icon='file-medical-alt'),
			dac.SidebarHeader(children="Boxes"),
			dac.SidebarMenuItem(id='tab_basic_boxes', label='Basic boxes', icon='desktop'),
			dac.SidebarMenuItem(id='tab_value_boxes', label='Value/Info boxes', icon='suitcase'),
			dac.SidebarHeader(children="Gallery"),
			dac.SidebarMenuItem(label='Galleries', icon='cubes', children=subitems),
		]
	),
    title='Lucas',
	skin="light",
    color="primary",
	brand_color="primary",
    url="https://quantee.ai",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

# Body
body = dac.Body(
    dac.TabItems([
        anomaly_tab,
        validation_tab,
        tab_cards_tab,
        basic_boxes_tab,
        value_boxes_tab,
        dac.TabItem(html.P('Gallery 1 (You can add Dash Bootstrap Components!)'),
                    id='content_gallery_1'),
        dac.TabItem(html.P('Gallery 2 (You can add Dash Bootstrap Components!)'),
                    id='content_gallery_2'),
    ])
)

# Controlbar
controlbar = dac.Controlbar(
    [
        html.Br(),
        html.P("Slide to change graph in Basic Boxes"),
        dcc.Slider(
            id='controlbar-slider',
            min=10,
            max=50,
            step=1,
            value=20
        ),
	    dcc.DatePickerRange( id='date-picker-range',
	        start_date = new_rnt_diaria.ds.min(), end_date=dt.now() )
    ],
    title = "My right sidebar",
    skin = "light"
)

# Footer
footer = dac.Footer(
	html.A("Antarctic Analytics",
		href = "https://www.antarctic.ai/",
		target = "_blank",
	),
	right_text = "2020"
)

# =============================================================================
# App Layout
# =============================================================================
app.layout = dac.Page([navbar, sidebar, body, controlbar, footer])

# =============================================================================
# Callbacks
# =============================================================================
def activate(input_id,
             n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
             n_value_boxes, n_gallery_1, n_gallery_2):

    # Depending on tab which triggered a callback, show/hide contents of app
    if input_id == 'tab_anomaly' and n_cards:
        return True, False, False, False, False, False, False
    elif input_id == 'tab_validations' and n_social_cards:
        return False, True, False, False, False, False, False
    elif input_id == 'tab_tab_cards' and n_tab_cards:
        return False, False, True, False, False, False, False
    elif input_id == 'tab_basic_boxes' and n_basic_boxes:
        return False, False, False, True, False, False, False
    elif input_id == 'tab_value_boxes' and n_value_boxes:
        return False, False, False, False, True, False, False
    elif input_id == 'tab_gallery_1' and n_gallery_1:
        return False, False, False, False, False, True, False
    elif input_id == 'tab_gallery_2' and n_gallery_2:
        return False, False, False, False, False, False, True
    else:
        return True, False, False, False, False, False, False # App init

@app.callback([Output('anomaly_cards', 'active'),
               Output('validations_cards', 'active'),
               Output('content_tab_cards', 'active'),
               Output('content_basic_boxes', 'active'),
               Output('content_value_boxes', 'active'),
               Output('content_gallery_1', 'active'),
               Output('content_gallery_2', 'active')],
               [Input('tab_anomaly', 'n_clicks'),
                Input('tab_validations', 'n_clicks'),
                Input('tab_tab_cards', 'n_clicks'),
                Input('tab_basic_boxes', 'n_clicks'),
                Input('tab_value_boxes', 'n_clicks'),
                Input('tab_gallery_1', 'n_clicks'),
                Input('tab_gallery_2', 'n_clicks')]
)
def display_tab(n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
                n_value_boxes, n_gallery_1, n_gallery_2):

    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return activate(input_id,
                    n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
                    n_value_boxes, n_gallery_1, n_gallery_2)

@app.callback([Output('tab_anomaly', 'active'),
               Output('tab_validations', 'active'),
               Output('tab_tab_cards', 'active'),
               Output('tab_basic_boxes', 'active'),
               Output('tab_value_boxes', 'active'),
               Output('tab_gallery_1', 'active'),
               Output('tab_gallery_2', 'active')],
               [Input('tab_anomaly', 'n_clicks'),
                Input('tab_validations', 'n_clicks'),
                Input('tab_tab_cards', 'n_clicks'),
                Input('tab_basic_boxes', 'n_clicks'),
                Input('tab_value_boxes', 'n_clicks'),
                Input('tab_gallery_1', 'n_clicks'),
                Input('tab_gallery_2', 'n_clicks')]
)
def activate_tab(n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
                n_value_boxes, n_gallery_1, n_gallery_2):

    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return activate(input_id,
                    n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
                    n_value_boxes, n_gallery_1, n_gallery_2)

# Update Renta Diaria y Acumulada
@app.callback(
    [Output('box-renta_diaria', 'figure'),
	Output('box-renta_acum', 'figure')],
    [#Input('controlbar-slider', 'value'),
	Input('date-picker-range','start_date'),
    Input('date-picker-range','end_date')])
def update_box_graph(start_date,end_date):
    return plot_rnt_diaria(start_date,end_date),plot_rnt_acum(start_date,end_date)

# =============================================================================
# Run app
# =============================================================================
if __name__ == '__main__':
    app.run_server(debug=True)
