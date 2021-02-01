import time
from collections import OrderedDict
import django_filters.rest_framework

from rest_framework import generics, filters
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import OwnResourcePermission
from api.models import Post, Group, Follow, Comment
from api.serializers import PostSerializer, GroupSerializer, FollowSerializer, CommentSerializer

User = get_user_model()


class Index(APIView):
    def get(self, request):
        return Response("INDEX")


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnResourcePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['group', ]

    # def get_queryset(self):
    #     group_id = self.request.query_params.get('group', None)
    #     if group_id is not None:
    #         group = get_object_or_404(Group, id=group_id)
    #         queryset = Post.objects.filter(group=group)
    #     else:
    #         queryset = Post.objects.all()
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']
    # search_fields = ['user__username']
    # search_fields = ['following__username']

    # def get_queryset(self):
    #     username = self.request.query_params.get('search', None)
    #     if username is not None:
    #         user = get_object_or_404(User, username=username)
    #         # queryset = Follow.objects.filter(following=Q(following=user) | Q(user=user))
    #         queryset = Follow.objects.filter(user=user)
    #     else:
    #         queryset = Follow.objects.all()
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnResourcePermission]
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(post=post, author=self.request.user)
