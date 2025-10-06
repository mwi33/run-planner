from flask import render_template

from . import web_bp


@web_bp.get("/")
def home():
    return render_template("run_plans/list.html", run_plans=[])
