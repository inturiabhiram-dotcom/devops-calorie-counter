"""Django tests here"""
from django.test import TestCase
from django.urls import reverse

class MyViewTestCase(TestCase):
    """Djago test case"""
    def test_home_view(self):
        """Test if login page returns 200 status"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
