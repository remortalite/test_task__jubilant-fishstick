from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField
from wtforms.validators import InputRequired


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
