from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import Email, InputRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("Please add a username")])
    password = PasswordField("Password", validators=[InputRequired("Please add a password")])
    email = StringField("Email", validators=[InputRequired("Please add an email")])
    first_name = StringField("First Name", validators=[InputRequired("First name can't be blank")])
    last_name = StringField("Last Name", validators=[InputRequired("Last name can't be blank")])

