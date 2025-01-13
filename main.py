import flask 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_required
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from dotenv import load_dotenv
import hashlib

import uuid
import os


STATUSES = ["Waiting", "Confirmed", "Cancelled", "Expired"]

load_dotenv()

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



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


def hash_password(password):
    hash = password + str(app.secret_key)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = flask.request.form['username']
    password = flask.request.form['password']
    print(username, password)
    user = Users.query.filter_by(username=username).first()
    if user and hash_password(password) == user.password:
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return f'Logged in as: {flask_login.current_user.username}'


@app.route('/logout')
def logout():
    username = flask_login.current_user.username
    flask_login.logout_user()
    return f'Logged out, bye {username}!'


class AdminView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


admin.add_view(AdminView(Clients, db.session))
admin.add_view(AdminView(Transactions, db.session))

if __name__ == "__main__":
    app.run()
