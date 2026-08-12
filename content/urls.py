from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    PostReactionViewSet,
)


router = DefaultRouter()

router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("reactions", PostReactionViewSet)


urlpatterns = [
    path("", include(router.urls)),
]