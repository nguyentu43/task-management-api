from django.contrib import admin
from .models import Project, Section, Tag
from chat.models import Message


class ChatInline(admin.TabularInline):
    model = Message


class SectionInline(admin.TabularInline):
    model = Section


class TagInline(admin.TabularInline):
    model = Tag


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'owner']
    list_display_links = ['title', 'owner']
    inlines = [SectionInline, TagInline, ChatInline]


admin.site.register(Project, ProjectAdmin)
