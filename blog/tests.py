from django.test import TestCase
from django.urls import reverse
from .models import User, BlogPost, Category

class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.cat = Category.objects.create(name="Django")
        self.post = BlogPost.objects.create(title="Hello", content="Body", author=self.user)
        self.post.categories.add(self.cat)

    def test_home_status_code(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)

    def test_post_str(self):
        self.assertEqual(str(self.post), "Hello")
