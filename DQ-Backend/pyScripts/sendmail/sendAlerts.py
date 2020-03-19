import pandas as pd
import configparser
import os
import ../db_access as db

######################
######################
### Configurations ###
######################
######################
CONFIG_FILE = '../../API/logs/config.ini'
config = configparser.ConfigParser(allow_no_value=True)
config.read(CONFIG_FILE)

anomD = db.extract_db_data('calculos', 'anomalias_renta_diaria') #Anomalías renta diaria

mails=['ldavid@miuandes.cl']
modulo = ['Detección de Anomalías','Validaciones']

css = """<head>
<style>
#tablita {
    font-family: "Calibri", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

#tablita td, #tablita th {
    border: 1px solid #ddd;
    padding: 8px;
}


#tablita tr:hover {background-color: #ddd;}

#tablita th {
    padding-top: 11px;
    padding-bottom: 11px;
    text-align: left;
    background-color: #608dd6;
    color: white;
}
</style>
</head>"""

def diferencias(df,df1):
    # Retorna un DataFrame en donde se encontró diferencias y un boolean, False: sin diferecnias, True: con diferencias
    dfs_dictionary = {'DF':df,'DF1':df1}
    dff=pd.concat(dfs_dictionary)
    dff=dff.drop_duplicates(keep=False)
    if len(dff)==0:
        return dff, False
    else:
        DF2=dff.loc[dff.index.levels[0][1]]
    return DF2, True

def makeEmail(email, modulo, df):
    msj = f"""<h4><span style="color:red">{len(df)}</span> Inconsistencias encontradas en {modulo}</h6>"""
    pre_html=f"""Cc: {email}
        Subject: HTML email
        Content-Type: text/html; charset="utf8"
        Content-Disposition: inline
        """
    html=df.to_html(classes='table table-hover', table_id='tablita')
    with open('out.html', 'w') as f:
        print(pre_html+css+msj+html, file=f)

def sendAlert():
    cmd='date'
    command=f'echo "Subject: Test format";echo -e "MIME-Version: 1.0\nContent-Type: text/html;\n" | sendmail -vt {mails[0]}  < ./out.html'
    os.system(command)

def new_anomalies(df, df1):
    anomNew, diff = diferencias(df, df1)
    if diff:
        makeEmail(mails[0], modulo[0], anomNew)
        sendAlert(anomNew)
