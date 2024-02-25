from django.test import TestCase
from .views import PostList, post_detail, post_delete
from .models import Post, Comment
from django.contrib.auth.models import User

# Create your tests here.

class ViewTests(TestCase):
    """
    Base test class for testing views
    """
    def setUp(self):
        """
        Create posts and comments for testing
        """

        # Create a User instance
        self.user = User.objects.create_user(
            username='testuser',
            password='qwertyuiopå'
        )

        # Log the user in to enable testing of views that require login
        self.client.login(username='testuser', password='qwertyuiopå')

        # Create multiple Post instances
        self.posts = []
        for i in range(5):  # Adjust the range to create the desired number of posts
            post = Post.objects.create(
                title=f"Test Post {i}",
                body=f"Test body",
                author=self.user,
                slug=f"test-post-{i}",
            )
            self.posts.append(post)
        
        # Create multiple Comment instances for each Post
        self.comments = []
        for post in self.posts:
            comment = Comment.objects.create(
                post=post,
                author=self.user,
                body=f"Test comment for {post.title}",
            )
            self.comments.append(comment)


class TestPostListView(ViewTests):
    """
    Test that the post list view works correctly
    """

    def test_post_list_view_uses_correct_template(self):
        """
        Test that the post list view uses the correct template
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, "board/index.html")

    def test_post_list_view_returns_posts(self):
        """
        Test that the post list view returns posts
        """
        response = self.client.get("/")
        self.assertIn("post_list", response.context)

    def test_post_list_view_returns_posts_with_correct_comment_count(self):
        """
        Test that the post list view returns posts with the correct comment count
        """
        response = self.client.get("/")
        post_list = response.context["post_list"]
        self.assertEqual(post_list[0].comment_count, 1)

    def test_post_list_view_returns_searched_posts(self):
        """
        Test that the post list view returns searched posts
        """
        response = self.client.get("/?search=Test")
        post_list = response.context["post_list"]
        self.assertGreaterEqual(len(post_list), 1)

    def test_post_list_view_returns_no_posts_when_search_fails(self):
        """
        Test that the post list view returns no posts when the search fails
        """
        response = self.client.get("/?search=NoSuchPost")
        post_list = response.context["post_list"]
        self.assertEqual(len(post_list), 0)


class TestPostDetailView(ViewTests):
    """
    Test that the post detail view works correctly
    """

    def test_post_detail_view_uses_correct_template(self):
        """
        Test that the post detail view uses the correct template
        """
        response = self.client.get(f"/{self.posts[0].slug}/")
        self.assertTemplateUsed(response, "board/post_detail.html")

    def test_post_detail_view_returns_post(self):
        """
        Test that the post detail view returns a post
        """
        response = self.client.get(f"/{self.posts[0].slug}/")
        self.assertIn("post", response.context)

    def test_post_detail_view_returns_comments(self):
        """
        Test that the post detail view returns comments
        """
        response = self.client.get(f"/{self.posts[0].slug}/")
        self.assertIn("comments", response.context)

    def test_post_detail_view_returns_comment_count(self):
        """
        Test that the post detail view returns the correct comment count
        """
        response = self.client.get(f"/{self.posts[0].slug}/")
        comments = response.context["comments"]
        self.assertEqual(len(comments), 1)


class TestPostDeleteView(ViewTests):
    """
    Test that the post delete view works correctly
    """

    def test_post_delete_view_deletes_post(self):
        """
        Test that the post delete view deletes a post
        """
        response = self.client.post(f"/delete/post/{self.posts[0].id}")
        self.assertEqual(Post.objects.count(), 4)

    def test_post_delete_view_deletes_comments(self):
        """
        Test that the post delete view deletes comments
        """
        response = self.client.post(f"/delete/post/{self.posts[0].id}")
        self.assertEqual(Comment.objects.count(), 4)