import re
from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/bilgi/OneDrive/Masaüstü/Todo/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        todo = Todo(title=title, content=content, complete=False)

        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("index"))

    else:
        return redirect(url_for("index"))

@app.route("/complete/<int:id>")
def complete(id):
        todo = Todo.query.filter_by(id=id).first()
        if todo == None:
            return redirect(url_for("index"))
        
        if todo.complete == False:
            todo.complete = True
        else:
            todo.complete = False

        db.session.commit()
        return redirect(url_for("index"))

@app.route("/remove/<int:id>")
def remove(id):
        todo = Todo.query.filter_by(id=id).first()
        if todo == None:
            return redirect(url_for("index"))
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/detail/<int:id>")
def detail(id):
        todo = Todo.query.filter_by(id=id).first()
        if todo == None:
            return redirect(url_for("index"))
        return render_template("detail.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True)