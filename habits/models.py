from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import Truncator


class Habit(models.Model):
    """ Модель привычки """

    owner: models.ForeignKey                   # Пользователь добавивший привычку
    place: models.CharField                    # Место привычки
    time: models.TimeField                     # Время привычки
    action: models.CharField                   # Привычка
    is_pleasant: models.BooleanField           # Приятная ли привычка
    related_pleasant_habit: models.ForeignKey  # Ссылка на полезную привычку
    periodicity: models.PositiveIntegerField   # Периодичность
    award: models.CharField                    # Вознаграждение
    duration: models.PositiveIntegerField      # Длительность
    is_publicity: models.BooleanField          # Публичная ли привычка

    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место действия привычки',
        blank=True,
        null=True
    )

    time = models.TimeField(
        verbose_name='Время в которое выполняется привычка',
        blank=True,
        null=True
    )

    action = models.CharField(
        max_length=1000,
        verbose_name='Действие (описание привычки)'
    )

    is_pleasant = models.BooleanField(
        verbose_name='Признак приятной привычки'
    )

    related_pleasant_habit = models.ForeignKey(
        'habits.Habit',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Связанная приятная привычка'
    )

    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name='Периодичность выполнения привычки (в днях)'
    )

    award = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Вознаграждение за полезную привычку'
    )

    duration = models.PositiveIntegerField(
        verbose_name='Время на выполнение привычки'
    )

    is_publicity = models.BooleanField(
        verbose_name='Признак публичности'
    )

    def clean(self):
        if self.related_pleasant_habit and self.award:
            raise ValidationError(
                'Можно указать либо связанную приятную привычку, либо награду'
            )

        if self.is_pleasant and self.award:
            raise ValidationError(
                'У приятной привычки не может быть вознаграждения'
            )

        if not self.is_pleasant:
            if not self.award and self.related_pleasant_habit:
                raise ValidationError(
                    'У полезной привычки должна быть приятная привычка, или вознаграждение'
                )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'{self.owner} - {Truncator(self.action).chars(20)}'
