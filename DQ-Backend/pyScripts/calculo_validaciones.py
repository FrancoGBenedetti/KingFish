from sqlalchemy import create_engine
import pymysql
import pandas as pd
import numpy as np
from decimal import Decimal, InvalidOperation
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import CustomElementValidation

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

decimal_validation = [CustomElementValidation(lambda d: check_decimal(d), 'no es decimal')]
int_validation = [CustomElementValidation(lambda i: check_int(i), 'no es entero')]
null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'this field cannot be null')]
bool_validation = [CustomElementValidation(lambda i: valid_bool(i),'debe ser 0 o 1')]
date_validation = [CustomElementValidation(lambda i: valid_date(date_format,i),'no calza con el patrón de fecha "'+ date_format + '"')]
dv_validation = [CustomElementValidation(lambda i: valid_pattern(i,dv_pattern),
                                            'no calza con el patrón de dv "'
                                            +dv_pattern+'"')]

schema = pandas_schema.Schema([
            Column('RUT', null_validation),
            Column('FECHA', date_validation),
            Column('APORTES', int_validation),
            Column('RETIROS', int_validation),
            Column('PATRIMONIO', decimal_validation),
            Column('rent_diaria', decimal_validation),
            Column('rent_acum', decimal_validation)])

############################### Ejecución de Funciones ###################################

df = extract_db_data('fuentedatos', 'rentaclientes')
errors = schema.validate(df)
errors_index_rows = [e.row for e in errors]
data_clean = df.drop(index=errors_index_rows)
#Todos los errores detectados
allErrors=pd.DataFrame()
for i in range(0,len(errors)):
    df3 = pd.DataFrame({'columna':[errors[i].column],'fila':[errors[i].row],'mensaje':[errors[i].message],'valor':[errors[i].value]})
    allErrors = allErrors.append(df3)
allErrors.reset_index(inplace=True, drop =True)

validation = allErrors.groupby(['columna']).count()
#Todos los RUT disponibles
available_indicators = df['RUT'].unique()

#Se insertan las validaciones a la Base de datos
df2mysql(allErrors,'validaciones','calculos')
