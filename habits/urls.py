from django.urls import path
from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitsUserListAPIView,
    HabitsPublicListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='create'),
    path('my/list/', HabitsUserListAPIView.as_view(), name='habits_my_list'),
    path('public/list/', HabitsPublicListAPIView.as_view(), name='habits_public_list'),
    path('<int:pk>/detail/', HabitRetrieveAPIView.as_view(), name='detail_list'),
    path('<int:pk>/update/', HabitUpdateAPIView.as_view(), name='update_list'),
    path('<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='delete_list'),
]
