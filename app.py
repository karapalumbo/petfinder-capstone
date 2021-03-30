from secret import API_TOKEN, API_SECRET_KEY, API_CLIENT_KEY
from flask import Flask, render_template, flash, redirect, request, session, json, g
import requests
import petpy
from models import connect_db, db, User, Pet
from forms import LoginForm, UserAddForm, PetTypeForm
from sqlalchemy.exc import IntegrityError
# from flask_debugtoolbar import DebugToolbarExtension

BASE_URL = "https://api.petfinder.com/v2"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1NmVjaHhhU3RxcUVic2hXNXFNN1VpSURuY0xQRjk2b3h5N0JYblNHYUl1Ymx0OXdmNCIsImp0aSI6ImVmMWIwZDhmZjEyNjc1ZDY0ZTQ4MTYyNmFjZTY5M2YzYWUyYzgxMjY4MjVlNmVmY2M5ZDgxZTM2NjBjYjMyYTJlNjhjMWU5NTJiNjRkZmY2IiwiaWF0IjoxNjE3MTMyNzgxLCJuYmYiOjE2MTcxMzI3ODEsImV4cCI6MTYxNzEzNjM4MSwic3ViIjoiIiwic2NvcGVzIjpbXX0.a1I4IstpzDN2hdT6hooeNtSnBfWnz0RIbTyyzWbJweG5JKBtg1cPagn67nsu3DSBJdkNMn1SUaZFRt-aFv-U7BLeM7SYew4Av7rCnCqOOOxS4BiYBCsjwSIPHeTZyUztsXe9Zwf5qBaZMg-OEeuqbGa7V1uptOmXsPuy_XBgLWT4Hux3SlDOgfKmkKH-yEyLEIlAh57UJ5m2Z16vgApnxaaDcToj4dLsHFQ4k6F2SaO4ZzBFH_ftuUz16aCsL-qiO_y7Cw1OJZgI6z-Fd2M4izI1NhlQUXNz62hy6WEs6YAnoRThfXQShQXhsad_OF8GnZXYxrJxNFR5vXcibkarwA"
CURR_USER_KEY = "current_user"

pf = petpy.Petfinder(key=API_CLIENT_KEY, secret=API_SECRET_KEY)

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

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username = form.username.data,
                password = form.password.data,
                email = form.email.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
            )
            db.session.add(user)
            db.session.commit()
        
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)
        
        do_login(user)
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
            flash(f"Welcome back {user.username}!", "success")
            return redirect('/pets')
        
        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)
    

@app.route("/pets", methods=['GET', 'POST'])
def pets():
    """Show all pets."""

    if not g.user:
        flash("Please login or register.", "danger")
        return redirect("/register")

    user = User.query.all()

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/animals', headers=headers)
    pet_info = response.json()

    return render_template("pets.html", user=user, pet_info=pet_info)


@app.route('/search', methods=['GET', 'POST'])
def pet_types():
    """Seach by type."""

    if not g.user:
        flash("Please login or register.", "danger")
        return redirect("/register")

    form = PetTypeForm()

    show_random_pet = False
    animals_data = []

    if form.validate_on_submit():
        species = form.species.data 
        gender = form.gender.data 
        age = form.age.data 
        size = form.size.data 
        color = form.color.data

        pet = Pet(species=species, gender=gender, age=age, size=size, color=color)
        
        db.session.add(pet)
        db.session.commit()

        animals_data = pf.animals(animal_type=f'{pet.species}', gender=f'{pet.gender}', age=f'{pet.age}', size=f'{pet.size}', color=f'{pet.color}')

        if len(animals_data['animals']) == 0:
            show_random_pet = True

    random_animal = pf.animals(results_per_page=1)

    return render_template("pet_types.html", form=form, animal=animals_data, random_animal=random_animal, show_random_pet=show_random_pet)


@app.route("/pet/<int:pet_id>", methods=['GET'])
def aboutPet(pet_id):
    """Show info about pet."""

    if not g.user:
        flash("Please login or register.", "danger")
        return redirect("/register")

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/animals/{pet_id}', headers=headers)
    pet_info = response.json()

    return render_template("pet_info.html", pet_info=pet_info)


@app.route("/contact/<int:pet_id>", methods=['GET'])
def contactOrg(pet_id):
    """Show orgs contact info."""

    if not g.user:
        flash("Please login or register.", "danger")
        return redirect("/register")

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/animals/{pet_id}', headers=headers)
    pet_info = response.json()

    return render_template("orgs.html", pet_info=pet_info)


@app.route('/logout')
def logout():
    session.pop(CURR_USER_KEY)
    return redirect('/login')

