from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_tutor = db.Column(db.String(100), nullable=False)
    pets = db.relationship('Pet', backref='tutor', lazy=True)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_pet = db.Column(db.String(100), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)


class TutorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'pets')

class PetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'tutor_id')