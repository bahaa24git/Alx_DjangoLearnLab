from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post, Comment, Like

User = get_user_model()


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    # Accept post as PK; can be overridden in perform_create if needed
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ["id", "post", "author",
                  "content", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "comments_count",
            "likes_count",
            "liked",
        ]
        read_only_fields = [
            "author",
            "created_at",
            "updated_at",
            "comments_count",
            "likes_count",
            "liked",
        ]

    def get_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None
        if not user or not user.is_authenticated:
            return False
        # Use annotated flag when present; otherwise check DB
        if hasattr(obj, "_liked_by_request_user"):
            return obj._liked_by_request_user
        return Like.objects.filter(user=user, post=obj).exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["comments_count"] = getattr(
            instance, "comments_count", instance.comments.count())
        data["likes_count"] = getattr(
            instance, "likes_count", instance.likes.count())
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)
