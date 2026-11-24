
from flask import render_template
from app.routes import main


@main.route("/")
def dashboard():
    return render_template("dashboard.html")
