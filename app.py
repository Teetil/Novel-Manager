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
        novel_synopsis = request.form["novel-synopsis"]
        author_id =  authors.get_author_by_name(author_name)
        if not author_id:
            author_id = authors.add_new_author(author_name)
            author_id = author_id
        else:
            author_id = author_id[0]
        novels.add_novel(novel_name, author_id, novel_synopsis)
        return redirect("/")

@app.route("/novel/<int:novel_id>", methods=["GET", "POST"])
def novel_page(novel_id):
    if request.method == "GET":
        novel_info = novels.get_novel_info(novel_id)
        return render_template("novel.html", novel_name = novel_info[0], novel_synopsis = novel_info[1], author_name = novel_info[2].capitalize(), author_id = novel_info[3])
    if request.method == "POST":
        novels.remove_novel(novel_id)
        return redirect("/")

@app.route("/author/<int:author_id>")
def author_page(author_id):
    author_info = authors.get_author_info(author_id)
    author_novels = [(n[1], n[2]) for n in author_info]
    return render_template("author.html", author_name = author_info[0][0].capitalize(), author_novels=author_novels)


app.run(debug=True)