import sqlite3
from datetime import datetime, timedelta

def get_sql(sql):
    # get basestation from DB for user
    db_path = "missingsock.db"

    db = sqlite3.connect(db_path)
    cursor = db.execute(sql)

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

date_1_hour_ago = datetime.now() - timedelta(hours=7)
date_1_days_ago = datetime.now() - timedelta(days=1)
date_7_days_ago = datetime.now() - timedelta(days=7)

print(f"date_1_hour_ago = {date_1_hour_ago}")
print(f"date_1_days_ago = {date_1_days_ago}")
print(f"date_7_days_ago = {date_7_days_ago}")