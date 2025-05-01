import secrets
import sqlite3
from flask import Flask
from flask import abort, redirect, flash,  render_template, request, session, make_response
import db
import config
import items
import users
import re
import markupsafe
import math


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    thread_count = items.count_items()
    page_count = math.ceil(thread_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    
    all_items = items.get_items(page, page_size)
    return render_template("index.html", page=page, page_count=page_count, items = all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user = user, items = items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query = query, results = results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    #print("CLASSES:", classes)
    for row in classes:
        print(dict(row))

    reviews = items.get_reviews(item_id)
    
    return render_template("show_item.html", item=item, classes=classes, reviews=reviews)


@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)



@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    all_classes=items.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""

    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]


    return render_template("edit_item.html", item = item, classes = classes, all_classes = all_classes)

@app.route("/remove_item/<int:item_id>", methods = ["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_item.html", item = item)
    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        return redirect("/item/"+str(item_id))

@app.route("/update_item", methods = ["POST"])
def update_item():
    require_login()
    check_csrf()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if not title or len(title)>60:
        abort(403)
    description = request.form["description"]
    if not description or len(description)>400:
        abort(403)
    story = request.form["story"]
    if not story:
        abort(403)
    all_classes = items.get_all_classes()
    classes = []

    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.update_item(item_id, title, description, story, classes)
    return redirect("/item/"+str(item_id))

@app.route("/create_item", methods = ["POST"])
def create_item():

    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title)>60:
        abort(403)

    description = request.form["description"]

    if not description or len(description)>400:
        abort(403)
    story = request.form["story"]
    if not story:
        abort(403)
    user_id = session["user_id"]

    all_classes = items.get_all_classes()


    classes = []

    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.add_item(title, description, story, user_id, classes)
    return redirect("/")

@app.route("/create_review", methods = ["POST"])
def create_review():
    require_login()
    check_csrf()
    grade = request.form["grade"]
    if not re.search("^([1-9]|10)$", grade):
        abort(403)
    review = request.form["review"]
    if not review or len(review)>400:
        abort(403)

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)

    user_id = session["user_id"]

    items.add_review(item_id, user_id, grade, review)
    return redirect("/item/"+str(item_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if username == "" or password2 == "" or password2 == "":
        flash("VIRHE: Kentät eivät voi olla tyhjiä")
        return render_template("register.html", username=username)
    if password1 != password2:
        flash("VIRHE: Salasanat eivät ole samat")
        return render_template("register.html", username=username)
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: Tunnus on jo varattu")
        return redirect("/register")
    user_id = users.check_login(username, password1)
    session["user_id"] = user_id
    session["username"] = username
    session["csrf_token"] = secrets.token_hex(16)
    flash("Tervetuloa!")
    return redirect("/")
    

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            flash("Tervetuloa!")
            return redirect("/")
        
        flash("VIRHE: Väärä tunnus tai salasana")
        return render_template("login.html", username=username)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")