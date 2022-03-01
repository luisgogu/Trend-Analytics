from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html', list_of_names=['chris', '🚀', 'pizza'])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/authors')
def authors():
    s = "<h1>AUTHORS 🚀</h1>" + "<br> PEPE <br> PEPA <br> PEPO"
    return s

@app.route('/<string:name>')
def greet(name):
    return f'Hello {name}, WELCOME'

if __name__ == '__main__':
    app.run(debug=True)