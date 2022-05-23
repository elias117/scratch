import json
from flask import request
from flask import Flask, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

print(__name__)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/todo"
db = SQLAlchemy(app)


class Todos(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)


db.create_all()


@app.route("/")
def index():
    return render_template('index.html', data=Todos.query.all())


@app.route("/todo/create", methods=["POST"])
def create_todo():
    description = request.form.get("description", None)
    if description is None:
        return jsonify({
            "success": False
        })
    try:
        new_todo = Todos(description=description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))
    except BaseException:
        return jsonify({
            "success": False
        })
