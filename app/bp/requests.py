from flask import Blueprint, session, request, redirect, flash, url_for
from app.db import db

from app.models import BookRequest


bp = Blueprint("request", __name__, url_prefix="/request")


@bp.route("/books/<book_id>", methods=["GET", "POST"])
def book_request(book_id):
    user_id = session.get("user_id")
    if request.method == "POST":
        new_request = BookRequest(user_id=user_id, book_id=book_id)
        db.session.add(new_request)
        db.session.commit()
        flash("Book request sent successfully", "info")
        return redirect(url_for("book.list_books"))
