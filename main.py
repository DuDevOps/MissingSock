from flask import  Flask, render_template, request, url_for, redirect, flash, jsonify
# from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.orm import close_all_sessions

from  werkzeug.security import generate_password_hash, check_password_hash

import mysql
import pymysql

from datetime import datetime, timedelta, date

import json

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from MissingSockDBQueries import MissingSock_sql
from MissingSockDBQueries.MissingSock_orm_models import sql_result_to_dict, Users, Asset_registry, \
    Asset_medical, Asset_breeding, Asset_offspring, Base_station, Tag, Asset_produce

from MissingSockDBQueries.MissingSock_database import db_session


app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



app.config['SECRET_KEY'] = 'mySuperDoeperSecretWord'

# CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    new_user = Users.query.get(int(user_id))
    #db_session.close()
    return new_user

def get_base_stations():
    base_station_current = MissingSock_sql.get_base_station()
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

    # load up for javascript in JSON format
    # JSON.dumps convert dict to string
    loadJson = f'"base_stations" : {json.dumps(base_station_current)} ,'
    loadJson += '"middle_point": {' + f'"lat":"{str(lat_middle)}", "long":"{str(long_middle)}" ' + '}'

    return loadJson

@app.route("/")
def test_deploy():
    return "Hello World"

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
        db_session.commit()
        #db_session.close()

        
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
            db_session.commit()
            #db_session.close()
            #User already exists
            flash("Email is already registered, please log in")
            
            return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated)
        
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = Users(
            email=request.form.get('email'),
            password=hash_and_salted_password
        )
        
        db_session.add(new_user)
        db_session.commit()
        #db_session.close()

        login_user(new_user)
        
        flash(f"New user created for {request.form.get('email')}")
        return render_template("index.html", loadHtml="home")

    return render_template("index.html", loadHtml="register", logged_in=current_user.is_authenticated)

@app.route("/rep_animal_register", methods=["GET","POST"]) 
@login_required
def rep_animal_register():
    #close_all_sessions()

    if request.method == "POST":
        pass
    
    #get List of assets for current user
   
    asset_result = Asset_registry.query.filter_by(users_id=current_user.id).all()
    #db_session.close()
    
    #Change to dict
    asset_dict = sql_result_to_dict(asset_result)
    
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
        db_session.commit()
        #db_session.close()
        asset_medical_dict = sql_result_to_dict(asset_medical_result)

        record['asset_medical'] = asset_medical_dict

        # get produce record
        asset_produce_result = Asset_produce.query.filter(Asset_produce.asset_registry_id == record['id']).all()
        db_session.commit()
        #db_session.close()
        asset_produce_dict = sql_result_to_dict(asset_produce_result)

        record['asset_produce'] = asset_produce_dict

        # get Breeding info
        asset_breeding_result = Asset_breeding.query.\
            filter(or_(Asset_breeding.asset_registry_father_id == record['id'], Asset_breeding.asset_registry_mother_id == record['id']) ).all()
        db_session.commit()
        #db_session.close()
        asset_breeding_dict = sql_result_to_dict(asset_breeding_result)

        # # get breeding detail
        for breed in asset_breeding_dict:
            father_detail_list = []

            father_detail = Asset_registry.query.filter(Asset_registry.id == breed['asset_registry_father_id']).all()
            db_session.commit()
            #db_session.close()
            father_detail_dict = sql_result_to_dict(father_detail)
            father_detail_list.append(father_detail_dict[0])
            breed['father_detail'] = father_detail_list

            mother_detail_list = []

            mother_detail = Asset_registry.query.filter(Asset_registry.id == breed['asset_registry_mother_id']).all()
            db_session.commit()
            #db_session.close()
            mother_detail_dict = sql_result_to_dict(mother_detail)
            mother_detail_list.append(mother_detail_dict[0])
            breed['mother_detail'] = mother_detail_list
            

        record['asset_breeding'] = asset_breeding_dict

        # get offspring info
        asset_offspring_result = Asset_offspring.query.\
            filter(or_(Asset_offspring.asset_father_id == record['id'], Asset_offspring.asset_mother_id == record['id']) ).all()
        db_session.commit()
        #db_session.close()
        asset_offspring_dict = sql_result_to_dict(asset_offspring_result)

        

        # # get offspring detail
        for rec in asset_offspring_dict:
            offspring_detail_list = []

            off_asset_result = Asset_registry.query.filter(Asset_registry.id == rec['asset_offspring_id']).all()
            db_session.commit()
            #db_session.close()
            off_asset_dict = sql_result_to_dict(off_asset_result)
            offspring_detail_list.append(off_asset_dict[0])
            rec['offspring_detail'] = offspring_detail_list

            father_detail_list = []

            father_detail = Asset_registry.query.filter(Asset_registry.id == rec['asset_father_id']).all()
            db_session.commit()
            #db_session.close()
            father_detail_dict = sql_result_to_dict(father_detail)
            father_detail_list.append(father_detail_dict[0])
            rec['father_detail'] = father_detail_list

            mother_detail_list = []

            mother_detail = Asset_registry.query.filter(Asset_registry.id == rec['asset_mother_id']).all()
            db_session.commit()
            #db_session.close()
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
    #close_all_sessions()
    if request.method == "POST":
        pass

    if request.method == "PUSH": # Update
        recv_rec = request.get_json()
        new_rec = db_session.query(Asset_registry).filter(Asset_registry.id == int(recv_rec['id'])).first()
        db_session.commit()
        #db_session.close()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            elif val == 'None':
                val = None
            
            # convert JSON str types to int
            setattr(new_rec, key, val)

        db_session.commit() 
        #db_session.close()

    if request.method == "PUT":

        recv_rec = request.get_json()
        new_rec = Asset_registry()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            
            # convert JSON str types to int
            if key == "id": # don't add ID for insert
                pass
            elif key == "users_id":
                new_rec.users_id  = current_user.id
            else:
                setattr(new_rec, key, val)

        db_session.add(new_rec)
        db_session.commit()

    if request.method == "DELETE":
        recv_rec = request.get_json()
         
        new_rec = db_session.query(Asset_registry).filter(Asset_registry.id == int(recv_rec['id'])).first()
        
        #
        db_session.delete(new_rec)
        db_session.commit() 
        #db_session.close()

    # Get all row at least 1 row must exist
    try:
        record_list = Asset_registry.query.filter(Asset_registry.users_id == current_user.id).all()
    finally:
        # if table has no records add first default rec - else nothing works right
        if len(record_list) == 0 :
            new_rec = Asset_registry()
            new_rec.users_id  = current_user.id

            db_session.add(new_rec)
            db_session.commit()
            record_list = Asset_registry.query.filter(Asset_registry.users_id == current_user.id).all()


    db_session.commit()
    record_dict = sql_result_to_dict(record_list)

    try:
        list_of_columns=list(record_dict[0].keys())
        list_of_columns.remove('id')
    except:
        pass

    return render_template("index.html", loadHtml="asset_registry", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method, list_of_columns=list_of_columns)

@app.route("/asset_medical", methods=["GET","POST","PUSH","PUT","DELETE"]) 
@login_required
def asset_medical():
    if request.method == "POST":
        pass

    if request.method == "PUSH": # Update
        recv_rec = request.get_json()
        new_rec = db_session.query(Asset_medical).filter(Asset_medical.id == int(recv_rec['id'])).first()
        db_session.commit()
        #db_session.close()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            elif val == 'None':
                val = None
            
            # convert JSON str types to int
            setattr(new_rec, key, val)

        db_session.commit() 
        #db_session.close()

    if request.method == "PUT":

        recv_rec = request.get_json()
        new_rec = Asset_medical()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            
            # convert JSON str types to int
            if key == "id": # don't add ID for insert
                pass
            elif key == "users_id":
                new_rec.users_id  = current_user.id
            else:
                setattr(new_rec, key, val)

        db_session.add(new_rec)
        db_session.commit()
        #db_session.close()

    if request.method == "DELETE":
        recv_rec = request.get_json()
         
        new_rec = db_session.query(Asset_medical).filter(Asset_medical.id == int(recv_rec['id'])).first()
        
        #
        db_session.delete(new_rec)
        db_session.commit() 
        #db_session.close()


     # Get all row at least 1 row must exist
    try:
        record_list = Asset_medical.query.filter(Asset_medical.users_id == current_user.id).all()
    finally:
        # if table has no records add first default rec - else nothing works right
        if len(record_list) == 0 :
            new_rec = Asset_medical()
            new_rec.users_id  = current_user.id
            
            db_session.add(new_rec)
            db_session.commit()
            record_list = Asset_registry.query.filter(Asset_registry.users_id == current_user.id).all()

    record_dict = sql_result_to_dict(record_list)

    try:
        list_of_columns=list(record_dict[0].keys())
        list_of_columns.remove('id')
    except:
        pass

    return render_template("index.html", loadHtml="asset_medical", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method, list_of_columns=list_of_columns)

@app.route("/asset_breeding", methods=["GET","POST","PUSH","PUT","DELETE"]) 
@login_required
def asset_breeding():
    if request.method == "POST":
        pass

    if request.method == "PUSH": # Update
        recv_rec = request.get_json()
        new_rec = db_session.query(Asset_breeding).filter(Asset_breeding.id == int(recv_rec['id'])).first()
        db_session.commit()
        #db_session.close()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            elif val == 'None':
                val = None
            
            # convert JSON str types to int
            setattr(new_rec, key, val)

        db_session.commit() 
        #db_session.close()

    if request.method == "PUT":

        recv_rec = request.get_json()
        new_rec = Asset_breeding()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            
            # convert JSON str types to int
            if key == "id": # don't add ID for insert
                pass
            elif key == "users_id":
                new_rec.users_id  = current_user.id
            else:
                setattr(new_rec, key, val)

        db_session.add(new_rec)
        db_session.commit()

    if request.method == "DELETE":
        recv_rec = request.get_json()
         
        new_rec = db_session.query(Asset_breeding).filter(Asset_breeding.id == int(recv_rec['id'])).first()
        
        #
        db_session.delete(new_rec)
        db_session.commit() 
    
    # Get all row at least 1 row must exist
    try:
        record_list = db_session.query(Asset_breeding).join(Asset_registry,or_(Asset_registry.id == Asset_breeding.asset_registry_father_id, Asset_registry.id == Asset_breeding.asset_registry_mother_id)).filter(Asset_registry.users_id == current_user.id).all()
    finally:
        # if table has no records add first default rec - else nothing works right
        record_list = Asset_breeding.query.filter(Asset_breeding.users_id == current_user.id).all()
        if len(record_list) == 0 :
            new_rec = Asset_breeding()
            new_rec.users_id  = current_user.id
            
            db_session.add(new_rec)
            db_session.commit()
            record_list = Asset_breeding.query.filter(Asset_breeding.users_id == current_user.id).all()

    record_dict = sql_result_to_dict(record_list)

    try:
        list_of_columns=list(record_dict[0].keys())
        list_of_columns.remove('id')
    except:
        pass

    return render_template("index.html", loadHtml="asset_breeding", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method, list_of_columns=list_of_columns)


@app.route("/asset_offspring", methods=["GET","POST","PUSH","PUT","DELETE"]) 
@login_required
def asset_offspring():
    if request.method == "POST":
        pass

    if request.method == "PUSH": # Update
        recv_rec = request.get_json()
        new_rec = db_session.query(Asset_offspring).filter(Asset_offspring.id == int(recv_rec['id'])).first()
        db_session.commit()
        #db_session.close()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            elif val == 'None':
                val = None
            
            # convert JSON str types to int
            setattr(new_rec, key, val)

        db_session.commit() 
        #db_session.close()

    if request.method == "PUT":

        recv_rec = request.get_json()
        new_rec = Asset_offspring()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            
            # convert JSON str types to int
            if key == "id": # don't add ID for insert
                pass
            elif key == "users_id":
                new_rec.users_id  = current_user.id
            else:
                setattr(new_rec, key, val)

        db_session.add(new_rec)
        db_session.commit()

    if request.method == "DELETE":
        recv_rec = request.get_json()
         
        new_rec = db_session.query(Asset_offspring).filter(Asset_offspring.id == int(recv_rec['id'])).first()
        
        #
        db_session.delete(new_rec)
        db_session.commit() 
        #db_session.close()
    
    # Get all row at least 1 row must exist
    try:
        record_list = db_session.query(Asset_offspring).join(Asset_registry, \
        or_(Asset_registry.id == Asset_offspring.asset_father_id, \
            Asset_registry.id == Asset_offspring.asset_mother_id, \
            Asset_registry.id == Asset_offspring.asset_offspring_id )).\
            filter(Asset_registry.users_id == current_user.id).all()
    finally:
        # if table has no records add first default rec - else nothing works right
        record_list = Asset_offspring.query.filter(Asset_offspring.users_id == current_user.id).all()
        if len(record_list) == 0 :
            new_rec = Asset_offspring()
            new_rec.users_id  = current_user.id
            
            db_session.add(new_rec)
            db_session.commit()
            record_list = Asset_offspring.query.filter(Asset_offspring.users_id == current_user.id).all()

    record_dict = sql_result_to_dict(record_list)

    try:
        list_of_columns=list(record_dict[0].keys())
        list_of_columns.remove('id')
    except:
        pass

    return render_template("index.html", loadHtml="asset_offspring", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method, list_of_columns=list_of_columns)

@app.route("/asset_produce", methods=["GET","POST","PUSH","PUT","DELETE"]) 
@login_required
def asset_produce():
    if request.method == "POST":
        pass

    if request.method == "PUSH": # Update
        recv_rec = request.get_json()
        new_rec = db_session.query(Asset_produce).filter(Asset_produce.id == int(recv_rec['id'])).first()
        db_session.commit()
        #db_session.close()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            elif val == 'None':
                val = None
            
            # convert JSON str types to int
            setattr(new_rec, key, val)

        db_session.commit() 
        #db_session.close()

    if request.method == "PUT":

        recv_rec = request.get_json()
        new_rec = Asset_produce()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            
            # convert JSON str types to int
            if key == "id": # don't add ID for insert
                pass
            elif key == "users_id":
                new_rec.users_id  = current_user.id
            else:
                setattr(new_rec, key, val)

        db_session.add(new_rec)
        db_session.commit()
        #db_session.close()

    if request.method == "DELETE":
        recv_rec = request.get_json()
         
        new_rec = db_session.query(Asset_produce).filter(Asset_produce.id == int(recv_rec['id'])).first()
        
        #
        db_session.delete(new_rec)
        db_session.commit() 
        #db_session.close()


    # Get all row at least 1 row must exist
    try:
        record_list = db_session.query(Asset_produce).\
            join(Asset_registry, Asset_registry.id == Asset_produce.asset_registry_id).\
                filter(Asset_registry.users_id == current_user.id).all()
    finally:
        # if table has no records add first default rec - else nothing works right
        record_list = Asset_produce.query.filter(Asset_produce.users_id == current_user.id).all()
        if len(record_list) == 0 :
            new_rec = Asset_produce()
            new_rec.users_id  = current_user.id
            
            db_session.add(new_rec)
            db_session.commit()
            record_list = Asset_produce.query.filter(Asset_produce.users_id == current_user.id).all()

    record_dict = sql_result_to_dict(record_list)

    try:
        list_of_columns=list(record_dict[0].keys())
        list_of_columns.remove('id')
    except:
        pass

    db_session.commit()

    return render_template("index.html", loadHtml="asset_produce", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method, list_of_columns=list_of_columns)

@app.route("/dashboard")
@login_required
def dashboard():
    total_stations = MissingSock_sql.get_total_base_stations()
    total_tags = MissingSock_sql.get_total_tags()
    
    total_hours_1 = MissingSock_sql.count_tags_not_read_past_hours(1)
    total_days_1 = MissingSock_sql.count_tags_not_read_past_days(1)
    total_stations_days_1 = MissingSock_sql.count_base_not_read_past_days(1)

    base_station_current = MissingSock_sql.get_base_station_tag_current()

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
    
    sql_return = MissingSock_sql.get_tag()

    timeNow = datetime.now().strftime("%d %B %Y %H:%M:%S")

    return render_template("index.html", loadHtml="dashboard", logged_in=current_user.is_authenticated, loadJson=loadJson, tag_count=total_tags, timeNow=timeNow )

@app.route("/base_station", methods=["GET","POST","PUSH","PUT","DELETE"]) 
@login_required
def base_station():
    if request.method == "POST":
        pass

    if request.method == "PUSH": # Update
        recv_rec = request.get_json()
        new_rec = db_session.query(Base_station).filter(Base_station.id == int(recv_rec['id'])).first()
        db_session.commit()
        #db_session.close()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            elif val == 'None':
                val = None
            
            # convert JSON str types to int
            setattr(new_rec, key, val)

        db_session.commit() 
        #db_session.close()

    if request.method == "PUT":

        recv_rec = request.get_json()
        new_rec = Base_station()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            
            # convert JSON str types to int
            if key == "id": # don't add ID for insert
                pass
            elif key == "users_id":
                new_rec.users_id  = current_user.id
            else:
                setattr(new_rec, key, val)

        db_session.add(new_rec)
        db_session.commit()
        #db_session.close()

    if request.method == "DELETE":
        recv_rec = request.get_json()
         
        new_rec = db_session.query(Base_station).filter(Base_station.id == int(recv_rec['id'])).first()
        
        #
        db_session.delete(new_rec)
        db_session.commit() 
        #db_session.close()


    record_list = db_session.query(Base_station).filter(or_(Base_station.users_id == current_user.id, Base_station.users_id == None)).all()
    #db_session.close()
    record_dict = sql_result_to_dict(record_list)
    
    try:
        list_of_columns=list(record_dict[0].keys())
        list_of_columns.remove('id')
    except:
        pass

    return render_template("index.html", loadHtml="base_station", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method, list_of_columns=list_of_columns)

@app.route("/tag", methods=["GET","POST","PUSH","PUT","DELETE"]) 
@login_required
def tag():
    if request.method == "POST":
        pass

    if request.method == "PUSH": # Update
        recv_rec = request.get_json()
        new_rec = db_session.query(Tag).filter(Tag.id == int(recv_rec['id'])).first()
        db_session.commit()
        #db_session.close()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            elif val == 'None':
                val = None
            
            # convert JSON str types to int
            setattr(new_rec, key, val)

        db_session.commit() 
        #db_session.close()

    if request.method == "PUT":

        recv_rec = request.get_json()
        new_rec = Tag()

        for key, val in recv_rec.items():
            # change all '' to None which will be added as Null
            if len(val) == 0 :
                val = None
            
            # convert JSON str types to int
            if key == "id": # don't add ID for insert
                pass
            elif key == "users_id":
                new_rec.users_id  = current_user.id
            else:
                setattr(new_rec, key, val)

        db_session.add(new_rec)
        db_session.commit()

    if request.method == "DELETE":
        recv_rec = request.get_json()
         
        new_rec = db_session.query(Tag).filter(Tag.id == int(recv_rec['id'])).first()
        
        #
        db_session.delete(new_rec)
        db_session.commit() 
        #db_session.close()


    record_list = db_session.query(Tag).filter(or_(Tag.users_id == current_user.id, Tag.users_id == None)).all()
    #db_session.close()
    record_dict = sql_result_to_dict(record_list)

    try:
        list_of_columns=list(record_dict[0].keys())
        list_of_columns.remove('id')
    except:
        pass

    return render_template("index.html", loadHtml="tag", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method, list_of_columns=list_of_columns)

@app.route("/report_no_read_tag_hour", methods=["GET","POST"])
@login_required
def report_no_read_tag_hour_1(get_hours=1):
    try :
        hour = request.form["hours"]
    except :
        hour = 1
    
    if int(get_hours) > 1 :
        hour = get_hours
    
    total_stations = MissingSock_sql.get_total_base_stations()
    total_tags = MissingSock_sql.get_total_tags()
    
    total_hours_1 = MissingSock_sql.count_tags_not_read_past_hours(hour)
    total_days_1 = MissingSock_sql.count_tags_not_read_past_days(1)
    total_stations_days_1 = MissingSock_sql.count_base_not_read_past_days(1)

    all_tags = MissingSock_sql.tags_not_read_past_hours(hour)


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
    
    total_stations = MissingSock_sql.get_total_base_stations()
    total_tags = MissingSock_sql.get_total_tags()
    
    total_hours_1 = MissingSock_sql.count_tags_not_read_past_hours(1)
    total_days_1 = MissingSock_sql.count_tags_not_read_past_days(1)

    all_base = MissingSock_sql.base_not_read_past_hours(hour)
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
    app.run(port=5110, debug=True)

