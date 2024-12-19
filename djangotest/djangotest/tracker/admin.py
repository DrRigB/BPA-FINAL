from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'duration_minutes', 'heart_rate', 'calories_burned', 'date')
    list_filter = ('user', 'name', 'date')
    search_fields = ('user__username', 'name')
    ordering = ('-date',)
