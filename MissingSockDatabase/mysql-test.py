import mysql.connector
sql="select * from assets"

mydb = mysql.connector.connect(
  host="192.168.0.118",
  user="iodynami_script1",
  password="pass@script1",
  db="missingsock"
)

cursor = mydb.cursor()

cursor.execute(sql)

sql_result = []
column_names =[]

for col_name in cursor.description :
  column_names.append(col_name[0])

for record in cursor.fetchall():
  rec = {}
  for idx, col in enumerate(column_names):
      rec[col]=record[idx]

  sql_result.append(rec)

print(f"{sql_result}")