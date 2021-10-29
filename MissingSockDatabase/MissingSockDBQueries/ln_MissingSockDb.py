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

    cursor.execute(sql_statement)

    sql_result = []
    column_names =[]

    for col_name in cursor.description :
        column_names.append(col_name[0])

    for record in cursor.fetchall():
        rec = {}
        for idx, col in enumerate(column_names):
            rec[col]=record[idx]

            sql_result.append(rec)

    return sql_result

def ins_user(email):
    sql = f"insert into users(email) values ({email})"
    sql_result = run_sql(sql)

    return sql_result

def ins_assets(asset_name, asset_description, users_id):
    sql = " insert into assets (asset_name, asset_description, users_id) "
    sql+= f" values({asset_name}, {asset_description}, {users_id}) "

    sql_result = run_sql(sql)

    return sql_result

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