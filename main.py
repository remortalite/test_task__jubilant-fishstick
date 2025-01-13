from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
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


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float]
    commission_rate: Mapped[float]
    url_webhook: Mapped[str]
    

class Transaction(db.Model):
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

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Transaction, db.session))


if __name__ == "__main__":
    app.run()
