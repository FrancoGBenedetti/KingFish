from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
from datetime import date

#response = requests.get('https://casas.mitula.cl/searchRE/nivel1-Metropolitana/nivel2-Santiago/orden-0/q-santiago/pag-1')
#soup = BeautifulSoup(response.text,'html.parser')
gral = pd.DataFrame()
arriendos = pd.DataFrame()
weas=['<span>','<strong>','</strong>','</','>','$','.',' ','span','baños','dormitorios','dormitorio',' m2','m²','baño']

def sacar_weas(data,str_columna, weas):

    for i in weas:
        data[str_columna] = data[str_columna].map(lambda x: x.replace(i,''))
    return data[str_columna]

def populate_table():
    descrip=[]
    for container in soup.find_all(class_='adDescription'):
        a = container.find('h5').findAll('span')
        descrip.append(a)
    precio=[]
    for container in soup.find_all(class_='adPrice'):
        a = container.text
        precio.append(a)
    descr_largo=[]
    for container in soup.find_all(class_='adTeaser ellipsis'):
        a = container.text
        descr_largo.append(a)
    df = pd.DataFrame(data=descrip, index=None, columns=['ubicacion','tipo_operacion', 'tipo_propiedad', 'metros', 'dorm', 'baños'])
    df['precio']=precio

    df.ubicacion=df.ubicacion.astype(str)
    df.tipo_operacion=df.tipo_operacion.astype(str)
    df.tipo_propiedad=df.tipo_propiedad.astype(str)
    df.metros=df.metros.astype(str)
    df.dorm=df.dorm.astype(str)
    df.baños=df.baños.astype(str)
    df.precio=df.precio.astype(str)

    for col in df.columns:
        df[col]=sacar_weas(df,col, weas)
    df.precio=df.precio.astype(int)
    df['fecha_obtencion_datos'] = date.today().strftime("%d-%m-%Y")
    return df

#General
for i in range(1, 50):
    response = requests.get(f'https://casas.mitula.cl/searchRE/nivel1-Metropolitana/nivel2-Santiago/orden-0/q-santiago/pag-{i}?t_sec=1&t_or=0')
    soup = BeautifulSoup(response.text,'html.parser')
    df1 = populate_table()
    gral=gral.append(df1)
    print('Pagina: '+i)
    print('Prop x pagina: '+len(df1))
print('General: ')
print(len(gral))
#gral.to_excel("general.xlsx")

#Arriendos
# for i in range(1, 100):
#     response = requests.get(f'https://casas.mitula.cl/searchRE/orden-0/op-2/q-arriendo-santiago/pag-{i}?t_sec=1&t_or=0')
#     soup = BeautifulSoup(response.text,'html.parser')
#     df1 = populate_table()
#     arriendos=arriendos.append(df1)
# print('Arriendos: ')
# print(len(arriendos))
# arriendos.to_excel("arriendos.xlsx")
