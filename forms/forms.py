from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField, PasswordField, TextAreaField, validators
from wtforms.validators import InputRequired, EqualTo
import re


class loginForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])

    submit = SubmitField("Submit")


class registerForm(FlaskForm):
    username = StringField("Username: ", validators=[
                           validators.InputRequired(), validators.Length(min=5)])
    password = PasswordField("Password: ", validators=[
        validators.InputRequired(),
        validators.Length(min=8),
        validators.Regexp(
            regex=r'^(?=.*[\W_]).+$', message='Password must contain at least one special character'),
    ])
    password2 = PasswordField("Confirm password: ", validators=[
                              validators.InputRequired(), validators.EqualTo("password")])
    name = StringField("Given name: ", validators=[validators.InputRequired()])
    surname = StringField("Family name: ", validators=[
                          validators.InputRequired()])
    submit = SubmitField("Submit")


class categoryForm(FlaskForm):
    category = StringField("Category: ", validators=[InputRequired()])
    submit = SubmitField("Add")


class settingsForm(FlaskForm):
    daily_limit = DecimalField("Daily limit: ", validators=[InputRequired()])
    monthly_limit = DecimalField(
        "Monthly limit: ", validators=[InputRequired()])
    submit = SubmitField("Save")


class itemForm(FlaskForm):
    item = StringField("Item: ", validators=[InputRequired()])
    price = DecimalField("Price: ", validators=[InputRequired()])
    category = SelectField("Category: ")
    description = TextAreaField('Description')
