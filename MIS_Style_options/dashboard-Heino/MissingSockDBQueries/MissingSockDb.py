import mysql.connector
from datetime import datetime, timedelta

def run_sql(sql_statement):

    mydb = mysql.connector.connect(
    host="192.168.0.118",
    user="iodynami_script1",
    password="pass@script1",
    db="missingsock"
    )

    cursor = mydb.cursor()

    #print(f"run_sql = {sql_statement}")

    cursor.execute(sql_statement)

    sql_result = []
    column_names =[]

    # print(f"description = {cursor.description}")
    
    for col_name in cursor.description :
        column_names.append(col_name[0])
    
    # print(f"colname = {column_names}")
    for record in cursor.fetchall():
        rec = {}
        # print(f"{record}")
        
        for idx, col in enumerate(column_names):
            # print(f"col {col} for rec at index {idx} {record[idx]}")
            rec[col]=record[idx]

        sql_result.append(rec)
    
    # print(f"{sql_result}")
    
    return sql_result

def run_commit_sql(sql_statement):

    mydb = mysql.connector.connect(
    host="192.168.0.118",
    user="iodynami_script1",
    password="pass@script1",
    db="missingsock"
    )

    cursor = mydb.cursor()

    #print(f"run_commit_sql = {sql_statement}")

    cursor.execute(sql_statement)

    # commit after each
    cursor.execute("commit")

    return True

def get_max_user_id() :
    sql="select max(id) max from users"
    sql_result = run_sql(sql)

    return sql_result

def bool_user_exits(user_name):
    sql=f"select count(*) count from users where email = '{user_name}' "
    sql_result = run_sql(sql)

    if sql_result[0]['count'] >= 1 :
        return True
    else:
        return False

def ins_users(email, passwd):
    sql = f"insert into users(email, password) values ('{email}','{passwd}')"
    sql_result = run_commit_sql(sql)

    return sql_result

def upd_users(id,email):
    sql = f"update users(email) set email={email} where id = '{id}'"
    sql_result = run_commit_sql(sql)

    return sql_result

def get_users(id='%'):
    sql = f"select * from users where convert(id, CHAR)  like '{id}' "
    sql_result = run_sql(sql)

    return sql_result

def get_users_by_email(email):
    sql = f"select * from users where email = '{email}'"
    sql_result = run_sql(sql)

    return sql_result

def ins_assets(asset_name, asset_description, tag_id, dz_tag_id, old_tag_id, dz_old_tag_id, users_id):
    sql = " insert into assets (asset_name, asset_description, tag_id, dz_tag_id, users_id) "
    sql+= f" values('{asset_name}', '{asset_description}', {tag_id}, '{dz_tag_id}', '{users_id}') "

    sql_result = run_commit_sql(sql)

    return sql_result

def upd_assets(id, asset_name, asset_description, tag_id, dz_tag_id, old_tag_id, dz_old_tag_id, users_id):
    sql = " update assets "
    sql+= f" set id = '{id}', asset_name = '{asset_name}', asset_description = '{asset_description}', "
    sql+= f"   tag_id = '{tag_id}', dz_tag_id= '{dz_tag_id}', old_tag_id='{old_tag_id}', "
    sql+= f"   dz_old_tag_id= '{dz_old_tag_id}' , users_id= '{users_id}' "
    sql+= f" where id = {id} "

    sql_result = run_commit_sql(sql)

    return sql_result

def get_assets():
    sql = f"select * from assets "
    sql_result = run_sql(sql)

    return sql_result

def get_assets_by_id(id='%'):
    sql = f"select * from assets where convert(id, CHAR)  like '{id}' "
    sql_result = run_sql(sql)

    return sql_result

def get_total_assets():
    sql_query = " select count(*) count from assets "
    
    result = run_sql(sql_query)
    return result

def ins_base_stations(base_id, nickname, users_id):
    sql = " insert into base_station (base_id, nickname, users_id) "
    sql+= f" values('{base_id}', '{nickname}', '{users_id}') "

    sql_result = run_commit_sql(sql)

    return sql_result

def upd_base_station(id, base_id, nickname, users_id):
    sql = " update base_station "
    sql+= f" set id={id}, base_id='{base_id}', nickname='{nickname}', users_id={users_id}"
    sql+= f" where id = {id} "

    sql_result = run_commit_sql(sql)

    return sql_result

def get_base_station ():
    sql = f"select a.id, a.sync_base_id, a.nickname , b.gps_lat, b.gps_long "
    sql += f" from base_station a,base_station_current b "
    sql += f" where a.id = b.id  "
    sql_result = run_sql(sql)

    return sql_result

def get_base_station_by_id (id='%'):
    sql = f"select * from base_station where convert(id, CHAR)  like '{id}'"
    sql_result = run_sql(sql)

    return sql_result

def get_base_station_by_base_id (base_id):
    sql = f"select * from base_station where base_id  = '{base_id}'"
    sql_result = run_sql(sql)

    return sql_result

def get_base_station_current():
    sql = f"select * from base_station_current "
    sql_result = run_sql(sql)

    return sql_result

def get_base_station_tag_current():
    sql = f"select a.id , a.sync_base_id , a.nickname, b.tag_count , c.gps_lat, c.gps_long"
    sql += f" from base_station a"          
    sql += f" left join (select distinct base_station_id , count(*) tag_count "
    sql += f" from tag_current ) b on a.id =  b.base_station_id "
    sql += f" left join base_station_current c on a.id = c.id "

    sql_result = run_sql(sql)

    return sql_result

def ins_billing(timestamp, description, debit, credit, users_id):
    sql = " insert into billing (id, timestamp, description, debit, credit, users_id) "
    sql+= f" values('{timestamp}', '{description}', {debit}, {credit}, {users_id}) "

    sql_result = run_commit_sql(sql)

    return sql_result

def upd_billing(id, timestamp, description, debit, credit, users_id):
    sql = " update billing "
    sql+= f" set timestamp='{timestamp}', description='{description}', debit={debit}, "
    sql+= f" credit={credit}, users_id={users_id}"
    sql+= f" where id = {id} "

    sql_result = run_commit_sql(sql)

    return sql_result

def get_billing(id='%'):
    sql = f"select * from billing where convert(id, CHAR)  like '{id}' "
    sql_result = run_sql(sql)

    return sql_result

def ins_tag(tag_id, nickname, users_id):
    sql = " insert into tag (tag_id, nickname, users_id) "
    sql+= f" values('{tag_id}', '{nickname}', {users_id}) "

    sql_result = run_commit_sql(sql)

    return sql_result

def upd_tag(tag_id, nickname, users_id):
    sql = " update tag "
    sql+= f" set tag_id='{tag_id}', nickname='{nickname}', users_id={users_id} "
    sql+= f" where id = {id} "

    sql_result = run_commit_sql(sql)

    return sql_result

def get_tag():
    sql = f"select * from tag"
    sql_result = run_sql(sql)

    return sql_result

def get_tag_by_id(id='%'):
    sql = f"select * from tag where convert(id, CHAR)  like '{id}' "
    sql_result = run_sql(sql)

    return sql_result

def get_tag_by_tag_id(tag_id):
    sql = f"select * from tag where tag_id  = '{tag_id}' "
    sql_result = run_sql(sql)

    return sql_result

def get_total_tags():
    sql_query = " select count(*) count from tag "
    
    result = run_sql(sql_query)
    return result

# ========= copied from dashboard.main ==========

def get_total_base_stations():
    sql_query = " select count(*) count from base_station "
    
    result = run_sql(sql_query)
    return result

def get_tags_at_basestation_date(base_id, dateStart):
    sql_query = '''
        select count(*) count from base_sync
        where  
    '''
    sql_query += f" base_id = '{base_id}' "
    sql_query += f" and timestamp >= convert('{dateStart}', DATETIME) "
    
    #print(f"{sql_query}")
 
    result = run_sql(sql_query)
    return result

def get_dashboard():

    # Get Base Stations + location + last tag 
    
    sql_query = '''
select a.id, a.asset_name, a.asset_description, a.tag_id, a.old_tag_id ,
    b.tag_id , b.nickname, 
    c.base_id, c.max_time,
    c.GPS_lat, c.GPS_long 
from assets a 
left join tag b on a.tag_id = b.id
left join tag_last_recv c on b.tag_id = c.tag_id 
            '''

    result = run_sql(sql_query)
    return result

def get_report_last_at_basestation():

    # Get Base Stations + location + last tag 
    
    sql_query = '''
    select a.base_id, a.tag_id, a.max_time,
           b.nickname, a.gps_lat, a.gps_long
    from base_sync_last_recv a
    left join base_station b on a.base_id = b.base_id
            '''

    result = run_sql(sql_query)
    return result


def tags_not_read_past_hours(HOURS):

    sql_query = "select * from tag_current "
    sql_query += f" where timestamp  <  NOW() - INTERVAL {HOURS} HOUR "
    
    result = run_sql(sql_query)
    return result

def tags_not_read_past_days(DAYS):

    sql_query = "select * from tag_current "
    sql_query += f" where timestamp  <  NOW() - INTERVAL {DAYS} DAY "
   
    result = run_sql(sql_query)
    return result

def base_not_read_past_hours(HOURS):

    sql_query = "select * from base_station_current "
    sql_query += f" where timestamp  < NOW() - INTERVAL {HOURS} HOUR "
    
    result = run_sql(sql_query)
    return result

def base_not_read_past_days(DAYS):

    sql_query = "select * from base_station_current "
    sql_query += f" where timestamp  < NOW() - INTERVAL {DAYS} DAY "
    
    result = run_sql(sql_query)
    return result

# ===================================================

def count_tags_not_read_past_hours(HOURS):

    sql_query = "select count(*) count from tag_current "
    sql_query += f" where timestamp  <  NOW() - INTERVAL {HOURS} HOUR "
    
    result = run_sql(sql_query)
    return result

def count_tags_not_read_past_days(DAYS):

    sql_query = "select count(*) count from tag_current "
    sql_query += f" where timestamp  <  NOW() - INTERVAL {DAYS} DAY "
   
    result = run_sql(sql_query)
    return result

def count_base_not_read_past_hours(HOURS):

    sql_query = "select count(*) count from base_station_current "
    sql_query += f" where timestamp  < NOW() - INTERVAL {HOURS} HOUR "
    
    result = run_sql(sql_query)
    return result

def count_base_not_read_past_days(DAYS):

    sql_query = "select count(*) count from base_station_current "
    sql_query += f" where timestamp  < NOW() - INTERVAL {DAYS} DAY "
    
    result = run_sql(sql_query)
    return result