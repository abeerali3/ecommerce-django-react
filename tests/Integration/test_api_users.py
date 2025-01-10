# tests.py in the same app as user_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from base.serializers import UserSerializerWithToken

class UserViewsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_register_user(self):
        url = reverse('register')
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user_profile_update')
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'password': 'updatedpassword123'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser@example.com')

    def test_get_users(self):
        admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)
        url = reverse('deleteUser', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

