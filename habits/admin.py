from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    model = Habit

    list_display = ('id', '__str__', 'is_publicity')
    search_fields = ('action',)
    ordering = ('id',)
