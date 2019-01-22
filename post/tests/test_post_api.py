from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post

from post.serializers import PostSerializer

POST_URL = reverse('post:post-list')

def detail_url(post_id):
    return reverse('post:post-detail', args=[post_id,])

def sample_user(username="testuser", email="testuser@mail.com", password="testuserpass"):
    return get_user_model().objects.create_user(username, email, password)

def sample_post(user, title="test post"):
    return Post.objects.create(user=user, title=title)


class PrivateRecipeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_post_creation(self):
        payload = {
            'creator': self.user,
            'title': 'test post'
        }
        sample_post(self.user)

        post = self.client.get("http://localhost:8000/api/post/")

        print(post)

        self.assertEqual(post.status_code, status.HTTP_200_OK)
