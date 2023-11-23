import sqlite3
import flask_session
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# Configure session
app.secret_key = 'my_secret_key'

# Get data from froshims.db
def get_data():
    db = sqlite3.connect("froshims.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM registrants")
    data = cursor.fetchall()
    return data

# Set or insert new data to froshims.db
def set_data(name, sport):
    db = sqlite3.connect("froshims.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", (name, sport))
    db.commit()

# Drop or delete data using id
def drop_data(id):
    db = sqlite3.connect("froshims.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM registrants WHERE id = ?", id)
    db.commit()

# Define a list of sports
SPORTS = [
    "Basketball",
    "Soccer",
    "Swimming"
]


@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html", sports=SPORTS)
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username == "admin" and password == "admin":
        session["username"] = username
        return redirect("/")
    else:
        return render_template("login.html", error="Invalid username and password")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    
    # Validate submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")
    
    # return render_template("success.html")
    set_data(name, sport)
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    registrants = get_data()
    return render_template("registrants.html", registrants=registrants)


@app.route("/remove", methods=["POST"])
def remove():
    id = request.form.get("id")
    if id:
        drop_data(id)
    return redirect("/registrants")


if __name__ == "__main__":
    app.run()