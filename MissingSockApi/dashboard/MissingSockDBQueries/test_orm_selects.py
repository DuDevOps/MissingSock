from flask import  Flask, render_template, request, url_for, redirect, flash, jsonify
# from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from  werkzeug.security import generate_password_hash, check_password_hash

import mysql
import pymysql

from datetime import datetime, timedelta, date

import json

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

# from MissingSockDBQueries import MissingSockDb
from MissingSock_ORM import sql_result_to_dict, Users, Asset_registry, Asset_medical, Asset_breeding

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

if __name__ == "__main__":
    current_user = Users.query.filter_by(email="koosbilly9@gmail.com").first()

    asset_result = Asset_registry.query.join(Asset_medical)\
        .filter(Asset_registry.users_id==current_user.id).all()

    asset_result = Asset_registry.query.join(Asset_medical).join(Asset_breeding)\
        .filter(Asset_registry.users_id==current_user.id).all()
    
    print(f"{asset_result}")

    asset_result[0]
    
    asset_result[0].__dict__

