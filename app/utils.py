from functools import wraps
from flask import session, flash, redirect, url_for
from werkzeug.security import check_password_hash
from flask import current_app as app


def login_required(role):
    def wrapper(original):
        @wraps(original)
        def inner(*args, **kwargs):
            if session.get("username") and session.get("role") == role:
                return original(*args, **kwargs)
            else:
                flash(f"You need to login as {role}", "warning")
                return redirect(url_for("login"))

        return inner

    return wrapper


def check_password(exist_pass, curr_pass):
    return check_password_hash(exist_pass, curr_pass)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )
