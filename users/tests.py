from django.shortcuts import reverse
from django.test import TestCase
from .models import CustomUser


class TestRegister(TestCase):
    fixtures = ['initial_data']

    def test_create_user(self):
        response = self.client.post(reverse('signup'),
                                    {'username': 'mohammed', 'email': 
                                    'mohammed@gmm.com',  
                                    'password1': 'moh@1234', 
                                    'password2': 'moh@1234'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CustomUser.objects.last().is_active)
