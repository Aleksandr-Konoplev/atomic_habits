from typing import Any, cast

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


User = get_user_model()
UserModel = cast(Any, User)


class UserCRUDTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(email='owner@example.com', password='testpass123', first_name='Owner')
        self.other_user = self.create_user(email='other@example.com', password='testpass123', first_name='Other')
        self.client.force_authenticate(user=self.user)

        self.register_url = reverse('users:register')
        self.list_url = reverse('users:users_list')

    @staticmethod
    def create_user(email, password, **extra_fields):
        user = UserModel.objects.create(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_user_payload(**overrides):
        payload = {
            'email': 'newuser@example.com',
            'password': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '+79990000000',
            'telegram_id': '123456789',
        }
        payload.update(overrides)
        return payload

    def test_register_user(self):
        response = cast(Any, self.client.post(self.register_url, self.get_user_payload(), format='json'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = UserModel.objects.get(email='newuser@example.com')
        self.assertEqual(created_user.first_name, 'New')
        self.assertNotEqual(created_user.password, 'strongpass123')
        self.assertTrue(created_user.check_password('strongpass123'))

    def test_users_list_returns_all_users_for_authenticated_user(self):
        response = cast(Any, self.client.get(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result_ids = [item['id'] for item in response.data['results']]
        self.assertEqual(response.data['count'], 2)
        self.assertIn(self.user.id, result_ids)
        self.assertIn(self.other_user.id, result_ids)

    def test_retrieve_user_detail(self):
        response = cast(Any, self.client.get(reverse('users:user_detail', args=[self.other_user.pk])))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.other_user.id)
        self.assertEqual(response.data['email'], self.other_user.email)

    def test_update_user(self):
        payload = self.get_user_payload(
            email='updated@example.com',
            password='updatedpass123',
            first_name='Updated',
            last_name='Name',
            phone_number='+78880000000',
            telegram_id='987654321',
        )

        response = cast(Any, self.client.put(reverse('users:user_update', args=[self.user.pk]), payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.phone_number, payload['phone_number'])

    def test_delete_user(self):
        response = cast(Any, self.client.delete(reverse('users:user_delete', args=[self.other_user.pk])))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserModel.objects.filter(pk=self.other_user.pk).exists())
