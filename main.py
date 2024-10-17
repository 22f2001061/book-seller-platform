from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps

from app.db import db

from app.models import User, Category, BookRequest

from app.config import LocalConfig
from app.utils import login_required, check_password

from app.bp.book import bp as book_bp
from app.bp.category import bp as category_bp
from app.bp.requests import bp as request_bp


app = Flask(__name__)


app.config.from_object(LocalConfig)
db.init_app(app)

app.register_blueprint(book_bp)
app.register_blueprint(category_bp)
app.register_blueprint(request_bp)


# http://localhost:5000/
@app.route("/")
def home():
    buyer_requests = []
    all_requests = []
    user_role = session.get("role")
    if user_role:
        if user_role == "admin":
            all_requests = BookRequest.query.all()
        elif user_role == "buyer":
            buyer_id = session.get("user_id")
            buyer_requests = BookRequest.query.filter_by(user_id=buyer_id).all()
        return render_template(
            "index.html", all_requests=all_requests, buyer_requests=buyer_requests
        )
    else:
        return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        # Send the html register form to the view layer
        return render_template("user/register.html")
    elif request.method == "POST":

        # print(request.form)

        # 1. grab the data from the request
        username = request.form.get("username", "")
        # if username is not 4 or more character
        # flash the message saying the error -> username should atleast be 4 chars long
        # return a redirect to the register page

        print("username is : ", username)
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if password1 != password2:
            flash("Confirm password does not match with Password", "warning")
            return redirect(url_for("register"))
        role = request.form.get("role")

        # 2. make an entry to the database
        try:
            new_user = User(
                username=username,
                email=email,
                fname=fname,
                lname=lname,
                password=generate_password_hash(password1),
                role=role,
            )
            db.session.add(new_user)
            db.session.commit()
            # 3. redirect with the appropriate response
            flash("Registration successful!", "success")
            return redirect(url_for("home"))
        except Exception as e:
            # if IntegrityError with username:
            #   msg = username exist
            # elif integrityError with email:
            #   msg = email already exist
            # flash(msg, "warning")
            flash("Something went wrong", "danger")
            return e


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("home"))
    if request.method == "GET":
        return render_template("user/login.html")
    elif request.method == "POST":
        # 1. get the data from the form
        email_or_username = request.form.get("username")
        password = request.form.get("password")

        # 2. make an entry or find an entry from the database
        existing_user = User.query.filter_by(username=email_or_username).first()
        print(existing_user)
        print(url_for("login"))
        # verify the user identity
        if existing_user:
            if check_password(existing_user.password, password):
                session["user_id"] = existing_user.id
                session["username"] = existing_user.username
                session["role"] = existing_user.role
                flash("Login Successfull", "info")
                return redirect(url_for("home"))
            else:
                flash("Please enter correct password.", "warning")
                return redirect(url_for("login"))
        else:
            flash("Username does not exist", "warning")
            return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user_id")
    session.pop("username")
    session.pop("role")
    return redirect(url_for("home"))


@app.route("/sample-chart")
def sample_chart():
    return render_template("sample_chart.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()


# @app.route("create_user")
# def create_user():
#     # get the input data from request
#     # save the data in the database and create a new user
#     pass
