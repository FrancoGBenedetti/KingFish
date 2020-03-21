import pandas as pd
import numpy as np
from sqlalchemy import create_engine

df = pd.read_csv('../../todos_3.csv',sep=',')
df['FECHA'] = pd.to_datetime(df.FECHA)

df1=df.copy()
df1.loc[df1.index==5,'RUT']='bbb'
df1.loc[df1.index==800,'rent_diaria']=0.5310
df1.loc[df1.index==555,'rent_diaria']=0.654
df1=df1.iloc[:2000]

def df2mysql(df,tableName,db):
    sqlEngine = create_engine(f'mysql+pymysql://root:@127.0.0.1/{db}', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    df.to_sql(name=tableName, con=dbConnection, if_exists='replace',
              index=False)
    dbConnection.close()

df2mysql(df,'rentaclientes','fuentedatos')
df2mysql(df1,'rentaclientes2','fuentedatos')
