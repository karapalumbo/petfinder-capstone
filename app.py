from secret import API_TOKEN, API_SECRET_KEY, API_CLIENT_KEY
from flask import Flask, render_template, flash, redirect, request, session, json, g
import requests
from models import connect_db, db, User, Favorite, Pet
from forms import LoginForm, UserAddForm
from sqlalchemy.exc import IntegrityError
# from flask_debugtoolbar import DebugToolbarExtension

BASE_URL = "https://api.petfinder.com/v2/animals"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1NmVjaHhhU3RxcUVic2hXNXFNN1VpSURuY0xQRjk2b3h5N0JYblNHYUl1Ymx0OXdmNCIsImp0aSI6IjgwMDk1NzAwMjYwNTkxMGJkMzUxYmUwNTIxNDRjNjBjYTg0NjJkNmFjNDU2YmE3NzA3OWY2ZTk4NDFjOGEzNjhhZTkwNTNkOGUzMzZjNTA2IiwiaWF0IjoxNjE2OTY1Mjk4LCJuYmYiOjE2MTY5NjUyOTgsImV4cCI6MTYxNjk2ODg5OCwic3ViIjoiIiwic2NvcGVzIjpbXX0.QS3NqAAZ-LdI0lZFZDC0k_uDsmxwAZE8oQ2uyCxWKlJx20zCQCRdhohbsM1zczIxf9EO2s4QlC3AoPTqhBPn181F6ZuIsCTbuziOqRvhMTMCEi-5Eq31VYOjFLdtuEw98nJ10A9ucaSHic6UbWBakPjB5JSYZHqbvVTJ5CLgtecZrtkO-OLkAOKIax4_7SGHKUQbvUzWp3jCbPx7FHW4uClzmmqFWrK8HfSbHeLUcj0CQdx2tq2WqXGbEkHnWEQX22eFdskQk8Kv0ddacKWMFbd3Xng01D9xrhBXkzI7hOVTbKf0bFuhbkUSs3hjiS8tjFmAUsqcWztnCN0QMY2KTg"
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
db.create_all()


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
    

@app.route("/pets", methods=['GET', 'POST'])
def pets():
    """Show all pets."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/register")

    user = User.query.all()

    js_data = request.get_json()

    print('****************', js_data)
    # return js_data
    
    return render_template("pets.html", user=user, data=js_data)


@app.route("/pet/<int:pet_id>", methods=['GET'])
def aboutPet(pet_id):
    """Show info about pet."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/register")

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/{pet_id}', headers=headers)
    pet_info = response.json()

    return render_template("pet_info.html", pet_info=pet_info)


@app.route("/contact/<int:pet_id>", methods=['GET'])
def contactOrg(pet_id):
    """Show orgs contact info."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/register")

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/{pet_id}', headers=headers)
    pet_info = response.json()

    return render_template("orgs.html", pet_info=pet_info)



@app.route('/favorite/<int:pet_id>', methods=['GET','POST'])
def add_favorite(pet_id):
    """add pet to favorites."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/register")

    if request.method == 'GET':
        
        headers = {
        'Authorization': f'Bearer {TOKEN}',
        }

        response = requests.get(f'{BASE_URL}/{pet_id}', headers=headers)
        pet_info = response.json()

        users = User.query.all()
        # print('$$$$$$$$$$$$$$$$$$$', list(db.session.query(User.id).all()[0])[0])
        
        pet = Pet(
            name=pet_info['animal']['name']
        )

        pets = Pet.query.all()
        
        for p in pets:
            p_id = list(db.session.query(p.id).all()[0])[0]
        #     print('$$$$$$$$$$$$$$$$$$$$$', list(db.session.query(p.id).all()[0])[0])

        fav_pet = Favorite(
            user_id=list(db.session.query(User.id).all()[0])[0],
            pet_id=p_id
        )

        db.session.add(pet)
        db.session.add(fav_pet)

        db.session.commit()


        return redirect('/pets')
        
    return render_template("favorites.html", pet=pet, fav_pet=fav_pet)


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def show_favorites(user_id):
        """show user favorites."""

        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/register")

        user = User.query.get_or_404(user_id)

        return render_template('favorites.html', user=user, fav_pets=user.pets)


@app.route('/logout')
def logout():
    session.pop(CURR_USER_KEY)
    return redirect('/login')

