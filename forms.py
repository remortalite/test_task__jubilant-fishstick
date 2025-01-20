from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SearchField
from wtforms.validators import InputRequired
from sqlalchemy import select

from models import Clients


class TransactionForm(FlaskForm):
	sum = DecimalField('Sum', validators=[InputRequired()])
	status = SelectField('Status', 
						 choices=[
						 	("Waiting", "Waiting"), 
							("Confirmed","Confirmed"),
							("Cancelled","Cancelled"),
							("Expired","Expired")],
						 validators=[InputRequired()],
						)
	client_id = SelectField('Client', coerce=int)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client_id.choices = [(client.id, client) for client in Clients.query.all()]
