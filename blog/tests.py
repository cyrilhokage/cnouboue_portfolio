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
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'image.jpg'
        u = User(username=username)
        u.set_password(password)
        # u.profile.pic = file_mock
        p = Profile( pic=file_mock)
        p.user = u
        u.save()
        self.assertEqual(u.username, username)
        self.assertTrue(u.check_password(password))
