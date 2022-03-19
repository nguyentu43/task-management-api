from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, SectionViewSet, TagViewSet
from chat.views import MessageViewSet
from task.views import TaskViewSet, TodoItemViewSet, CommentViewSet, ReactionViewSet

router = routers.SimpleRouter()
router.register(r'', ProjectViewSet, basename='project')

projects_router = routers.NestedSimpleRouter(router, r'', lookup='project')
projects_router.register(r'sections', SectionViewSet, basename='section')
projects_router.register(r'tags', TagViewSet, basename='tag')
projects_router.register(r'messages', MessageViewSet, basename='message')
projects_router.register(r'tasks', TaskViewSet, basename='task')

task_router = routers.NestedSimpleRouter(projects_router, r'tasks', lookup='task')
task_router.register(r'todo', TodoItemViewSet, basename='todo')
task_router.register(r'comments', CommentViewSet, basename='todo')

comment_router = routers.NestedSimpleRouter(task_router, r'comments', lookup='comment')
comment_router.register(r'reactions', ReactionViewSet, basename='reaction')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(projects_router.urls)),
    path(r'', include(task_router.urls)),
    path(r'', include(comment_router.urls))
]
