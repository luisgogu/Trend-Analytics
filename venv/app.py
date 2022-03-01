from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>TRACK-TREND</h1>"

if __name__ == '__main__':
    app.run(debug=True)