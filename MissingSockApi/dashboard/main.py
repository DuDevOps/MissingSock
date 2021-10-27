from flask import Flask, render_template, request, url_for
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# get basestation from DB for user
db = sqlite3.connect("missingsock.db")
cursor = db.cursor()

def get_sql(sql):
    db = sqlite3.connect("missingsock.db")
    cursor = db.cursor()
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    return sql_result

def get_total_tags():
    sql_query = " select count(*) from tag_name "
    
    result = get_sql(sql_query)
    return result

def get_tags_at_basestation_date(base_id, dateto, datefrom):
    sql_query = '''
        select count(*) from base_sync
        where  
    '''
    sql_query += f" base_id = '{base_id}' "
    sql_query += f" and timestamp >= {dateto} "
    sql_query += f" and timestamp <= {datefrom} "

    result = get_sql(sql_query)
    return result

def get_base_stations():

    # Get Base Stations + location + last tag 
    
    sql_query = '''
    select a.id, a.base_id, a.tag_id, a.timestamp, a.RSSI, a.sync_id,
                                       b.nicename, a.gps_lat, a.gps_long
                                    from base_sync a
                                    left join base_station b on a.base_id = b.base_id
                                    where a.base_id||a.timestamp in (
                                    select distinct a.base_id||max(a.timestamp)
                                     from base_sync a
                                     group by a.base_id)
            '''

    result = get_sql(sql_query)
    return result

def set_base_station(base_station_json):
    
    sql_query = "update base_station (id, base_id, nicename, user_id)"
    sql_query += f"set id = {base_station_json['id']} ,"
    sql_query += f"base_id = {base_station_json['base_id']} ,"
    sql_query += f"nicename = {base_station_json['nicename']} ,"
    sql_query += f"user_id = {base_station_json['user_id']} "
    sql_query += f"where id = {base_station_json['id']} "


    result = get_sql(sql_query)
    return result

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html", loadHtml="dashboard")

@app.route("/dashboard")
def dashboard():
    return render_template("index.html", loadHtml="dashboard")

@app.route("/basestations")
def base_station():
    sql_result = get_base_stations()
    total_tags = get_total_tags()

    
    # date_1_hour_ago = datetime.now() - timedelta(days=7)
    # date_1_days_ago = datetime.now() - timedelta(days=7)
    # date_7_days_ago = datetime.now() - timedelta(days=7)

    # for x in sql_result:
    #     hour_1 = get_tags_at_basestation_date(x[1],date_1_hour_ago,datetime.now())
    #     days_1 = get_tags_at_basestation_date(x[1],date_1_days_ago,datetime.now())
    #     days_7 = get_tags_at_basestation_date(x[1],date_1_days_ago,datetime.now())

    #     x.append({"hour_1":hour_1, "days_1":days_1, "days_7":days_7})

    return render_template("index.html", loadHtml="basestations", base_stations=sql_result , total_tag=total_tags[0][0])

@app.route("/tags")
def tags():
    return render_template("index.html", loadHtml="tags")

if __name__ == "__main__":
    app.run(debug=True, port=5110)

