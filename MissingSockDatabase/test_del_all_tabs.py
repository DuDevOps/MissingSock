import mysql.connector
from datetime import datetime, timedelta

import os, sys

from MissingSockDBQueries import ln_MissingSockDb as MissingSockDb

sql_return = MissingSockDb.run_commit_sql("truncate table  base_sync ")
print(f"{sql_return} = truncate base_sync")

sql_return = MissingSockDb.run_commit_sql("truncate table  base_station_current ")
print(f"{sql_return} = truncate base_station_current")

sql_return = MissingSockDb.run_commit_sql("truncate table  base_station_hist ")
print(f"{sql_return} = truncate base_station_hist")

sql_return = MissingSockDb.run_commit_sql("truncate table  tag_current ")
print(f"{sql_return} = truncate tag_current")

sql_return = MissingSockDb.run_commit_sql("truncate table  tag_hist ")
print(f"{sql_return} = truncate tag_hist")

sql_return = MissingSockDb.run_commit_sql("truncate table billing ")
print(f"{sql_return} = truncate billing")

sql_return = MissingSockDb.run_commit_sql("truncate  assets ")
print(f"{sql_return} = truncate assets")

sql_return = MissingSockDb.run_commit_sql("delete from  tag ")
print(f"{sql_return} = delete  tag_name")

sql_return = MissingSockDb.run_commit_sql("delete from  base_station ")
print(f"{sql_return} = delete base_station")

sql_return = MissingSockDb.run_commit_sql("delete from  users ")
print(f"{sql_return} = users")

