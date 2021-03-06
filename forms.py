from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DecimalField
from wtforms.validators import DataRequired, InputRequired, Email


class ContactForm(FlaskForm):                    #https://stackoverflow.com/questions/25324113/email-validation-from-wtform-using-flask
  name = StringField("name",  [InputRequired("Please enter your name.")])
  email = StringField("email", [InputRequired("Please enter your email address."),  Email("This field requires a valid email address")])
  message = TextAreaField("message",  [InputRequired("Not including a message would be stupid")])
  send = SubmitField("Send")


class BalanceForm(FlaskForm):
    accbal = DecimalField("Account Balance", validators=[DataRequired()])
    moninc = DecimalField("Monthly Income", validators=[DataRequired()])
    monexp = DecimalField("Monthly Expenses", validators=[DataRequired()])
    weekexp = DecimalField("Weekly Expenses", validators=[DataRequired()])
    submit = SubmitField("Generate Report")