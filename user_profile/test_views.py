from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="qwertyuiopå"
        )

    def test_get_profile_page(self):
        response = self.client.get(f"/profile/{self.user.username}")
        self.assertEqual(response.status_code, 301)
