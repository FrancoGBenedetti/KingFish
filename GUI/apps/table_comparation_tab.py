import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac
import dash_bootstrap_components as dbc

from datetime import datetime as dt
import datetime

from example_plots import plot_rnt, indicator
import pyScripts.datos as data
import pyScripts.table_comparation as tc

df1=data.td.copy()
df1.loc[df1.index==5,'RUT']='bbb'
df1.loc[df1.index==800,'rent_diaria']=0.5310
df1.loc[df1.index==845,'rent_diaria']=0.76782

rec1, rec2=tc.reconciliation(data.td, df1)
invalid_col, invalid_row = tc.indicator(rec1,rec2)

table = dbc.Table(
    #table_header + table_body,
    tc.generate_table(rec1, rec2)[0] + tc.generate_table(rec1, rec2)[1],
    bordered=True,
    #dark=True,
    hover=True,
    responsive=True,
    striped=True,
)
table2 = dbc.Table(
    #table_header + table_body,
    tc.generate_table(rec2, rec1)[0] + tc.generate_table(rec2, rec1)[1],
    bordered=True,
    #dark=True,
    hover=True,
    responsive=True,
    striped=True,
)

table_comparison_tab = dac.TabItem(id='content_table_comparation',

    children=html.Div(
        [
        html.Div([html.H4('Fuente de Datos: PostgresSQL'),table], className='container'),
        html.Div([html.H4('Fuente de Datos: Archivo CSV'),table2], className='container')
        ],
        className='container'
    )
)
