from django.test import TestCase
from django.contrib.auth.models import User
from notebook.models import Profile
from django.core.files import File
import mock

# Create your tests here.


class UserTestCase(TestCase):
    def test_user(self):
        username = "shetu"
        password = "hello"
        u.save()
        self.assertEqual(u.username, username)
        self.assertTrue(u.check_password(password))
