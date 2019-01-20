from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post.views import PostViewSet, PostDetailView, PostLikeToggleView, PostPrivateViewSet, PostDislikeToggleView

router = DefaultRouter()
router.register('', PostViewSet)


app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/', PostDetailView.as_view(), name="details"),
    path('<int:pk>/like/', PostLikeToggleView.as_view(), name="post-like"),
    path('<int:pk>/dislike/', PostDislikeToggleView.as_view(), name="post-dislike"),
    path('me/', PostPrivateViewSet.as_view(), name="personal-posts"),
]
