from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Comment, PostReaction
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    PostSerializer,
    CommentSerializer,
    PostReactionSerializer,
)


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):

        if self.action in [
            "like",
            "unlike",
            "dislike",
            "remove_dislike",
        ]:
            permission_classes = [
                permissions.IsAuthenticated,
            ]

        else:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerOrReadOnly,
            ]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Like a post
    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):

        post = self.get_object()

        reaction, created = PostReaction.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={
                "reaction": "like",
            },
        )

        return Response(
            {
                "message": "Post liked successfully.",
                "reaction": reaction.reaction,
            }
        )

    # Unlike a post
    @action(detail=True, methods=["delete"])
    def unlike(self, request, pk=None):

        post = self.get_object()

        deleted, _ = PostReaction.objects.filter(
            user=request.user,
            post=post,
            reaction="like",
        ).delete()

        if deleted:
            return Response(
                {
                    "message": "Post unliked successfully."
                }
            )

        return Response(
            {
                "message": "Post was not liked."
            },
            status=404,
        )

    # Dislike a post
    @action(detail=True, methods=["post"])
    def dislike(self, request, pk=None):

        post = self.get_object()

        reaction, created = PostReaction.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={
                "reaction": "dislike",
            },
        )

        return Response(
            {
                "message": "Post disliked successfully.",
                "reaction": reaction.reaction,
            }
        )

    # Remove dislike
    @action(detail=True, methods=["delete"])
    def remove_dislike(self, request, pk=None):

        post = self.get_object()

        deleted, _ = PostReaction.objects.filter(
            user=request.user,
            post=post,
            reaction="dislike",
        ).delete()

        if deleted:
            return Response(
                {
                    "message": "Dislike removed successfully."
                }
            )

        return Response(
            {
                "message": "Post was not disliked."
            },
            status=404,
        )


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostReactionViewSet(viewsets.ModelViewSet):

    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]