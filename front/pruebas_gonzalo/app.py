from flask import Flask, render_template, request, redirect, url_for
from forms import Todo
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(240))

    def __str__(self):
        return f'{self.content, {self.id}}'

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

@app.route("/todo", methods=['GET', 'POST'])
def todo():
    todo_form = Todo()
    if todo_form.validate_on_submit():
        print(todo_form.content.data)
        return redirect('/')
    return render_template('todo.html', form=todo_form)
    

if __name__ == '__main__':
    app.run(debug=True)

