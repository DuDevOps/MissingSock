from flask import Flask, render_template, request, url_for
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta

import json

from MissingSockDBQueries import MissingSockDb

app = Flask(__name__)
CORS(app)

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html", loadHtml="dashboard")

@app.route("/dashboard")
def dashboard():
    total_stations = MissingSockDb.get_total_base_stations()
    total_tags = MissingSockDb.get_total_tags()
    total_assets = MissingSockDb.get_total_assets()

    base_station_current = MissingSockDb.get_base_station_current()

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
    loadJson += f"'base_stations' : {json.dumps(base_station_current)} ,"
    loadJson += f"'total_stations': {json.dumps(total_stations)} ,"
    loadJson += f"'total_tags': {json.dumps(total_tags)} ,"
    loadJson += f"'total_assets': {json.dumps(total_assets)} ,"
    loadJson += "'middle_point': {" + f"'lat':'{str(lat_middle)}', 'long':'{str(long_middle)}' " + "},"
    loadJson += "}"
    
    # print(f"{loadJson}")
    
    sql_return = MissingSockDb.get_tag()

    return render_template("index.html", loadHtml="dashboard", dashboard=sql_return, loadJson=loadJson, tag_count=total_tags, \
           base_stations_count=total_stations[0], asset_count=total_assets[0],\
           base_station_current=base_station_current )

@app.route("/basestations")
def base_station():
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
    loadJson += f"'base_stations' : {json.dumps(base_station_current)} ,"
    loadJson += "'middle_point': {" + f"'lat':'{str(lat_middle)}', 'long':'{str(long_middle)}' " + "}"
    loadJson += "}"
    
    return render_template("index.html", loadHtml="base_stations",  loadJson=loadJson, base_stations=base_station_current , total_stations=count)

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

@app.route("/report_last_at_basestation")
def report_last_at_basestation():
    total_stations = MissingSockDb.get_total_base_stations()
    total_tags = MissingSockDb.get_total_tags()
    total_assets = MissingSockDb.get_total_assets()

    sql_return = MissingSockDb.get_report_last_at_basestation()
    

    date_1_hour_ago = datetime.now() - timedelta(hours=1)
    date_1_days_ago = datetime.now() - timedelta(days=1)
    date_7_days_ago = datetime.now() - timedelta(days=7)
    
    dashboard_list=[]

    for idx, record in enumerate(sql_return):
        new_item = record

        hour_1 = MissingSockDb.get_tags_at_basestation_date(record['base_id'],date_1_hour_ago)
        days_1 = MissingSockDb.get_tags_at_basestation_date(record['base_id'],date_1_days_ago)
        days_7 = MissingSockDb.get_tags_at_basestation_date(record['base_id'],date_7_days_ago)
        
        new_item['past_hour'] = hour_1[0]['count']
        new_item['past_day_1'] = days_1[0]['count']
        new_item['past_day_7'] = days_7[0]['count']

        dashboard_list.append(new_item)

    return render_template("index.html", loadHtml="report_last_at_basestation", dashboard=dashboard_list , tag_count=total_tags, base_stations_count=total_stations[0], asset_count=total_assets[0] )


if __name__ == "__main__":
    app.run(debug=True, port=5110)

