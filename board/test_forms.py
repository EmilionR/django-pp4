from django.test import TestCase
from .forms import PostForm, CommentForm, EditPostForm

# Create your tests here.


class TestPostForm(TestCase):

    def test_form_is_valid(self):
        post_form = PostForm({'title': 'Testing.', 'body': 'This is a test.'})
        self.assertTrue(post_form.is_valid())

    def test_form_is_invalid(self):
        post_form = PostForm({'title': '', 'body': ''})
        self.assertFalse(post_form.is_valid(), msg="Form is valid")


class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        comment_form = CommentForm({'body': 'This is a test.'})
        self.assertTrue(comment_form.is_valid())

    def test_form_is_invalid(self):
        comment_form = CommentForm({'body': ''})
        self.assertFalse(comment_form.is_valid(), msg="Form is valid")


class TestEditForm(TestCase):

    def test_form_is_valid(self):
        edit_form = EditPostForm({'body': 'This is a test.'})
        self.assertTrue(edit_form.is_valid())

    def test_form_is_invalid(self):
        edit_form = EditPostForm({'body': ''})
        self.assertFalse(edit_form.is_valid(), msg="Form is valid")
        