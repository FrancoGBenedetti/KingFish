import dash_html_components as html
import dash_admin_components as dac
import dash_core_components as dcc
import dash_table

tab_inicio = dac.TabItem(id='content_inicio',

    children=[

        html.Div([
                html.Div(
                    [
                    dac.UserCard(
                      src = "https://adminlte.io/themes/AdminLTE/dist/img/user1-128x128.jpg",
                      color = "info",
                      title = "Bienvenido",
                      subtitle = "Administrador",
                      elevation = 4,
                      children="Plataforma de DataQuality"
                    )
                    ],
                    className='row d-flex justify-content-center'
                ),], className='container'),

                html.Div([
                html.Div([
                #html.Div([
                    dcc.Upload(
                        id='datatable-upload',
                        children=html.Div([
                            'Drag & Drop o ',
                            html.A('Seleccione un archivo')
                        ]),
                        style={
                            'width': "100%", 'height': '60px', 'lineHeight': '60px',
                            'borderWidth': '1px', 'borderStyle': 'outset',
                            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px',
                            'color':'#ffffff', 'background-color':'#eb8c17'},)
                    ], className='row d-flex justify-content-center'),
                    html.Div([
                    dash_table.DataTable(
                        id='datatable-upload-container',
            			style_as_list_view=True,
            			style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}],
            			style_header={'backgroundColor': '#f5b86e','fontWeight': 'bold'},
            			style_table={'overflowX': 'scroll'},
                        fixed_rows={ 'headers': True, 'data': 0 },
                        )
                #], className="col-12")
                ], className="row d-flex justify-content-center")
        ], className='container')

    ]
)
