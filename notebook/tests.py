from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Program, ViewProgram

# Create your tests here.
class ProfileTests(TestCase):
    def Profile_is_created_successfully(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        profile = Profile(
            user=self.user,
            slug='test-slug',
            bio='Bio Test',
            pic = ''
        )
        profile.save()