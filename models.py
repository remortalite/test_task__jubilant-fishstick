from app import app, db
from sqlalchemy.orm import Mapped, mapped_column, validates
from flask_login import UserMixin


STATUSES = ["Waiting", "Confirmed", "Cancelled", "Expired"]


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
