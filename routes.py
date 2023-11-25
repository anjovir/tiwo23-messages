from app import app
from flask import render_template, request, redirect
import messages, users, threads
from datetime import datetime

@app.route("/")
def index():
    list1 = messages.get_list_by_topic(1)
    list2 = messages.get_list_by_topic(2)
    list3 = messages.get_list_by_topic(3)
    default = ('0', 'default', datetime(2023, 11, 11, 00, 00, 00, 000000), 1)

    #intial situation, if no topics and messages added to db
    if len(list1) == 0 or len(list2) == 0 or len(list3) == 0:
        return render_template("index.html", count1=len(list1), last_m1=default,
                               count2=len(list2), last_m2=default,
                               count3=len(list3), last_m3=default)
    return render_template("index.html", 
                           count_threads1= len(threads.get_list(1)), count1=len(list1), last_m1=list1[-1],
                           count_threads2=len(threads.get_list(2)), count2=len(list2), last_m2=list2[-1], 
                            count_threads3=len(threads.get_list(3)), count3=len(list3), last_m3=list3[-1])

@app.route("/general")
def general():
    list_t = threads.get_list(1)
    last_m_list = {}
    m_list = {}
    links_t = {}

    for thread in list_t:
        m_list[thread[4]] = (messages.count_messages(thread[4]))[0]
        last_m_list[thread[4]] = messages.get_list_by_thread(thread[4])[-1]
        links_t[thread[4]] = ({"name": f"{thread[0]}", "url": f"/thread?thread_id={thread[4]}" })
        

    return render_template("general.html", 
                           threads=list_t,
                           m_count=m_list, last_m=last_m_list,
                           links=links_t)

@app.route("/politics")
def politics():
    list_t = threads.get_list(2)
    last_m_list = {}
    m_list = {}
    links_t = {}

    for thread in list_t:
        m_list[thread[4]] = (messages.count_messages(thread[4]))[0]
        last_m_list[thread[4]] = messages.get_list_by_thread(thread[4])[-1]
        links_t[thread[4]] = ({"name": f"{thread[0]}", "url": f"/thread?thread_id={thread[4]}" })
        

    return render_template("politics.html", 
                           threads=list_t,
                           m_count=m_list, last_m=last_m_list,
                           links=links_t)

@app.route("/economy")
def economy():
    list_t = threads.get_list(3)
    last_m_list = {}
    m_list = {}
    links_t = {}

    for thread in list_t:
        m_list[thread[4]] = (messages.count_messages(thread[4]))[0]
        last_m_list[thread[4]] = messages.get_list_by_thread(thread[4])[-1]
        links_t[thread[4]] = ({"name": f"{thread[0]}", "url": f"/thread?thread_id={thread[4]}" })
        

    return render_template("economy.html", 
                           threads=list_t,
                           m_count=m_list, last_m=last_m_list,
                           links=links_t)

@app.route("/thread")
def thread():
    list = messages.get_list_by_thread(request.args.get("thread_id"))
    return render_template("thread.html",count=len(list), messages=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    thread_id = request.form["thread_id"]
    topic_id = request.form["topic_id"]
    print(thread_id)
    print(topic_id)
    if messages.send(content, thread_id, topic_id):
        return redirect(f"/thread?thread_id={thread_id}")
    else:
        return render_template("error.html", message="Failed to send the message")
    
@app.route("/new_thread")
def new_thread():
    return render_template("new_thread.html")
    
@app.route("/newt", methods=["POST"])
def newt():
    topic = request.form["topic"]
    thread = request.form["thread"]
    message = request.form["content"]

    if messages.newt(thread,message,topic):
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