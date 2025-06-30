from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, IPAddress

class IPCalculatorForm(FlaskForm):
    ip = StringField('IP Address', validators=[DataRequired(), IPAddress(ipv4=True)])
    subnet = StringField('Subnet Mask or CIDR', validators=[DataRequired()])
    show_details = BooleanField('Show Detailed Information')
    submit = SubmitField('Calculate')
