from secret import API_TOKEN, API_SECRET_KEY, API_CLIENT_KEY
from flask import Flask, render_template, flash, redirect, request, session, json
import requests
from models import connect_db, db, User, Favorite
from forms import LoginForm, UserAddForm
from sqlalchemy.exc import IntegrityError
# from flask_debugtoolbar import DebugToolbarExtension

BASE_URL = "https://api.petfinder.com/v2/animals"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1NmVjaHhhU3RxcUVic2hXNXFNN1VpSURuY0xQRjk2b3h5N0JYblNHYUl1Ymx0OXdmNCIsImp0aSI6IjRlODRjOGQ0M2E0MTAwZjU3MmFjYzZjMTlmM2JiOWUwMWU4MTkwOWQ4NzdhYTFkOTYzOWU4NDlkZTNiNDJiNWE1MjQ1MTk3ZGJkNDk5ZjVhIiwiaWF0IjoxNjE2NjI2MjkxLCJuYmYiOjE2MTY2MjYyOTEsImV4cCI6MTYxNjYyOTg5MSwic3ViIjoiIiwic2NvcGVzIjpbXX0.GETr7-TZP8DAYo0sPzHVnjz0oO5EkcGssJejRXDM1_zL2sLXe4vuxhTgIWdYjJ9vVsueE8nWEdO1c1wkYg1Z2uKWSCLdI0VcEhiNvODHZTx-R1GTa_zQ7hq6R_d7nySVq4sUIpYO67_IbtyftnCfbri-u90SDwpKOIZMTrXHNumOHUjh79cyUb95LxI8qfjm4IwYnkV62BHW00Jh919wy5BE_8GEabGbaBUFvgwAey5_e8Tq8cyDXUtrorync-68ehHm7XchBkapHi0my_dAZVaDXWaKbH1xrabXiXbn6iqRU_kmUjdeewFySAiuQOgHLihGNEtzqYIp6kH6xgklbg"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///petfinder"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "seeecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
# db.create_all()


@app.route('/')
def homepage():
    """Show register form."""

    return redirect('/register')


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
            return render_template('register.html', form=form)

    return render_template('login.html', form=form)
    

@app.route("/pets")
def pets():
    """Show all pets."""

    user = User.query.all()
    return render_template("pets.html", user=user)


@app.route("/pet/<int:pet_id>", methods=['GET'])
def aboutPet(pet_id):
    """Show info about pet."""

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/{id}', headers=headers)
    pet_info = response.json()

    print('********',pet_info)
    return render_template("pet_info.html", pet_info=pet_info)


@app.route("/contact/<int:pet_id>", methods=['GET'])
def contactOrg(pet_id):
    """Show orgs contact info."""

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/{id}', headers=headers)
    pet_info = response.json()

    return render_template("orgs.html", pet_info=pet_info)


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def show_favorites(user_id):
        """show user favorites."""

        user = User.query.get_or_404(user_id)
        print("*******************", user_id)
        return render_template('favorites.html', user=user, favorites=user.favorites)



@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')

