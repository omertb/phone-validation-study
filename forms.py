from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    phone_number = StringField('phone_number', validators=[DataRequired(), Length(min=10, max=10)])


class EnterOtpForm(FlaskForm):
    otp_field = StringField('otp_field', validators=[DataRequired(), Length(min=6, max=6)])
