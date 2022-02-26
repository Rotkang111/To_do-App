from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# find current app path where db is to be stored on os
# directory where DB is to be stored
project_dir = os.path.dirname(os.path.abspath(__file__))

# create database file
database_file = f'sqlite:///{os.path.join(project_dir, "todo.db")}'

# Conneccting database_file(todo.db) to SQLAlchemy dependencies
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    todo_item = db.Column(db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return f'{self.todo_item}'


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.form:
        new_item = request.form.get('new_todo')

        todo = Todo(todo_item=new_item)
        db.session.add(todo)
        db.session.commit()
    todos = Todo.query.all()

    # REVERSE THE LIST FOR LAST ITEMS TO SHOW ON THE TOP AND FIRST ITEM TO SHOW AT THE BOTTOM
    # reveresed_list = todos[::-1]
    reveresed_list = reversed(todos)

    return render_template("index.html", todos=reveresed_list)


@app.route('/delete/<todo_item>')
def delete(todo_item):
    todo_data.remove(todo_item)

    return redirect(url_for("index"))


# renders page to update
@app.route('/update/<todo_item>', methods=['GET', 'POST'])
def update(todo_item):

    # render and take todo_item
    return render_template('update.html', todo_item=todo_item)


"""
@app.route('/update_item', methods=['POST'])  #performs the update function
def update_item():
    if request.method == 'POST':
        new_item = request.form.get('new_item')  #get that particular item u just updated from the form


    return redirect(url_for('index')) # redirect to index page
"""

if __name__ == "__main__":
    app.run(debug=True)
