from django.conf import settings
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]


class PostReaction(models.Model):
    REACTION_CHOICES = (
        ("like", "Like"),
        ("dislike", "Dislike"),
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reactions",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_reactions",
    )

    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES,
    )

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.post.title} - "
            f"{self.reaction}"
        )