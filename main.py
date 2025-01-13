from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_required
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from dotenv import load_dotenv

import uuid
import os


STATUSES = ["Waiting", "Confirmed", "Cancelled", "Expired"]


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
app.secret_key = os.getenv("SECRET_KEY")

admin = Admin(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Clients(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float]
    commission_rate: Mapped[float]
    url_webhook: Mapped[str]
    

class Transactions(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    sum: Mapped[float]
    status: Mapped[str]

    @validates("status")
    def validate_status(self, key, status):
        if status not in STATUSES:
            raise ValueError(f"Failed status name validation. Choose from {STATUSES}.")
        return status


with app.app_context():
    db.create_all()

admin.add_view(ModelView(Clients, db.session))
admin.add_view(ModelView(Transactions, db.session))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


def hash_password(password):
    hash = password + app.secret_key
    hash = hashlib.sha1(hash.encode())
    password = hash.hexdigest()
    return password


@app.cli.command("create-admin")
def create_user():
    with app.app_context():
        username = input("Set username:")
        password = hash_password(input("Set password:"))
        
        user = Users(username=username,
                     password=password)
        db.session.add(user)
        db.session.commit()


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


if __name__ == "__main__":
    app.run()
