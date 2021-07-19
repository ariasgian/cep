# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import Form, validators, RadioField, SelectField, SubmitField,StringField
from wtforms.validators import DataRequired
import cargar_datos
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

class InfoForm(FlaskForm):
    terminaL_cpk = RadioField('r', choices=[])
    Submit = SubmitField('Seleccionar')
    

#%%

graf, data= cargar_datos.crear_grafica()
tamano= len(data)
#%%
@app.route('/', methods=("POST", "GET"))
def images():
    #matriz= {'terminal': ['abc', 'cde'], 'cpk': [1, 2]}
    graf, data= cargar_datos.crear_grafica()
    
    #data = pd.DataFrame(matriz)
    tamano= len(data)
    form = InfoForm()
    if request.method =='GET':
        return render_template('test.html',tables= data, tam=tamano, form= form)
    if request.method =='POST':
        abc= request.form.get('terminal')
        print(abc)
        print('OK')
        return abc
    #return render_template('test.html', graphJSON=graphJSON)
     
@app.route('/test')   
def test():
    matriz= {'terminal': ['abc', 'cde'], 'cpk': [1, 2]}
    data = pd.DataFrame(matriz)
    for item in data:
        print(item)
    return 'observa la consola'

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = InfoForm()
    if form.validate_on_submit():
        print('ok')
    


if __name__ == '__main__':
    app.run(port='8050', host='0.0.0.0',debug=True)