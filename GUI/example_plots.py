import numpy as np
import pandas as pd
from datos import *
import plotly.graph_objs as go

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

def plot_rnt_diaria(start_date,end_date):
    return {
    'data': [go.Scatter(
                x=new_rnt_diaria[(new_rnt_diaria['ds']>=start_date)&(new_rnt_diaria['ds']<=end_date)]['ds'],
                y=new_rnt_diaria[(new_rnt_diaria['ds']>=start_date)&(new_rnt_diaria['ds']<=end_date)]['fact'],
                name='renta diaria',
                mode = 'markers',
                marker=dict(size=1.2, colorscale='Viridis',color='#68C3C9')
    ),
    go.Scatter(
            x=new_rnt_diaria[(new_rnt_diaria['ds']>=start_date)&(new_rnt_diaria['ds']<=end_date)]['ds'],
            y=new_rnt_diaria[(new_rnt_diaria['ds']>=start_date)&(new_rnt_diaria['ds']<=end_date)]['yhat_upper'],
            name='upper',
            mode = 'lines',
            opacity=0.5,
            marker=dict(color='#A51919')
    ),
    go.Scatter(
            x=new_rnt_diaria[(new_rnt_diaria['ds']>=start_date)&(new_rnt_diaria['ds']<=end_date)]['ds'],
            y=new_rnt_diaria[(new_rnt_diaria['ds']>=start_date)&(new_rnt_diaria['ds']<=end_date)]['yhat_lower'],
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
                marker=dict(size=1.2,color='#68C3C9')
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

def plot_surface():
    z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

    data = [
        go.Surface(
            z=z_data.values,
            contours=go.surface.Contours(
                z=go.surface.contours.Z(
                  show=True,
                  usecolormap=True,
                  highlightcolor="#42f462",
                  project=dict(z=True)
                )
            )
        )
    ]
    layout = go.Layout(
        title='Mt Bruno Elevation',
        scene=dict(camera=dict(eye=dict(x=1.87, y=0.88, z=-0.64))),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            l=35,
            r=20,
            b=35,
            t=45
        )
    )
    return go.Figure(data=data, layout=layout)
