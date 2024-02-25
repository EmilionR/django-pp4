from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from .forms import ProfileForm
from .models import Profile


class ProfileFormTest(TestCase):
    def test_clean_avatar(self):
        """
        Test that the avatar is cleaned properly,
        amd that the file size is checked.
        """
        # Create a file larger than the size limit
        large_file = SimpleUploadedFile("large_image.jpg", b" " * (524288 + 1))

        # Create form data with the large file
        form_data = {'avatar': large_file}
        form = ProfileForm(data={'about': 'test bio'}, files=form_data)

        # Check if the form is rejected due to file size
        self.assertFalse(form.is_valid())
        self.assertTrue('avatar' in form.errors)
        self.assertEqual(
            form.errors['avatar'], ['File size must be less than 0.5 MB.']
                )

    def test_clean_avatar_valid(self):
        """
        Test that the form is valid when the file size is within the limit.
        """
        # Create a file smaller than the size limit
        small_file = SimpleUploadedFile("small_image.jpg", b" " * (524288 - 1))

        # Create form data with the small file
        form_data = {'avatar': small_file}
        form = ProfileForm(data={'about': 'test bio'}, files=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())
