import mysql.connector
from datetime import datetime, timedelta
import random

import os, sys

from time import sleep

from MissingSockDBQueries import ln_MissingSockDb as MissingSockDb



def ins_base_sync(timestamp):
    sql="insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp) "
    sql+= f" select b.base_id, a.tag_id, 28 , -28 , 20 , 100, '{timestamp}' "
    sql+=f" from base_station b , tag_name a "

    sql_return = MissingSockDb.run_commit_sql(sql)

    return sql_return

def get_new_base_sync_scan_date():
    ins_date = datetime.now() - timedelta(days=day, hours=hour , seconds=seconds )
    formattedDate = ins_date.strftime('%Y-%m-%d %H:%M:%S')
    return formattedDate

def get_gps_base_station () :
    # side markers
    marker1 = (-25.557164, 28.49824)
    marker2 = (-25.557527, 28.500515)
    marker3 = (-25.559192, 28.500756)   
    marker4 = (-25.55866, 28.498444)


def create_base_sync(days=10, user_name="famer1@gmail.com", tags=900 ):
    
    # every 10sec 1 message per tag, 
    calls_per_day=8640
    day_set=[]
    new_set=""

    # system bom at tag 9 with full 8640
    # check last tag and start from there 
    sql = " select max(sync_tag_id) maxed from tag "
    sql_return = MissingSockDb.run_sql(sql)

    try :
        start_at_tag = sql_return[0]["maxed"][4:]
    except Exception as e:
        print(f" exception = {e}")
        start_at_tag = 0

    print(f"max tag = {sql_return[0]['maxed']} {start_at_tag}")

    # base_stations
    base_stations = {0:(-25.557164, 28.49824),
    1:(-25.557527, 28.500515),
    2:(-25.559192, 28.500756) ,  
    3:(-25.55866, 28.498444) }

    if start_at_tag == 0 :
        
        # get time range
        time_list = []
        for hour in range(24):
            for minute in range(60):
                for second in (10, 20, 30, 40, 50) :
                    timeIn = datetime.now() - timedelta(days= 1 , hours= hour, minutes= minute, seconds= second)
                    timeFormat = timeIn.strftime('%Y-%m-%d %H:%M:%S')

                    time_list.append(timeFormat)

        # print(f"{time_list} , {len(time_list)}")

        tag = 0

        print(f"insert day 1 for Tag {tag} / {tags}")
        for count, scan in enumerate(time_list):
            # insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp)
            module_3 = len(time_list)/3
            base = round((count / module_3))

            # use 4 base in 4 even spread for the 8640 inserts per day
            rec = []

            rec.append(f"base_{base}") 
            rec.append(f"tag_{tag}")
            rec.append(base_stations[base][0])
            rec.append(base_stations[base][1])
            rec.append(85)
            rec.append(count)
            rec.append(scan)

            #print(f"{rec}")

            day_set.append(rec)

        for idx, rec in enumerate(day_set):
            rec_set = f"('{rec[0]}', '{rec[1]}', {rec[2]}, {rec[3]}, {rec[4]}, {rec[5]}, '{rec[6]}' ),"
            new_set += rec_set

        #print(f"{new_set}")    
        sql = f" insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp) values "
        sql += f"{new_set[:-1]}"

        MissingSockDb.run_commit_sql(sql)

        start_at_tag = 1

    # create tags not yet created for day 1
    if start_at_tag != 1 :
        pass
    else :
        for tag in range(int(start_at_tag), tags):
            print(f"insert Tag {tag} of {tags}")
            # copy tag_0 se data
            sql = " insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp)  "
            sql += f" select base_id, 'tag_{tag}', gps_lat, gps_long, rssi, sync_id, "
            sql += f" timestamp"
            sql += f" from base_sync where tag_id = 'tag_0' "

            MissingSockDb.run_commit_sql(sql)

    for day in range(2, days):

        print(f" insert Day {day} for all tags")
        timeIn = datetime.now() - timedelta(days= 1 )
        DAY_1 = timeIn.strftime('%Y-%m-%d')

        sql = " insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp)  "
        sql += f" select base_id, tag_id, gps_lat, gps_long, rssi, sync_id, "
        sql += f" DATE_SUB(timestamp, INTERVAL {day} DAY) "
        sql += f" from base_sync where timestamp like '{DAY_1}%' "

        MissingSockDb.run_commit_sql(sql)
    
    # insert asset
    sql = "insert into assets (asset_name, asset_description) "
    sql += " select 'asset' , 'some beast' from tag "

    MissingSockDb.run_commit_sql(sql)

    # check if tables are updated
    sql = " select count(*) count from tag "
    tag_count = MissingSockDb.run_sql(sql)
    print(f"tag = {tag_count}")

    sql = " select count(*) count from tag_current "
    tag_count_cur = MissingSockDb.run_sql(sql)
    print(f"tag_current = {tag_count_cur}")

    sql = " select count(*) count from tag_hist "
    tag_count_hist = MissingSockDb.run_sql(sql)
    print(f"tag_hist = {tag_count_hist}")

    sql = " select count(*) count from base_sync "
    base_sync_count = MissingSockDb.run_sql(sql)
    print(f"base_sync = {base_sync_count}")

    sql = " select count(*) count from base_station "
    base_station_count = MissingSockDb.run_sql(sql)
    print(f"base_station = {base_station_count}")

    sql = " select count(*) count from base_station_current "
    base_station_cur_count = MissingSockDb.run_sql(sql)
    print(f"base_station_cur = {base_station_cur_count}")

    sql = " select count(*) count from base_station_hist "
    base_station_hist_count = MissingSockDb.run_sql(sql)
    print(f"base_station_hist = {base_station_hist_count}")





if __name__ == "__main__":
    # user_name = input("Enter email of user to create 90 days of data : ")
    # days = int(input("for how many days must base_sync data be created : "))
    # create_farmer(user_name=user_name, days=days )

    #at least 4 base stations

    #create_farmer(user_name="piet@gmail.com", days=90, cows=9000, base_stations=5 )

    create_base_sync()
