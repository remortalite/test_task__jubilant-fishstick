from login import login_manager, hash_password
from app import app, db
from admin import ClientsAdminView, TransactionsAdminView
from views import DashboardView
import models

import flask
from flask import request
import flask_login
import hashlib
from flask_admin import Admin
from dotenv import load_dotenv

import json
import uuid
import os


load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

login_manager.init_app(app)

admin = Admin(app)

admin.add_view(DashboardView(name='Dashboard', endpoint='dashboard'))
admin.add_view(ClientsAdminView(models.Clients, db.session))
admin.add_view(TransactionsAdminView(models.Transactions, db.session))


@app.cli.command("create-admin")
def create_user():
    with app.app_context():
        username = input("Set username:")
        password = hash_password(input("Set password:"))
        
        user = models.Users(username=username,
                            password=password)
        db.session.add(user)
        db.session.commit()


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
    user = models.Users.query.filter_by(username=username).first()
    if user and hash_password(password) == user.password:
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return f'Logged in as: {flask_login.current_user.username}. Admin panel <a href="/admin">here</a>'


@app.route('/logout')
def logout():
    username = flask_login.current_user.username
    flask_login.logout_user()
    return f'Logged out, bye {username}! <a href="/login">Login</a>'


@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    with app.app_context():
        data = request.get_json()
        transaction = models.Transactions(**data)
        db.session.add(transaction)
        db.session.commit()

        transaction_id = transaction.id
    return "Transaction created. Id: %s" % transaction_id, 200


@app.route('/cancel_transaction', methods=['POST'])
def cancel_transaction():
    with app.app_context():
        data = request.get_json()
        transaction_id = data['id']
        transaction = models.Transactions.query.get(transaction_id)
        if transaction:
            transaction.status = 'Cancelled'
            db.session.commit()
            return 'Cancelled', 200
    return 'Bad data', 300


@app.route('/check_transaction', methods=['GET'])
def check_transaction():
    with app.app_context():
        data = request.get_json()
        transaction_id = data['id']
        transaction = models.Transactions.query.get(transaction_id)
        return {
            'id': transaction.id,
            'sum': transaction.sum,
            'status': transaction.status,
            'client_id': transaction.client_id,
            }
    return "Bad data", 300


if __name__ == "__main__":
    app.run()
