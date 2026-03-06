from rest_framework.serializers import ValidationError


class DurationValidator:
    """Валидация длительности привычки"""

    def __init__(self, field):
        self.field = field
        self.max_duration = 120

    def __call__(self, attrs):
        duration = attrs.get(self.field)

        if duration is not None and duration > self.max_duration:
            raise ValidationError(f'Продолжительность действия привычки не должна превышать {self.max_duration} секунд.')
        return attrs


class PeriodicityValidator:
    """Валидация интервалов между привычками"""

    def __init__(self, field):
        self.field = field
        self.max_periodicity = 7

    def __call__(self, attrs):
        periodicity = attrs.get(self.field)

        if periodicity is not None and periodicity > self.max_periodicity:
            raise ValidationError(f'Периодичность привычки не должна превышать {self.max_periodicity} дней.')
        return attrs


class RelatedPleasantHabitValidator:
    """Валидатор для проверки связанных приятных привычек."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        # В related_habit лежит объект, так нам отдал сериализатор
        related_habit = attrs.get(self.field)

        if related_habit is not None:

            if not related_habit.is_pleasant:
                raise ValidationError('Связанная привычка должна быть приятной.')

        return attrs
