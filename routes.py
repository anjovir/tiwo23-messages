from app import app
from flask import render_template, request, redirect
import messages, users

@app.route("/")
def index():
    list1 = messages.get_list_by_topic(1)
    list2 = messages.get_list_by_topic(2)
    list3 = messages.get_list_by_topic(3)

    if len(list1) == 0:
        return render_template("index.html", count=0)
    return render_template("index.html", count1=len(list1), last_m1=list1[-1],
                           count2=len(list2), last_m2=list1[-1], 
                           count3=len(list3), last_m3=list1[-1])

@app.route("/threads")
def threads():
    list = messages.get_list()
    return render_template("threads.html", count=len(list), messages=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Failed to send the message")
    
@app.route("/new_thread")
def new_thread():
    return render_template("new_thread.html")
    
@app.route("/newt", methods=["POST"])
def newt():
    thread = request.form["thread"]
    message = request.form["content"]
    
    if messages.newt(thread,message):
        return redirect("/")
    else:
        return render_template("error.html", message="Failed to send the message")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")