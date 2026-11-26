from flask import render_template, redirect, url_for, session
from app.routes import main

@main.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    return render_template("dashboard.html")