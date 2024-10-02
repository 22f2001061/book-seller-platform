from flask import Flask

app = Flask(__name__)


# http://localhost:5000/
@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    # if request.method == "GET":
    ...
    # Send the html register form to the view layer
    pass


# @app.route("create_user")
# def create_user():
#     # get the input data from request
#     # save the data in the database and create a new user
#     pass
