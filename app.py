from secret import API_TOKEN, API_SECRET_KEY, API_CLIENT_KEY
from flask import Flask, render_template, flash, redirect, request, session, json
import requests
from requests_oauthlib import OAuth1Session
from models import connect_db, db, User
from forms import LoginForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
# from flask_debugtoolbar import DebugToolbarExtension

BASE_URL = "https://api.petfinder.com/v2/animals"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1NmVjaHhhU3RxcUVic2hXNXFNN1VpSURuY0xQRjk2b3h5N0JYblNHYUl1Ymx0OXdmNCIsImp0aSI6IjY5NGViMzA0MGQyZDYxYzgzMTc4MmFkZTk4NGFiNTcwMmZiNzNlMGFhMDg3ZjljNGM4ODcwZTdmOTE1MDE3MTk5NTEyM2Q4MDdiZjU3N2Q1IiwiaWF0IjoxNjE2NjE0Mjg2LCJuYmYiOjE2MTY2MTQyODYsImV4cCI6MTYxNjYxNzg4Niwic3ViIjoiIiwic2NvcGVzIjpbXX0.vBhl9VeOrZLkIFP3RpOj3qOL1UbgMMmoL2TpXhj6Z3j9BQcB9SfvzsJwGrZKn7w8_14Ag7BdfmtKkDHz0FNEXVH4zCcN_5YXzzOM7_dLV1WVWm41BdSjBAgaDVV27PajXCmya-2uRvi-OyDXGPqSGLX1w9CjkU_L2yBNZKl23H3zX54rn5dx0axgEzcsUUO-zGuGT3xVzSKW1mMThyGw_BIziAmVZc_KEzlS5xCU5hlNe5NIfP6NJ-g9vXSTs7IlvoqR9YQ-QcHlnNXyrW71mkrJLPnGVlLG4w71sIkMbRm2EQUR-M56WittMKexJfUSQZkAHY16JwED-xtsLiNeCA"

app = Flask(__name__)\

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
def signup():
    """Show login/register form."""

    return redirect('/register')

@app.route("/pets")
def homepage():
    """Show homepage."""

    return render_template("pets.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user."""

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login existing user."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect('/pets')
        else:
            form.username.errors = ['Invalid username and/or password.']
            return render_template('register.html', form=form)

    return render_template('login.html', form=form)
    

@app.route("/about/<int:id>", methods=['GET'])
def aboutPet(id):
    """Show info about pet."""

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/{id}', headers=headers)
    pet_info = response.json()

    print('********',pet_info)
    return render_template("pet_info.html", pet_info=pet_info)


@app.route("/contact/<int:id>", methods=['GET'])
def contactOrg(id):
    """Show orgs contact info."""

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/{id}', headers=headers)
    pet_info = response.json()

    return render_template("orgs.html", pet_info=pet_info)



@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

