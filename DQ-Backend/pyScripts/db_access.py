from sqlalchemy import create_engine
import pymysql
import pandas as pd

#Extraer Fuente de datos de Base de datos a un DataFrame
def extract_db_data(db, table):
    sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    frame = pd.read_sql(f"select * from {db}.{table}", dbConnection);
    pd.set_option('display.expand_frame_repr', False)
    dbConnection.close()
    return frame

#Insertar DataFrame a Base de datos
def df2mysql(df,tableName,db):
    sqlEngine = create_engine(f'mysql+pymysql://root:@127.0.0.1/{db}', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    df.to_sql(name=tableName, con=dbConnection, if_exists='replace',
              index=False)
    dbConnection.close()

def df2mysql_2(df,tableName,db):
    df_db=extract_db_data(db, tableName)
    # Se obtiene la diferencia entre la tabla a insertar y la ya existente en la BD
    try:
        df_to_append, df_bool = diferencias(df, df_db)
    except:
        print('HOLA HOLA HOLA HOLA')
        df_bool=False
    if df_bool:
        print('ALO ALO ALO ALO ALO')
        sqlEngine = create_engine(f'mysql+pymysql://root:@127.0.0.1/{db}', pool_recycle=3600)
        dbConnection = sqlEngine.connect()
        df_to_append.to_sql(name=tableName, con=dbConnection, if_exists='append',
                  index=False)
        dbConnection.close()

# Retorna un DataFrame en donde se encontró diferencias y un boolean, False: sin diferecnias, True: con diferencias
def diferencias(df,df1):
    dfs_dictionary = {'DF':df,'DF1':df1}
    dff=pd.concat(dfs_dictionary)
    dff=dff.drop_duplicates(keep=False)
    if len(dff)==0:
        return dff, False
    else:
        DF2=dff.loc[dff.index.levels[0][1]]
    return DF2, True
