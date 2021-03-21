from secret import API_TOKEN, API_SECRET_KEY, API_CLIENT_KEY
from flask import Flask, render_template, flash, redirect, request, session
from models import connect_db, db, User
from forms import LoginForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
# from flask_debugtoolbar import DebugToolbarExtension

BASE_URL = "https://api.petfinder.com/v2/animals"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///petfinder"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "seeecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()

@app.route("/")
def login():
    """Show login/register form."""

    return redirect('/register')

@app.route("/pets")
def homepage():
    """Show homepage."""

    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 
        email = form.email.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data

        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username

        return redirect('/pets')

    else:
        return render_template('register.html', form=form)


@app.route("/about")
def aboutPet():
    """Show info about pet."""

    return render_template("about.html", data=data)