from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Email, InputRequired, DataRequired, Length

class LoginForm(FlaskForm):
    """Form for logging users in."""

    username = StringField("Username", validators=[InputRequired("Please add a username")])
    password = PasswordField("Password", validators=[InputRequired("Please add a password")])
    email = StringField("Email", validators=[InputRequired("Please add an email")])
    first_name = StringField("First Name", validators=[InputRequired("First name can't be blank")])
    last_name = StringField("Last Name", validators=[InputRequired("Last name can't be blank")])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('E-mail', validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])


class PetTypeForm(FlaskForm):
    """Form for searching by pet type."""

    species = SelectField(u'Species', choices=[('cat'), ('dog'), ('rabbit')])
    gender = SelectField(u'Gender', choices=[('male'), ('female')])
    age = SelectField(u'Age', choices=[('baby'), ('young'), ('adult'), ('senior')])
    size = SelectField(u"Size", choices=[('small'), ('medium'), ('large')])
    color = SelectField(u"Color", choices=[('black'), ('white'), ('brown')])