from django.contrib import admin
from .models import Task, TodoItem, Comment, Activity, Reaction
from django_admin_relation_links import AdminChangeLinksMixin


class TodoItemInline(admin.TabularInline):
    model = TodoItem


class CommentInline(admin.TabularInline):
    model = Comment


class ActivityInline(admin.TabularInline):
    model = Activity


class TaskAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ['title', 'created_at', 'project_link', 'owner_link']
    list_display_links = ['title']
    change_links = ['project', 'owner']
    inlines = [TodoItemInline, CommentInline, ActivityInline]


class ReactionInline(admin.TabularInline):
    model = Reaction


class CommentAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ('content', 'owner_link', 'created_at', 'task_link')
    list_display_links = ['content']
    change_links = ['owner', 'task']
    inlines = [ReactionInline]


class ActivityAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ['title', 'type', 'task_link']
    list_display_links = ['title']
    change_links = ['task']


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Activity, ActivityAdmin)
