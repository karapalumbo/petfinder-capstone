import os
from unittest import TestCase

from models import db, User, Pet

os.environ['DATABASE_URL'] = "postgresql:///petfinder-test"

from app import app

db.create_all()


class UserTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()

        user1 = User.register("user1", "password1", "user1@user1.com", "first1", "last1")
        user1_id = 111
        user1.id = user1_id

        user2 = User.register("user2", "password2", "user2@user2.com", "first2", "last2" )
        user2_id = 222
        user2.id = user2_id

        db.session.add(user1, user2)
        db.session.commit()

        user1 = User.query.get(user1_id)
        user2 = User.query.get(user2_id)

        self.user1 = user1
        self.user2 = user2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            password="HASHED_PASSWORD",
            email="test@test.com",
            first_name="test1",
            last_name="testing1"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.favorites), 0)


    def test_user_credentials(self):
        self.assertEqual(self.user1.username, "user1")
        self.assertEqual(self.user1.email, "user1@user1.com")
        self.assertNotEqual(self.user1.password, "password1")

    
    def test_invalid_username(self):
        self.assertNotEqual(self.user1.username, "user4")


    def test_user_authentication(self):
        u = User.authenticate(self.user1.username, "password1")
        self.assertEqual(u.id, self.user1.id)


    def test_invalid_username_authentication(self):
        self.assertFalse(User.authenticate("wrong", "password1"))
    
    
    def test_invalid_password_authentication(self):
        self.assertFalse(User.authenticate(self.user1.username, "wrong"))