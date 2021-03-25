from secret import API_TOKEN, API_SECRET_KEY, API_CLIENT_KEY
from flask import Flask, render_template, flash, redirect, request, session, json, g
import requests
from models import connect_db, db, User, Favorite
from forms import LoginForm, UserAddForm
from sqlalchemy.exc import IntegrityError
# from flask_debugtoolbar import DebugToolbarExtension

BASE_URL = "https://api.petfinder.com/v2/animals"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1NmVjaHhhU3RxcUVic2hXNXFNN1VpSURuY0xQRjk2b3h5N0JYblNHYUl1Ymx0OXdmNCIsImp0aSI6IjMyMzMxZmExZDdjNDUzYzA4MDU3N2JhMWM4MzliYjdkNTc0Mzg0NGNlZTAxM2I0YmIxMDA4N2Y1YTU2NmYzZDdiNWQxMmI3NmJmNGJkNWZiIiwiaWF0IjoxNjE2NjkyNzE1LCJuYmYiOjE2MTY2OTI3MTUsImV4cCI6MTYxNjY5NjMxNSwic3ViIjoiIiwic2NvcGVzIjpbXX0.AUbBMyTo1-ALDueYkf-gukRnirnDuk98MzjiYgf-ATXnZ9WxQHPG1ECihkwgn8rM8qvCTe4YLZdcQJvRPW2lhenSWjH8mgdKKrxhhGUYLPPoxuMCtv-8WH6Srlg9CiDhKUtZ3dNAITCDUAExMg_mu9uAM5eqVXCpQMRjmAYHzZSM34aauEE_aIcTUoAvbfFpgb-xwHRdWiusS-PYunYIGY4o4GSKTg0HUh207rk8Ox3GghF9Dz0UQE9LXWgZENJyzWYBujQoYEUJjkGv5rtCcOKR1lZVVaKkNeW3EhcglGHoNSV6zT0bDKb9HPDDYSgsvj9bcpy3M2_sRccuQ8Z8Pg"
CURR_USER_KEY = "current_user"

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


@app.before_request
def add_user_to_g():
    """Add user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


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
            do_login(user)
            return redirect('/pets')

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

    response = requests.get(f'{BASE_URL}/{pet_id}', headers=headers)
    pet_info = response.json()

    return render_template("pet_info.html", pet_info=pet_info)


@app.route("/contact/<int:pet_id>", methods=['GET'])
def contactOrg(pet_id):
    """Show orgs contact info."""

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/{pet_id}', headers=headers)
    pet_info = response.json()

    return render_template("orgs.html", pet_info=pet_info)


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def show_favorites(user_id):
        """show user favorites."""

        user = User.query.get_or_404(user_id)

        return render_template('favorites.html', user=user, favorites=user.favorites)


@app.route('/favorite/<int:fav_id>/<int:pet_id>', methods=['POST'])
def add_favorite(fav_id, pet_id):
    """add pet to favorites."""

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/{pet_id}', headers=headers)
    pet_info = response.json()

    fav_pet = Favorite.query.get_or_404(fav_id)
    if fav_pet.user_id == g.user.id:
        return abort(403)

    user_fav = g.user.favorites

    if fav_pet in user_fav:
        g.user.favorites = [favorite for favorite in user_favorites if favorite != fav_pet]
    else:
        g.user.favorites.append(fav_pet)

    db.session.commit()

    return redirect('/pets')


@app.route('/logout')
def logout():
    session.pop(CURR_USER_KEY)
    return redirect('/login')

