import pytest
from django.urls import reverse
from rest_framework import status
from blog.models import User, Comment, Blog

@pytest.mark.django_db
class TestUserListViews:

    def test_user_list_admin_only(self, token_admin_client):
        url = reverse("user-list")
        response = token_admin_client.get(url)
        assert response.status_code == 200

    def test_user_can_see_userlist(self, token_regular_user_client):
        url = reverse("user-list")
        response = token_regular_user_client.get(url)
        assert response.status_code == 403

    def test_unauthenticated_user_can_see_userlist(self, client):
        url = reverse("user-list")
        response = client.get(url)
        assert response.status_code == 401



    def test_user_detail_view(self, token_admin_client, regular_user):
        url = reverse("user-detail", kwargs={"pk": regular_user.pk})
        response = token_admin_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == regular_user.id

    def test_owner_can_see_his_detail(self, token_regular_user_client, regular_user):
        url = reverse("user-detail", kwargs={"pk": regular_user.pk})
        response = token_regular_user_client.get(url)
        assert response.status_code == 200

    def test_anotheruser_can_see_others_detail(self, token_another_user_client, regular_user):
        url = reverse("user-detail", kwargs={"pk": regular_user.pk})
        response = token_another_user_client.get(url)
        assert response.status_code == 403


    def test_user_create(self, client):
        url = reverse("user-create")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "phone": "09123456789",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        response = client.post(url, data)
        assert response.status_code == 201

    def test_owner_user_can_update(self, token_regular_user_client, regular_user):
        url = reverse("user-update", kwargs={"pk": regular_user.pk})
        data = {"username": "Updated"}
        response = token_regular_user_client.put(url, data)
        assert response.status_code == 200
        assert response.data["username"] == "Updated"


    def test_another_user_can_update_another_one(self, token_another_user_client, regular_user):
        url = reverse("user-update", kwargs={"pk": regular_user.pk})
        data = {"username": "Updated"}
        response = token_another_user_client.put(url, data)
        assert response.status_code == 403

    def test_admin_can_update_users_detail(self, token_admin_client, regular_user):
        url = reverse("user-update", kwargs={"pk": regular_user.pk})
        data = {"username": "Updated"}
        response = token_admin_client.put(url, data)
        assert response.status_code == 200
        assert response.data["username"] == "Updated"

    def test_owner_can_deactive_his_profile(self, token_regular_user_client, regular_user):
        url = reverse("user-delete", kwargs={"pk": regular_user.pk})
        response = token_regular_user_client.delete(url)
        assert response.status_code == 204
        regular_user.refresh_from_db()
        assert regular_user.is_active is False

    def test_admin_can_deactive_users_profile(self, token_admin_client, regular_user):
        url = reverse("user-delete", kwargs={"pk": regular_user.pk})
        response = token_admin_client.delete(url)
        assert response.status_code == 204
        regular_user.refresh_from_db()
        assert regular_user.is_active is False

    def test_another_user_can_deactive_anothers(self, token_another_user_client, regular_user):
        url = reverse("user-delete", kwargs={"pk": regular_user.pk})
        response = token_another_user_client.delete(url)
        assert response.status_code == 403


@pytest.mark.django_db
class TestBlogViews:

    def test_blog_list_authenticated(self, token_regular_user_client):
        url = reverse("blog-list")
        response = token_regular_user_client.get(url)
        assert response.status_code == 200

    def test_blog_list_unauthenticated(self, client):
        url = reverse("blog-list")
        response = client.get(url)
        assert response.status_code == 401

    def test_authenticated_user_blog_create(self, token_regular_user_client):
        url = reverse("blog-create")
        data = {
            "title": "Test Blog",
            "content": "Some content here."
        }
        response = token_regular_user_client.post(url, data)
        assert response.status_code == 201

    def test_unauthenticated_user_blog_create(self, client):
        url = reverse("blog-create")
        data = {
            "title": "Test Blog",
            "content": "Some content here."
        }
        response = client.post(url, data)
        assert response.status_code == 401

    def test_owner_can_update_own_blog(self, blog_by_regular_user, token_regular_user_client):
        url = reverse("blog-update", kwargs={"pk": blog_by_regular_user.pk})
        data = {"title": "Updated-Title"}
        response = token_regular_user_client.put(url, data)
        assert response.status_code == 200
        assert response.data["title"] == "Updated-Title"


    def test_admin_can_update_user_blog(self, blog_by_regular_user, token_admin_client):
        url = reverse("blog-update", kwargs={"pk": blog_by_regular_user.pk})
        data = {"title": "Updated-Title"}
        response = token_admin_client.put(url, data)
        assert response.status_code == 200
        assert response.data["title"] == "Updated-Title"

    def test_another_user_cannot_update_regular_user(self, blog_by_regular_user, token_another_user_client):
        url = reverse("blog-update", kwargs={"pk": blog_by_regular_user.pk})
        data = {"title": "Updated-Title"}
        response = token_another_user_client.put(url, data)
        assert response.status_code == 403


    def test_user_can_deactive_own_blog(self, token_regular_user_client, blog_by_regular_user):
        url = reverse("blog-delete", kwargs={"pk": blog_by_regular_user.pk})
        response = token_regular_user_client.delete(url)
        assert response.status_code == 204
        blog_by_regular_user.refresh_from_db()
        assert blog_by_regular_user.is_active is False

    def test_another_user_can_deactive_others_blog(self, token_another_user_client, blog_by_regular_user):
        url = reverse("blog-delete", kwargs={"pk": blog_by_regular_user.pk})
        response = token_another_user_client.delete(url)
        assert response.status_code == 403

    def test_admin_can_deactive_users_blog(self, token_regular_user_client, blog_by_regular_user):
        url = reverse("blog-delete", kwargs={"pk": blog_by_regular_user.pk})
        response = token_regular_user_client.delete(url)
        assert response.status_code == 204
        blog_by_regular_user.refresh_from_db()
        assert blog_by_regular_user.is_active is False



@pytest.mark.django_db
class TestCommentViews:

    def test_authenticated_user_comment_list(self, token_regular_user_client):
        url = reverse("comment-list")
        response = token_regular_user_client.get(url)
        assert response.status_code == 200

    def test_unauthenticated_user_comment_list(self, client):
        url = reverse("comment-list")
        response = client.get(url)
        assert response.status_code == 401

    def test_authenticated_user_can_create_comment(self, token_regular_user_client, blog_by_regular_user):
        url = reverse("comment-create")
        data = {
            "content": "Nice blog!",
            "post": blog_by_regular_user.id,
            "parent":""
        }
        response = token_regular_user_client.post(url, data)
        assert response.status_code == 201
        assert response.data["content"] == "Nice blog!"

    def test_unauthenticated_user_can_create_comment(self, client, blog_by_regular_user):
        url = reverse("comment-create")
        data = {
            "content": "Nice blog!",
            "post": blog_by_regular_user.id
        }
        response = client.post(url, data)
        assert response.status_code == 401



    def test_owner_update_comment(self, token_regular_user_client, comment_by_regular_user):
        url = reverse("comment-update", kwargs={"pk": comment_by_regular_user.pk})
        data = {"content": "Updated comment"}
        response = token_regular_user_client.put(url, data)
        assert response.status_code == 200
        assert response.data["content"] == "Updated comment"

    def test_another_user_update_comment(self, token_another_user_client, comment_by_regular_user):
        url = reverse("comment-update", kwargs={"pk": comment_by_regular_user.pk})
        data = {"content": "Updated comment"}
        response = token_another_user_client.put(url, data)
        assert response.status_code == 403

    def test_admin_can_update_comment(self, token_admin_client, comment_by_regular_user):
        url = reverse("comment-update", kwargs={"pk": comment_by_regular_user.pk})
        data = {"content": "Updated comment"}
        response = token_admin_client.put(url, data)
        assert response.status_code == 200




    def test_owner_delete_comment(self, token_regular_user_client, comment_by_regular_user):
        url = reverse("comment-delete", kwargs={"pk": comment_by_regular_user.pk})
        response = token_regular_user_client.delete(url)
        assert response.status_code == 204
        comment_by_regular_user.refresh_from_db()
        assert comment_by_regular_user.is_active is False

    def test_another_user_delete_comment(self, token_another_user_client, comment_by_regular_user):
        url = reverse("comment-delete", kwargs={"pk": comment_by_regular_user.pk})
        response = token_another_user_client.delete(url)
        assert response.status_code == 403

    def test_admin_can_delete_comment(self, token_admin_client, comment_by_regular_user):
        url = reverse("comment-delete", kwargs={"pk": comment_by_regular_user.pk})
        response = token_admin_client.delete(url)
        assert response.status_code == 204
        comment_by_regular_user.refresh_from_db()
        assert comment_by_regular_user.is_active is False