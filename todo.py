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
    data = request.get_json()
    description = data.get("description", None)
    if description is None:
        return jsonify({
            "success": False
        })
    try:
        new_todo = Todos(description=description)
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({
            'id': new_todo.id,
            'description': new_todo.description
        })
    except BaseException:
        return jsonify({
            "success": False
        })


@app.route("/todo/delete/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo_to_delete = Todos.query.filter(Todos.id == todo_id).one()
    db.session.delete(todo_to_delete)
    db.session.commit()
    return jsonify({
        "success": True
    }), 200


@app.route("/todo/update", methods=["PATCH"])
def update_todo():
    data = request.get_json()
    id_to_update = data["id"]
    new_description = data["description"]
    todo_to_update = Todos.query.filter(Todos.id == id_to_update).one()
    todo_to_update.description = new_description
    db.session.add(todo_to_update)
    db.session.commit()
    return jsonify({
        "success": True,
    })
