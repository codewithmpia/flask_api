from pathlib import Path

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


BASE_DIR = Path(__file__).resolve().parent


app = Flask(__name__, instance_path=BASE_DIR)
app.config["SECRET_KEY"] = "top-secret"

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///db.sqlite3"
db = SQLAlchemy(app)

# Marshmallow
ma = Marshmallow(app)

# Cors
#cors = CORS(app)

# On autorise tous les urls commençant par /persons/---
cors = CORS(app, resources={r"/persons/*": {"origins": "*"}})

class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer(), primary_key=True)
    first_name= db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(20), nullable=False)

    def __str__(self):
        return self.first_name
    

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person

persons_schema = PersonSchema(many=True)
person_schema = PersonSchema()


@app.route("/")
@app.route("/persons/")
def person_list():
    persons = Person.query.all()
    return persons_schema.dumps(persons), 200


@app.route("/persons/<int:person_id>/")
def person_detail(person_id):
    person = Person.query.get_or_404(person_id)
    return person_schema.dump(person), 200


@app.route("/persons/add/", methods=("GET", "POST"))
def add_person():
    if request.method == "POST":
        data = request.get_json()

        new_person = Person(
            first_name = data["first_name"],
            last_name = data["last_name"],
            gender = data["gender"],
            email = data["email"],
            phone = data["phone"],
            city = data["city"],
            country = data["country"],
            country_code = data["country_code"]
        )
        db.session.add(new_person)
        db.session.commit()

        return jsonify({"message": "success"}), 200
    else:
        pass
    return jsonify({"message": "success"}), 200


# JSON data
@app.route("/persons/edit/<int:person_id>/", methods=("GET", "POST"))
def edit_person(person_id):
    person = Person.query.get_or_404(person_id)
    
    if request.method == "POST":
        data = request.get_json()

        person.first_name = data["first_name"]
        person.last_name = data["last_name"]
        person.gender = data["gender"]
        person.email = data["email"]
        person.phone = data["phone"]
        person.city = data["city"]
        person.country = data["country"]
        person.country_code = data["country_code"]

        db.session.commit()

        return jsonify({"message": "success"}), 200
    
    else:
        pass
    
    return jsonify({"message": "success"}), 200


@app.route("/persons/delete/<int:person_id>/")
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "success"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)