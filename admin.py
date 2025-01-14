from flask_admin.contrib.sqla import ModelView
import flask_login
import flask


class AdminView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(url_for('login', next=request.url))
