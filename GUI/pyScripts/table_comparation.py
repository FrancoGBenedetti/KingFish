import dash
import dash_core_components as dcc
import dash_admin_components as dac
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

def reconciliation(df,df1):
    # Retorna 2 DataFrames en donde se encontró diferencias
    dfs_dictionary = {'DF':df,'DF1':df1}
    dff=pd.concat(dfs_dictionary)
    dff=dff.drop_duplicates(keep=False)
    DF1=dff.loc[dff.index.levels[0][0]]
    DF2=dff.loc[dff.index.levels[0][1]]
    return DF1,DF2

def indicator(df,df1):
    # Retorna una lista con las columnas inválidas y otra con las filas inválidas
    invalid_col=[]
    invalid_row=[]
    for x in df.index:
        for i in sorted(df.columns):
            if df[i][x] != df1[i][x]:
                if pd.isnull(df[i][x])==False:
                    invalid_col.append(i)
                    invalid_row.append(x)
    return invalid_col, invalid_row

def cell_style(value, value1):
#Retorna style de celda de la tabla en donde los valores no coincidan
    style = {}
    if (pd.isnull(value) & pd.isnull(value1)) == False:
        if value != value1:
            style = {
                'backgroundColor': '#d7301f',
                'color': 'white'
            }
    return style

def generate_table(DF, DF1):
    # Retorna el header y el body de la tabla
    rows = []
    for i in range(len(DF)):
        row = []
        for col in DF.columns:
            value = DF.iloc[i][col]
            value1 = DF1.iloc[i][col]
            style = cell_style(value, value1)
            row.append(html.Td(value, style=style))
        rows.append(html.Tr(row))

    table_header  = [html.Thead(html.Tr([html.Th(col) for col in DF.columns]), className='thead-dark')]
    table_body = [html.Tbody(rows)]
    return table_header, table_body
