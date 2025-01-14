import models

from flask_login import LoginManager, UserMixin, login_required

import hashlib


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.filter_by(id=user_id).first()


def hash_password(password):
    hash = password + "NOTSECURE"
    hash = hashlib.sha1(hash.encode())
    password = hash.hexdigest()
    return password


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized. Login: <a href="/login">there</a>', 401
