# """Django tests here"""
# from django.test import TestCase
# from django.urls import reverse

# class MyViewTestCase(TestCase):
#     """Djago test case"""
#     def test_home_view(self):
#         """Test if login page returns 200 status"""
#         response = self.client.get(reverse('login'))
#         self.assertEqual(response.status_code, 200)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class BasicViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_home_requires_login(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_user_login(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpassword123"
        })
        self.assertEqual(response.status_code, 302)