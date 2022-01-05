from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from cs50 import SQL
from helpers import login_required, search_song, search_song_by_id

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to db
db = SQL("sqlite:///project.db")

@app.route("/welcome")
def welcome():

    return render_template("welcome.html")


@app.route("/login", methods=['GET', 'POST'])
def login():

    # Forget any user_id
    #session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            flash("Please input a valid email address", "email_error")
            return redirect("/login")


        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please input a valid password", "password_error")
            return redirect('/login')

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("email"))

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Incorrect Username or Password", "incorrect_details")
            return redirect('/login')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to index page
        return redirect(url_for("index"))

    else:
        return render_template("login.html")


@app.route("/", methods=['GET','POST'])
@login_required
def index():

    rows = db.execute("SELECT * FROM hosts")

    return render_template("index.html", rows=rows)


@app.route("/search/<location>", methods=['GET','POST'])
@login_required
def search(location):

    if request.method == 'POST':

        # Get song name
        song = request.form.get("name")

        # If there is a valid input
        if song != "":

            # Get song information
            info = search_song(song)

            # Sender ID
            sender_id = session["user_id"]

            # Pass song info to searched
            return render_template("searched.html", info=info, name=song, location=location, sender_id=sender_id)

    return render_template("search.html", location=location)


@app.route("/about")
def about():

    return render_template("about.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        # Ensure username
        if not request.form.get("username"):
            flash("Please input a valid username", 'username_error')
            return redirect("/register")

        # Ensure email
        elif not request.form.get("email"):
            flash("Please input a valid email address", "email_error")
            return redirect("/register")

        # Ensure password
        elif not request.form.get("password"):
            flash("Please input a valid password", "password_error")
            return redirect("/register")

        # Ensure password match
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Please ensure passwords match", "match_error")
            return redirect("/register")

        else:

            # query db for username
            rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))
            if len(rows) != 0:
                flash("Username already in use!", "username_in_use")
                return redirect("/register")

            # query db for email
            rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("email"))
            if len(rows) != 0:
                flash("Email already in use!", "email_in_use")
                return redirect("/register")

            else:
                name = request.form.get("username")
                email = request.form.get("email")
                hash = generate_password_hash(request.form.get("password"))

                # Insert user data into db
                db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", name, email, hash)

                rows = db.execute("SELECT * FROM users WHERE username=?", name)
                session["user_id"] = rows[0]["id"]

                return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/host", methods=['GET', 'POST'])
@login_required
def host():

    host_id = session['user_id']
    location = db.execute("SELECT location FROM hosts WHERE host_id=?", host_id)

    if location:
        location=location[0]['location']
        return redirect(f"/hosting/{location}")

    if request.method == "POST":

        # Get location, host, host_id
        location = request.form.get("location")
        host = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        host = host[0]['username']
        host_id = session["user_id"]

        # Insert location into db
        db.execute("INSERT INTO hosts (location,host,host_id) VALUES(?,?,?)", location,host,host_id)

        return redirect(f"/hosting/{location}")

    return render_template("host.html")


@app.route("/hosting/<location>", methods=['GET', 'POST'])
@login_required
def hosting(location):


    host_id = session["user_id"]
    loc = db.execute("SELECT location_id FROM hosts WHERE host_id=?", host_id)
    location_id = loc[0]['location_id']

    if request.method == "POST":

        song_id = request.form['song_id']
        #sender_id = request.form["sender_id"]
        #print(sender_id)
        song_id = song_id.strip()
        db.execute("INSERT INTO requests(song_id, location_id) VALUES(?,?)", song_id,location_id)

        return redirect(f"/hosting/{location}")

    else:

        song_ids = db.execute("SELECT song_id FROM requests WHERE location_id=?", location_id)

        list_of_song_ids = []

        for i in range(len(song_ids)):
            list_of_song_ids.append(song_ids[i]['song_id'])

            '''
            Things to add:
            Make a counter for songs so that theres a record of number of requests
            make a limit to number of votes?
            Could change display to show popularity of requests

            '''

        list_of_song_ids = list(dict.fromkeys(list_of_song_ids))

        return render_template("hosting.html", location=location, song_ids=list_of_song_ids, f=search_song_by_id)


@app.route("/logout")
def logout():
    """Log user out"""

    host_id = session["user_id"]
    location = db.execute("SELECT location_id FROM hosts WHERE host_id=?", host_id)


    if location:

        # Remove songs from request db
        location_id = location[0]['location_id']
        db.execute("DELETE FROM requests WHERE location_id=?", location_id)

    # Remove host location from db
    db.execute("DELETE FROM hosts WHERE host_id=?", host_id)

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
