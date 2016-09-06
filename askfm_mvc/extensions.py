from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_security.forms import LoginForm
from wtforms import StringField
from wtforms.validators import InputRequired

db = SQLAlchemy()

security = Security()


class ExtendedLoginForm(LoginForm):
    email = StringField('Username or Email Address', [InputRequired()])
