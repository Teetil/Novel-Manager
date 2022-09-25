from flask import render_template, request, redirect
from setup import app, db
import novels
import authors

@app.route("/")
def index():
    return render_template("index.html", novels=novels.get_all_novels())

@app.route("/add", methods=["GET", "POST"])
def add_novel():
    if request.method == "GET":
        return render_template("add.html")
    
    if request.method == "POST":
        novel_name = request.form["novel-name"]
        author_name = request.form["author-name"]
        author_id =  authors.get_author_by_name(author_name)
        if not author_id:
            author_id = authors.add_new_author(author_name)
        author_id = author_id
        novels.add_novel(author_name, author_id, request.form["novel-synopsis"])
        print("added novel")
        return redirect("/")

app.run(debug=True)