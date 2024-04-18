from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))

class Priorauth(db.Model):
    memberID = db.Column(db.Integer, primary_key=True)
    memberName = db.Column(db.String(255))  # New column 'memberName'
    payor = db.Column(db.String(100))
    ICDCode = db.Column(db.Text)
    procedureCode = db.Column(db.String(100))
    priorAuthStatus  = db.Column(db.String(100))






   


