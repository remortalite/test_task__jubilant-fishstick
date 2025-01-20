from flask_admin import BaseView, expose
import flask_login

from models import Clients, Transactions


class DashboardView(BaseView):
	@flask_login.login_required
	@expose('/')
	def index(self):
		clients_count = Clients.query.count()
		transactions_count = Transactions.query.count()
		
		return self.render('dashboard_view.html', 
						   clients_count=clients_count,
						   transactions_count=transactions_count,
						   )

	def is_accessible(self):
		return flask_login.current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return flask.redirect(flask.url_for('login', next=flask.request.url))
