from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/scratch"
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)


@app.route("/")
def index():
    person = Person.query.filter(Person.name.ilike("{}".format("Elias"))).first()
    return "Hello {}!".format(person.name)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
