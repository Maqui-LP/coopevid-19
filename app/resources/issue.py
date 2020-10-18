from flask import redirect, render_template, request, url_for
from app.db import connection
from app.models.issue import Issue
from app.helpers.auth import authenticated
from app.helpers.granted import granted

# Public resources
def index():
    if not authenticated():
        abort(401)
    if not granted("issue_index"):
        abort(403)

    conn = connection()
    issues = Issue.all(conn)

    return render_template("issue/index.html", issues=issues)


def new():
    if not authenticated():
        abort(401)
    if not granted("issue_new"):
        abort(403)
    return render_template("issue/new.html")


def create():
    conn = connection()
    Issue.create(conn, request.form)

    return redirect(url_for("issue_index"))
