from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import getenv


app = Flask(__name__)

uri = getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)