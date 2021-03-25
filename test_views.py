"""User View tests."""

import os
from unittest import TestCase

from models import db, connect_db, User, Favorite

os.environ['DATABASE_URL'] = "postgresql:///petfinder-test"


from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):

        User.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    password="testuser",
                                    email="test@test.com",
                                    first_name="test1", 
                                    last_name="testing1"
                                    )
        self.testuser_id = 000
        self.testuser.id = self.testuser_id

        self.user1 = User.signup("user1", "password1", "user1@user1.com", "first1", "last1")
        self.user1_id = 111
        self.user1.id = self.user1_id

        self.user2 = User.signup("user2", "password2", "user2@user2.com", "first2", "last2")
        self.user2_id = 222
        self.user2.id = self.user2_id

        db.session.commit()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

