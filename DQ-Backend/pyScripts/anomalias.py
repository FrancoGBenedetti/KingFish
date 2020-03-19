import dash_table
from sqlalchemy import create_engine
import pymysql
from datetime import datetime as dt
from fbprophet import Prophet
import pandas as pd
import numpy as np
from decimal import Decimal, InvalidOperation
from db_access import *

def fit_predict_model(dataframe, interval_width = 0.99, changepoint_range = 0.8):

    m = Prophet(daily_seasonality = False, yearly_seasonality = False, weekly_seasonality = False,
                #seasonality_mode = 'multiplicative',
                seasonality_mode = 'additive',
                interval_width = interval_width,
                changepoint_range = changepoint_range)
    m = m.fit(dataframe)
    forecast = m.predict(dataframe)
    forecast['fact'] = dataframe['y'].reset_index(drop = True)
    return forecast

def detect_anomalies(forecast):
    forecasted = forecast[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()

    forecasted['anomaly'] = 0
    forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'], 'anomaly'] = 1
    forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'], 'anomaly'] = -1

    #anomaly importances
    forecasted['importance'] = 0
    forecasted.loc[forecasted['anomaly'] ==1, 'importance'] = \
        (forecasted['fact'] - forecasted['yhat_upper'])/forecast['fact']
    forecasted.loc[forecasted['anomaly'] ==-1, 'importance'] = \
        (forecasted['yhat_lower'] - forecasted['fact'])/forecast['fact']

    return forecasted

def join_rnts(df,rnt):
    rnt.index.name='row'
    df.index.name='row'
    new_rnt=pd.merge(rnt,df,on='row', how='inner', left_index=True, right_index=True)
    return new_rnt

def anomaly_counts(renta,tipo_renta):
    # Calcula anomalías de una variable (renta) y retorna:
    #     -anomaly: Tabla con las anomalías, descripción, importancia, valor esperado, lower y upper
    #     -anomaly_cont: Tabla con la cantidad de anomalías en el tiempo
    #     -anomaly_lastMonth: Cantidad de anomalías del mes pasado
    #     -anomaly_previousMonth: Cantidad de anomalías del mes antepasado
        anomaly = renta.loc[renta['anomaly']!=0].loc[:,['ds','fact','yhat','anomaly','importance','yhat_lower','yhat_upper']]
        anomaly.index.name='row'
        anomaly=pd.merge(anomaly, df, on='row', how='inner').loc[:,['ds','yhat','yhat_lower','yhat_upper','anomaly','importance','RUT','APORTES','RETIROS','PATRIMONIO',tipo_renta]]
        anomaly['description']=''
        for i in anomaly.index:
            a=anomaly.loc[i,tipo_renta]/anomaly.loc[i,'yhat']
            anomaly['description'][i] = f'{a:.4} x veces lo esperado'
        #Contador de anomalías en el tiempo Renta
        anomaly_cont=anomaly.ds.value_counts().resample('D').sum()
        df2=pd.DataFrame()
        for i in range(0,len(anomaly_cont)):
            df3 =  pd.DataFrame({'Fecha':[anomaly_cont.index[i]],'cont':[anomaly_cont[i]]})
            df2 = df2.append(df3)
        anomaly_cont=df2
        anomaly_lastMonth = len(anomaly_cont[anomaly_cont["Fecha"] >= (dt.now() - pd.Timedelta(days=30))])
        anomaly_previousMonth = len(anomaly_cont[(anomaly_cont["Fecha"] >= (dt.now() - pd.Timedelta(days=60)))
                                & (anomaly_cont["Fecha"] <= (dt.now() - pd.Timedelta(days=30)))])
        anomaly.rename(columns={"ds": "FECHA", "anomaly": "ANOMALIA","yhat":"VALOR_ESPERADO",
                    "importance":"IMPORTANCIA","description":"DESCRIPCION",
                    "yhat_lower":"lower","yhat_upper":"upper"}, inplace=True)

        return anomaly, anomaly_cont, anomaly_lastMonth, anomaly_previousMonth

def get_lastmonths_counts(anomaly_cont):
    anomaly_lastMonth = len(anomaly_cont[anomaly_cont["Fecha"] >= (dt.now() - pd.Timedelta(days=30))])
    anomaly_previousMonth = len(anomaly_cont[(anomaly_cont["Fecha"] >= (dt.now() - pd.Timedelta(days=60)))
                            & (anomaly_cont["Fecha"] <= (dt.now() - pd.Timedelta(days=30)))])
    return anomaly_lastMonth, anomaly_previousMonth

############################### Ejecución de Funciones ###################################

df = extract_db_data('fuentedatos', 'rentaclientes')

df['FECHA'] = pd.to_datetime(df.FECHA)
data=df.set_index('FECHA')
df.index.name='row'
#Se seleccionan los campos FECHA y el valor a predecir (Renta diaria y Renta acumulada)
rd=df.loc[:,['FECHA','rent_diaria']]
rd.rename(columns={"FECHA": "ds", "rent_diaria": "y"}, inplace=True)

ra=df.loc[:,['FECHA','rent_acum']]
ra.rename(columns={"FECHA": "ds", "rent_acum": "y"}, inplace=True)
#Se calculan las anomalías de las rentas diaria y acumulada
rnt_diaria = fit_predict_model(rd, interval_width = 0.9)
rnt_diaria = detect_anomalies(rnt_diaria)
new_rnt_diaria=join_rnts(df,rnt_diaria)

rnt_acum = fit_predict_model(ra, interval_width = 0.9)
rnt_acum = detect_anomalies(rnt_acum)
new_rnt_acum=join_rnts(df,rnt_acum)
#Se calculan los contadores de anomalías de las rentas diaria y acumulada
anomD, anomD_cont, anomD_lastMonth, anomD_previousMonth = anomaly_counts(rnt_diaria,'rent_diaria')
anomA, anomA_cont, anomA_lastMonth, anomA_previousMonth = anomaly_counts(rnt_acum,'rent_acum')
#Todos los RUT disponibles
available_indicators = df['RUT'].unique()

###################################
##### Inserción de datos a DB #####
###################################

#Se insertan las anomalías en la Base de datos
df2mysql_2(anomD,'anomalias_renta_diaria','calculos')
df2mysql_2(anomA,'anomalias_renta_acumulada','calculos')
#Se inserta la cantidad de anomalías en la Base de datos
df2mysql_2(anomD_cont,'cantidad_anom_renta_diaria','calculos')
df2mysql_2(anomA_cont,'cantidad_anom_renta_acum','calculos')
#Se inserta la tabla fuente pero con lower, upper y las anomalías detectadas en la Base de datos
df2mysql_2(new_rnt_diaria,'new_rnt_diaria','calculos')
df2mysql_2(new_rnt_acum,'new_rnt_acum','calculos')
