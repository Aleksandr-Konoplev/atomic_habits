from rest_framework.serializers import ValidationError


class DurationValidator:
    """Валидация длительности привычки"""

    def __init__(self, field):
        self.field = field
        self.max_duration = 120

    def __call__(self, attrs):
        duration = attrs.get(self.field)

        if duration <= self.max_duration:
            return attrs
        raise ValidationError(f'Продолжительность действия привычки не должна превышать {self.max_duration} секунд.')


class PeriodicityValidator:
    """Валидация интервалов между привычками"""

    def __init__(self, field):
        self.field = field
        self.max_periodicity = 7

    def __call__(self, attrs):
        periodicity = attrs.get(self.field)

        if periodicity <= self.max_periodicity:
            return attrs
        raise ValidationError(f'Периодичность привычки не должна превышать {self.max_periodicity} дней.')


class RelatedPleasantHabitValidator:
    """Валидатор для проверки связанных приятных привычек."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        related_habit = attrs.get(self.field)

        if related_habit is not None:

            if not related_habit.is_pleasant:
                raise ValidationError('Связанная привычка должна быть приятной.')

        return attrs
