from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.post = BlogPost.objects.create(
            title="First Post",
            content="This is the content.",
            author=self.user,
        )

    def test_str(self):
        self.assertEqual(str(self.post), "First Post")


class BlogPostFormTest(TestCase):
    def test_valid_form(self):
        form = BlogPostForm(data={"title": "Test Title", "content": "Test content"})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = BlogPostForm(data={"title": ""})
        self.assertFalse(form.is_valid())


class BlogViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="author", password="password123")
        self.post = BlogPost.objects.create(
            title="Django Post",
            content="Django content",
            author=self.user,
        )

    def test_post_list(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Post")

    def test_post_detail(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Post")

    def test_post_create(self):
        self.client.login(username="author", password="password123")
        response = self.client.post(
            reverse("post_create"),
            {"title": "New Title", "content": "New Content"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BlogPost.objects.filter(title="New Title").exists())

    def test_post_edit(self):
        self.client.login(username="author", password="password123")
        response = self.client.post(
            reverse("post_edit", kwargs={"pk": self.post.pk}),
            {"title": "Updated Title", "content": "Updated Content"},
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_post_delete(self):
        self.client.login(username="author", password="password123")
        response = self.client.post(reverse("post_delete", kwargs={"pk": self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BlogPost.objects.filter(pk=self.post.pk).exists())

    def test_search(self):
        response = self.client.get(reverse("search_posts") + "?q=Django")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Post")


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "password1": "ComplexPassword123!",
                "password2": "ComplexPassword123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_logout(self):
        User.objects.create_user(username="loginuser", password="securepassword")
        response = self.client.post(
            reverse("login"),
            {"username": "loginuser", "password": "securepassword"},
        )
        self.assertEqual(response.status_code, 302)

        logout_res = self.client.get(reverse("logout"))
        self.assertEqual(logout_res.status_code, 302)
