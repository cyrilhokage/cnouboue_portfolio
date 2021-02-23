from django.test import TestCase
from blog.models import Post


class PostTestCase(TestCase):
    def testPost(self):

        post = Post(title="My Title", technos="Blurb", summary="Post Body")
        self.assertEqual(post.title, "My Title")
        self.assertEqual(post.technos, "Blurb")
        self.assertEqual(post.summary, "Post Body")
