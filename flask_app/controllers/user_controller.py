from flask_app import app

# import all the features we need to run our app routes
from flask import render_template , redirect, request, session, flash 

# import all the models we will need to access for class/ static methods 
from flask_app.models.user_model import User
from flask_app.models.rhyme_model import Rhyme 

# import bcrypt to hash password info 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return redirect("/login")

# I want to make sure a user isnt logged in and if they are then i redirect back to dash board
# validate email and passwords match and that username has over a minimum length 
# create the user using the request form and the user method for adding a user
# add a session["user.id"] to be in there while the person is signed in 
# store the password using bcrypt
@app.route("/signup")
def signup():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("signup.html")

@app.route("/signup_post", methods = ["POST"])
def signup_post():
    if not User.validate_register(request.form):
        return redirect("/signup")
    pw_hash = bcrypt.generate_password_hash(request.form["pw"])

    data = {
        "username": request.form["username"],
        "email": request.form["email"],
        "pw_hash": pw_hash
    }
    user_id = User.add_user(data)
    session["user_id"] = user_id
    return redirect("/home")

@app.route("/login")
def login():
    if "user_id" in session:
        return redirect("/home")
    return render_template("login.html")

@app.route("/login_post", methods =["POST"])
def login_post():
    data = {
        "email": request.form["email"],
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Incorrect Email or Password.", "err.log")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.pw_hash,request.form["pw"]):
        flash("Incorrect Email or Password.", "err.log")
        return redirect("/login")
    session["user_id"] = user_in_db.id
    return redirect("/home")


@app.route("/home")
def home():
    if "user_id" not in session:
        flash("You must register or log in to view content.")
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    user = User.get_one(data)
    all_users = User.get_all_users()
    rhymes = Rhyme.get_all_rhymes()
    return render_template("home.html", user = user, rhymes = rhymes, all_users = all_users )

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You must register or log in to view content.")
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    user = User.get_one(data)
    all_users = User.get_all_users()
    rhymes = Rhyme.get_all_rhymes()
    return render_template("dashboard.html", user = user, rhymes = rhymes, all_users = all_users )



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

