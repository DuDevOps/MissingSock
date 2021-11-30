import sqlite3

db = sqlite3.connect("missingsock.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE base_sync (\
  id int PRIMARY KEY ,\
  base_id text ,\
  Tag_id text,\
  GPS_lat text ,\
  GPS_long text ,\
  RSSI integer,\
  sync_id varchar(30),\
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )")

cursor.execute("CREATE TABLE users (\
  id INTEGER PRIMARY KEY ,\
  username varchar(250) not null,\
  password varchar(20) not null  )")

cursor.execute("CREATE TABLE base_station (\
  id int PRIMARY KEY,\
  base_id TEXT ,\
  nicename TEXT ,\
  user_id integer not null, \
  FOREIGN KEY (user_id) REFERENCES user(id) )")

cursor.execute("CREATE TABLE tag_name (\
  id int PRIMARY KEY ,\
  tag_id TEXT ,\
  nicename TEXT ,\
  user_id integer,\
  FOREIGN KEY (user_id) REFERENCES user(id) )" )

cursor.execute("CREATE TABLE billing (\
  id integer PRIMARY KEY ,\
  user_id integer not null,\
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
  description text , \
  debit DECIMAL ,\
  credit DECIMAL, \
  FOREIGN KEY(user_id) REFERENCES user(id) )")


db.commit()