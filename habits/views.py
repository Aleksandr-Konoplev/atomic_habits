from django.db.models import Q
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HabitsUserListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitsPublicListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_publicity=True)


class HabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(Q(owner=self.request.user) | Q(is_publicity=True))


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
