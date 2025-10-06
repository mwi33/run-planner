from flask import render_template
from flask.typing import ResponseReturnValue

from . import web_bp


@web_bp.get("/")
def home() -> ResponseReturnValue:
    return render_template("run_plans/list.html", run_plans=[])
