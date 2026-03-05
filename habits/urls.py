from django.urls import path
from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView
)


app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='create'),
    path('list/', HabitListAPIView.as_view(), name='habits_list'),
    path('detail/', HabitRetrieveAPIView.as_view(), name='detail_list'),
    path('update/', HabitUpdateAPIView.as_view(), name='update_list'),
    path('delete/', HabitDestroyAPIView.as_view(), name='delete_list'),
]