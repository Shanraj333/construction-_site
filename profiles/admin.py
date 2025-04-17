# profiles/admin.py

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_approved']
    list_filter = ['category', 'is_approved']
    search_fields = ['name', 'category']
    actions = ['approve_profiles']

    def approve_profiles(self, request, queryset):
        queryset.update(is_approved=True)
    approve_profiles.short_description = "Approve selected profiles"
