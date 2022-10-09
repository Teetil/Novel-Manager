from flask import render_template, request, redirect, session
from setup import app, db
import novels
import authors
import tags
import users
import reviews

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
        return render_template("novel.html", novel_info=novel_info, novel_id=novel_id, tags=novels.get_novel_tags(novel_id))
    if request.method == "POST":
        novels.remove_novel(novel_id)
        return redirect("/")

@app.route("/author/<int:author_id>")
def author_page(author_id):
    author_info = authors.get_author_info(author_id)
    author_novels = [(n[1], n[2]) for n in author_info]
    return render_template("author.html", author_name = author_info[0][0].capitalize(), author_novels=author_novels)

@app.route("/novel/<int:novel_id>/tags", methods=["GET", "POST"])
def novel_tag_page(novel_id):
    novel_info = novels.get_novel_info(novel_id)
    tag_info = tags.get_all_tags()
    if request.method == "GET":
        return render_template("novel_tags.html", tags=tag_info, novel_name = novel_info[0])
    if request.method == "POST":
        if "create_tag" in request.form:
            tags.add_new_tag(request.form["create_tag"])
            return render_template("novel_tags.html", tags=tag_info, novel_name = novel_info[0])
        elif "add_novel_tag" in request.form:
            for tup in tag_info:
                if request.form["add_novel_tag"].lower() in tup:
                    novel_tags = [i[0] for i in novels.get_novel_tags(novel_id)]
                    if tup[0] not in novel_tags:
                        tags.add_novel_tag(novel_id, tup[0])
            return redirect(f"/novel/{novel_id}")

@app.route("/tag/<int:tag_id>")
def tag_page(tag_id):
    return render_template("tag.html", tag_name = tags.get_tag_by_id(tag_id), novels=novels.get_novels_by_tag(tag_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users.login(username, password)
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password1"]
        role = request.form["role"]
        if password != request.form["password2"]:
            return redirect("/")
        users.add_user(username, password, role)
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/novel/<int:novel_id>/reviews", methods=["GET", "POST"])
def review(novel_id):
    if request.method == "POST":
        reviews.add_review(session["user_id"], novel_id, int(request.form["rating"]), request.form["add_review"])
    return render_template("reviews.html", novel_info = novels.get_novel_info(novel_id), reviews = novels.get_novel_reviews(novel_id))


app.run(debug=True)