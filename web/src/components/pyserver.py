from flask import Flask
from flask import request
import json as js
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
    print(data)
    open('query.json', 'w').close()
    #del data
    return json

@app.route("/features/", methods = ['POST'])
def features():
    open('query.json', 'w').close()
    data = request.get_json(force=True)
    #write
    with open('query.json', 'w') as f:
        js.dump(data, f)

    #result = foo(data)
    print(data)
    open('query.json', 'w').close()
    return json

app.run(port = 5000)