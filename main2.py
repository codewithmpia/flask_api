from pathlib import Path

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from flask_cors import CORS


BASE_DIR = Path(__file__).resolve().parent


app = Flask(__name__, instance_path=BASE_DIR)
app.config["SECRET_KEY"] = "top-secret"

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///db.sqlite3"
db = SQLAlchemy(app)

# Flask-Restfull
api = Api(app)

# Serialization
ma = Marshmallow(app)

# Cors
#cors = CORS(app)

# On autorise toutes les requetes commençant par /persons/---
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


class PersonListApiView(Resource):
    # Get all persons
    def get(self):
        """
        import requests

        def send_request():
            # all_persons
            # GET http://127.0.0.1:5000/persons/

            try:
                response = requests.get(
                    url="http://127.0.0.1:5000/persons/",
                )
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                print('Response HTTP Response Body: {content}'.format(
                    content=response.content))
            except requests.exceptions.RequestException:
                print('HTTP Request failed')
        """
        persons = Person.query.all()
        return persons_schema.dump(persons), 200
    
    # Add person
    def post(self):
        """
        # Install the Python Requests library:
        # `pip install requests`

        import requests
        import json

        def send_request():
            # add_person
            # POST http://127.0.0.1:5000/persons/

            try:
                response = requests.post(
                    url="http://127.0.0.1:5000/persons/",
                    headers={
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=json.dumps({
                        "gender": "Female",
                        "phone": "00000000000",
                        "city": "Paris",
                        "country": "France",
                        "last_name": "Puludisu",
                        "email": "stella@g.com",
                        "country_code": "FR",
                        "first_name": "Stella"
                    })
                )
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                print('Response HTTP Response Body: {content}'.format(
                    content=response.content))
            except requests.exceptions.RequestException:
                print('HTTP Request failed')      
        """
        data = request.get_json()
        new_person = Person(
            first_name=data["first_name"],
            last_name=data["last_name"],
            gender=data["gender"],
            email=data["email"],
            phone=data["phone"],
            city=data["city"],
            country=data["country"],
            country_code=data["country_code"]
        )
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dumps(new_person), 200
    

class PersonApiView(Resource):
    # Get one person
    def get(self, person_id):
        """
        import requests

        def send_request():
            # one_person
            # GET http://127.0.0.1:5000/persons/1002

            try:
                response = requests.get(
                    url="http://127.0.0.1:5000/persons/1002",
                )
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                print('Response HTTP Response Body: {content}'.format(
                    content=response.content))
            except requests.exceptions.RequestException:
                print('HTTP Request failed')
        """
        person = Person.query.get_or_404(person_id)
        return person_schema.dump(person), 200
    
    # Edit person
    def patch(self, person_id):
        """
        import requests
        import json

        def send_request():
            # edit_person
            # PATCH http://127.0.0.1:5000/persons/1002

            try:
                response = requests.patch(
                    url="http://127.0.0.1:5000/persons/1002",
                    headers={
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=json.dumps({
                        "gender": "Female",
                        "phone": "00000000001",
                        "city": "Paris",
                        "country": "France",
                        "last_name": "Puludisu",
                        "email": "stella@g.com",
                        "country_code": "FR",
                        "first_name": "Tella"
                    })
                )
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                print('Response HTTP Response Body: {content}'.format(
                    content=response.content))
            except requests.exceptions.RequestException:
                print('HTTP Request failed')
        """
        person = Person.query.get_or_404(person_id)
        data = request.get_json()
        if data != None:
            person.first_name=data["first_name"]
            person.last_name=data["last_name"]
            person.gender=data["gender"]
            person.email=data["email"]
            person.phone=data["phone"]
            person.city=data["city"]
            person.country=data["country"]
            person.country_code=data["country_code"]
        db.session.commit()
        return person_schema.dump(person), 200
    
    # Delete person
    def delete(self, person_id):
        """
        import requests

        def send_request():
            # delete_person
            # DELETE http://127.0.0.1:5000/persons/100

            try:
                response = requests.delete(
                    url="http://127.0.0.1:5000/persons/100",
                )
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                print('Response HTTP Response Body: {content}'.format(
                    content=response.content))
            except requests.exceptions.RequestException:
                print('HTTP Request failed')
        """
        person = Person.query.get_or_404(person_id)
        db.session.delete(person)
        db.session.commit()
        return "Person has been successfully deleted", 204
    

api.add_resource(PersonListApiView, "/persons")
api.add_resource(PersonApiView, "/persons/<int:person_id>")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)