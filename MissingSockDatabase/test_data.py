import sqlite3
import time

db = sqlite3.connect("missingsock.db")
cursor = db.cursor()

cursor.execute("insert into users(id, username, password) values (1,'koosbilly9@gmail.com','kooskoos')")

cursor.execute("insert into BILLING(user_id, debit ) values(1,200)")

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0132','TAG0001','-25.6859','28.2726',23.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0132','TAG0002','-25.6859','28.2726',1.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0132','TAG0003','-25.6859','28.2726',20.9,'T002001') ")
time.sleep(30)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0132','TAG0001','-25.6859','28.2726',3.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0132','TAG0002','-25.6859','28.2726',0.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0132','TAG0003','-25.6859','28.2726',2.9,'T002001') ")
time.sleep(30)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0140','TAG0001','-25.7059','28.2726',3.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0140','TAG0002','-25.7059','28.2726',0.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0140','TAG0003','-25.7059','28.2726',2.9,'T002001') ")
time.sleep(10)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0150','TAG0001','-25.7159','28.3026',13.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0150','TAG0002','-25.7159','28.3026',10.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0150','TAG0003','-25.7159','28.3026',12.9,'T002001') ")
time.sleep(5)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0160','TAG0001','-25.6870','28.2726',13.9,'T002001') ")
time.sleep(3)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0160','TAG0002','-25.6875','28.2726',10.9,'T002001') ")
time.sleep(3)

cursor.execute("insert into base_sync(base_id,tag_id,gps_lat, gps_long,rssi,sync_id) \
  values('BASE0160','TAG0003','-25.7158','28.2726',12.9,'T002001') ")
time.sleep(1)

cursor.execute("insert into base_station(base_id, nicename, user_id) values('BASE0132','Water Gat',1)")
cursor.execute("insert into base_station(base_id, nicename, user_id) values('BASE0140','Kraal',1)")
cursor.execute("insert into base_station(base_id, nicename, user_id) values('BASE0150','Pad Hek',1)")
cursor.execute("insert into base_station(base_id, nicename, user_id) values('BASE0150','Land Rover',1)")

cursor.execute("insert into tag_name(tag_id,nicename,user_id) values('TAG001','Brown Cow',1) ")
cursor.execute("insert into tag_name(tag_id,nicename,user_id) values('TAG002','Green Cow',1) ")
cursor.execute("insert into tag_name(tag_id,nicename,user_id) values('TAG003','Pink Cow',1) ")



db.commit()