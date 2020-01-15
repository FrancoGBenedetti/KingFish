import numpy as np
import pandas as pd
from pyScripts.datos import *
import plotly.graph_objs as go
import dash_table

def plot_pie():
    colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']

    trace = go.Pie(labels=validation.index, values=validation.message,
                   hoverinfo='label+percent', textinfo='value',
                   textfont=dict(size=20),
                   marker=dict(colors=colors,
                               line=dict(color='#C0C0C0', width=2)))

    return dict(data=[trace])

def plot_bar():
    trace = go.Bar(x=validation.message, y=validation.index, orientation='h',
                    marker={'color':validation.message.values.tolist(),'colorscale':'Viridis',
                    'colorbar': {"title": 'Cantidad',"titleside": 'top',
                                "tickmode": 'array',"tickvals": [validation.message.values.min(), validation.message.values.max()/2, validation.message.values.max()],
                                "ticktext": ['Bajo', 'Medio', 'Alto'],
                                "ticks": 'outside'}})
    return {'data':[trace],
            "layout": go.Layout(
                      xaxis={"title":"# datos inválidos"}
                     )}

def plot_rnt(df,start_date,end_date,available_indicators):
    return {
    'data': [go.Scatter(
                x=df[(df['ds']>=start_date)&(df['ds']<=end_date)]['ds'][(df['RUT'].isin(available_indicators))],
                y=df[(df['ds']>=start_date)&(df['ds']<=end_date)]['fact'][(df['RUT'].isin(available_indicators))],
                name='renta diaria',
                mode = 'lines+markers',
                marker=dict(size=1.3, colorscale='Viridis',color='#68C3C9')
    ),
    go.Scatter(
            x=df[(df['ds']>=start_date)&(df['ds']<=end_date)]['ds'],
            y=df[(df['ds']>=start_date)&(df['ds']<=end_date)]['yhat_upper'],
            name='upper',
            mode = 'lines',
            opacity=0.5,
            marker=dict(color='#A51919')
    ),
    go.Scatter(
            x=df[(df['ds']>=start_date)&(df['ds']<=end_date)]['ds'],
            y=df[(df['ds']>=start_date)&(df['ds']<=end_date)]['yhat_lower'],
            name='lower',
            mode = 'lines',
            opacity=0.5,
            marker=dict(color='#A51919')
    ),
                ]
            ,
    "layout": go.Layout(
               xaxis={"title":"Fecha"}, yaxis={"title":"Renta Diaria"},
               legend={'x':-.1,'y':1.5}
             )
        }

def plot_rnt_acum(start_date,end_date):
    return {
    'data': [go.Scatter(
                x=new_rnt_acum[(new_rnt_acum['ds']>=start_date)&(new_rnt_acum['ds']<=end_date)]['ds'],
                y=new_rnt_acum[(new_rnt_acum['ds']>=start_date)&(new_rnt_acum['ds']<=end_date)]['fact'],
                name='renta acumulada',
                mode = 'lines+markers',
                marker=dict(size=1.3,color='#68C3C9')
    ),
    go.Scatter(
            x=new_rnt_acum[(new_rnt_acum['ds']>=start_date)&(new_rnt_acum['ds']<=end_date)]['ds'],
            y=new_rnt_acum[(new_rnt_acum['ds']>=start_date)&(new_rnt_acum['ds']<=end_date)]['yhat_upper'],
            name='upper',
            mode = 'lines',
            opacity=0.5,
            marker=dict(color='#A51919')
    ),
    go.Scatter(
            x=new_rnt_acum[(new_rnt_acum['ds']>=start_date)&(new_rnt_acum['ds']<=end_date)]['ds'],
            y=new_rnt_acum[(new_rnt_acum['ds']>=start_date)&(new_rnt_acum['ds']<=end_date)]['yhat_lower'],
            name='lower',
            mode = 'lines',
            opacity=0.5,
            marker=dict(color='#A51919')
    ),
                ]
            ,
    "layout": go.Layout(
               xaxis={"title":"Fecha"}, yaxis={"title":"Renta Acumulada"},
               legend={'x':-.1,'y':1.5}
             )
        }

def plot_anom_cont(df,start_date,end_date):
    return {
    'data': [go.Scatter(
        x=df[(df['Fecha']>=start_date)&(df['Fecha']<=end_date)]['Fecha'],
        y=df[(df['Fecha']>=start_date)&(df['Fecha']<=end_date)]['cont'],
        name='Cantidad de anomalías',
        mode='lines+markers',
        marker=dict(size=1.2,color='#68C3C9',line=dict(color='MediumPurple',width=8))
    )],
    'layout': go.Layout(
                xaxis={"title":"Fecha"}, yaxis={"title":"Contador"},)
    }

def indicator(lastMonth, previousMonth, titulo):
    return{
    'data': [go.Indicator(
            mode="gauge+number+delta",
            value=lastMonth,
            domain={'x':[0,1],'y':[0,1]},
            title={'text':titulo},
            delta = {'reference': previousMonth},
            gauge = {'axis': {'range': [None, 30]},
             'steps' : [
                 {'range': [0, 15], 'color': "lightgray"},
                 {'range': [15, 25], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
    )]
    }

def create_table(df,page_current, sort_by,start_date,end_date):
    table=dash_table.DataTable(
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in sorted(df.columns)
        ],
        page_current=0,
        page_action='custom',
        sort_action='custom',
        sort_mode='single',
        sort_by=[]
    )
    return table
