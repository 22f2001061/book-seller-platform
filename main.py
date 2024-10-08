from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash

from db import db

from model import User, Category


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "some_secret"
db.init_app(app)


# http://localhost:5000/
@app.route("/")
def home():
    return render_template("index.html")


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


def check_password(exist_pass, curr_pass):
    return check_password_hash(exist_pass, curr_pass)


@app.route("/login", methods=["GET", "POST"])
def login():
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
                flash("Login Successfull", "info")
                return redirect(url_for("home"))
            else:
                flash("Please enter correct password.", "warning")
                return redirect(url_for("login"))
        else:
            flash("Username does not exist", "warning")
            return redirect(url_for("login"))


@app.route("/about/<user_name>")
def about(user_name):
    age = 28
    return render_template("about.html", name=user_name, age=age)


@app.route("/books")
def list_books():
    book_list = [
        {"id": 1, "title": "Book title 1", "author": "author 1"},
        {"id": 2, "title": "Book title 2", "author": "author 2"},
        {"id": 3, "title": "Book title 3", "author": "author 3"},
    ]
    return render_template("book_list.html", books=book_list)


@app.route("/categories")
def list_categories():
    categoreies = Category.query.all()
    return render_template("category/list.html", existing_categories=categoreies)


@app.route("/create/category", methods=["GET", "POST"])
def create_category():
    if request.method == "GET":
        return render_template("category/create.html")
    elif request.method == "POST":
        name = request.form.get("categoryName")
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()

        flash("Category added successfully!", "success")
        return redirect(url_for("list_categories"))


@app.route("/edit/category/<id>", methods=["GET", "POST"])
def edit_category(id):
    existing_cat = Category.query.get(id)
    if existing_cat:
        ...


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# @app.route("create_user")
# def create_user():
#     # get the input data from request
#     # save the data in the database and create a new user
#     pass
