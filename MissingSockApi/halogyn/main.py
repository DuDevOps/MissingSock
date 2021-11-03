from flask import Flask, render_template, request, url_for
import sqlite3 

app = Flask(__name__)

NoLogIn = True

# get basestation from DB for user
db = sqlite3.connect("missingsock.db")
cursor = db.cursor()

def get_sql(sql):
    db = sqlite3.connect("missingsock.db")
    cursor = db.cursor()
    cursor.execute(sql)
    sql_result = cursor.fetchall()
    return sql_result

def get_base_station():
    
    sql_query = '''
    select a.id, a.base_id, a.tag_id, a.created, a.gps_local, a.signal_strength, a.sync_id
                                       , b.nicename 
                                    from base_sync a
                                    left join base_station b on a.base_id = b.base_id
                                    where a.base_id||a.created in (
                                    select distinct a.base_id||max(a.created)
                                     from base_sync a
                                     group by a.base_id)
            '''

    result = get_sql(sql_query)
    return result

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/threecolumn.html")
def threecolumn():
   
    return render_template("threecolumn.html")

@app.route("/baseStations.html", methods=["GET","POST"])
def baseStations(*args, **kwargs):
    
    try:
        print(f"kwargs value for email = {kwargs['email']}")
    except Exception as ex:
        print(f"ex")

    sql_base_stations = get_base_station()

    return render_template("baseStations.html", base_stations=sql_base_stations)

@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST" :
        # add function to validate / get userid
        loginEmail = request.form["email"]
        NoLogIn = False
        
        print(f"what nou {NoLogIn} {loginEmail} ")
        
        return baseStations(NoLogin=False, email=loginEmail )

    return render_template("login.html")

@app.route("/twocolumn2.html")
def twocolumn2():
    
    return render_template("twocolumn2.html")

if __name__ == "__main__":
    app.run(port=5110, debug=True)