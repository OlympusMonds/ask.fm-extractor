from .extensions import db
from .models import User, Role
from flask import Blueprint
from flask_security import login_required

bp = Blueprint('askfm', __name__)

@bp.route("/")
@login_required
def index():
    return ("<h1> Ask.fm extractor </h1><p>"
            "To use this site, add a /username after the .com</br>"
            "For example olympusmonds.pythonanywhere.com/olympusmonds")


@bp.route("/<username>")
def extract_for_user(username):
    print("Request for {}".format(username))

    html = True
    if html:
        pass #output = extract(username, newline="<br/>")
    else:
        pass #output = extract(username)
    return "Blarg"  #output


@bp.route("/register")
def register():
    return register_user_form()


