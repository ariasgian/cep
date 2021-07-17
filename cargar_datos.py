#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 20:54:09 2021

@author: gian
"""
import csv
import psycopg2
import pandas as pd
import datetime as dt
#import carga_bd 
import manufacturing as manu
import plotly.express as px
#import plotly
import  numpy as np

def conectar():
    ip= 'localhost'
    conn = psycopg2.connect(database="corte", user = "lear", password = "1234", host = ip, port = "5432")
    cur = conn.cursor()
    return cur, conn

def crear_data():
    cur,conn=conectar()
    sql= "select * from altura"
    cur.execute(sql,)
    data = cur.fetchall()
    cur.execute(sql,(data[0][3],))
    cable = cur.fetchall()
    seccion= cable[0][1]
    terminal = data[0][4]
    id_= str(seccion) + '_' + terminal
    sql= "select * from validacion where id= %s"
    cur.execute(sql,(id_,))
    #validacion= cable = cur.fetchall()
    alturas = pd.read_sql("select * from altura where tipo = 'MEASUREMENT_DATA_CH_2'", conn)
    cables=pd.read_sql("select * from cable", conn)
    validaciones= pd.read_sql("select * from validacion", conn)
    conn.close()
    prueba=pd.merge(
    alturas,
    cables, 
    left_on='cable', 
    right_on='pn', 
    how = "inner").drop('pn', axis=1)

    prueba['id_']= prueba['seccion'].astype(str) + '_'+ prueba['terminal']

    tabla=prueba.merge(
        validaciones, 
        left_on='id_',
        right_on='id',
        suffixes=('_left', '_right')
    ).drop(['id_right',  'terminal_right', 'seccion_right', 'ich'], axis=1)
    terminales= tabla['id_'].unique()
    return tabla, terminales

def test_cpk(terminal_seccion):
    data, terminales= crear_data()
    terminal= terminal_seccion
    test= data.loc[data.id_==terminal]
    return test

def cargar_validacion():
    tabla= pd.DataFrame(columns=['id', 'terminal', 'seccion', 'cch', 'ich'])
    cur,conn = conectar()
    sql="Insert into validacion(id, terminal, seccion, cch, ich) values(%s,%s,%s,%s,%s)"
    archivo = open('validacion.csv', 'r')
    data1 = csv.reader(archivo)
    next(data1, None)
    for linea in data1:
        terminal= linea[0]
        seccion = linea[1]
        conductor = linea[2]
        id_= seccion+'_'+ terminal      
        try: 
            float(linea[3])          
            aislante = linea[3]
        except:
 
            aislante=0
        cur.execute(sql,(id_, terminal, seccion, conductor, aislante))  
        tabla= tabla.append({'id': id_, 'terminal':terminal, 'seccion':seccion, 'cch': conductor, 'ich': aislante}, ignore_index=True)
    conn.commit()
    conn.close()
    return tabla

def cargar_cable():
    cur,conn = conectar()
    sql="Insert into cable(pn, seccion) values(%s,%s)"
    archivo = open('cable.csv', 'r')
    data1 = csv.reader(archivo)
    next(data1, None)
    for linea in data1:
        pn = linea[0]
        seccion = linea[1] 
        cur.execute(sql,(pn, seccion))           
    conn.commit()
    conn.close()

def cargar():
    cur,conn = conectar()
    sql="Insert into altura(maquina, tipo, cable, terminal, altura, fecha) values(%s,%s,%s,%s,%s,%s)"
    archivo = open('altura2.csv', 'r')
    data = csv.reader(archivo, skipinitialspace=True)
    for linea in data:
        if linea[4] == 'TRUE':
            maquina = linea[0]
            tipo = linea[1]
            cable = linea[2]
            terminal = linea[3]
            altura = linea[5]
            fecha = dt.datetime.strptime(linea[6], '%Y-%m-%d %H:%M:%S.%f')
            cur.execute(sql,(maquina, tipo, cable,terminal, altura, fecha))
    conn.commit()
    conn.close()

def alturas_conductor():
    cur,conn = conectar()
    sql = "select id, cable,terminal, altura from public.altura where tipo= 'MEASUREMENT_DATA_IH_2'"
    cur.execute(sql,)
    data = cur.fetchall()
    conn.close()
    return data

def graficar_2(terminal,data,cpk, tamaño):
    data.reset_index(drop=True, inplace=True)
    titulo= terminal+ ' CPK= '+ str(cpk)+ ' N ='+ str(tamaño)
    fig = px.line(data, 
                  x=data.index, 
                  y="altura", 
                  title=titulo,
                  )
    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.add_hline(y=data['cch'].mean()+0.05)
    fig.add_hline(y=data['cch'].mean()-0.05)
    fig.add_hline(y=data['cch'].mean())
    return fig 

def crear_grafica():
    graf=''
    data, terminales= crear_data()
    tabla= pd.DataFrame(columns=['terminal', 'cpk', 'muestras'])
    for terminal in terminales:
        test= data.loc[data.id_==terminal]
        cch=test['cch'].mean()
        liminferior=cch - 0.05
        limsuperior = cch + 0.05
        tamaño=len(test['altura'])
        if tamaño>7:
            cpk= manu.calc_ppk(test['altura'], limsuperior, liminferior)
            cpk = round(cpk,2)
            graf= graficar_2(terminal,test,cpk, tamaño)
        else:
            cpk=np.NaN
        tabla= tabla.append({'terminal': terminal, 'cpk':cpk, 'muestras':tamaño}, ignore_index=True)
    tabla.sort_values(by=['muestras'], inplace=True, ascending=False)
    tabla.reset_index(drop=True, inplace=True)    
    return graf, tabla