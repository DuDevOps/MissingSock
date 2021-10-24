from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/threecolumn.html")
def threecolumn():
    return render_template("threecolumn.html")

@app.route("/twocolumn1.html")
def twocolumn1():
    return render_template("twocolumn1.html")

@app.route("/twocolumn2.html")
def twocolumn2():
    return render_template("twocolumn2.html")

@app.route("/onecolumn.html")
def onecolumn():
    return render_template("onecolumn.html")

if __name__ == "__main__":
    app.run(port=5100, debug=True)