from flask_admin import BaseView, expose
import flask_login


class DashboardView(BaseView):
	@flask_login.login_required
	@expose('/')
	def index(self):
		return self.render('dashboard_view.html')

	def is_accessible(self):
		return flask_login.current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return flask.redirect(flask.url_for('login', next=flask.request.url))
