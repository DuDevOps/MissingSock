import json
from os import truncate
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

from datetime import datetime

app = Flask(__name__)

host="192.168.0.109"
user="iodynami_script1"
password="koosK##S"
db="missingsock"

app.config['SECRET_KEY'] = 'secret-key-goes-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{db}'

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
    __tablename__ = 'asset_registry'

    id = db.Column(db.Integer, primary_key=True)	
    tag_id = db.Column(db.Integer, nullable=True)
    asset_type = db.Column(db.String(255), nullable=True)
    asset_number = db.Column(db.String(255), nullable=True)	
    group_number = db.Column(db.String(255), nullable=True)	
    date_of_birth = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    gender = db.Column(db.String(255), nullable=True)	
    breed_type = db.Column(db.String(255), nullable=True)
    father_id = db.Column(db.Integer, nullable=True)
    father_note = db.Column(db.String(255), nullable=True)
    mother_id = db.Column(db.Integer, nullable=True)
    mother_note = db.Column(db.String(255), nullable=True)
    users_id = db.Column(db.Integer, primary_key=True)

class Asset_medical(UserMixin, db.Model):
    __tablename__ = 'asset_medical'

    id = db.Column(db.Integer, primary_key=True)	
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reason = db.Column(db.String(255), nullable=True)	
    medicine = db.Column(db.String(255), nullable=True)
    dosage = db.Column(db.Float	, nullable=True)
    note = db.Column(db.String(255), nullable=True)
    asset_registry_id = db.Column(db.Integer,  nullable=False)


class Asset_breeding(UserMixin, db.Model):
    __tablename__ = 'asset_breeding'

    id = db.Column(db.Integer, primary_key=True)	
    breeding_number = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    twin_number	= db.Column(db.String(255), nullable=True)
    pregnant = db.Column(db.Integer, nullable=True)
    asset_registry_father_id = db.Column(db.Integer, nullable=True)
    asset_registry_mother_id = db.Column(db.Integer, nullable=True)

class Asset_offspring(UserMixin, db.Model):
    __tablename__ = 'asset_offspring'

    id = db.Column(db.Integer, primary_key=True)	
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    asset_father_id = db.Column(db.Integer, nullable=True)
    asset_mother_id = db.Column(db.Integer, nullable=True)
    asset_offspring_id = db.Column(db.Integer, nullable=True)
    asset_breeding_id = db.Column(db.Integer, nullable=True)
    

def sql_result_to_json(sql_result):
    result = [
           row2dict(report)
           for report in sql_result
    ]

    result_json = json.dumps(result)

    return result_json

def sql_result_to_dict(sql_result):
    result = [
           row2dict(row)
           for row in sql_result
    ]

    return result

def row2dict(row):
    return {
        # cuts out foreignkey
        c.name: str(getattr(row, c.name))
        for c in row.__table__.columns
    }