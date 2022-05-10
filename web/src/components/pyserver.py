from flask import Flask
from flask import request
import json as js
app = Flask(__name__)

json = {}
@app.route("/prod/", methods = ['POST'])
def prod():
    data = request.get_json(force=True)
    #print(data)
    json.update(data)
    with open('query.json', 'w') as f:
        js.dump(json, f)
    return json

@app.route("/date/", methods = ['POST'])
def date():
    data = request.get_json(force=True)
    #print(data)
    json.update(data)
    with open('query.json', 'w') as f:
        js.dump(json, f)
    return json


app.run(port = 5000)






# d = {'from': ['2022-04-12']}
# d.update({'to': ['2022-04-29']})
# d