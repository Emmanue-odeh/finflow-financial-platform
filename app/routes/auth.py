
from flask import render_template, request, redirect, url_for, flash, session
from app.routes import main
from app.services.auth_service import register_user, login_user


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        user, error = register_user(
            full_name,
            email,
            password
        )

        if error:
            flash(error, "error")
            return redirect(url_for("main.register"))

        flash("Your FinFlow account has been created successfully!", "success")
        return redirect(url_for("main.register"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user, error = login_user(email, password)

        if error:
            flash(error, "error")
            return redirect(url_for("main.login"))

        session.clear()
        session["user_id"] = user.id

        return redirect(url_for("main.dashboard"))

    return render_template("login.html")
