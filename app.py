from flask import render_template, request, redirect
from setup import app, db
import novels


@app.route("/")
def index():
    return render_template("index.html", novels=novels.get_all_novels())

app.run(debug=True)