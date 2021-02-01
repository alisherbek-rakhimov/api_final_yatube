from django.urls import path, include
from .views import Index

from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
router.register('follow', FollowViewSet, basename='follows')
router.register('group', GroupViewSet, basename='groups')

urlpatterns = [
    path('', include(router.urls))
]
