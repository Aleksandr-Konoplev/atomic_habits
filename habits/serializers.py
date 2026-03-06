from rest_framework.serializers import ModelSerializer
from habits.models import Habit
from habits.validators import DurationValidator, PeriodicityValidator


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ('owner',)
        validators = [DurationValidator(field='duration'), PeriodicityValidator(field='periodicity')]
