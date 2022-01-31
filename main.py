from flask import  Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import or_
from sqlalchemy.orm import close_all_sessions

import logging
import os

from  werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta, date

import json

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from MissingSockDBQueries import MissingSock_sql
from MissingSockDBQueries.MissingSock_orm_models import sql_result_to_dict, Users, Asset_registry, \
    Asset_medical, Asset_breeding, Asset_offspring, Base_station, Tag, Asset_produce, Tag_current, \
    Base_station_current    

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

@app.before_first_request
def before_first_request():
    log_level = logging.INFO
 
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
 
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)
 
    app.logger.setLevel(log_level)

    defaultFormatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(defaultFormatter)


@app.route("/login_error")
def login_error():
    return render_template("index.html", loadHtml="login_error")

@app.route("/" , methods=["GET","POST"])
@app.route("/home" , methods=["GET","POST"])
@app.route("/index" , methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"]) 
def login():

    app.logger.info(f"func(login): received {request.method} for request.form.get('email')")

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = Users.query.filter_by(email=email).first()
        db_session.commit()
        
        #Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return render_template("index.html", loadHtml="login_error")
        
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return render_template("index.html", loadHtml="login_error")
        
        else:
            login_user(user)
            return render_template("index.html", loadHtml="rep_animal_register", logged_in=current_user.is_authenticated)
        
    return render_template("index.html", loadHtml="login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('user is now logged out ')
    return render_template("index.html", loadHtml="login_error")



@app.route("/register", methods=["GET","POST"])
def register():

    app.logger.info(f"Register : {request.method} ")

    if request.method == "POST":
        
        if Users.query.filter_by(email=request.form.get('email')).first():
            db_session.commit()
            
            #User already exists
            flash("Email is already registered, please log in")
            
            return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated, flash_type="register")
        
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = Users(
            email=request.form.get('email'),
            password=hash_and_salted_password,
            name = request.form.get('fname'),
            surname = request.form.get('surname'),
            phone = request.form.get('phone'),
            farm_name = request.form.get('farm_name'),
            address_1 = request.form.get('address_1'),
            address_2 = request.form.get('address_2'),
            province = request.form.get('province'),
            area = request.form.get('area'),
            postal_code = request.form.get('postal_code'),
            gps_lat = request.form.get('gps_lat'),
            gps_long = request.form.get('gps_long')
        )
        
        app.logger.info(f"Register : insert new user : {new_user.email} ")
        db_session.add(new_user)
        db_session.commit()

        login_user(new_user)
        
        flash(f"New user created for {request.form.get('email')}")
        return render_template("index.html", loadHtml="login_error")

    return render_template("index.html", loadHtml="register", logged_in=current_user.is_authenticated)

@app.route("/my_profile", methods=["GET","POST"])
def my_profile():

    app.logger.info(f"my_profile : {request.method} ")

    if request.method == "POST":
        recv_rec = request.get_json()
        update_rec = db_session.query(Users).filter(Users.id == current_user.id).first()
        
        update_rec.email=request.form.get('email'),
        update_rec.name = request.form.get('fname'),
        update_rec.surname = request.form.get('surname'),
        update_rec.phone = request.form.get('phone'),
        update_rec.farm_name = request.form.get('farm_name'),
        update_rec.address_1 = request.form.get('address_1'),
        update_rec.address_2 = request.form.get('address_2'),
        update_rec.province = request.form.get('province'),
        update_rec.area = request.form.get('area'),
        update_rec.postal_code = request.form.get('postal_code'),
        update_rec.gps_lat = request.form.get('gps_lat'),
        update_rec.gps_long = request.form.get('gps_long')

        db_session.commit() 
        
        app.logger.info(f"my_profile : update user : {current_user.id} ")

    user_list = db_session.query(Users).filter(Users.id == current_user.id).all()
    user_dict = sql_result_to_dict(user_list)

    return render_template("index.html", loadHtml="my_profile", \
        user_detail=user_dict[0], \
        logged_in=current_user.is_authenticated)

@app.route("/new_animal_register", methods=["GET","POST"])
@login_required
def new_animal_register():

    return render_template("index.html", loadHtml="new_animal_register", \
        logged_in=current_user.is_authenticated )


@app.route("/activities", methods=["GET","POST"])
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

    # Insert/update both on PUT --- Push does not work on chemicloud fnw 
    if request.method == "PUT":

        recv_rec = request.get_json()
        
        # Check if this is insert or update
        if str(recv_rec['id'])[:4] == "ins_" :
            db_action = "INSERT"
        else :
            db_action = "UPDATE"

        if db_action == "INSERT":
            app.logger.info(f"Insert : {recv_rec['id']}")
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
        
        if db_action == "UPDATE":
            app.logger.info(f"Update : {recv_rec['id']}")
            recv_rec = request.get_json()
            new_rec = db_session.query(Asset_registry).filter(Asset_registry.id == int(recv_rec['id'])).first()
            db_session.commit()

            for key, val in recv_rec.items():
                # change all '' to None which will be added as Null
                if len(val) == 0 :
                    val = None
                elif val == 'None':
                    val = None
                
                # convert JSON str types to int
                setattr(new_rec, key, val) 

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
        rec_list_count= len(record_list), method=request.method,\
             list_of_columns=list_of_columns)

@app.route("/asset_medical", methods=["GET","POST","PUSH","PUT","DELETE"]) 
@login_required
def asset_medical():
    if request.method == "POST":
        pass

    # Insert/update both on PUT --- Push does not work on chemicloud fnw 
    if request.method == "PUT":

        recv_rec = request.get_json()
        
        # Check if this is insert or update
        if str(recv_rec['id'])[:4] == "ins_" :
            db_action = "INSERT"
        else :
            db_action = "UPDATE"

        if db_action == "UPDATE": # Update
            recv_rec = request.get_json()
            new_rec = db_session.query(Asset_medical).filter(Asset_medical.id == int(recv_rec['id'])).first()
            db_session.commit()

            for key, val in recv_rec.items():
                # change all '' to None which will be added as Null
                if len(val) == 0 :
                    val = None
                elif val == 'None':
                    val = None
                
                # convert JSON str types to int
                setattr(new_rec, key, val)

            db_session.commit() 

        if db_action == "INSERT":

            # Check if this is insert or update
            if str(recv_rec['id'])[:4] == "ins_" :
                db_action = "INSERT"
            else :
                db_action = "UPDATE"

            if db_action == "INSERT":
                app.logger.info(f"Insert : {recv_rec['id']}")

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

        # Insert/update both on PUT --- Push does not work on chemicloud fnw 
    if request.method == "PUT":

        recv_rec = request.get_json()
        
        # Check if this is insert or update
        if str(recv_rec['id'])[:4] == "ins_" :
            db_action = "INSERT"
        else :
            db_action = "UPDATE"

        if db_action == "UPDATE": # Update
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

        if db_action == "INSERT":

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

        # Insert/update both on PUT --- Push does not work on chemicloud fnw 
    if request.method == "PUT":

        recv_rec = request.get_json()
        
        # Check if this is insert or update
        if str(recv_rec['id'])[:4] == "ins_" :
            db_action = "INSERT"
        else :
            db_action = "UPDATE"

        if db_action == "UPDATE": # Update
            recv_rec = request.get_json()
            new_rec = db_session.query(Asset_offspring).filter(Asset_offspring.id == int(recv_rec['id'])).first()
            db_session.commit()

            for key, val in recv_rec.items():
                # change all '' to None which will be added as Null
                if len(val) == 0 :
                    val = None
                elif val == 'None':
                    val = None
                
                # convert JSON str types to int
                setattr(new_rec, key, val)

            db_session.commit() 

        if db_action == "INSERT":

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

        # Insert/update both on PUT --- Push does not work on chemicloud fnw 
    if request.method == "PUT":

        recv_rec = request.get_json()
        
        # Check if this is insert or update
        if str(recv_rec['id'])[:4] == "ins_" :
            db_action = "INSERT"
        else :
            db_action = "UPDATE"

        if db_action == "UPDATE": # Update
            recv_rec = request.get_json()
            new_rec = db_session.query(Asset_produce).filter(Asset_produce.id == int(recv_rec['id'])).first()
            db_session.commit()

            for key, val in recv_rec.items():
                # change all '' to None which will be added as Null
                if len(val) == 0 :
                    val = None
                elif val == 'None':
                    val = None
                
                # convert JSON str types to int
                setattr(new_rec, key, val)

            db_session.commit()

        if db_action == "INSERT":

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
def dashboard(get_hours=24):

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

    try :
        hour = request.form["hours"]
    except :
        hour = 1
    
    if int(get_hours) > 1 :
        hour = get_hours

    # info for row 3 map/chart

    # Check if user has at least 1 tag
    tag_list = db_session.query(Tag).filter(Tag.users_id == current_user.id).all()
    tag_dict = sql_result_to_dict(tag_list)

    if len(tag_dict) == 0 :
        flash("Report not available - Please add at least Animal with a linked tag ")
        return render_template("index.html", loadHtml="error_page", logged_in=current_user.is_authenticated, flash_type="no_tag")
 
    
    total_hours_1 = MissingSock_sql.count_tags_not_read_past_hours(1, current_user.id)

    # find middle point for map
    user_list = db_session.query(Users).filter(Users.id == current_user.id).all()
    user_dict = sql_result_to_dict(user_list)
    
    lat_middle = user_dict[0]['gps_lat']
    long_middle = user_dict[0]['gps_long']

    # tag location + detail 
    sql_return = MissingSock_sql.tags_last_location_by_userid(current_user.id)
    print(f"TAGS = {sql_return}")
    
    # load up for javascript in JSON format
    # JSON.dumps convert dict to string
 

    loadJson ="{"
    loadJson += f'"total_tags": {len(tag_dict)} ,'
    loadJson += f'"total_hours_1": {total_hours_1[0]["count"]} ,'
    loadJson += '"middle_point": {' + f'"lat":"{str(lat_middle)}", "long":"{str(long_middle)}" ' + '},'
    loadJson += f'"tags": {sql_return} ,'
    loadJson += "}"
    
    timeNow = datetime.now().strftime("%d %B %Y %H:%M:%S")

    return render_template("index.html", loadHtml="dashboard", \
        logged_in=current_user.is_authenticated, record_list=record_dict,\
        rec_list_count= len(record_list), method=request.method,\
        list_of_columns=list_of_columns, \
        loadJson=loadJson, \
        tag_count=len(tag_dict), timeNow=timeNow)


@app.route("/report_no_read_tag_hour", methods=["GET","POST"])
@login_required
def report_no_read_tag_hour_1(get_hours=1):
    try :
        hour = request.form["hours"]
    except :
        hour = 1
    
    if int(get_hours) > 1 :
        hour = get_hours

    # Check if user has at least 1 base_stations
    base_station_list = db_session.query(Base_station).filter(Base_station.users_id == current_user.id).all()
    base_station_dict = sql_result_to_dict(base_station_list)

    if len(base_station_dict) == 0 :
        flash("Report not available - Please add at least 1 basestation ")
        return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated, flash_type="no_base_station")
 
    # Check if user has at least 1 tag
    tag_list = db_session.query(Tag).filter(Tag.users_id == current_user.id).all()
    tag_dict = sql_result_to_dict(tag_list)

    if len(tag_dict) == 0 :
        flash("Report not available - Please add at least 1 tag ")
        return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated, flash_type="no_tag")

    
    total_hours_1 = MissingSock_sql.count_tags_not_read_past_hours(hour, current_user.id)
    total_days_1 = MissingSock_sql.count_tags_not_read_past_days(1)
    total_stations_days_1 = MissingSock_sql.count_base_not_read_past_days(1)

    all_tags = MissingSock_sql.tags_not_read_past_hours(hour)


    for station in all_tags:
        station["href_open_street_map"] = f"https://www.openstreetmap.org/?mlat={station['gps_lat']}&mlon={station['gps_long']}#map=12/{station['gps_lat']}/{station['gps_long']}"
       
    count = len(all_tags)

    
    loadJson ="{"
    loadJson += get_base_stations() + ","
    loadJson += f'"total_stations": {len(base_station_dict)} ,'
    loadJson += f'"total_tags": {len(tag_dict)} ,'
    loadJson += f'"total_hours_1": {total_hours_1[0]["count"]} ,'
    loadJson += f'"total_days_1": {total_days_1[0]["count"]} ,'
    loadJson += f'"total_stations_days_1": {total_stations_days_1[0]["count"]} ,'
    loadJson += "}"

    return render_template("index.html", loadHtml="report_no_read_tag_hour", \
     logged_in=current_user.is_authenticated, loadJson=loadJson , \
     tag_list=all_tags, total_tags=count, hour=hour)

@app.route("/overview", methods=["GET","POST"])
@app.route("/report_no_read_base_hour", methods=["GET","POST"])
@login_required
def report_no_read_base_hour_1(get_hours=1):
    try :
        hour = int(request.form["hours"])
    except :
        hour = 1
    
    if int(get_hours) > 1 :
        hour = get_hours
    
    # Check if user has at least 1 base_stations
    base_station_list = db_session.query(Base_station).filter(Base_station.users_id == current_user.id).all()
    base_station_dict = sql_result_to_dict(base_station_list)

    if len(base_station_dict) == 0 :
        flash("Report not available - Please add at least 1 basestation ")
        return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated, flash_type="no_base_station")
 
    # Check if user has at least 1 tag
    tag_list = db_session.query(Tag).filter(Tag.users_id == current_user.id).all()
    tag_dict = sql_result_to_dict(tag_list)

    if len(tag_dict) == 0 :
        flash("Report not available - Please add at least 1 tag ")
        return render_template("index.html", loadHtml="home", logged_in=current_user.is_authenticated, flash_type="no_tag")

    # Get all tags not scanned in the past hour
    hour_1 = datetime.now() - timedelta(hours=1)

    total_hours_1_list = db_session.query(Tag_current, Tag).filter(Tag_current.id == Tag.id,\
         Tag.users_id == current_user.id,\
         Tag_current.timestamp < hour_1).all()

    total_hours_1_dict = total_hours_1_list[0][0].__dict__
    total_hours_1 = len(total_hours_1_dict)

    # get all Tags not scanned in the past day
    day_1 = datetime.now() - timedelta(days=1)

    total_days_1_list = db_session.query(Tag_current, Tag).filter(Tag_current.id == Tag.id,\
         Tag.users_id == current_user.id,\
         Tag_current.timestamp < day_1).all()
    total_days_1_dict = total_days_1_list[0][0].__dict__
    total_days_1 = len(total_days_1_dict)

    # get all Base_stations with no reads in the past <var:hour> hours
    hour_var = datetime.now() - timedelta(hours=hour)

    all_base_query_result = db_session.query(Base_station_current, Base_station).\
        filter(Base_station.id == Base_station_current.id,\
        Base_station.users_id == current_user.id,\
        Base_station_current.timestamp < hour_var).all()
    
    all_base_current_dict = []

    # get each row , Base_station_current table result convert to dict
    for row in all_base_query_result :
        all_base_current_dict.append(row.Base_station_current.__dict__)

    for station in all_base_current_dict:
        station["href_open_street_map"] = f"https://www.openstreetmap.org/?mlat={station['gps_lat']}&mlon={station['gps_long']}#map=12/{station['gps_lat']}/{station['gps_long']}"
    
    total_stations_days_1 = len(all_base_current_dict)

    loadJson ="{"
    loadJson += get_base_stations() + ","
    loadJson += f'"total_stations": {len(base_station_dict)} ,'
    loadJson += f'"total_tags": {len(tag_dict)} ,'
    loadJson += f'"total_hours_1": {total_hours_1} ,'
    loadJson += f'"total_days_1": {total_days_1} ,'
    loadJson += f'"total_stations_days_1": {total_stations_days_1} ,'
    loadJson += "}"     

    print(f"{loadJson}")             

    return render_template("index.html", loadHtml="report_no_read_base_hour", logged_in=current_user.is_authenticated, loadJson=loadJson , base_list=all_base_current_dict, total_base=len(all_base_current_dict), hour=hour)

if __name__ == "__main__":

    before_first_request()

    # app.logger.debug("START : LOG SHOW debug")
    app.logger.info("=============================")
    app.logger.info("START : web server started")
    # app.logger.warning("START : LOG SHOW warning")
    # app.logger.error("START : LOG SHOW error")
    # app.logger.critical("START : LOG SHOW critical")

    app.run(debug=True)
    # version 0.0.0.2

