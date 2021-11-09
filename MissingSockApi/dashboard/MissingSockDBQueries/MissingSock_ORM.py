from os import truncate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)

class Base_station(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sync_base_id = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255), nullable=True)

class Tag(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sync_tag_id = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255), nullable=True)

class Asset_registry(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)	
    tag_id = db.Column(db.Integer, nullable=True)
    asset_number = db.Column(db.String(255), nullable=True)	
    group_number = db.Column(db.String(255), nullable=True)	
    date_of_birth = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Gender = db.Column(db.String(255), nullable=True)	
    breed_type = db.Column(db.String(255), nullable=True)
    farther_id = db.Column(db.Integer, nullable=True)
    farther_note = db.Column(db.String(255), nullable=True)
    mother_id = db.Column(db.Integer, nullable=True)
    mother_note = db.Column(db.String(255), nullable=True)
    users_id = db.Column(db.Integer, primary_key=True)

    def get_id(self):
        return self.id

class Asset_medical(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)	
    asset_registry_id = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Reason = db.Column(db.String(255), nullable=True)	
    Medicine = db.Column(db.String(255), nullable=True)
    Dosage = db.Column(db.Float	, nullable=True)
    Note = db.Column(db.String(255), nullable=True)

class Asset_breeding(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)	
    asset_registry_id = db.Column(db.String(255), nullable=False)
    breeding_number = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    twin_number	= db.Column(db.String(255), nullable=True)
    pregnant = db.Column(db.Integer, nullable=True)