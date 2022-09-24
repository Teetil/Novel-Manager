from flask import render_template, request, redirect, Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)



app.config["SQLALCHEMY_DATABSE_URI"] = "postgresql://root"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

#result = db.session.execute("INSERT INTO tags (name) VALUES ('Action')")

#app.run(debug=True)