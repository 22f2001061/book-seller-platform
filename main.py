from flask import Flask, render_template, request, redirect, url_for

from db import db

from model import User


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
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
        print("username is : ", username)
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        role = request.form.get("role")

        # 2. make an entry to the database
        try:
            new_user = User(
                username=username,
                email=email,
                fname=fname,
                lname=lname,
                password=password1,
                role=role,
            )
            db.session.add(new_user)
            db.session.commit()
            # 3. redirect with the appropriate response
            return redirect(url_for("home"))
        except Exception as e:
            return e


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


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)


# @app.route("create_user")
# def create_user():
#     # get the input data from request
#     # save the data in the database and create a new user
#     pass
