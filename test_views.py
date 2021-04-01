"""User View tests."""

import os
import requests 
from unittest import TestCase
from models import db, connect_db, User, Pet
from petpy.api import Petfinder 
from secret import API_TOKEN, API_SECRET_KEY, API_CLIENT_KEY

os.environ['DATABASE_URL'] = "postgresql:///petfinder-test"

from app import app, CURR_USER_KEY
TOKEN = API_TOKEN


db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

# FLASK_ENV=production python -m unittest test_views.py

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):

        User.query.delete()

        self.client = app.test_client()

        self.testpet = Pet(species="cat", gender="m", age="young", size="small", color="black")

        self.testpet_id = 1
        self.testpet.id = self.testpet_id 

        self.testuser = User.register(username="testuser",
                                    password="testuser",
                                    email="test@test.com",
                                    first_name="test1", 
                                    last_name="testing1"
                                    )
        self.testuser_id = 000
        self.testuser.id = self.testuser_id

        db.session.commit()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_login_user(self):
        """Test login user."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/pets", data={"text": "Helping"})

            self.assertEqual(resp.status_code, 302)



    def test_request_pets(self):
        """Test get pets from API."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

        headers = {
            'Authorization': f'Bearer {TOKEN}',
        }

        resp = requests.get("https://api.petfinder.com/v2/animals", headers=headers)
        
        self.assertEqual(resp.status_code, 200)

    

    def test_single_pet(self):
        """test single pet page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

        response = c.get(f"/pet/{self.testpet_id}", data={"text": "About"})

        self.assertEqual(response.status_code, 302)


    def test_org_page(self):
        """test org page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

        response = c.get(f"/contact/{self.testpet_id}", data={"text": "Contact"})

        self.assertEqual(response.status_code, 302)