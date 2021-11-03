import sqlite3
import time

db = sqlite3.connect("missingsock.db")
cursor = db.cursor()

cursor.execute("insert into tag_name(tag_id,nicename,user_id) values('TAG004','Brown Cow 2',1) ")
cursor.execute("insert into tag_name(tag_id,nicename,user_id) values('TAG005','Green Cow 3',1) ")
cursor.execute("insert into tag_name(tag_id,nicename,user_id) values('TAG006','Pink Cow 4',1) ")



db.commit()