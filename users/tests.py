from django.shortcuts import reverse
from django.test import TestCase
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


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

    def test_activate_user(self):
        user_before = CustomUser.objects.get(username='mohamed3')
        user_before_active = user_before.is_active
        self.assertFalse(user_before_active)
        token = default_token_generator.make_token(user_before)
        username_hash = urlsafe_base64_encode(
            force_bytes(user_before.username))
        response = self.client.get(reverse('user-activation-link',
                                           args=[username_hash,
                                                 token]))
        user_after = CustomUser.objects.get(username='mohamed3')
        user_after = user_after.is_active
        self.assertTrue(user_after)
        self.assertEqual(response.status_code, 200)

    def test_activate_user_invalid_token(self):
        user_before = CustomUser.objects.get(username='mohamed3')
        user_before = user_before.is_active
        response = self.client.get(reverse('user-activation-link',
                                           args=["b'bW9oYW1lZDM'",
                                                 '54e-6eeff711e8d444def5b8']))
        user_after = CustomUser.objects.get(username='mohamed3')
        user_after = user_after.is_active
        self.assertFalse(user_before)
        self.assertFalse(user_after)
        self.assertEqual(response.status_code, 200)
