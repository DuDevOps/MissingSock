from flask import  Flask, render_template, request, url_for, redirect, flash, jsonify
# from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from  werkzeug.security import generate_password_hash, check_password_hash

import mysql
import pymysql

from datetime import datetime, timedelta, date

import json

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from MissingSockDBQueries import MissingSockDb
from MissingSockDBQueries.MissingSock_ORM import sql_result_to_dict, Users, Asset_registry, \
    Asset_medical, Asset_breeding, Asset_offspring

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

# CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# class Users(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), unique=True, nullable=False)


def get_base_stations():
    base_station_current = MissingSockDb.get_base_station()
    count = len(base_station_current)

    # find middle point of base stations
    long_list = []
    lat_list = []
    
    for station in base_station_current:
        lat_list.append(station['gps_lat'])
        long_list.append(station['gps_long'])
       
        station["href_open_street_map"] = f"https://www.openstreetmap.org/?mlat={station['gps_lat']}&mlon={station['gps_long']}#map=12/{station['gps_lat']}/{station['gps_long']}"
       
    
    lat_list.sort()
    long_list.sort()

    lat_middle = round(((float(lat_list[0]) + float(lat_list[len(lat_list)-1])) / 2),6)
    long_middle = round(((float(long_list[0]) + float(long_list[len(long_list)-1])) / 2),6)

    # href_open_street_map=f"https://www.openstreetmap.org/?mlat={base['GPS_lat']}&mlon={base['GPS_long']}#map=12/{base['GPS_lat']}/{base['GPS_long']}"

       # load up for javascript in JSON format
    # JSON.dumps convert dict to string
    loadJson = f'"base_stations" : {json.dumps(base_station_current)} ,'
    loadJson += '"middle_point": {' + f'"lat":"{str(lat_middle)}", "long":"{str(long_middle)}" ' + '}'

    return loadJson

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated)

@app.route("/login", methods=["GET","POST"]) 
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = Users.query.filter_by(email=email).first()
        
        #Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return render_template("index.html", loadHtml="login", logged_in=current_user.is_authenticated)
        
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return render_template("index.html", loadHtml="login", logged_in=current_user.is_authenticated)
        
        else:
            login_user(user)
            return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated)
        
    return render_template("index.html", loadHtml="login", logged_in=current_user.is_authenticated)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        
        if Users.query.filter_by(email=request.form.get('email')).first():
            #User already exists
            flash("Email is already registered, please log in")
            
            return render_template("index.html", loadHtml="login", logged_in=current_user.is_authenticated)
        
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = Users(
            email=request.form.get('email'),
            password=hash_and_salted_password
        )
        
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        
        flash(f"New user created for {request.form.get('email')}")
        return render_template("index.html", loadHtml="home")

    return render_template("index.html", loadHtml="register", logged_in=current_user.is_authenticated)

@app.route("/rep_animal_register", methods=["GET","POST"]) 
@login_required
def rep_animal_register():
    if request.method == "POST":
        pass
    
    #get List of assets for current user
   
    asset_result = Asset_registry.query.filter_by(users_id=current_user.id).all()
    
    #Change to dict
    asset_dict = sql_result_to_dict(asset_result)
    #     for breed_rec in row.asset_breeding:
    #         new_breed_rec = breed_rec.__dict__
    #         new_breed_rec['timestamp'] = breed_rec.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    #         list_breed_rec.append(new_breed_rec)
            
        
    #     # add join col:val list to row dict
    #     asset_record['asset_breeding'] = list_breed_rec

    #     asset_dict.append(asset_record)

 

    # add  age Years / months
    for record in asset_dict :
        birth = datetime.strptime(record['date_of_birth'],'%Y-%m-%d %H:%M:%S')
        # birth = record['date_of_birth']
        now = date.today()
        record['age_year'] = now.year - birth.year
        record['age_month'] = now.month - birth.month  
        record['birth_year'] = birth.year
        record['birth_month'] = birth.month

        # get medical record
        asset_medical_result = Asset_medical.query.filter(Asset_medical.asset_registry_id == record['id']).all()
        asset_medical_dict = sql_result_to_dict(asset_medical_result)

        record['asset_medical'] = asset_medical_dict

        # get Breeding info
        asset_breeding_result = Asset_breeding.query.\
            filter(or_(Asset_breeding.asset_registry_father_id == record['id'], Asset_breeding.asset_registry_mother_id == record['id']) ).all()
        asset_breeding_dict = sql_result_to_dict(asset_breeding_result)

        # # get breeding detail
        for breed in asset_breeding_dict:
            father_detail_list = []

            father_detail = Asset_registry.query.filter(Asset_registry.id == breed['asset_registry_father_id']).all()
            father_detail_dict = sql_result_to_dict(father_detail)
            father_detail_list.append(father_detail_dict[0])
            breed['father_detail'] = father_detail_list

            mother_detail_list = []

            mother_detail = Asset_registry.query.filter(Asset_registry.id == breed['asset_registry_mother_id']).all()
            mother_detail_dict = sql_result_to_dict(mother_detail)
            mother_detail_list.append(mother_detail_dict[0])
            breed['mother_detail'] = mother_detail_list
            

        record['asset_breeding'] = asset_breeding_dict

        # get offspring info
        asset_offspring_result = Asset_offspring.query.\
            filter(or_(Asset_offspring.asset_father_id == record['id'], Asset_offspring.asset_mother_id == record['id']) ).all()
        asset_offspring_dict = sql_result_to_dict(asset_offspring_result)

        

        # # get offspring detail
        for rec in asset_offspring_dict:
            offspring_detail_list = []

            off_asset_result = Asset_registry.query.filter(Asset_registry.id == rec['asset_offspring_id']).all()
            off_asset_dict = sql_result_to_dict(off_asset_result)
            offspring_detail_list.append(off_asset_dict[0])
            rec['offspring_detail'] = offspring_detail_list

            father_detail_list = []

            father_detail = Asset_registry.query.filter(Asset_registry.id == rec['asset_father_id']).all()
            father_detail_dict = sql_result_to_dict(father_detail)
            father_detail_list.append(father_detail_dict[0])
            rec['father_detail'] = father_detail_list

            mother_detail_list = []

            mother_detail = Asset_registry.query.filter(Asset_registry.id == rec['asset_mother_id']).all()
            mother_detail_dict = sql_result_to_dict(mother_detail)
            mother_detail_list.append(mother_detail_dict[0])
            rec['mother_detail'] = mother_detail_list

        record['asset_offspring'] = asset_offspring_dict
      

    return render_template("index.html", loadHtml="rep_animal_register",\
         logged_in=current_user.is_authenticated,\
             asset_list=asset_dict , total_assets=len(asset_dict) )

@app.route("/asset_registry", methods=["GET","POST","PUSH","PUT","DELETE"]) 
@login_required
def asset_registry():
    if request.method == "POST":
        print(f"POST {request.get_json()}")

    if request.method == "PUSH":
        print(f"PUSH {request.get_json()}")

    if request.method == "PUT":
        print(f"PUT {request.get_json()}")

    if request.method == "DELETE":
        print(f"DELETE {request.get_json()}")

    record_list = Asset_registry.query.filter(Asset_registry.users_id == current_user.id).all()
    record_dict = sql_result_to_dict(record_list)

    list_of_columns=list(record_dict[0].keys())
    
    
    print(f"{type(list_of_columns)}")

    return render_template("index.html", loadHtml="asset_registry", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method, list_of_columns=list_of_columns)

@app.route("/asset_medical", methods=["GET","POST"]) 
@login_required
def asset_medical():
    return render_template("index.html", loadHtml="asset_medical")

@app.route("/asset_breeding", methods=["GET","POST"]) 
@login_required
def asset_breeding():
    return render_template("index.html", loadHtml="asset_breeding")

@app.route("/asset_offspring", methods=["GET","POST"]) 
@login_required
def asset_offspring():
    return render_template("index.html", loadHtml="asset_offspring")

@app.route("/dashboard")
@login_required
def dashboard():
    total_stations = MissingSockDb.get_total_base_stations()
    total_tags = MissingSockDb.get_total_tags()
    
    total_hours_1 = MissingSockDb.count_tags_not_read_past_hours(1)
    total_days_1 = MissingSockDb.count_tags_not_read_past_days(1)
    total_stations_days_1 = MissingSockDb.count_base_not_read_past_days(1)

    base_station_current = MissingSockDb.get_base_station_tag_current()

    # find middle point of base stations
    long_list = []
    lat_list = []
    for station in base_station_current:
        lat_list.append(station['gps_lat'])
        long_list.append(station['gps_long'])
    
    lat_list.sort()
    long_list.sort()
    
    # lat_middle = float(lat_list[0]) - (float(lat_list[0]) - float(lat_list[len(lat_list)-1]) )
    # long_middle = float(long_list[0]) - (float(long_list[0]) - float(long_list[len(long_list)-1]) )

    lat_middle = round(((float(lat_list[0]) + float(lat_list[len(lat_list)-1])) / 2),6)
    long_middle = round(((float(long_list[0]) + float(long_list[len(long_list)-1])) / 2),6)
    
    # load up for javascript in JSON format
    # JSON.dumps convert dict to string
 

    loadJson ="{"
    loadJson += f'"base_stations" : {json.dumps(base_station_current)} ,'
    loadJson += f'"total_stations": {total_stations[0]["count"]} ,'
    loadJson += f'"total_tags": {json.dumps(total_tags)} ,'
    loadJson += f'"total_hours_1": {total_hours_1[0]["count"]} ,'
    loadJson += f'"total_days_1": {total_days_1[0]["count"]} ,'
    loadJson += f'"total_stations_days_1": {total_stations_days_1[0]["count"]} ,'
    loadJson += '"middle_point": {' + f'"lat":"{str(lat_middle)}", "long":"{str(long_middle)}" ' + '},'
    loadJson += "}"
    
    sql_return = MissingSockDb.get_tag()

    timeNow = datetime.now().strftime("%d %B %Y %H:%M:%S")

    return render_template("index.html", loadHtml="dashboard", logged_in=current_user.is_authenticated, loadJson=loadJson, tag_count=total_tags, timeNow=timeNow )

@app.route("/basestations", methods=["GET","POST","PUT","PUSH","DELETE"])
@login_required
def base_station():

    try: 
        recv_json = request.get_json()
    except :
        pass

    if request.method == 'GET':
        method = "GET"
    
    if request.method == 'POST':
        method = "POST"
    
    if request.method == 'PUT':
        
        # MissingSockDb.upd_base_station(recv_json.id, recv_json.base_id, recv_json.nickname, user_id)
        # change to get 
        method = "GET"
    
    if request.method == 'PUSH':
        
        MissingSockDb.upd_base_station(recv_json.id, recv_json.base_id, recv_json.nickname, user_id)
        # change to get 
        method = "GET"
    
    if request.method == 'DELETE':
        
        # change to get 
        method = "GET"

    loadJson = "{"
    loadJson += get_base_stations()
    loadJson += "}"

    base_stations = json.loads(loadJson)["base_stations"]
    count = len(base_stations)
    
    return render_template("index.html", loadHtml="base_stations",logged_in=current_user.is_authenticated, method=method, loadJson=loadJson, base_stations=base_stations , total_stations=count)

@app.route("/tags", methods=["GET","POST","PUT","PUSH","DELETE"])
@login_required
def tags():
    if request.method == 'GET':
        method = "GET"
    
    if request.method == 'POST':
        method = "POST"
    
    if request.method == 'PUT':

        # change to get 
        method = "GET"
    
    if request.method == 'PUSH':
        
        # change to get 
        method = "GET"
    
    if request.method == 'DELETE':
        
        # change to get 
        method = "GET"

    try: 
        print(f"{request.get_json()}")
    except :
        print(" request.form is empty or null")
    
    print(f"method = {method}")

    all_tags = MissingSockDb.get_tag()
    count = len(all_tags)


    return render_template("index.html", loadHtml="tags", logged_in=current_user.is_authenticated, tag_list=all_tags, total_tags=count, method=method)


@app.route("/report_no_read_tag_hour", methods=["GET","POST"])
@login_required
def report_no_read_tag_hour_1(get_hours=1):
    try :
        hour = request.form["hours"]
    except :
        hour = 1
    
    if int(get_hours) > 1 :
        hour = get_hours
    
    total_stations = MissingSockDb.get_total_base_stations()
    total_tags = MissingSockDb.get_total_tags()
    
    total_hours_1 = MissingSockDb.count_tags_not_read_past_hours(hour)
    total_days_1 = MissingSockDb.count_tags_not_read_past_days(1)
    total_stations_days_1 = MissingSockDb.count_base_not_read_past_days(1)

    all_tags = MissingSockDb.tags_not_read_past_hours(hour)


    for station in all_tags:
        station["href_open_street_map"] = f"https://www.openstreetmap.org/?mlat={station['gps_lat']}&mlon={station['gps_long']}#map=12/{station['gps_lat']}/{station['gps_long']}"
       
    count = len(all_tags)

    
    loadJson ="{"
    loadJson += get_base_stations() + ","
    loadJson += f'"total_stations": {total_stations[0]["count"]} ,'
    loadJson += f'"total_tags": {json.dumps(total_tags)} ,'
    loadJson += f'"total_hours_1": {total_hours_1[0]["count"]} ,'
    loadJson += f'"total_days_1": {total_days_1[0]["count"]} ,'
    loadJson += f'"total_stations_days_1": {total_stations_days_1[0]["count"]} ,'
    loadJson += "}"

    return render_template("index.html", loadHtml="report_no_read_tag_hour", logged_in=current_user.is_authenticated, loadJson=loadJson , tag_list=all_tags, total_tags=count, hour=hour)

@app.route("/report_no_read_base_hour", methods=["GET","POST"])
@login_required
def report_no_read_base_hour_1(get_hours=1):
    try :
        hour = request.form["hours"]
    except :
        hour = 1
    
    if int(get_hours) > 1 :
        hour = get_hours
    
    total_stations = MissingSockDb.get_total_base_stations()
    total_tags = MissingSockDb.get_total_tags()
    
    total_hours_1 = MissingSockDb.count_tags_not_read_past_hours(1)
    total_days_1 = MissingSockDb.count_tags_not_read_past_days(1)

    all_base = MissingSockDb.base_not_read_past_hours(hour)
    for station in all_base:
        station["href_open_street_map"] = f"https://www.openstreetmap.org/?mlat={station['gps_lat']}&mlon={station['gps_long']}#map=12/{station['gps_lat']}/{station['gps_long']}"
    
    count = len(all_base)

    total_stations_days_1 = count


    loadJson ="{"
    loadJson += get_base_stations() + ","
    loadJson += f'"total_stations": {total_stations[0]["count"]} ,'
    loadJson += f'"total_tags": {json.dumps(total_tags)} ,'
    loadJson += f'"total_hours_1": {total_hours_1[0]["count"]} ,'
    loadJson += f'"total_days_1": {total_days_1[0]["count"]} ,'
    loadJson += f'"total_stations_days_1": {total_stations_days_1} ,'
    loadJson += "}"                  

    return render_template("index.html", loadHtml="report_no_read_base_hour", logged_in=current_user.is_authenticated, loadJson=loadJson , base_list=all_base, total_base=count, hour=hour)

if __name__ == "__main__":
    app.run(debug=True, port=5110)

