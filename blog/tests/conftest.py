import pytest
from _pytest.nodes import Item
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from blog.models import User, Blog, Comment


@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_user(
        username="root",
        email="rooot@gmail.com",
        password="root1234/",
        phone="123153533",
        is_staff=True,
        is_superuser=True,
    )

@pytest.fixture
def regular_user(django_user_model):
    return django_user_model.objects.create_user(
        username="user",
        email="user@test.com",
        password="userpass123",  # ← اصلاح این خط
        phone="1231535444",
    )

@pytest.fixture
def another_user(django_user_model):
    return User.objects.create_user(
        email="another@example.com",
        username="anotheruser",
        password="anotherpass123",
        phone="123153544124",
        is_staff=False,
        is_superuser=False,
    )

@pytest.fixture
def token_admin_client(admin_user):
    client = APIClient()
    token = AccessToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def token_regular_user_client(regular_user):
    client = APIClient()
    token = AccessToken.for_user(regular_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def token_another_user_client(another_user):
    client = APIClient()
    token = AccessToken.for_user(another_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client

@pytest.fixture
def blog_by_regular_user(regular_user):
    return Blog.objects.create(
        title="MyBlog",
        content="Some content",
        author=regular_user,
    )

@pytest.fixture
def comment_by_regular_user(regular_user,blog_by_regular_user):
    return Comment.objects.create(
        author=regular_user,
        post=blog_by_regular_user,
        content="Nice blog!",
    )