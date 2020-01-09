import dash_html_components as html
import dash_admin_components as dac

tab_cards_tab = dac.TabItem(id='content_tab_cards',

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
                )
        ], className='container')

    ]
)
