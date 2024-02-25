from django.test import TestCase
from .models import Post, Comment, Like
from django.contrib.auth.models import User


class ModelTestCase(TestCase):
    """
    Base test case for setup,
    to avoid repeating the same setup in every test
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='qwertyuiopå'
        )

        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='Test Body',
            is_sticky=True
        )

        self.comment = Comment.objects.create(
            author=self.user,
            body='Test Body',
            is_sticky=True,
            post=self.post
        )


class TestPostModel(ModelTestCase):
    """
    Test that post models work correctly
    """

    def test_post_string_method_returns_title_and_author(self):
        """
        Test string method for Post class
        """
        self.assertEqual(
            str(self.post), f'{self.post.title} by {self.post.author}'
            )

    def test_post_get_absolute_url(self):
        """
        Test get_absolute_url method for Post class
        """
        self.assertEqual(self.post.get_absolute_url(), f'/{self.post.slug}/')

    def test_post_latest_activity_is_set_to_now_if_not_set(self):
        """
        Test that latest_activity is set to now if not set
        """
        self.assertIsNotNone(self.post.latest_activity)


class TestCommentModel(ModelTestCase):
    """
    Test that comment models work correctly
    """

    def test_comment_string_method_returns_author(self):
        """
        Test string method for Comment class
        """
        self.assertEqual(
            str(self.comment), f'Comment by {self.comment.author}'
            )


class TestLikeModel(ModelTestCase):
    """
    Test that like models work correctly
    """

    def test_like_post(self):
        """
        Test string method for Like class
        """
        self.like = Like.objects.create(
            user=self.user,
            post=self.post,
        )
        self.assertEqual(
            str(self.like), f'{self.like.user} likes {self.like.post}'
                )

    def test_like_comment(self):
        """
        Test string method for Like class
        """
        self.like = Like.objects.create(
            user=self.user,
            comment=self.comment,
        )
        self.assertEqual(
            str(self.like), f'{self.like.user} likes {self.like.comment}'
            )
