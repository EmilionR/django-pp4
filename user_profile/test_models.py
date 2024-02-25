from django.test import TestCase
from . import models
# Create your tests here.


class TestProfile(TestCase):
    def setUp(self):
        self.user = models.User.objects.create_user(
            username="test_user",
            password="qwertyuiopå"
        )

        self.profile = self.user.profile

    def test_profile_str(self):
        self.assertEqual(str(self.profile), f"{self.user.username} Profile")
