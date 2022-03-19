from django.contrib import admin
from .models import Profile
from project.models import Project

class ProjectInline(admin.StackedInline):
    model = Project

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'created_at']
    inlines = [ProjectInline]

admin.site.register(Profile, ProfileAdmin)
