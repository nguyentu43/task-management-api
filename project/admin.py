from django.contrib import admin
from .models import Project, Section, Tag
from chat.models import Message
from django_admin_relation_links import AdminChangeLinksMixin


class ChatInline(admin.TabularInline):
    model = Message


class SectionInline(admin.TabularInline):
    model = Section


class TagInline(admin.TabularInline):
    model = Tag


class ProjectAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ['title', 'created_at', 'owner_link']
    list_display_links = ['title']
    change_links = ['owner']
    inlines = [SectionInline, TagInline, ChatInline]


admin.site.register(Project, ProjectAdmin)
