from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    group = serializers.SlugRelatedField(slug_field='title', queryset=Group.objects.all(), required=False)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ['post']
        write_only_fields = ''


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title',)
        model = Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username',)
        model = User


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        # read_only_fields = ('user',)  # needed to to get it from user

        validators = [
            UniqueTogetherValidator(queryset=Follow.objects.all(), fields=('user', 'following'))
        ]
    #
    # def create(self, validated_data):
    #     print(validated_data)
    #     following = validated_data.get('following')
    #     user = validated_data.get('user')
    #     following = get_object_or_404(User, username=following)
    #     return Follow.objects.create(following=following, user=user)

    # return super().create(validated_data)
