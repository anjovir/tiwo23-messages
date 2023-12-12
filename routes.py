from app import app
from flask import render_template, request, redirect
import messages, users, threads, topics
from datetime import datetime


@app.route("/")
def index():
    #will create admin, if not already created
    users.create_admin()

    topics = messages.get_topics_list()
    last_m_list = {}
    m_count = {}
    thread_count = {}
    links_t = {}
    default = ('0', 'default', datetime(2023, 11, 11, 00, 00, 00, 000000), 1)

    for topic in topics:
        m_count[topic[0]] = len(messages.get_list_by_topic(topic[0]))
        links_t[topic[0]] = ({"name": f"{topic[1]}", "url": f"/topic?topic_id={topic[0]}" })

        #checks if there is a topic where there are no messages
        if m_count[topic[0]] != 0 :
            last_m_list[topic[0]] = messages.get_list_by_topic(topic[0])[-1]
            thread_count[topic[0]] = len(threads.get_list(topic[0]))
        else:
            last_m_list[topic[0]] = default
            thread_count[topic[0]] = 0
    
    is_admin = users.check_if_admin(users.user_id())

    #this will check if the user is a member of some secret room
    sroom_user_list = users.list_all_sroom_users()
    sroom_user = {}
    
    for i in range(users.max_id()[0]+1):
        sroom_user[i] = (None,None)

    for user in sroom_user_list:
        sroom_user[user[1]] = (user[0],user[2])
        
    return render_template("index.html", 
                           topics=topics,
                           m_count=m_count, last_m=last_m_list,
                           thread_count=thread_count,
                           links=links_t,
                           is_admin=is_admin,
                           sroom_user_list=sroom_user)

@app.route("/add_topic", methods=["POST"])
def add_topic():
    users.check_csfr(request.form["csrf_token"])
    content = request.form["content"]
    is_secret = request.form["is_secret"]
    if is_secret == "True":
        is_secret = True
    else:
        is_secret = False
    if topics.add_topic(content,is_secret):
        return redirect("/")
    else:
        return render_template("error.html", message="Failed to send the message")
    

@app.route("/delete_topic", methods=["POST"])
def delete_topic():
    topic_id = request.form["topic_id"]
    if topics.delete_topic(topic_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Failed to send the message")

@app.route("/search", methods=["GET"])
def search():
    query = request.args["query"]
    result = messages.search(query)
    thread_links = {}

    for m in result:
        thread_links[m[4]] = ({"name": f"{m[3]}", "url": f"/thread?thread_id={m[4]}" })

    return render_template("result.html", messages=result, thread_links=thread_links)

@app.route("/topic")
def topic():
    list_t = threads.get_list(request.args.get("topic_id"))
    topic = threads.get_topic(request.args.get("topic_id"))
    last_m_list = {}
    m_list = {}
    links_t = {}

    is_admin = users.check_if_admin(users.user_id())
    
    sroom_user = {}
    for i in range(users.max_id()[0]+1):
        sroom_user[i] = (None,None)
    
    sroom_user_list = users.list_sroom_users(topic[1])
    for user in sroom_user_list:
        sroom_user[user[1]] = (user[0],user[2])

    default = ('0', 'default', datetime(1111, 11, 11, 11, 11, 11, 111111), 1)
    
    for thread in list_t:
        m_list[thread[4]] = (messages.count_messages(thread[4]))[0]
        try:
            last_m_list[thread[4]] = messages.get_list_by_thread(thread[4])[-1]
        except:
            last_m_list[thread[4]] = default
        links_t[thread[4]] = ({"name": f"{thread[0]}", "url": f"/thread?thread_id={thread[4]}" })

    return render_template("topic.html", 
                           threads=list_t,
                           m_count=m_list, last_m=last_m_list,
                           topic=topic,
                           links=links_t,
                           is_admin=is_admin, sroom_user_list=sroom_user)

@app.route("/sroom_users", methods=["GET","POST"])
def sroom_users():
    if request.method == "GET":
        topic_id = request.args.get("topic_id")
        sroom_user_list = users.list_sroom_users(topic_id)
        user_list = users.list_users()
        sroom_user = {}
        is_admin = users.check_if_admin(users.user_id())
    
        for i in range(users.max_id()[0]+1):
            sroom_user[i] = (None,topic_id)

        for user in sroom_user_list:
            sroom_user[user[1]] = (user[0],user[2])
        
        return render_template("sroom_users.html", topic_id=topic_id, sroom_user_list=sroom_user, user_list=user_list, is_admin=is_admin)
    
    if request.method == "POST":
        topic_id = request.form["topic_id"]
        return redirect(f"/sroom_users?topic_id={topic_id}")

@app.route("/add_member", methods=["POST"])
def add_member():
    topic_id = request.form["topic_id"]
    user_id = request.form["user_id"]
    if users.add_user(topic_id, user_id):
        return redirect(f"/sroom_users?topic_id={topic_id}")
    return render_template("error.html", message="Failed to add user")

@app.route("/remove_member", methods=["POST"])
def remove_member():
    topic_id = request.form["topic_id"]
    user_id = request.form["user_id"]
    if users.remove_user(topic_id, user_id):
        return redirect(f"/sroom_users?topic_id={topic_id}")
    return render_template("error.html", message="Failed to add user")

@app.route("/thread")
def thread():
    list = messages.get_list_by_thread(request.args.get("thread_id"))
    thread = threads.get_thread(request.args.get("thread_id"))
    if len(list) == 0:
        list = [('0', 'default', datetime(1111, 11, 11, 11, 11, 11, 111111), request.args.get("thread_id"), thread[4]),
                ('0', 'default', datetime(2222, 11, 11, 11, 11, 11, 111111), request.args.get("thread_id"), thread[4])]


    return render_template("thread.html",count=len(list), messages=list, thread=thread, m_edit=None, edit_t=None)

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    thread_id = request.form["thread_id"]
    topic_id = request.form["topic_id"]
    users.check_csfr(request.form["csrf_token"])

    if messages.send(content, thread_id, topic_id):
        return redirect(f"/thread?thread_id={thread_id}")
    else:
        return render_template("error.html", message="Failed to send the message")
    
@app.route("/new_thread", methods=["GET", "POST"])
def new_thread():
    if request.method == "GET":
        topic_id = request.args.get("topic_id")
        return render_template("new_thread.html", topic_id=topic_id)
    if request.method == "POST":
        topic_id = request.form["topic_id"]
        return redirect(f"/new_thread?topic_id={topic_id}")

    
@app.route("/newt", methods=["POST"])
def newt():
    thread = request.form["thread"]
    message = request.form["content"]
    topic = request.form["topic_id"]
    users.check_csfr(request.form["csrf_token"])

    if messages.newt(thread,message,topic):
        return redirect(f"/topic?topic_id={topic}")
    else:
        return render_template("error.html", message="Failed to send the message")

@app.route("/edit", methods=["POST"])
def edit():
    m_id = request.form["m_id"]
    thread_id = request.form["t_id"]
    message = messages.get_message(m_id)
    list = messages.get_list_by_thread(thread_id)
    thread = threads.get_thread(thread_id)

    return render_template("thread.html", count=len(list), messages=list, thread=thread, m_edit=message, edit_t=None)

@app.route("/edit_message", methods=["POST"])
def edit_message():
    thread_id = request.form["thread_id"]
    content = request.form["content"]
    m_id = int(request.form["m_id"])
    users.check_csfr(request.form["csrf_token"])
    
    if messages.edit_m(m_id, content):
        return redirect(f"/thread?thread_id={thread_id}")
    else:
        return render_template("error.html", message="Failed to edit the message")

@app.route("/delete_message", methods=["POST"])
def delete_message():
    m_id = request.form["m_id"]
    thread_id = request.form["t_id"]

    if messages.delete_m(m_id):
        return redirect(f"/thread?thread_id={thread_id}")
    else:
        return render_template("error.html", message="Failed to delete the message")

@app.route("/edit_t", methods=["POST"])
def edit_t():
    thread_id = request.form["t_id"]
    list = messages.get_list_by_thread(thread_id)
    thread = threads.get_thread(thread_id)

    if len(list) == 0:
        list = [('0', 'default', datetime(1111, 11, 11, 11, 11, 11, 111111), request.args.get("thread_id"), thread[4]),
                ('0', 'default', datetime(2222, 11, 11, 11, 11, 11, 111111), request.args.get("thread_id"), thread[4])]

    return render_template("thread.html", count=len(list), messages=list, thread=thread, edit_t=thread, m_edit=None)

@app.route("/edit_thread", methods=["POST"])
def edit_thread():
    thread_id = request.form["t_id"]
    thread = request.form["thread"]
    print(thread_id)
    users.check_csfr(request.form["csrf_token"])

    if threads.edit_t(thread_id, thread):
        return redirect(f"/thread?thread_id={thread_id}")
    else:
        return render_template("error.html", message="Failed to edit thread name")

@app.route("/delete_thread", methods=["POST"])
def delete_thread():
    thread_id = request.form["t_id"]
    if threads.delete_t(thread_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Failed to delete the message")
 
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
            return render_template("error.html", message="Passwords differ")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed")
        
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template("user.html")
    if request.method == "POST":
        user_id = request.form["user_id"]
        password0 = request.form["password0"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        users.check_csfr(request.form["csrf_token"])
        if password1 != password2:
            return render_template("error.html", message="Passwords differ")
        if users.change_password(user_id,password0,password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Changing password failed")




