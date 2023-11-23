from flask import Flask, render_template, request

app = Flask(__name__)

# request.args -> GET
# request.form -> POST
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        title = "Welcome"
        return render_template("index.html", title=title)
    elif request.method == "POST":
        name = request.form.get("name", "world")
        title = "Hello, " + name
        return render_template("greet.html", title=title, name=name)