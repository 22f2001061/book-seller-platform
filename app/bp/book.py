import os
from flask import Blueprint, redirect, request, url_for, render_template, session, flash
from flask import current_app as app

from app.db import db
from app.models import Book, Category
from app.utils import login_required, allowed_file
from sqlalchemy import or_
from werkzeug.utils import secure_filename

import json

bp = Blueprint(
    "book",
    __name__,
)


# CRUD on Books
# base/books -> list of all the books


# q = "Book" -> case 1
# q = "book" -> case 2
@bp.route("/books")
def list_books():
    query = request.args.get("q")
    books = Book.query.all()
    if query:
        # %query%
        query = f"%{query}%"
        books = Book.query.filter(
            or_(
                Book.title.ilike(query),
                Book.author.ilike(query),
            )
        ).all()
    # return {"title": books[0].title, "author": books[0].author}
    return render_template("book/list.html", books=books)


@bp.route("/create/books", methods=["GET", "POST"])
@login_required("admin")
def create_and_list_books():
    categories = Category.query.all()
    if request.method == "GET":
        return render_template("book/create.html", available_categories=categories)
    elif request.method == "POST":
        author_name = request.form.get("authorName")
        category_id = request.form.get("categoryId")
        title = request.form.get("bookTitle")
        print(request.files)
        print(request.form)
        if "bookFile" not in request.files:
            flash("No book content uploaded", "warning")
            return redirect(url_for("book.create_and_list_books"))
        book_content = request.files["bookFile"]
        thumbnail = request.files["thumbnail"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if book_content.filename == "":
            flash("No selected file", "warning")
            return redirect(request.url)
        if book_content and allowed_file(book_content.filename):
            print(book_content.filename)
            book_file_name = secure_filename(book_content.filename)
            print(book_file_name)
            book_content.save(os.path.join(app.config["UPLOAD_FOLDER"], book_file_name))
        if thumbnail and allowed_file(thumbnail.filename):
            thumbnail_name = secure_filename(thumbnail.filename)
            thumbnail.save(os.path.join(app.config["UPLOAD_FOLDER"], thumbnail_name))
        new_book = Book(
            title=title,
            content=book_file_name,
            thumbnail=thumbnail_name,
            author=author_name,
            category_id=category_id,
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f"New book with title: {title} is created!", "success")
        return redirect(url_for("book.list_books"))


@bp.route("/edit/books/<book_id>", methods=["GET", "POST"])
@login_required("admin")
def edit_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if request.method == "GET":
        Categorys = Category.query.all()
        return render_template(
            "book/edit.html", book=book, available_Categorys=Categorys
        )
    if request.method == "POST":
        title = request.form.get("bookTitle")
        book_content = request.form.get("bookContent")
        author_name = request.form.get("authorName")
        category_id = request.form.get("CategoryId")
        book.title = title
        book.content = book_content
        book.author = author_name
        book.category_id = category_id
        db.session.add(book)
        db.session.commit()
        flash(f"Book with title: {title} is edited successfully!", "info")
        return redirect(url_for("book.list_books"))


@bp.route("/delete/books/<book_id>", methods=["GET", "POST"])
@login_required("admin")
def delete_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if request.method == "GET":
        return render_template("book/confirm_delete.html", book=book)
    if request.method == "POST":
        # handle edit operation.
        if book:
            db.session.delete(book)
            db.session.commit()
            flash(
                f"Book with id: {book.book_id} is deleted successfully!",
                "success",
            )
        else:
            flash(f"Book with id: {book_id} is does not exit!", "warning")

        return redirect(url_for("book.list_books"))
