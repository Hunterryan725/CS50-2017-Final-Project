from cs50 import SQL
import os
import smtplib
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import random

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

UPLOAD_FOLDER = os.path.basename('/workspace/project/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@login_required
def index():
    """Display list of forums"""

    # Render index
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("email"):
            return apology("missing email")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Generate random value to be used as access key
        r = random.randint(11111, 99999)

        # Store value of firstname in "firstname"
        firstname = request.form.get("firstname")

        # Add user and information to database
        id = db.execute("INSERT INTO users (firstname, lastname, hash, email, accesskey, university, graduation, major) \
        VALUES(:firstname, :lastname, :hash, :email, :accesskey, :university, :graduation, :major)",
                        firstname=firstname,
                        lastname=request.form.get("lastname"),
                        hash=generate_password_hash(request.form.get("password")),
                        email=request.form.get("email"),
                        accesskey=r,
                        university=request.form.get("university"),
                        graduation=request.form.get("graduation"),
                        major=request.form.get("major")),

        # Confirm user information does not already exist in database
        if not id:
            return apology("username taken")

        # Store the user's email in email
        email = request.form.get("email")

        # Send the user a sign up confirmation email containing a short message and their access key
        message = (
            f"Congratulations {firstname}, You are registered for Locality at Yale! Your access key is - {r}")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("localityyale@gmail.com", os.getenv("PASSWORD"))
        server.sendmail("localityyale@gmail.com", email, message)

        # Let user know they're registered
        flash("Registered!")
        return redirect("/login")

    # GET
    else:

        # Render register
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("email"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Access the user's access key in database and store
        accesskey = rows[0]["accesskey"]

        # Store the user's inputted key
        inputkey = request.form.get("accesskey")

        # Make sure the access key the user inputs and and the access key in the database match
        if (accesskey) != int(inputkey):
            return apology("incorrect access key", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Render login
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """Allow user to post a forum to the server"""

    # POST
    if request.method == "POST":

        # Store the post in the database
        forum = db.execute("INSERT INTO forums (thread, title, description, id) VALUES(:thread, :title, :description, :id)",
                           thread=request.form.get("thread"),
                           title=request.form.get("title"),
                           description=request.form.get("description"),
                           id=session["user_id"]),

        if not forum:
            return apology("thread invalid")

        # Redirect to index page
        return redirect("/")

    # GET
    else:

        # Render post
        return render_template("post.html")


@app.route('/myposts', methods=['GET'])
@login_required
def myposts():
    """Allow the user to view the the threads he or she created"""

    # Return threads that were created by the user
    threads = db.execute("SELECT * FROM forums WHERE id = :id",
                         id=session["user_id"]),

    # Render myposts
    return render_template("myposts.html", threads=threads[0])


@app.route('/forums/<forum>', methods=['GET', "POST"])
@login_required
def forum(forum):
    """Display a list of threads a user can click on, as well as the option to post a thread"""

    # GET
    if request.method == "GET":

        # Returns from database threads that were posted under the same forum category
        threads = db.execute("SELECT users.firstname, users.lastname, forums.time, forums.title, users.id, forums.thread, forums.threadid \
        FROM users INNER JOIN forums ON users.id = forums.id WHERE thread = :thread", thread=forum),

        # Render forums
        return render_template("forums.html", threads=threads[0])

    # POST
    if request.method == "POST":

        # Render threads
        return redirect(f"/post/{forum}")


@app.route('/forums/<forum>/<article>', methods=['GET', "POST"])
@login_required
def thread(forum, article):
    """Allows user to view the original post and all comments on it"""

    # GET
    if request.method == "GET":

        # Returns the original post
        threads = db.execute("SELECT users.firstname, users.lastname, users.id, forums.description, forums.title, forums.time \
        FROM users INNER JOIN forums ON users.id = forums.id WHERE threadid = :threadid", threadid=article),

        # Returns the comments on the post
        comments = db.execute("SELECT users.firstname, users.lastname, users.id, threads.comment, threads.time, threads.id \
        FROM users INNER JOIN threads ON users.id = threads.id WHERE threadid = :threadid", threadid=article),

        # Render threads
        return render_template("threads.html", threads=threads[0], comments=comments[0])

    # POST
    if request.method == "POST":

        # Store new comment in database
        results = db.execute("INSERT INTO threads (threadid, id, comment) VALUES(:threadid, :id, :comment)",
                             threadid=article,
                             id=session["user_id"],
                             comment=request.form.get("comment")),

        # Refresh the page
        return redirect(f"/forums/{forum}/{article}")


@app.route("/profile", methods=['GET', "POST"])
@login_required
def profile():
    """A more private page displaying user personal information"""

    # GET
    if request.method == "GET":

        # Return user information
        users = db.execute("SELECT * FROM users WHERE id = :id",
                           id=session["user_id"]),

        # Render Profile
        return render_template("profile.html", users=users[0])

    # POST
    if request.method == "POST":

        # Upload Image
        file = request.files['image']
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Store image name in database for user
        users = db.execute("UPDATE users SET image = :image WHERE id = :id",
                           image=f,
                           id=session["user_id"]),

        # Save Image
        file.save(f)

        # Redirect user back to profile
        return redirect("/profile")


@app.route("/profile/<name>", methods=['GET'])
@login_required
def uprofile(name):
    """Public profile page all user's can see"""

    # Return user information from the database
    users = db.execute("SELECT * FROM users WHERE id = :id", id=name),

    # Render userprofile
    return render_template("userprofile.html", users=users[0])


@app.route("/userposts/<name>", methods=['GET'])
@login_required
def userposts(name):
    """Displays a user's created threads for all to see"""

    # Return user created threads and information
    threads = db.execute("SELECT users.firstname, users.lastname, forums.time, forums.title, users.id, forums.thread, forums.threadid \
        FROM users INNER JOIN forums ON users.id = forums.id WHERE users.id = :id", id=name),

    # Render userposts
    return render_template("userposts.html", threads=threads[0])


@app.route('/post/<forum>', methods=['GET', "POST"])
@login_required
def spost(forum):
    """Allows user to post after clicking on post buttton on forums page"""

    # POST
    if request.method == "POST":

        # Store thread in database
        sposts = db.execute("INSERT INTO forums (thread, title, description, id) VALUES(:thread, :title, :description, :id)",
                            thread=forum,
                            title=request.form.get("title"),
                            description=request.form.get("description"),
                            id=session["user_id"]),
        # Ensure forum is valid
        if not forum:
            return apology("thread invalid")

        # Redirect to homepage
        return redirect("/")

    # GET
    else:

        # Render sposts
        return render_template("spost.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
