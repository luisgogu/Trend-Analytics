from flask import Flask
from flask import request
import json as js
import pandas as pd
import numpy as np
from Query import Answer_Query_Alg1
from Query import Answer_Query_Alg2

app = Flask(__name__)

json = {}

@app.route("/date/", methods = ['POST'])
def date():
    open('query.json', 'w').close()
    data = request.get_json(force=True)
    json.update(data)
    with open('query.json', 'w') as f:
        js.dump(json, f)
    return json

@app.route("/prod/", methods = ['POST'])
def prod():
    data = request.get_json(force=True)

    #write
    json.update(data)
    with open('query.json', 'w') as f:
        js.dump(json, f)

    #read
    with open('query.json', 'r') as f:
        data = js.load(f)

    #result = foo(data)

    print(data["from"])
    r = Answer_Query_Alg1(data)

    open('query.json', 'w').close()

    with open('data.json', 'w') as f:
        js.dump(r.ranking, f)

    return json

@app.route("/prodfeatures/", methods = ['POST'])
def prodfeatures():
    open('query_features.json', 'w').close()
    data = request.get_json(force=True)
    #write
    with open('query_features.json', 'w') as f:
        js.dump(data, f)

    return json

@app.route("/features/", methods = ['POST'])
def features():
    data = pd.json_normalize(request.get_json(force=True))
    product = str(pd.read_json('query_features.json',typ = 'series')[0])
    feature = str(data['feature'][0])
    #r = foo(product,feature)
    print(product,feature)
    r = Answer_Query_Alg2({"feature":feature, "product":[product]})
    # dict = pd.read_json('result.json')
    # df = pd.json_normalize(dict["product"])
    # result = js.dumps({"Feature": df[feature].to_list()},indent=4)
    # #print(result)
    # #write
    with open('feature_list.json', 'w') as f:
        js.dump(r.dic, f)

    return json


app.run(port = 5000)


# consulta producto - resultado escrito en un json
# en react desde el codigo leer el archivo json
# filtar en la web sin enviar cconsulta, filtrar segun selected options en el click
# el resultado final modifica/crea un nuevo json 