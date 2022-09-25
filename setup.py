from flask_sqlalchemy import SQLAlchemy
from flask import Flask



app = Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://teemu:asd@localhost"
db = SQLAlchemy(app)