from login import login_manager, hash_password
from app import app, db
from admin import AdminView
import models

import flask
import flask_login
import hashlib
from flask_admin import Admin


import uuid
import os


from dotenv import load_dotenv

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

login_manager.init_app(app)


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
    return f'Logged in as: {flask_login.current_user.username}'


@app.route('/logout')
def logout():
    username = flask_login.current_user.username
    flask_login.logout_user()
    return f'Logged out, bye {username}!'



admin = Admin(app)

admin.add_view(AdminView(models.Clients, db.session))
admin.add_view(AdminView(models.Transactions, db.session))



if __name__ == "__main__":
    app.run()
