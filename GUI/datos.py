import dash_table
from datetime import datetime as dt
from fbprophet import Prophet
import pandas as pd
import numpy as np
from decimal import Decimal, InvalidOperation
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import CustomElementValidation

td = pd.read_csv('../../../Proyectos/LarrainVial/todos_3.csv',sep=',')
td['FECHA'] = pd.to_datetime(td.FECHA)
data=td.set_index('FECHA')
td.index.name='row'

rd=td.loc[:,['FECHA','rent_diaria']]
rd.rename(columns={"FECHA": "ds", "rent_diaria": "y"}, inplace=True)

ra=td.loc[:,['FECHA','rent_acum']]
ra.rename(columns={"FECHA": "ds", "rent_acum": "y"}, inplace=True)

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
    #forecast['fact'] = df['y']

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
    #rnt.rename(columns={"ds": "FECHA", "yhat_lower": "lower",'yhat_upper':'upper'},inplace=True)
    #df.rename(columns={"ds": "FECHA"},inplace=True)
    rnt.index.name='row'
    df.index.name='row'
    #df.set_index('FECHA',inplace=True)
    #rnt.set_index('FECHA',inplace=True)
    new_rnt=pd.merge(rnt,df,on='row', how='inner', left_index=True, right_index=True)
    return new_rnt

rnt_diaria = fit_predict_model(rd, interval_width = 0.9)
rnt_diaria = detect_anomalies(rnt_diaria)
new_rnt_diaria=join_rnts(td,rnt_diaria)

rnt_acum = fit_predict_model(ra, interval_width = 0.9)
rnt_acum = detect_anomalies(rnt_acum)
new_rnt_acum=join_rnts(td,rnt_acum)

anomD = rnt_diaria.loc[rnt_diaria['anomaly']!=0].loc[:,['ds','fact','yhat','anomaly','importance']]
anomD.index.name='row'
anomD=pd.merge(anomD, td, on='row', how='inner').loc[:,['ds','fact','yhat','anomaly','importance','RUT','APORTES','RETIROS','PATRIMONIO','rent_diaria']]
anomD['description']=''
for i in anomD.index:
    a=anomD.loc[i,'fact']/anomD.loc[i,'yhat']
    anomD['description'][i] = f'{a:.4} x veces lo esperado'
#Contador de anomalias en el tiempo Renta Diaria
anomD_cont=anomD.ds.value_counts().resample('D').sum()
df2=pd.DataFrame()
for i in range(0,len(anomD_cont)):
    df3 =  pd.DataFrame({'Fecha':[anomD_cont.index[i]],'cont':[anomD_cont[i]]})
    df2 = df2.append(df3)
anomD_cont=df2

anomD_lastMonth = len(anomD_cont[anomD_cont["Fecha"] >= (dt.now() - pd.Timedelta(days=30))])
anomD_previousMonth = len(anomD_cont[(anomD_cont["Fecha"] >= (dt.now() - pd.Timedelta(days=60)))
                        & (anomD_cont["Fecha"] <= (dt.now() - pd.Timedelta(days=30)))])

anomA = rnt_acum.loc[rnt_acum['anomaly']!=0].loc[:,['ds','fact','yhat','anomaly','importance']]
anomA.index.name='row'
anomA=pd.merge(anomA, td, on='row', how='inner').loc[:,['ds','fact','yhat','anomaly','importance','RUT','APORTES','RETIROS','PATRIMONIO','rent_acum']]
anomA['description']=''
for i in anomA.index:
    a=anomA.loc[i,'fact']/anomA.loc[i,'yhat']
    anomA['description'][i] = f'{a:.4} x veces lo esperado'
#Contador de anomalias en el tiempo Renta Acumulada
anomA_cont=anomA.ds.value_counts().resample('D').sum()
df2=pd.DataFrame()
for i in range(0,len(anomA_cont)):
    df3 =  pd.DataFrame({'Fecha':[anomA_cont.index[i]],'cont':[anomA_cont[i]]})
    df2 = df2.append(df3)
anomA_cont=df2
anomA_lastMonth = len(anomA_cont[anomA_cont["Fecha"] >= (dt.now() - pd.Timedelta(days=30))])
anomA_previousMonth = len(anomA_cont[(anomA_cont["Fecha"] >= (dt.now() - pd.Timedelta(days=60)))
                        & (anomA_cont["Fecha"] <= (dt.now() - pd.Timedelta(days=30)))])

graf1='Renta Diaria'
graf2='Renta Acumulada'
graf3='Errores encontrados'

date_format = '%d-%m-%Y'
bool_pattern = '^[0-1]$'
dv_pattern = '^([0-9]|k|K)$'

def isNaN(num):
    return num != num

def check_decimal(dec):
    try:
        Decimal(dec)
    except InvalidOperation:
        return False
    return True

def check_int(num):
    try:
        int(num)
    except ValueError:
        return False
    return True

def valid_date(date_format, val):
    if isNaN(val):
        return True
    else:
        try:
            dt.strptime(val, date_format)
            return True
        except:
            return False

def valid_bool(value):
    if isNaN(value):
        return True
    else:
        try:
            if (int(value) == 1 or int(value) == 0):
                return True
            else:
                return False
        except:
            return False

def valid_pattern(value, pattern):
    if isNaN(value):
        return True
    else:
        try:
            return bool(re.match(pattern, str(value)))
        except:
            False

decimal_validation = [CustomElementValidation(lambda d: check_decimal(d), 'is not decimal')]
int_validation = [CustomElementValidation(lambda i: check_int(i), 'is not integer')]
null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'this field cannot be null')]
bool_validation = [CustomElementValidation(lambda i: valid_bool(i),'debe ser 0 o 1')]
date_validation = [CustomElementValidation(lambda i: valid_date(date_format,i),'no calza con el patron de fecha "'+ date_format + '"')]
dv_validation = [CustomElementValidation(lambda i: valid_pattern(i,dv_pattern),
                                            'no calza con el patron de dv "'
                                            +dv_pattern+'"')]

schema = pandas_schema.Schema([
            Column('RUT', null_validation),
            Column('FECHA', date_validation),
            Column('APORTES', int_validation),
            Column('RETIROS', int_validation),
            Column('PATRIMONIO', decimal_validation),
            Column('rent_diaria', decimal_validation),
            Column('rent_acum', decimal_validation)])

errors = schema.validate(td)
errors_index_rows = [e.row for e in errors]
data_clean = td.drop(index=errors_index_rows)

all_errors=pd.DataFrame()
for i in range(0,len(errors)):
    df3 = pd.DataFrame({'column':[errors[i].column],'row':[errors[i].row],'message':[errors[i].message],'value':[errors[i].value]})
    all_errors = all_errors.append(df3)
all_errors.reset_index(inplace=True, drop =True)

validation = all_errors.groupby(['column']).count()

#start_date = new_rnt_diaria.ds.min()
#end_date=dt.now()

available_indicators = td['RUT'].unique()
