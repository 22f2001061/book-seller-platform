from flask import Blueprint, render_template, url_for, redirect, flash, request
from app.db import db
from app.models import Category
from app.utils import login_required


bp = Blueprint("category", __name__, url_prefix="")


@bp.route("/categories")
def list_categories():
    categoreies = Category.query.all()
    return render_template("category/list.html", existing_categories=categoreies)


@bp.route("/create/category", methods=["GET", "POST"])
@login_required("admin")
def create_category():
    if request.method == "GET":
        return render_template("category/create.html")
    elif request.method == "POST":
        name = request.form.get("categoryName")
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()

        flash("Category added successfully!", "success")
        return redirect(url_for("category.list_categories"))


@bp.route("/edit/category/<id>", methods=["GET", "POST"])
@login_required("admin")
def edit_category(id):
    existing_cat = Category.query.get(id)
    if existing_cat:
        if request.method == "GET":
            return render_template("category/edit.html", category=existing_cat)
        elif request.method == "POST":
            new_name = request.form.get("categoryName")
            message = "Category update sucessfully!"
            if new_name != existing_cat.name:
                existing_cat.name = new_name
                db.session.add(existing_cat)
                db.session.commit()
            flash(message, "info")
            return redirect(url_for("category.list_categories"))
    else:
        return redirect(url_for("home"))


@bp.route("/delete/category/<id>", methods=["GET", "POST"])
@login_required("admin")
def delete_category(id):
    existing_cat = Category.query.get(id)
    if existing_cat:
        if request.method == "GET":
            return render_template(
                "category/confirm_delete.html", category=existing_cat
            )
        elif request.method == "POST":
            db.session.delete(existing_cat)
            db.session.commit()
            message = "Category deleted sucessfully!"
            flash(message, "info")
            return redirect(url_for("category.list_categories"))
    else:
        flash("Category with the id not found!")
        return redirect(url_for("home"))
