from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Program, ViewProgram

"""
# Create your tests here.
class ProfileTest(TestCase):

    def create_user(self, username="test", password="hello"):
        return User.objects.create(username=username, password=password)

    def create_profile(self, slug="only-a-test", bio="yes, this is only a test"):
        #user = self.create_user()
        u =  User(username="test")
        u.set_password("password")
        u.save()
        p = Profile.objects.create(user=u, slug=slug, bio=bio)
        p.pic.url="https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/MarioNSMBUDeluxe.png/220px-MarioNSMBUDeluxe.png"
        return p


    def test_profile_creation(self):
        p = self.create_profile()
        #p.save()
        self.assertTrue(isinstance(p, Profile))
        self.assertEqual(w.__unicode__(), w.title)
"""
