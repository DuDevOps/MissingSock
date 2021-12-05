from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return f"hello w", 200
    
if __name__ == "__main__":
    app.run()