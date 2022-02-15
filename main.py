from random import random
from flask import  Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import or_, and_
from sqlalchemy.orm import close_all_sessions

import logging
import os

from  werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta, date

import json

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from MissingSockDBQueries import MissingSock_sql
from MissingSockDBQueries.MissingSock_orm_models import Asset_medical, sql_result_to_dict, Users, Asset_registry, \
    Asset_breeding, Asset_breeding, Asset_offspring, Base_station, Tag, Asset_produce, Tag_current, \
    Base_station_current, sql_result_column_list_to_dict, Base_station_hist, \
    Tag_hist 

from MissingSockDBQueries.MissingSock_database import db_session

Animal_dropdown = {"Cattle":[
	"Nguni",
	"Afrikaner",
	"Bonsmara",
	"Brahman",
	"Aberedeen Angus",
	"limousin",
	"Simmental",
	"Ankole-Watusi",
	"Charolais",
	"Boran",
	"Beefmaster" ] ,
"Sheep":[ 	
    "Merino",
	"Dorper",
	"Dohne Merino",
	"Dormer",
	"Black Headed Persian",
	"Afrino",
	"Suffolk" ],
"Goats": [ 	
    "Angora",
	"Boer",
	"Lamancha",
	"Nubian",
	"Obehasli",
	"Saanen",
	"Toggenburg" ],
"Pigs":[	
    "Chester White",
	"Duroc",
	"Hampshire",
	"Landrance",
	"Poland China",
	"Spotted",
	"Yorkshire"],
"Horse":[	
    "Abyssinian",
	"Boerperd",
	"Dongola",
	"Nooitgedachter",
	"Vlaamperd" ],
"Antelope": [	
    "Wildebees",
	"Eland",
	"Waterbuck",
	"Springbok",
	"SteenBok",
	"Duiker",
	"ReedBuck",
	"Impala",
	"Sable",
	"Gemsbok",
	"Kudu" ]
}

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

            count_asset_registry = db_session.query(Asset_registry).filter(Asset_registry.users_id == user.id).count()
            
            if (count_asset_registry == 0 ) :
                return redirect(url_for('animal_detail_upd_ins', loadHtml="animal_detail_upd_ins", logged_in=current_user.is_authenticated))
            else:
                return redirect(url_for('dashboard', loadHtml="animal_registry", logged_in=current_user.is_authenticated))

    return render_template("index.html", loadHtml="login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('user is now logged out ')
    return render_template("index.html", loadHtml="login_error")

@app.route('/reset_password', methods=["GET","POST"] )
@login_required
def reset_password():

    if request.method == "POST":
        user_email=request.form.get('email')

    return render_template("index.html", loadHtml="reset_password",
        logged_in=current_user.is_authenticated,
        user_email=user_email )

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
        
        flash(f"New user created for {request.form.get('email')} / login to start")
        return render_template("index.html", loadHtml="login_success")

    return render_template("index.html", loadHtml="register", 
    logged_in=current_user.is_authenticated)

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
        Asset_breeding_result = Asset_breeding.query.filter(Asset_breeding.asset_registry_id == record['id']).all()
        db_session.commit()
        #db_session.close()
        Asset_breeding_dict = sql_result_to_dict(Asset_breeding_result)

        record['Asset_breeding'] = Asset_breeding_dict

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


@app.route("/asset_registry", methods=["GET"]) 
@login_required
def asset_registry():

    # Get all row at least 1 row must exist
    list_of_columns = [Asset_registry.id,
            Asset_registry.animal_reg_no,
            Asset_registry.group_name,
            Asset_registry.asset_type,
            Asset_registry.gender,
            Asset_registry.date_of_birth,
            Asset_registry.tag_id,
            Asset_registry.father_id,
            Asset_registry.mother_id]

    # columns dictonary name
    col_list = [
        "id",
        "animal_reg_no",
        "group_name",
        "asset_type",
        "gender",
        "date_of_birth",
        "tag_id",
        "father_id",
        "mother_id"
        ]
    
    # columns dictonary name
    col_header = [
        "id",
        "Animal Reg No",
        "Group",
        "Type",
        "Gender",
        "Date of Birth",
        "Tag No",
        "Father Id",
        "Mother Id"
        ]

    try:
        sql_result = db_session.query(
            *list_of_columns
        ).filter(Asset_registry.users_id == current_user.id).all()
    finally:
        # if table has no entries -> send to new animal register
        if len(sql_result) == 0 :
            return redirect(url_for('new_animal_register', 
                loadHtml="new_animal_register", 
                logged_in=current_user.is_authenticated,
                user_id=current_user.id))

    record_dict = sql_result_column_list_to_dict(col_list, sql_result)

    return render_template("index.html", loadHtml="asset_registry", 
        logged_in=current_user.is_authenticated, 
        user_id=current_user.id, record_list=record_dict,
        rec_list_count= len(record_dict), method=request.method,
             list_of_columns=col_list, col_header=col_header)

@app.route("/animal_detail_upd_ins", methods=["GET","POST"]) 
@login_required
def animal_detail_upd_ins():

    father_dict = get_father_dict()
    mother_dict = get_mother_dict()
    breeding_dict = get_breeding_dict()

    mode = request.form.get('mode')

    if mode == "display" :
        asset_id = request.form.get('asset_id')
        animal_reg_no = request.form.get('animal_reg_no')

        sql_result = db_session.query(Asset_registry).filter(Asset_registry.id == asset_id).all()

        record_dict = sql_result_to_dict(sql_result)
        date_of_birth = html_date(record_dict[0]["date_of_birth"])

        return render_template("index.html", loadHtml="animal_detail_upd_ins", 
            logged_in=current_user.is_authenticated, 
            asset_id=asset_id, animal_reg_no=animal_reg_no,
            group_dropdown=Animal_dropdown.keys(),
            type_dropdown=Animal_dropdown,
            father_dict=father_dict,
            mother_dict=mother_dict,
            breeding_dict=breeding_dict,
            record_dict = record_dict[0], date_of_birth=date_of_birth,

            user_id=current_user.id )

    if mode == "delete" :
        asset_id = request.form.get('lineid')
        
        new_rec = db_session.query(Asset_registry).filter(Asset_registry.id == asset_id).first()
         
        # delete record
        db_session.delete(new_rec)
        db_session.commit()

        # redirect to asset_registry list
        return redirect(url_for('asset_registry', loadHtml="asset_registry", 
        logged_in=current_user.is_authenticated))

    if mode == "update" :
        asset_id = request.form.get('id')

        record_upd = db_session.query(Asset_registry).filter(Asset_registry.id == asset_id).first()
        
        if bool(record_upd) == False :
            # new record : insert blank line and then update
            app.logger.info(f"Insert : new record")
            randnum = random()
            new_rec = Asset_registry()
            new_rec.users_id  = current_user.id
            random_animal_name = f"{current_user.id}{randnum}"
            new_rec.animal_reg_no  = random_animal_name
            db_session.add(new_rec)
            db_session.commit()

            record_upd = db_session.query(Asset_registry).filter(Asset_registry.animal_reg_no  == random_animal_name).first()
        
        record_upd.users_id  = current_user.id
        record_upd.animal_reg_no  = request.form.get('animal_reg_no')
        record_upd.asset_type  = request.form.get('asset_type')
        record_upd.group_name  = request.form.get('group_name')
        record_upd.date_of_birth  = request.form.get('date_of_birth')
        record_upd.gender  = request.form.get('gender')
        record_upd.father_id  = check_null(request.form.get('father_id'))
        record_upd.father_note  = request.form.get('father_note')
        record_upd.mother_id  = check_null(request.form.get('mother_id'))
        record_upd.mother_note  = request.form.get('mother_note')

        db_session.commit()

        # redirect to asset_registry list
        return redirect(url_for('asset_registry', 
        loadHtml="asset_registry", logged_in=current_user.is_authenticated))

    #  Default empty return 
    return render_template("index.html", loadHtml="animal_detail_upd_ins", 
                logged_in=current_user.is_authenticated, 
                asset_id=f"", animal_reg_no="",
                group_dropdown=Animal_dropdown.keys(),
                type_dropdown=Animal_dropdown,
                father_dict=father_dict,
                mother_dict=mother_dict,
                breeding_dict=breeding_dict,
                user_id=current_user.id )

@app.route("/animal_medical_upd_ins", methods=["GET","POST"]) 
@login_required
def animal_medical_upd_ins():
    mode = request.form.get('mode')

    if mode == "new_rec" : # req from asset_registry page

        asset_id = request.form.get('asset_id')

        return render_template("index.html", loadHtml="animal_medical_upd_ins", \
            logged_in=current_user.is_authenticated, 
            asset_id=asset_id, 
            user_id=current_user.id )
    
    if mode == "display_rec" : # req from asset_registry page
        
        line_id = request.form.get('line_id')

        record_obj = db_session.query(Asset_medical).filter(Asset_medical.id == line_id).all()

        record_display = sql_result_to_dict(record_obj)

        asset_id = record_display[0]["asset_registry_id"]
        
        # Special handling for date
        html_timestamp = html_date(record_display[0]["timestamp"])
        
        return render_template("index.html", loadHtml="animal_medical_upd_ins", \
            logged_in=current_user.is_authenticated, html_timestamp=html_timestamp, \
            asset_id=asset_id, animal_reg_no="", \
            record_display=record_display[0] ,\
            user_id=current_user.id )

    if mode == "update" :
        line_id = request.form.get('line_id')

        record_upd = db_session.query(Asset_medical).filter(Asset_medical.id == line_id).first()
        
        if bool(record_upd) == False :
            # new record : insert blank line and then update
            app.logger.info(f"Insert : new record")
            randnum = random()
            new_rec = Asset_medical()
            new_rec.users_id  = current_user.id
            random_animal_name = f"{current_user.id}{randnum}"
            new_rec.reason  = random_animal_name
            db_session.add(new_rec)
            db_session.commit()

            record_upd = db_session.query(Asset_medical).filter(Asset_medical.reason  == random_animal_name).first()
        
        record_upd.users_id  = current_user.id
        record_upd.asset_registry_id  = request.form.get('asset_registry_id')
        record_upd.timestamp  = check_date(request.form.get('Timestamp'))
        record_upd.reason  = request.form.get('Reason')
        record_upd.medicine  = request.form.get('Medicine')
        record_upd.dosage  = check_null(request.form.get('Dosage'))
        record_upd.note  = request.form.get('Note')
        
        db_session.commit()

        # columns header name
        col_header = [
                "id",
                "Asset Reg No",
                "Date",
                "Reason",
                "Medicine",
                "Dosage",
                "Note"          
            ]

        # redirect to asset_medical list
        return redirect(url_for('asset_registry', 
             loadHtml="asset_registry", 
            logged_in=current_user.is_authenticated,
            col_header=col_header))

    if mode == "delete" :
        line_id = request.form.get('line_id')
        
        new_rec = db_session.query(Asset_medical).filter(Asset_medical.id == line_id).first()
         
        # delete record
        db_session.delete(new_rec)
        db_session.commit()

        # redirect to asset_medical list
        return redirect(url_for('asset_registry', loadHtml="asset_registry", logged_in=current_user.is_authenticated))

    
@app.route("/animal_produce_upd_ins", methods=["GET","POST"]) 
@login_required
def animal_produce_upd_ins():
                                                           
    mode = request.form.get('mode')

    if mode == "new_rec":
        asset_id = request.form.get('asset_id')

        return render_template("index.html", loadHtml="animal_produce_upd_ins", 
            logged_in=current_user.is_authenticated, 
            asset_id=asset_id,
            user_id=current_user.id)

    if mode == "display_rec" :
        line_id = request.form.get('line_id')
        animal_reg_no = request.form.get('animal_reg_no')

        record_obj = db_session.query(Asset_produce).filter(Asset_produce.id == line_id).all()

        record_display = sql_result_to_dict(record_obj)
        
        # Special handling for date
        html_timestamp = html_date(record_display[0]["timestamp"])
        asset_id = record_display[0]["asset_registry_id"]
        
        return render_template("index.html", loadHtml="animal_produce_upd_ins", 
            logged_in=current_user.is_authenticated, html_timestamp=html_timestamp,
            asset_id=asset_id, animal_reg_no=animal_reg_no, line_id=line_id,
            record_display=record_display[0], user_id=current_user.id)
    
    if mode == "update" :
        # insert new rec  or update existing rec
        line_id = request.form.get('line_id')
        
        record_upd = db_session.query(Asset_produce).filter(Asset_produce.id == line_id).first()
        
        # check if record exitsts else new record : insert blank line and then update
        if bool(record_upd) == False :
            
            app.logger.info(f"Insert : new record")
            randnum = random()
            new_rec = Asset_produce()
            new_rec.users_id  = current_user.id
            random_animal_name = f"{current_user.id}{randnum}"
            new_rec.note  = random_animal_name
            db_session.add(new_rec)
            db_session.commit()

            record_upd = db_session.query(Asset_produce).filter(Asset_produce.note  == random_animal_name).first()
        
        record_upd.users_id  = current_user.id
        record_upd.asset_registry_id  = request.form.get('asset_id')
        record_upd.timestamp  = request.form.get('Timestamp')
        record_upd.type  = request.form.get('Type')
        record_upd.quantity  = request.form.get('Quantity')
        record_upd.measurement  = request.form.get('Measurement')
        record_upd.note  = request.form.get('Note')
    
        db_session.commit()

        # redirect to asset_registry list
        return redirect(url_for('asset_produce', 
            loadHtml="asset_produce", 
            logged_in=current_user.is_authenticated))


    if mode == "delete" :
        line_id = request.form.get('line_id')
        
        new_rec = db_session.query(Asset_produce).filter(Asset_produce.id == line_id).first()
        
        # delete record
        db_session.delete(new_rec)
        db_session.commit()

        # redirect to asset_registry list
        return redirect(url_for('asset_produce', loadHtml="asset_produce", logged_in=current_user.is_authenticated))

@app.route("/animal_breeding_upd_ins", methods=["GET","POST"]) 
@login_required
def animal_breeding_upd_ins():
    mode = request.form.get('mode')

    father_dict = get_father_dict()
    mother_dict = get_mother_dict()
    # =========================

    if mode == "new_rec" : # req from asset_breeding page

        asset_id = request.form.get('asset_id')

        return render_template("index.html", loadHtml="animal_breeding_upd_ins",
            logged_in=current_user.is_authenticated, 
            asset_id=asset_id, 
            user_id=current_user.id,
            mother_dict=mother_dict,
            father_dict=father_dict )
    
    if mode == "display_rec" : # req from asset_registry page
        
        line_id = request.form.get('line_id')

        record_obj = db_session.query(Asset_breeding).filter(Asset_breeding.id == line_id).all()

        record_display = sql_result_to_dict(record_obj)
        
        # Special handling for date
        html_start_date = html_date(record_display[0]["start_date"])
        html_end_date = html_date(record_display[0]["end_date"])
        
        return render_template("index.html", loadHtml="animal_breeding_upd_ins", 
            logged_in=current_user.is_authenticated, 
            html_start_date=html_start_date, 
            html_end_date=html_end_date, record_display=record_display[0] ,
            user_id=current_user.id, 
            mother_dict=mother_dict,
            father_dict=father_dict)

    if mode == "update" :
        line_id = request.form.get('line_id')

        record_upd = db_session.query(Asset_breeding).filter(Asset_breeding.id == line_id).first()
        
        if bool(record_upd) == False :
            # new record : insert blank line and then update
            app.logger.info(f"Insert : new record")
            randnum = random()
            new_rec = Asset_breeding()
            new_rec.users_id  = current_user.id
            random_animal_name = f"{current_user.id}{randnum}"
            new_rec.notes  = random_animal_name
            db_session.add(new_rec)
            db_session.commit()

            record_upd = db_session.query(Asset_breeding).filter(Asset_breeding.notes  == random_animal_name).first()
        
        record_upd.users_id  = current_user.id
        record_upd.breeding_number  = request.form.get('Breeding_number')
        record_upd.start_date  = check_date(request.form.get('Start_date'))
        record_upd.end_date  = check_date(request.form.get('End_date'))
        record_upd.pregnant  = check_date(request.form.get('Pregnant'))
        record_upd.asset_registry_father_id  = request.form.get('Father_id')
        record_upd.asset_registry_mother_id  = request.form.get('Mother_id')
        record_upd.notes  = request.form.get('Notes')
        

        db_session.commit()

        # redirect to asset_breeding list
        return redirect(url_for('asset_breeding', loadHtml="Asset_breeding", \
            logged_in=current_user.is_authenticated))

    if mode == "delete" :
        line_id = request.form.get('line_id')
        
        new_rec = db_session.query(Asset_breeding).filter(Asset_breeding.id == line_id).first()
         
        # delete record
        db_session.delete(new_rec)
        db_session.commit()

        # redirect to asset_breeding list
        return redirect(url_for('asset_breeding', loadHtml="Asset_breeding", logged_in=current_user.is_authenticated))


@app.route("/asset_medical", methods=["GET"]) 
@login_required
def asset_medical():

    # Get all row at least 1 row must exist
    list_of_columns = [Asset_medical.id,
            Asset_medical.asset_registry_id,
            Asset_medical.timestamp,
            Asset_medical.reason,
            Asset_medical.medicine,
            Asset_medical.dosage,
            Asset_medical.note
            ]

    # columns dict name
    col_list = [
                "id",
                "asset_registry_id",
                "timestamp",
                "reason",
                "medicine",
                "dosage",
                "note"
    ]

     # columns header name
    col_header = [
                "id",
                "Asset Reg No",
                "Date",
                "Reason",
                "Medicine",
                "Dosage",
                "Note"          
    ]

    try:
        sql_result = db_session.query(
            *list_of_columns
        ).filter(Asset_medical.users_id == current_user.id).all()
    finally:
        # if table has no entries -> send to asset registry
        if len(sql_result) == 0 :
            return redirect(url_for('asset_registry', 
                loadHtml="asset_registry", 
                logged_in=current_user.is_authenticated,
                user_id=current_user.id))

    record_dict = sql_result_column_list_to_dict(col_list, sql_result)


    return render_template("index.html", loadHtml="asset_medical", 
        logged_in=current_user.is_authenticated, 
        med_record_list=record_dict,
        med_rec_list_count= len(record_dict),
        med_col_header=col_header,
        button_display="no")

#========================

@app.route("/asset_breeding", methods=["GET"]) 
@login_required
def asset_breeding():

    # Get all row at least 1 row must exist
    list_of_columns = [Asset_breeding.id,
            Asset_breeding.breeding_number,
            Asset_breeding.start_date,
            Asset_breeding.end_date,
            Asset_breeding.pregnant,
            Asset_breeding.asset_registry_father_id,
            Asset_breeding.asset_registry_mother_id
            ]

    # columns headings
    col_list = [
                "id",
                "breeding_number",
                "start_date",
                "end_date",
                "pregnant",
                "asset_registry_father_id",
                "asset_registry_mother_id"
    ]

    # columns headings
    col_header = [
                "id",
                "Breeding Number",
                "Start Date",
                "End Date",
                "Pregnant",
                "Father id",
                "Mother id"
    ]

    try:
        sql_result = db_session.query(
            *list_of_columns
        ).filter(Asset_breeding.users_id == current_user.id).all()
    finally:
        # if table has no entries -> send to asset registry
        if len(sql_result) == 0 :
            return redirect(url_for('asset_registry', 
                loadHtml="asset_registry", 
                logged_in=current_user.is_authenticated,
                user_id=current_user.id))

    record_dict = sql_result_column_list_to_dict(col_list, sql_result)


    return render_template("index.html", loadHtml="asset_breeding", 
        logged_in=current_user.is_authenticated, breeding_record_list=record_dict,
        breeding_rec_list_count= len(record_dict),
        breeding_column_list=col_list, 
        breeding_col_header=col_header)

    # ==========================

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

@app.route("/asset_produce", methods=["GET"]) 
@login_required
def asset_produce():
    
    # Get all row at least 1 row must exist
    list_of_columns = [Asset_produce.id,
            Asset_produce.asset_registry_id,
            Asset_produce.timestamp,
            Asset_produce.type,
            Asset_produce.measurement,
            Asset_produce.quantity,
            Asset_produce.note]

    # columns dict names
    col_list = [
                "id",
                "asset_registry_id",
                "timestamp",
                "type",
                "measurement",
                "quantity",
                "note"
    ]

    # columns headers
    col_header_list = [
                "id",
                "Asset Reg No",
                "Date",
                "Type",
                "Measurement",
                "Quantity",
                "Notes"
    ]

    try:
        sql_result = db_session.query(
            *list_of_columns
        ).filter(Asset_produce.users_id == current_user.id).all()
    finally:
        # if table has no entries -> send to asset registry
        if len(sql_result) == 0 :
            return redirect(url_for('asset_registry', 
                loadHtml="asset_registry", 
                logged_in=current_user.is_authenticated,
                user_id=current_user.id))

    record_dict = sql_result_column_list_to_dict(col_list, sql_result)


    return render_template("index.html", loadHtml="asset_produce", 
        logged_in=current_user.is_authenticated, 
        produce_record_list=record_dict,
        produce_rec_list_count=len(record_dict), 
        produce_column_list=col_list,
        produce_col_header_list=col_header_list)

@app.route("/dashboard")
@login_required
def dashboard():

    # Get all row at least 1 row must exist
    list_of_columns = [Asset_registry.id,
            Asset_registry.animal_reg_no,
            Asset_registry.group_name,
            Asset_registry.asset_type,
            Asset_registry.gender,
            Asset_registry.tag_id,
            Asset_registry.date_of_birth ]

    # columns headings
    col_list = [
        "id",
        "animal_reg_no",
        "group_name",
        "breed_type",
        "gender",
        "tag_id",
        "date_of_birth"
        ]

    # columns dictonary name
    col_header = [
        "id",
        "Animal Reg No",
        "Group",
        "Type",
        "Gender",        
        "Tag No",
        "Date of Birth"
        ]

    try:
        sql_result = db_session.query(
            *list_of_columns
        ).filter(Asset_registry.users_id == current_user.id).all()
    except:
        return render_template("index.html", loadHtml="new_animal_register", \
        logged_in=current_user.is_authenticated )
    else:
        # if table has no entries -> send to new animal register
        if len(sql_result) == 0 :
            return redirect(url_for('new_animal_register', \
                loadHtml="new_animal_register", \
                logged_in=current_user.is_authenticated,\
                user_id=current_user.id))

    record_dict = sql_result_column_list_to_dict(col_list, sql_result)

    # end - display registry

    #====== start maps / charts =============

    # get total tags for user
    total_tags = db_session.query(Asset_registry).\
        filter(and_(Asset_registry.users_id == current_user.id, Asset_registry.tag_id.isnot(None))).count()
    
    # get current location for tags
    hour_48 = datetime.now() - timedelta(hours=48)
    tags_read_48 = db_session.query(Tag, Tag_current).\
        filter(and_(Tag.id == Tag_current.id, 
              Tag.users_id == current_user.id,
              Tag_current.timestamp > hour_48)).\
            count()

    # get current location for tags
    
    tag_list = db_session.query(Tag_current, Tag).\
        filter(and_(Tag_current.id == Tag.id,
        Tag.users_id == current_user.id)).all()
    
    new_list = []
    for x in tag_list:        
        new_list.append(x[0])

    tag_dict = sql_result_to_dict(new_list)
   
    loadJson = {}
    loadJson['total_tags'] = total_tags
    loadJson['tags'] = tag_dict
    loadJson['tags_read'] = len(tag_dict)
    loadJson['tags_read_48'] = tags_read_48

    # JSON.dumps convert dict to JSONstring
    loadJson2 = json.dumps(loadJson)

    # end - map / charts

    return render_template("index.html", loadHtml="dashboard", 
        logged_in=current_user.is_authenticated, 
        user_id=current_user.id, record_list=record_dict,
        rec_list_count= len(record_dict), method=request.method,
             list_of_columns=col_list, loadJson=loadJson2,
             col_header=col_header )

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
         

    return render_template("index.html", loadHtml="report_overview", 
    logged_in=current_user.is_authenticated, loadJson=loadJson , 
    base_list=all_base_current_dict, 
    total_base=len(all_base_current_dict), hour=hour)

@app.route("/report_overview", methods=["GET","POST"])
@login_required
def report_overview():

    if request.method == "GET":
        fromDate = None       
                      
    if request.method == "POST":
        fromDate = request.form.get('fromDate')
        toDate = request.form.get('toDate')  

    # get total tags for user
    total_tags = db_session.query(Asset_registry).\
        filter(and_(Asset_registry.users_id == current_user.id, Asset_registry.tag_id.isnot(None))).count()
    
    # get current location for tags
    hour_48 = datetime.now() - timedelta(hours=48)
    tags_read_48 = db_session.query(Tag, Tag_current).\
        filter(and_(Tag.id == Tag_current.id, 
              Tag.users_id == current_user.id,
              Tag_current.timestamp > hour_48)).\
            count()

    # get current location for tags
    if fromDate :
        # fromDate_py = datetime.now() - timedelta(hours=48)
        # toDate_py = datetime.now() - timedelta(hours=48)

        tag_list = db_session.query(Tag_current, Tag).\
            filter(and_(Tag_current.id == Tag.id,
                Tag.users_id == current_user.id,
              Tag_current.timestamp > fromDate,
              Tag_current.timestamp < toDate )).all()
    else:
        tag_list = db_session.query(Tag_current, Tag).\
            filter(and_(Tag_current.id == Tag.id,
            Tag.users_id == current_user.id)).all()
    
    new_list = []
    for x in tag_list:        
        new_list.append(x[0])

    tag_dict = sql_result_to_dict(new_list)
   
    loadJson = {}
    loadJson['total_tags'] = total_tags
    loadJson['tags'] = tag_dict
    loadJson['tags_read'] = len(tag_dict)
    loadJson['tags_read_48'] = tags_read_48

    # JSON.dumps convert dict to JSONstring
    loadJson2 = json.dumps(loadJson)

    return render_template("index.html", 
    loadHtml="report_overview",
    logged_in=current_user.is_authenticated, 
    loadJson=loadJson2 )

    # ===================   end report_overview =========

@app.route("/report_tags", methods=["GET","POST"])
@login_required
def report_tags():

    if request.method == "GET":
        fromDate = None
        inTag = None
                      
    if request.method == "POST":
        fromDate = request.form.get('fromDate')
        toDate = request.form.get('toDate') 
        inTag = request.form.get('tag_id')  

    # get total tags for user
    total_tags = db_session.query(Asset_registry).\
        filter(and_(Asset_registry.users_id == current_user.id, Asset_registry.tag_id.isnot(None))).count()
    
    # get current location for tags
    hour_48 = datetime.now() - timedelta(hours=48)
    tags_read_48 = db_session.query(Tag, Tag_current).\
        filter(and_(Tag.id == Tag_current.id, 
              Tag.users_id == current_user.id,
              Tag_current.timestamp > hour_48)).\
            count()

    # get current location for tags
    if fromDate and inTag != "All":
        
        tag_list = db_session.query(Tag_current, Tag).\
            filter(and_(Tag_current.id == Tag.id,
                Tag.users_id == current_user.id,
              Tag_current.timestamp > fromDate,
              Tag_current.timestamp < toDate,
              Tag_current.id == inTag )).all()
    else:
        tag_list = db_session.query(Tag_current, Tag).\
            filter(and_(Tag_current.id == Tag.id,
            Tag.users_id == current_user.id)).all()
    
    new_list = []
    for x in tag_list:        
        new_list.append(x[0])

    tag_dict = sql_result_to_dict(new_list)

    tags = []
    for x in tag_list:        
        tags.append(x[1])

    tag_detail = sql_result_to_dict(tags)
   
    loadJson = {}
    loadJson['total_tags'] = total_tags
    loadJson['tags'] = tag_dict
    loadJson['tags_read'] = len(tag_dict)
    loadJson['tags_read_48'] = tags_read_48

    # JSON.dumps convert dict to JSONstring
    loadJson2 = json.dumps(loadJson)

    return render_template("index.html", 
    loadHtml="report_tags",
    logged_in=current_user.is_authenticated, 
    loadJson=loadJson2,
    tags=tag_detail)

    # ===================   end report_tags =========


@app.route("/report_base_station", methods=["GET","POST"])
@login_required
def report_base_station():

    if request.method == "GET":
        fromDate = None
        inBase = None
                      
    if request.method == "POST":
        fromDate = request.form.get('fromDate')
        toDate = request.form.get('toDate') 
        inBase = request.form.get('Base_staion')  

    # get total tags for user
    total_tags = db_session.query(Asset_registry).\
        filter(and_(Asset_registry.users_id == current_user.id, 
                 Asset_registry.tag_id.isnot(None))).count()
                
    if total_tags == 0 :
        return render_template("index.html", loadHtml="new_animal_register", \
        logged_in=current_user.is_authenticated )
    
    # get total base_stations for user
    total_base_stations = db_session.query(Base_station).\
        filter(Base_station.users_id == current_user.id).count()
    
    if total_base_stations == 0 :
        return render_template("index.html", loadHtml="new_animal_register", \
        logged_in=current_user.is_authenticated )
    
    # get count of (all) tags scanned at (all) basestation for the past 48 hours
    hour_48 = datetime.now() - timedelta(hours=48)
    tags_read_48 = db_session.query(Tag, Tag_current).\
        filter(and_(Tag.id == Tag_current.id, 
              Tag.users_id == current_user.id,
              Tag_current.timestamp > hour_48)).\
            count()

    # get (current) location for base_stations
    if fromDate and inBase != "All":
        
        base_stations_current_location = db_session.\
            query(Base_station_hist, Base_station).\
                filter(and_(Base_station_hist.base_id == Base_station.id,
                Base_station.users_id == current_user.id,
                Base_station_hist.base_id == inBase
                )).all()
    else:
        base_stations_current_location = db_session.\
            query(Base_station_current, Base_station).\
                filter(and_(Base_station_current.id == Base_station.id,
                Base_station.users_id == current_user.id)).all()
    
    # split result of 1 table (base_station_current)
   
    base_station_current_list = []
    for x in base_stations_current_location:        
        base_station_current_list.append(x[0]) # 1st table result store in index 0

    base_station_current_dict = sql_result_to_dict(base_station_current_list)

    # get count of tags currently at each base_ station
    count_tags_per_base_station_current = MissingSock_sql.cnt_tags_at_each_base_station(current_user.id)
   
    loadJson = {}
    loadJson['total_tags'] = total_tags
    loadJson['total_base_stations'] = total_base_stations
    loadJson['base_stations'] = base_station_current_dict
    
    loadJson['tags_read_48_all_base_stations'] = tags_read_48
    loadJson['count_tags_per_base_station_current'] = count_tags_per_base_station_current

    # JSON.dumps convert dict to JSONstring
    loadJson2 = json.dumps(loadJson)

    return render_template("index.html", 
    loadHtml="report_base_station",
    logged_in=current_user.is_authenticated, 
    loadJson=loadJson2, Base_station_list=base_station_current_dict )

    # ===================   end report_base_station =========

@app.route("/animal_profile_page", methods=["GET","POST"])
@login_required
def animal_profile_page():

    # animal_detail_upd_ins.html - update info 
    asset_id = request.form.get('Animal_id')

    sql_result = db_session.query(Asset_registry).filter(Asset_registry.id == asset_id).all()
    record_dict = sql_result_to_dict(sql_result)
    date_of_birth = html_date(record_dict[0]["date_of_birth"])
    animal_reg_no=record_dict[0]["animal_reg_no"]

    
    #======================================================================================
    
    # Asset_medical.html
    # Get all row at least 1 row must exist
    medical_list_of_columns = [Asset_medical.id,
            Asset_medical.asset_registry_id,
            Asset_medical.timestamp,
            Asset_medical.reason,
            Asset_medical.medicine,
            Asset_medical.dosage,
            Asset_medical.note
            ]

    # columns dict name
    medical_dict_name_list = [
                "id",
                "asset_registry_id",
                "timestamp",
                "reason",
                "medicine",
                "dosage",
                "note"
    ]

     # columns header name
    medical_col_header = [
                "id",
                "Asset Reg No",
                "Date",
                "Reason",
                "Medicine",
                "Dosage",
                "Note"          
    ]

    try:
        sql_result = db_session.query(
            *medical_list_of_columns
        ).filter(Asset_medical.asset_registry_id == asset_id).all()
    finally:
        # if table has no entries -> send to asset registry
        medical_record_dict = [{'id':'0'}]

    medical_record_dict = sql_result_column_list_to_dict(medical_dict_name_list, sql_result)

    #======================================================================================

    # Asset_produce

    produce_list_of_columns = [Asset_produce.id,
             Asset_produce.type, Asset_produce.timestamp, 
             Asset_produce.quantity, Asset_produce.measurement,
             Asset_produce.note, Asset_produce.asset_registry_id
    ]

    # name in form used for columns
    produce_dict_name_list = ["id", "type", "timestamp", "quantity",
           "measurement", "note", "asset_id"
    ]

    # columns headings
    produce_col_list = ["id", "Type", "Date", "Quantity",
           "Measurement", "Note", "asset_id"
    ]

    try:
        sql_result = db_session.query(
            *produce_list_of_columns
        ).filter(Asset_produce.asset_registry_id == asset_id).all()
    finally:
        # if table has no entries -> send empty dict
        produce_record_dict = [{'id':'0'}]

    produce_record_dict = sql_result_column_list_to_dict(produce_dict_name_list, sql_result)

    #==================================================================================

    return render_template("index.html", 
    loadHtml="animal_profile_page", logged_in=current_user.is_authenticated,
     record_dict = record_dict[0], 
     date_of_birth=date_of_birth, asset_id=asset_id,
     animal_reg_no=animal_reg_no,
    med_record_list=medical_record_dict, 
    med_rec_list_count= len(medical_record_dict),  
    med_col_header=medical_col_header, 
     produce_record_list=produce_record_dict, 
     produce_column_list=produce_col_list,
     produce_rec_list_count= len(produce_record_dict) ,
    button_display="yes" 
    )


def check_null(val):

    if len(val) == 0 :
        val = None
    elif val == 'None':
        val = None

    return val

def check_date(val):

    if val == 'None':
        today = date.today()
        val = today.strftime("%Y-%m-%d")

    return val

def html_date(val):

    date_time_obj = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
    val = date_time_obj.strftime("%Y-%m-%d")

    return val

def get_father_dict() :
    # Father list

    # Get all row at least 1 row must exist
    list_of_columns = [Asset_registry.id,
            Asset_registry.animal_reg_no
            ]

    # columns headings
    col_list = [
                "id",
                "animal_reg_no"
    ]
    try:
        sql_result = db_session.query(
            *list_of_columns
        ).filter(and_(Asset_registry.users_id == current_user.id, 
                Asset_registry.gender == "male" )).all()
    except:
        # if table has no entries -> send to asset registry
        return {"id":0, "animal_reg_no": 0}

    father_dict = sql_result_column_list_to_dict(col_list, sql_result)

    return father_dict

def get_mother_dict():

    # Mother list

    # Get all row at least 1 row must exist
    list_of_columns = [Asset_registry.id,
            Asset_registry.animal_reg_no
            ]

    # columns headings
    col_list = [
                "id",
                "animal_reg_no"
    ]
    try:
        sql_result = db_session.query(
            *list_of_columns
        ).filter(and_(Asset_registry.users_id == current_user.id, 
                Asset_registry.gender == "female" )).all()
    except:
        # if table has no entries -> send to asset registry
        return {"id":0, "animal_reg_no": 0}

    mother_dict = sql_result_column_list_to_dict(col_list, sql_result)

    return mother_dict

def get_breeding_dict():

    # Mother list

    # Get all row at least 1 row must exist
    list_of_columns = [Asset_breeding.id,
            Asset_breeding.breeding_number
            ]

    # columns headings
    col_list = [
                "id",
                "breeding_number"
    ]
    try:
        sql_result = db_session.query(
            *list_of_columns
        ).filter(Asset_breeding.users_id == current_user.id).all()
    except:
        return {"id":0, "breeding_number": 0}

    mother_dict = sql_result_column_list_to_dict(col_list, sql_result)

    return mother_dict


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

