from flask import Flask
import sqlite3
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash
import db
import config
import forum



app = Flask(__name__)
app.secret_key = config.secret_key



@app.route("/")
def index():
    return render_template("index.html")



#REGISTRATION
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    firstpassword = request.form["password1"]
    secondpassword = request.form["password2"]
    if firstpassword != secondpassword:
        return "Error: Given passwords don't match"
    password_hash = generate_password_hash(firstpassword)
    
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?,?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "Error: username already exists"
    
    return "Account created"

@app.route("/reviewpage")
def reviewpage():
    threads = forum.get_threads()
    return render_template("reviewpage.html", threads=threads)

@app.route("/new_thread", methods=["POST"])
def new_thread():
    title = request.form["title"]
    genres = request.form.getlist("genres")
    grade = request.form.get("grade")
    text = request.form["review"]

    user_id = session["user_id"]
    
    genres = ",".join(genres)
    thread_id = forum.add_thread(title, genres, grade, text, user_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/edit/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    thread = forum.get_thread(thread_id)
    if request.method == "GET":
        return render_template("edit.html", thread=thread)
    if request.method == "POST":
        review = request.form["review"]
        forum.update_thread(thread["id"], review)
        return redirect("/thread/" + str(thread["thread_id"]))

@app.route("/remove/<int:thread_id>", methods = ["GET", "POST"])
def remove_thread(thread_id):
    thread = forum.get_thread(thread_id)

    if request.method == "GET":
        return render_template("remove.html", thread=thread)
    
    if request.method == "POST":
        if "continue" in request.form:
            forum.remove_thread(thread["id"])
        return redirect("/thread/" + str(thread("thread_id")))


@app.route("/search")
def search():
    query = request.args.get("query")
    results = forum.search(query) if query else []
    return render_template("search.html", query=query, results=results)