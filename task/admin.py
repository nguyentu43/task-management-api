from django.contrib import admin
from .models import Task, TodoItem, Comment, Activity, Reaction


class TodoItemInline(admin.TabularInline):
    model = TodoItem


class CommentInline(admin.TabularInline):
    model = Comment


class ActivityInline(admin.TabularInline):
    model = Activity


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'project', 'owner']
    list_display_links = ['title', 'project', 'owner']
    inlines = [TodoItemInline, CommentInline, ActivityInline]


class ReactionInline(admin.TabularInline):
    model = Reaction


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'owner', 'created_at', 'task')
    list_display_links = ['content', 'owner', 'task']
    inlines = [ReactionInline]


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'task']
    list_display_links = ['title', 'task']


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Activity, ActivityAdmin)
