"""Smoke tests for the PIN login endpoint."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='budtender', password='irrelevant', login_pin='1234'
        )

    def test_valid_pin_returns_token(self):
        res = self.client.post('/api/login/', {'pin': '1234', 'terminal': '1'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', res.json())
        self.assertEqual(res.json()['username'], 'budtender')

    def test_invalid_pin_returns_401(self):
        res = self.client.post('/api/login/', {'pin': '0000'}, format='json')
        self.assertEqual(res.status_code, 401)

    def test_short_pin_returns_400(self):
        res = self.client.post('/api/login/', {'pin': '12'}, format='json')
        self.assertEqual(res.status_code, 400)
