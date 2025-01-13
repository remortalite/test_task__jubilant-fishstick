from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates

import uuid


STATUSES = ["Waiting", "Confirmed", "Cancelled", "Expired"]


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
app.secret_key = str(uuid.uuid4())

admin = Admin(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Users(db.Model):
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

admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Transactions, db.session))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


def create_user():
    username = input("Set username:")
    password = input("Set password:")
    
    user = Users(username=username,
                 password=password)
    db.session.add(user)
    db.session.commit()
    

if __name__ == "__main__":
    with app.app_context():
        create_user()
    app.run()
