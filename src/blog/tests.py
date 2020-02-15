from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Post


class TestPostModel(TestCase):
    def test_post_model_instance_name_should_be_post_title(self):
        # Given: Set test user and post
        test_user = User.objects.create_user(
            email="kwon5604@naver.com", username="thkwon", password="password"
        )
        test_post = Post.objects.create(
            author=test_user, title="title", text="text"
        )

        # When: Get post instance
        post_instance = Post.objects.get(id=test_post.id)

        # Then: post_instance.__str__ should be test_post.title
        self.assertEqual(post_instance.__str__(), test_post.title)
