from secret import API_TOKEN, API_SECRET_KEY, API_CLIENT_KEY
from flask import Flask, render_template, flash, redirect, request, session, json, g
import requests
import petpy
from models import connect_db, db, User, Favorite, Pet
from forms import LoginForm, UserAddForm, PetTypeForm
from sqlalchemy.exc import IntegrityError
# from flask_debugtoolbar import DebugToolbarExtension

BASE_URL = "https://api.petfinder.com/v2"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1NmVjaHhhU3RxcUVic2hXNXFNN1VpSURuY0xQRjk2b3h5N0JYblNHYUl1Ymx0OXdmNCIsImp0aSI6Ijg5MzE5MTY1Njk4NWU5OTVhMDc5OWViYTgzNGQ4ZWQ2ZDg1OTAyYWVmNzY0MWJiZTEwN2I0OTg3ZTIxNzYxZjAxNWFlMDhlODU0NmY2YWZkIiwiaWF0IjoxNjE3MTIzMDY4LCJuYmYiOjE2MTcxMjMwNjgsImV4cCI6MTYxNzEyNjY2OCwic3ViIjoiIiwic2NvcGVzIjpbXX0.F9ji5l2quU5_DP-IVGcmB7whQCC7h2402_0gZ1L4fBVbQYt6J-GaX4JWD2H7_6brHkDT8iVvKuVd8--FCfc0XF0q9CDGZxR-jsnGDxoiwkRUZ7GNqig2NaX-_YGbNmUAdER-OEDrovXhGSjQwikocx9HXmx2BXd5psGhCBlxVtFA55jhIRkg1POPSGiTlz0BHh_oon18E-Jk_EsvJeon-h60y-QVd03U6Bhg9_E8wHORHSnSaxe6WFkcqCp-PnWvU40xxjb7rZmvK0VoVn33Hplb29dNK7Z-rJuxDnKx3Bc10Q7nduvUYMLJtFH8kIsI8QFxZRMF28m-igR2PJoegA"
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

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/animals', headers=headers)
    pet_info = response.json()

    # js_data = request.get_json()
    # print('****************', js_data)
    # return js_data
    
    return render_template("pets.html", user=user, pet_info=pet_info)


@app.route('/types', methods=['GET', 'POST'])
def pet_types():
    """Seach by type."""

    if not g.user:
        flash("Access unauthorized.", "danger")
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
        flash("Access unauthorized.", "danger")
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
        flash("Access unauthorized.", "danger")
        return redirect("/register")

    headers = {
    'Authorization': f'Bearer {TOKEN}',
    }

    response = requests.get(f'{BASE_URL}/animals/{pet_id}', headers=headers)
    pet_info = response.json()

    return render_template("orgs.html", pet_info=pet_info)


# @app.route('/favorite/<int:pet_id>', methods=['GET','POST'])
# def add_favorite(pet_id):
#     """add pet to favorites."""

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/register")

#     if request.method == 'GET':
        
#         headers = {
#         'Authorization': f'Bearer {TOKEN}',
#         }

#         response = requests.get(f'{BASE_URL}/animals/{pet_id}', headers=headers)
#         pet_info = response.json()

#         users = User.query.all()
#         # print('$$$$$$$$$$$$$$$$$$$', list(db.session.query(User.id).all()[0])[0])
        
#         pet = Pet(
#             name=pet_info['animal']['name']
#         )

#         pets = Pet.query.all()
        
#         for p in pets:
#             p_id = list(db.session.query(p.id).all()[0])[0]
#         #     print('$$$$$$$$$$$$$$$$$$$$$', list(db.session.query(p.id).all()[0])[0])

#         fav_pet = Favorite(
#             user_id=list(db.session.query(User.id).all()[0])[0],
#             pet_id=p_id
#         )

#         db.session.add(pet)
#         db.session.add(fav_pet)

#         db.session.commit()


#         return redirect('/pets')
        
#     return render_template("favorites.html", pet=pet, fav_pet=fav_pet)


# @app.route('/users/<int:user_id>/favorites', methods=['GET'])
# def show_favorites(user_id):
#         """show user favorites."""

#         if not g.user:
#             flash("Access unauthorized.", "danger")
#             return redirect("/register")

#         user = User.query.get_or_404(user_id)

#         return render_template('favorites.html', user=user, fav_pets=user.pets)


@app.route('/logout')
def logout():
    session.pop(CURR_USER_KEY)
    return redirect('/login')

