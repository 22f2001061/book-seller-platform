from flask import Blueprint, session, request, redirect, flash, url_for
from app.db import db
from app.utils import login_required
from app.models import BookRequest
from datetime import datetime

bp = Blueprint("request", __name__, url_prefix="/request")


@bp.route("/books/<book_id>", methods=["GET", "POST"])
@login_required("buyer")
def book_request(book_id):
    user_id = session.get("user_id")
    if request.method == "POST":
        new_request = BookRequest(user_id=user_id, book_id=book_id)
        db.session.add(new_request)
        db.session.commit()
        flash("Book request sent successfully", "info")
        return redirect(url_for("book.list_books"))


@bp.route("/<action>/<request_id>")
@login_required("admin")
def update_request(action, request_id):
    book_request = BookRequest.query.get(request_id)
    if book_request:
        print(book_request.status)
        if action.lower() == "accept":
            book_request.date_issued = datetime.now()
            book_request.status = "accepted"
            db.session.add(book_request)
            db.session.commit()
            print("after edit")
            print(book_request.status)
        elif action.lower() == "reject":
            book_request.date_returned = datetime.now()
            book_request.status = "rejected"
            db.session.add(book_request)
            db.session.commit()

    return redirect(url_for("home"))
