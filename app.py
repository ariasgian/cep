# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
from flask import Flask, render_template
import cargar_datos


import pandas as pd
app = Flask(__name__)

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
    return render_template('test.html',tables= data, tam=tamano)
    #return render_template('test.html', graphJSON=graphJSON)
     
@app.route('/test')   

def test():
    matriz= {'terminal': ['abc', 'cde'], 'cpk': [1, 2]}
    data = pd.DataFrame(matriz)
    for item in data:
        print(item)
    return 'observa la consola'
if __name__ == '__main__':
    app.run(port='8050', host='0.0.0.0',debug=True)