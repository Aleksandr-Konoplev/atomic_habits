from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_message_to_tg


@shared_task
def send_habit_reminders():
    """
    Проверяет привычки и отправляет напоминания
    """

    now = timezone.localtime()

    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:

        user = habit.owner

        if not user.telegram_id:
            continue

        message = f'Напоминание!Привычка: {habit.action} Место: {habit.place}'

        send_message_to_tg(chat_id=user.telegram_id, message=message)
