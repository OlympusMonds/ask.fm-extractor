from flask import Flask

from askfm_mvc import settings
from askfm_mvc.extensions import db, security, ExtendedLoginForm
from askfm_mvc.models import User, Role
from askfm_mvc.index import bp as index

from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password


app = Flask(__name__, static_url_path = '')

app.config.from_object(settings)

db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, user_datastore,
                  login_form=ExtendedLoginForm)


app.register_blueprint(index)


def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.first():
            user_datastore.create_user(email=app.config['ADMIN_USERNAME'], 
                                       password=encrypt_password(app.config['ADMIN_PASSWORD']))
            db.session.commit()


if __name__ == "__main__":
    init_db()
    app.debug = True
    app.run()



