from flask import Flask, render_template, request, url_for, request
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta

import json

from MissingSockDBQueries import MissingSockDb

app = Flask(__name__)
CORS(app)

def get_base_stations():
    base_station_current = MissingSockDb.get_base_station()
    count = len(base_station_current)

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
    loadJson += '"middle_point": {' + f'"lat":"{str(lat_middle)}", "long":"{str(long_middle)}" ' + '}'
    loadJson += "}"

    return loadJson

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html", loadHtml="dashboard")

@app.route("/dashboard")
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
    # print(f"{total_stations_days_1} , {type(total_stations_days_1)}")

    loadJson ="{"
    loadJson += f'"base_stations" : {json.dumps(base_station_current)} ,'
    loadJson += f'"total_stations": {total_stations[0]["count"]} ,'
    loadJson += f'"total_tags": {json.dumps(total_tags)} ,'
    loadJson += f'"total_hours_1": {total_hours_1[0]["count"]} ,'
    loadJson += f'"total_days_1": {total_days_1[0]["count"]} ,'
    loadJson += f'"total_stations_days_1": {total_stations_days_1[0]["count"]} ,'
    loadJson += '"middle_point": {' + f'"lat":"{str(lat_middle)}", "long":"{str(long_middle)}" ' + '},'
    loadJson += "}"
    
    print(f"{loadJson}")
    
    sql_return = MissingSockDb.get_tag()

    timeNow = datetime.now().strftime("%d %B %Y %H:%M:%S")

    return render_template("index.html", loadHtml="dashboard", loadJson=loadJson, tag_count=total_tags,timeNow=timeNow )

@app.route("/basestations")
def base_station():
    
    loadJson = get_base_stations()
    # print(f"loadJson = {loadJson}")
    base_stations = json.loads(loadJson)["base_stations"]
    # print(f'base_stations = {base_stations}')
    count = len(base_stations)

    
    return render_template("index.html", loadHtml="base_stations",  loadJson=loadJson, base_stations=base_stations , total_stations=count)

@app.route("/tags")
def tags():
    all_tags = MissingSockDb.get_tag()
    count = len(all_tags)

    return render_template("index.html", loadHtml="tags", tag_list=all_tags, total_tags=count)

@app.route("/assets")
def assets():
    sql_return = MissingSockDb.get_assets()
    count = len(sql_return)

    return render_template("index.html", loadHtml="assets", asset_list=sql_return, total_assets=count)

@app.route("/report_no_read_tag_hour/<get_hours>", methods=["GET"])
@app.route("/report_no_read_tag_hour", methods=["GET","POST"])
def report_no_read_tag_hour_1(get_hours=1):
    try :
        hour = request.form["hours"]
    except :
        hour = 1
    
    if int(get_hours) > 1 :
        hour = get_hours
    
    print(f"{hour}")
    print(f"{get_hours}")

    all_tags = MissingSockDb.tags_not_read_past_hours(hour)
    count = len(all_tags)

    loadJson = get_base_stations()

    return render_template("index.html", loadHtml="report_no_read_tag_hour", loadJson=loadJson , tag_list=all_tags, total_tags=count, hour=hour)

@app.route("/report_no_read_base_hour", methods=["GET","POST"])
def report_no_read_base_hour_1(get_hours=1):
    try :
        hour = request.form["hours"]
    except :
        hour = 1
    
    if int(get_hours) > 1 :
        hour = get_hours

    all_tags = MissingSockDb.tags_not_read_past_hours(hour)
    count = len(all_tags)

    loadJson = get_base_stations()

    return render_template("index.html", loadHtml="report_no_read_base_hour", loadJson=loadJson , tag_list=all_tags, total_tags=count, hour=hour)

if __name__ == "__main__":
    app.run(debug=True, port=5110)

