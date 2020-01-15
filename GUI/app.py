from pyScripts.datos import *
import io
import base64
import dash
from dash.dependencies import Input, Output, State

import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate

from apps.cards import anomaly_tab
from apps.validations_cards import validation_tab
from apps.inicio import tab_inicio
from apps.table_comparation import table_comparison_tab
from apps.value_boxes import value_boxes_tab

from example_plots import *

# =============================================================================
# Dash App and Flask Server
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
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
			dac.SidebarMenuItem(id='inicio_tab', label='Inicio', icon='home'),
			dac.SidebarHeader(children="Dashboards"),
			dac.SidebarMenuItem(id='tab_anomaly', label='Detección Anomalías', icon='eye'),
            dac.SidebarMenuItem(id='tab_validations', label='Validaciones', icon='file-medical-alt'),
			dac.SidebarHeader(children="Herramientas"),
			dac.SidebarMenuItem(id='tab_table_comparation', label='Comparación de Fuentes', icon='balance-scale-left'),
			dac.SidebarMenuItem(id='tab_value_boxes', label='Value/Info boxes', icon='suitcase'),
			dac.SidebarHeader(children="Gallery"),
			dac.SidebarMenuItem(label='Galleries', icon='cubes', children=subitems),
		]
	),
    title='Lucas',
	skin="light",
    color="primary",
	brand_color="primary",
    url="https://www.antarctic.ai/",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

# Body
body = dac.Body(
    dac.TabItems([
        anomaly_tab,
        validation_tab,
        tab_inicio,
        table_comparison_tab,
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
        html.P("Seleccionar clientes"),
        dcc.Dropdown(
            id='crossfilter-rut',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value=available_indicators,
            multi=True
        ),
		html.Br(),
		html.P("Seleccionar rango de Fechas"),
	    dcc.DatePickerRange( id='date-picker-range',
	        start_date = new_rnt_diaria.ds.min(), end_date=dt.now() )
    ],
    title = "Filtros",
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
             n_tab_cards, n_social_cards, n_cards, n_basic_boxes,
             n_value_boxes, n_gallery_1, n_gallery_2):

    # Depending on tab which triggered a callback, show/hide contents of app
    if input_id == 'inicio_tab' and n_tab_cards:
        return True, False, False, False, False, False, False
    elif input_id == 'tab_validations' and n_social_cards:
        return False, True, False, False, False, False, False
    elif input_id == 'tab_anomaly' and n_cards:
        return False, False, True, False, False, False, False
    elif input_id == 'tab_table_comparation' and n_basic_boxes:
        return False, False, False, True, False, False, False
    elif input_id == 'tab_value_boxes' and n_value_boxes:
        return False, False, False, False, True, False, False
    elif input_id == 'tab_gallery_1' and n_gallery_1:
        return False, False, False, False, False, True, False
    elif input_id == 'tab_gallery_2' and n_gallery_2:
        return False, False, False, False, False, False, True
    else:
        return True, False, False, False, False, False, False # App init

@app.callback([Output('content_inicio', 'active'),
               Output('validations_cards', 'active'),
               Output('anomaly_cards', 'active'),
               Output('content_table_comparation', 'active'),
               Output('content_value_boxes', 'active'),
               Output('content_gallery_1', 'active'),
               Output('content_gallery_2', 'active')],
               [Input('inicio_tab', 'n_clicks'),
                Input('tab_validations', 'n_clicks'),
                Input('tab_anomaly', 'n_clicks'),
                Input('tab_table_comparation', 'n_clicks'),
                Input('tab_value_boxes', 'n_clicks'),
                Input('tab_gallery_1', 'n_clicks'),
                Input('tab_gallery_2', 'n_clicks')]
)
def display_tab(n_tab_cards, n_social_cards, n_cards, n_basic_boxes,
                n_value_boxes, n_gallery_1, n_gallery_2):

    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return activate(input_id,
                    n_tab_cards, n_social_cards, n_cards, n_basic_boxes,
                    n_value_boxes, n_gallery_1, n_gallery_2)

@app.callback([Output('inicio_tab', 'active'),
               Output('tab_validations', 'active'),
               Output('tab_anomaly', 'active'),
               Output('tab_table_comparation', 'active'),
               Output('tab_value_boxes', 'active'),
               Output('tab_gallery_1', 'active'),
               Output('tab_gallery_2', 'active')],
               [Input('inicio_tab', 'n_clicks'),
                Input('tab_validations', 'n_clicks'),
                Input('tab_anomaly', 'n_clicks'),
                Input('tab_table_comparation', 'n_clicks'),
                Input('tab_value_boxes', 'n_clicks'),
                Input('tab_gallery_1', 'n_clicks'),
                Input('tab_gallery_2', 'n_clicks')]
)
def activate_tab(n_tab_cards, n_social_cards, n_cards, n_basic_boxes,
                n_value_boxes, n_gallery_1, n_gallery_2):

    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return activate(input_id,
                    n_tab_cards, n_social_cards, n_cards, n_basic_boxes,
                    n_value_boxes, n_gallery_1, n_gallery_2)

# Update Renta Diaria y Acumulada
@app.callback(
    [Output('box-renta_diaria', 'figure'),
	Output('box-renta_acum', 'figure')],
    [Input('date-picker-range','start_date'),
    Input('date-picker-range','end_date'),
	Input('crossfilter-rut','value')])
def update_box_graph(start_date,end_date,available_indicators):
    return plot_rnt(new_rnt_diaria,start_date,end_date,available_indicators),plot_rnt(new_rnt_acum,start_date,end_date,available_indicators)

# Cantidad de anomalías Renta Diaria y Acumulada
@app.callback(
    [Output('box-anomD_cont', 'figure'),
	Output('box-anomA_cont', 'figure')],
    [Input('date-picker-range','start_date'),
    Input('date-picker-range','end_date')])
def update_graph(start_date,end_date):
    return plot_anom_cont(anomD_cont,start_date,end_date),plot_anom_cont(anomA_cont,start_date,end_date)

# Drag & Drop data
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' or 'xlsx' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))

# Tabla Drang & Drop
@app.callback([Output('datatable-upload-container', 'data'),
               Output('datatable-upload-container', 'columns')],
              [Input('datatable-upload', 'contents')],
              [State('datatable-upload', 'filename')])
def update_output(contents, filename):
    if contents is None:
        return [{}], []
    df = parse_contents(contents, filename)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

#Tabla Renta Diaria
@app.callback(
    Output('tabla_rnt_diaria', 'data'),
    [Input('tabla_rnt_diaria', "page_current"),
	 Input('tabla_rnt_diaria', "page_size"),
     Input('tabla_rnt_diaria', 'sort_by'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
	 Input('crossfilter-rut','value')])
def update_table(page_current, page_size,sort_by,start_date,end_date, available_indicators):
    if len(sort_by):
        dff = anomD.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = anomD
    dff=dff[(dff['RUT'].isin(available_indicators))]
    dff=dff[(dff['ds']>=start_date)&(dff['ds']<=end_date)]
    return dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
#Tabla Renta Acumulada
@app.callback(
    Output('tabla_rnt_acum', 'data'),
    [Input('tabla_rnt_acum', "page_current"),
	 Input('tabla_rnt_acum', "page_size"),
     Input('tabla_rnt_acum', 'sort_by'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
	 Input('crossfilter-rut','value')])
def update_table(page_current, page_size,sort_by,start_date,end_date, available_indicators):
    if len(sort_by):
        dff = anomA.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = anomA
    dff=dff[(dff['RUT'].isin(available_indicators))]
    dff=dff[(dff['ds']>=start_date)&(dff['ds']<=end_date)]
    return dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

#Tabla Validaciones
@app.callback(
    Output('errores-detectados', 'data'),
    [Input('errores-detectados', "page_current"),
     Input('errores-detectados', "page_size"),
     Input('errores-detectados', 'sort_by'),
	 Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')])
def update_table(page_current, page_size, sort_by, start_date, end_date):
    if len(sort_by):
        dff = all_errors.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = all_errors
	#dff=dff[(dff['ds']>=start_date)&(dff['ds']<=end_date)]
    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

# =============================================================================
# Run app
# =============================================================================
if __name__ == '__main__':
    app.run_server(debug=True)
