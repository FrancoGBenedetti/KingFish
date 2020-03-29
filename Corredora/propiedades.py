from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

response = requests.get('https://casas.mitula.cl/searchRE/nivel1-Metropolitana/nivel2-Santiago/orden-0/q-santiago/pag-1')
soup = BeautifulSoup(response.text,'html.parser')
df = pd.DataFrame()
weas=['<span>','<strong>','</strong>','</','>','$','.','span','baños','dormitorios','dormitorio',' m2','m²']

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
    return df

for i in range(1, 100):
    response = requests.get(f'https://casas.mitula.cl/searchRE/nivel1-Metropolitana/nivel2-Santiago/orden-0/q-santiago/pag-{i}')
    soup = BeautifulSoup(response.text,'html.parser')
    df1 = populate_table()
    df=df.append(df1)

df.to_excel("propiedades.xlsx")
