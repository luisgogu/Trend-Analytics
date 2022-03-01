from flask import Flask, render_template, request, redirect, url_for
from forms import Todo
app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'

@app.route("/", methods=['GET', 'POST'])
def hello_world():

    request_method = request.method
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        print("---------------")
        print(request.form)
        print("---------------")
        return redirect(url_for('name', first_name=first_name, last_name=last_name))
    return render_template("hello.html", request_method=request_method)
@app.route("/name/<string:first_name>/<string:last_name>")
def name(first_name, last_name):
    return f"Welcome {first_name} {last_name}! The web is in progress..."

@app.route("/todo", methods=['GET'])
def todo():
    todo_form = Todo()
    return render_template('todo.html', form=todo_form)
    

if __name__ == '__main__':
    app.run(debug=True)

