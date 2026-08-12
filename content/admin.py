from django.contrib import admin

from .models import Post, Comment, PostReaction


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "content",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "author",
        "content",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "content",
        "author__username",
        "post__title",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "user",
        "reaction",
    )

    search_fields = (
        "post__title",
        "user__username",
    )

    list_filter = (
        "reaction",
    )