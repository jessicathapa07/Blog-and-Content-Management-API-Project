from rest_framework import serializers

from .models import Post, Comment, PostReaction


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

        read_only_fields = (
            "id",
            "author",
            "created_at",
            "updated_at",
        )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

        read_only_fields = (
            "id",
            "author",
            "created_at",
            "updated_at",
        )


class PostReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostReaction
        fields = "__all__"

        read_only_fields = (
            "id",
            "user",
        )