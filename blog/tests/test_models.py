import pytest
from blog.models import User, Blog, Comment
from django.utils import timezone

!

@pytest.mark.django_db
class TestBlogModel:
    @pytest.fixture
    def author(self):
        return User.objects.create_user(
            username="authoruser",
            email="author@example.com",
            phone="09121112222",
            password="authorpass"
        )

    def test_create_blog(self, author):
        blog = Blog.objects.create(
            author=author,
            title="Test Blog Title",
            content="Sample blog content",
            status=True,
            published=True,
            is_active=True,
        )
        assert blog.title == "Test Blog Title"
        assert blog.author == author
        assert blog.status is True
        assert blog.published is True
        assert blog.is_active is True
        assert blog.created_at is not None


@pytest.mark.django_db
class TestCommentModel:
    @pytest.fixture
    def author(self):
        return User.objects.create_user(
            username="commenter",
            email="commenter@example.com",
            phone="09123334444",
            password="commentpass"
        )

    @pytest.fixture
    def blog(self, author):
        return Blog.objects.create(
            author=author,
            title="A blog post",
            content="Content of the blog post",
            status=True,
            published=True,
        )

    def test_create_comment(self, author, blog):
        comment = Comment.objects.create(
            author=author,
            post=blog,
            content="Nice blog!",
        )
        assert comment.content == "Nice blog!"
        assert comment.post == blog
        assert comment.author == author
        assert comment.parent is None

    def test_create_reply_to_comment(self, author, blog):
        parent = Comment.objects.create(
            author=author,
            post=blog,
            content="Parent comment"
        )
        reply = Comment.objects.create(
            author=author,
            post=blog,
            content="This is a reply",
            parent=parent
        )
        assert reply.parent == parent
        assert reply in parent.replies.all()
