from habits.models import Habit
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)


class HabitCreateAPIView(CreateAPIView):
    queryset = Habit.objects.all()


class HabitListAPIView(ListAPIView):
    pass


class HabitRetrieveAPIView(RetrieveAPIView):
    pass


class HabitUpdateAPIView(UpdateAPIView):
    pass


class HabitDestroyAPIView(DestroyAPIView):
    pass