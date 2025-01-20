from app import app, db
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from flask_login import UserMixin


STATUSES = ["Waiting", "Confirmed", "Cancelled", "Expired"]


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    commission_rate = db.Column(db.Float, nullable=False)
    url_webhook = db.Column(db.String(250), nullable=False)
    

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    sum = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey(Clients.id))
    client = db.relationship('Clients')

    @validates("status")
    def validate_status(self, key, status):
        if status not in STATUSES:
            raise ValueError(f"Failed status name validation. Choose from {STATUSES}.")
        return status


with app.app_context():
    db.create_all()
