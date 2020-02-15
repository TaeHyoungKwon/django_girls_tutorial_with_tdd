from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from blog.models import Post


class TestPostModel(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            email="kwon5604@naver.com", username="thkwon", password="password"
        )
        self.test_post = Post.objects.create(
            author=self.test_user, title="title", text="text"
        )

    def test_post_model_instance_name_should_be_post_title(self):
        # When: Get post instance
        post_instance = Post.objects.get(id=self.test_post.id)

        # Then: post_instance.__str__ should be test_post.title
        self.assertEqual(post_instance.__str__(), self.test_post.title)
