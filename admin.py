from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget 
import flask_login
import flask

from forms import TransactionForm


class AdminView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(flask.url_for('login', next=flask.request.url))


class ClientsAdminView(AdminView):
    column_list = ['balance', 'commission_rate', 'url_webhook']


class TransactionsAdminView(AdminView):
    column_list = ['sum', 'status', 'client', 'client_id']
    form = TransactionForm
