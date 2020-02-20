from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from datetime import datetime

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

    def test_post_model_instance_should_save_published_date_when_execute_publish_method(
        self
    ):
        # Given: Get post instance
        post_instance = Post.objects.get(id=self.test_post.id)

        with freeze_time("2020-02-15 09:00:00"):
            # When: Call post_instance method publish
            post_instance.publish()

            # Then: post_instance.__str__ should be test_post.title
            self.assertEqual(post_instance.published_date, timezone.now())


class TestAdmin(TestCase):
    def setUp(self) -> None:
        self.ADMIN_URL = "http://127.0.0.1:8000/admin/"
        self.admin = User.objects.create_superuser(
            username="admin",
            email="kwon5604@naver.com",
            password="admin_password",
        )
        self.c = Client()

    def test_admin_page_should_have_post_model(self):
        # Given: Login admin page
        self.c.login(username="admin", password="admin_password")

        # When: Call admin page
        response = self.c.get(self.ADMIN_URL)

        # Then: admin page shoud have 'Posts' string cause of registering model
        self.assertIn("Posts", str(response.content))


class TestViews(TestCase):
    def setUp(self) -> None:
        self.c = Client()

        user = User.objects.create_superuser(
            username="admin",
            email="kwon5604@naver.com",
            password="admin_password",
        )
        posts = Post.objects.create(
            title="test post", text="test text", author=user
        )
        posts.publish()

    def test_post_list_should_have_django_girls_blog_text(self):
        # Given: Set django girls blog text
        django_girls_blog_text = "Django Girls Blog"

        # When: Call post_list in views.py
        response = self.c.get(reverse("blog:list"))

        # Then: post_list should have django_girls_blog_text
        self.assertIn(django_girls_blog_text, str(response.content))

    def test_post_list_should_return_context_about_posts(self):
        # When: Call post_list in views.py
        response = self.c.get(reverse("blog:list"))

        # Then: post_list should return context about posts
        self.assertIn("posts", response.context)

    def test_post_list_should_return_post_instance_filtered_by_published_date_less_than_or_equal_to_today(
        self
    ):
        # When: Call post_list in views.py
        response = self.c.get(reverse("blog:list"))
        post_instance = response.context["posts"]

        # Then: post_list should return context about posts - filtered by publisehd date less than or equal to today
        self.assertLessEqual(post_instance[0].published_date, timezone.now())

    def test_post_list_should_return_rendered_template_with_post_title_and_text_and_published_date(
        self
    ):
        # When: Call post_list in views.py
        response = self.c.get(reverse("blog:list"))
        print(response.content)

        # Then: post_list should return post title, text and published:
        post_instance = response.context["posts"]
        self.assertIn(post_instance[0].title, str(response.content))
        self.assertIn(post_instance[0].text, str(response.content))
        self.assertIn("published: ", str(response.content))
