from typing import Any, cast

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from habits.models import Habit


User = get_user_model()
HabitModel = cast(Any, Habit)


class HabitCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = self.create_user(email='owner@example.com', password='testpass123')
        self.other_user = self.create_user(email='other@example.com', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.create_url = reverse('habits:create')
        self.my_list_url = reverse('habits:habits_my_list')

        self.habit = HabitModel.objects.create(
            owner=self.user,
            place='Home',
            time='08:30:00',
            action='Read 10 pages',
            is_pleasant=False,
            periodicity=1,
            award='Cup of coffee',
            duration=60,
            is_publicity=False,
        )
        self.pleasant_habit = HabitModel.objects.create(
            owner=self.user,
            place='Cafe',
            time='10:00:00',
            action='Drink coffee slowly',
            is_pleasant=True,
            periodicity=1,
            duration=15,
            is_publicity=False,
        )

    @staticmethod
    def create_user(email, password):
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_habit_payload(**overrides):
        payload = {
            'place': 'Gym',
            'time': '07:00:00',
            'action': 'Do morning workout',
            'is_pleasant': False,
            'periodicity': 1,
            'award': 'Healthy breakfast',
            'duration': 90,
            'is_publicity': False,
            'related_pleasant_habit': None,
        }
        payload.update(overrides)
        return payload

    def test_create_habit_sets_authenticated_user_as_owner(self):
        payload = self.get_habit_payload(owner=self.other_user.pk)

        response = cast(Any, self.client.post(self.create_url, payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_habit = HabitModel.objects.get(pk=response.data['id'])
        self.assertEqual(created_habit.owner, self.user)
        self.assertEqual(created_habit.action, payload['action'])

    def test_my_habits_list_returns_only_authenticated_user_habits(self):
        HabitModel.objects.create(
            owner=self.other_user,
            place='Park',
            time='09:00:00',
            action='Walk for 20 minutes',
            is_pleasant=False,
            periodicity=1,
            award='Fresh air',
            duration=20,
            is_publicity=True,
        )

        response = cast(Any, self.client.get(self.my_list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result_ids = [item['id'] for item in response.data['results']]
        self.assertEqual(response.data['count'], 2)
        self.assertIn(self.habit.id, result_ids)
        self.assertIn(self.pleasant_habit.id, result_ids)

    def test_retrieve_own_habit(self):
        url = reverse('habits:detail_list', args=[self.habit.pk])

        response = cast(Any, self.client.get(url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.habit.id)
        self.assertEqual(response.data['action'], self.habit.action)

    def test_update_own_habit(self):
        url = reverse('habits:update_list', args=[self.habit.pk])
        payload = self.get_habit_payload(
            place='Office',
            time='18:00:00',
            action='Plan next day',
            award='Watch one episode',
            duration=30,
            is_publicity=True,
        )

        response = cast(Any, self.client.put(url, payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, payload['place'])
        self.assertEqual(self.habit.action, payload['action'])
        self.assertTrue(self.habit.is_publicity)

    def test_delete_own_habit(self):
        url = reverse('habits:delete_list', args=[self.habit.pk])

        response = cast(Any, self.client.delete(url))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(HabitModel.objects.filter(pk=self.habit.pk).exists())

    def test_other_user_cannot_update_or_delete_habit(self):
        self.client.force_authenticate(user=self.other_user)
        update_url = reverse('habits:update_list', args=[self.habit.pk])
        delete_url = reverse('habits:delete_list', args=[self.habit.pk])

        update_response = cast(Any, self.client.put(
            update_url,
            self.get_habit_payload(action='Try to change another user habit'),
            format='json',
        ))
        delete_response = cast(Any, self.client.delete(delete_url))

        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(HabitModel.objects.filter(pk=self.habit.pk).exists())

    def test_create_habit_fails_when_duration_exceeds_limit(self):
        payload = self.get_habit_payload(duration=121)

        response = cast(Any, self.client.post(self.create_url, payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)
        self.assertEqual(HabitModel.objects.count(), 2)

    def test_create_habit_fails_when_periodicity_exceeds_limit(self):
        payload = self.get_habit_payload(periodicity=8)

        response = cast(Any, self.client.post(self.create_url, payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)
        self.assertEqual(HabitModel.objects.count(), 2)

    def test_create_habit_fails_when_award_and_related_habit_are_set_together(self):
        payload = self.get_habit_payload(
            award='Reward',
            related_pleasant_habit=self.pleasant_habit.pk,
        )

        response = cast(Any, self.client.post(self.create_url, payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)
        self.assertEqual(HabitModel.objects.count(), 2)

    def test_create_habit_fails_when_related_habit_is_not_pleasant(self):
        payload = self.get_habit_payload(
            award=None,
            related_pleasant_habit=self.habit.pk,
        )

        response = cast(Any, self.client.post(self.create_url, payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)
        self.assertEqual(HabitModel.objects.count(), 2)

    def test_create_habit_fails_when_useful_habit_has_no_award_or_related_habit(self):
        payload = self.get_habit_payload(award=None, related_pleasant_habit=None)

        response = cast(Any, self.client.post(self.create_url, payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)
        self.assertEqual(HabitModel.objects.count(), 2)

    def test_create_habit_fails_when_pleasant_habit_has_award(self):
        payload = self.get_habit_payload(is_pleasant=True, award='Reward', related_pleasant_habit=None)

        response = cast(Any, self.client.post(self.create_url, payload, format='json'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)
        self.assertEqual(HabitModel.objects.count(), 2)

    def test_retrieve_private_habit_of_other_user_returns_404(self):
        other_private_habit = HabitModel.objects.create(
            owner=self.other_user,
            place='Library',
            time='12:00:00',
            action='Study English words',
            is_pleasant=False,
            periodicity=1,
            award='Tea break',
            duration=45,
            is_publicity=False,
        )

        response = cast(Any, self.client.get(reverse('habits:detail_list', args=[other_private_habit.pk])))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_habit_requires_authentication(self):
        unauthenticated_client = APIClient()

        response = cast(Any, unauthenticated_client.post(self.create_url, self.get_habit_payload(), format='json'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
