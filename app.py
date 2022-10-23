from flask import render_template, request, redirect, session
from setup import app, db
import novels
import authors
import tags
import users
import reviews
import followers

@app.route("/")
def index():
    return render_template("index.html", novels=novels.get_all_novels())

@app.route("/add", methods=["GET", "POST"])
def add_novel():
    if request.method == "GET":
        return render_template("add.html")
    
    if request.method == "POST":
        users.check_csrf()
        novel_name = request.form["novel-name"]
        author_name = request.form["author-name"]
        novel_synopsis = request.form["novel-synopsis"]
        author_id =  authors.get_author_by_name(author_name)
        if not author_id:
            author_id = authors.add_new_author(author_name)
            author_id = author_id
        else:
            author_id = author_id[0]
        res = novels.add_novel(novel_name, author_id, novel_synopsis)
        if not res:
            return render_template("error.html", error="A novel with this name already exists")
        return redirect("/")

@app.route("/novel/<int:novel_id>", methods=["GET", "POST"])
def novel_page(novel_id):
    novel_info = novels.get_novel_info(novel_id)
    novel_followers = [n[0] for n in followers.get_novel_followers(novel_id)]
    if request.method == "GET":
        if "user_id" in session:
            followers.update_follow_chapter(session["user_id"], novel_id, novels.get_chapters(novel_id))
        return render_template("novel.html", novel_info=novel_info, novel_id=novel_id, tags=novels.get_novel_tags(novel_id), followers=novel_followers, chapters = novels.get_chapters(novel_id))
    if request.method == "POST":
        users.check_csrf()
        if "follow" in request.form:
            followers.add_follower(session["user_id"], novel_id)
        elif "unfollow" in request.form:
            followers.remove_follower(session["user_id"], novel_id)
        elif "add_chp" in request.form:
            novels.add_chapters(novel_id, int(request.form["add_chp"]))
        else:
            users.check_role(1)
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
        users.check_csrf()
        if "create_tag" in request.form:
            users.check_role(1)
            res = tags.add_new_tag(request.form["create_tag"])
            if not res:
                return render_template("error.html", error="This tag already exists")
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
        res = users.login(username, password)
        if not res:
            return render_template("error.html", error="Incorrect username or password")
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
            return render_template("error.html", error="Passwords do not match")
        res = users.add_user(username, password, role)
        if not res:
            return render_template("error.html", error="This user already exists")
        return redirect("/")

@app.route("/logout")
def logout():
    if "user_id" not in session:
        return render_template("error.html", error="Not logged in")
    users.logout()
    return redirect("/")

@app.route("/novel/<int:novel_id>/reviews", methods=["GET", "POST"])
def review(novel_id):
    if request.method == "POST":
        users.check_csrf()
        reviews.add_review(session["user_id"], novel_id, int(request.form["rating"]), request.form["add_review"])
    return render_template("reviews.html", novel_info = novels.get_novel_info(novel_id), reviews = novels.get_novel_reviews(novel_id))

@app.route("/user/<user_id>")
def user_page(user_id):
    user_info = users.get_user_info(user_id)
    user_following = followers.get_user_following(user_id)
    return render_template("user.html", user_info=user_info, reviews = reviews.get_reviews_by_user(user_id), following = user_following)
