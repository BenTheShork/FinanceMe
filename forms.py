from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, EqualTo

class loginForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])
    
    submit = SubmitField("Submit")

class registerForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])
    password2 = PasswordField("Confirm password: ", validators=[InputRequired(), EqualTo("password")])
    name = StringField("Given name: ", validators=[InputRequired()])
    surname = StringField("Family name: ", validators=[InputRequired()])
    
    submit = SubmitField("Submit")

class categoryForm(FlaskForm):
    category = StringField("Category: ", validators=[InputRequired()])
    submit = SubmitField("Add")
    
class settingsForm(FlaskForm):
    daily_limit = DecimalField("Daily limit: ", validators=[InputRequired()])
    monthly_limit = DecimalField("Monthly limit: ", validators=[InputRequired()])
    submit = SubmitField("Save")
    
class itemForm(FlaskForm):
    item = StringField("Item: ", validators=[InputRequired()])
    price = DecimalField("Price: ", validators=[InputRequired()])
    category = SelectField("Category: ")
    description = TextAreaField('Description')  