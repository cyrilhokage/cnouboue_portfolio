from django.test import TestCase
from django.contrib.auth.models import User
from notebook.models import Profile


# Create your tests here.


class UserTestCase(TestCase):
    def test_user(self):
        username = "shetu"
        password = "hello"
        u = User(username=username)
        u.set_password(password)
        p = Profile(
            user=u,
            pic="https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/MarioNSMBUDeluxe.png/220px-MarioNSMBUDeluxe.png",
        )
        u.save()
        self.assertEqual(u.username, username)
        self.assertTrue(u.check_password(password))
