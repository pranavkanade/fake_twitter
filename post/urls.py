from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post.views import PostViewSet, PostDetailView, PostLikeToggleView

router = DefaultRouter()
router.register('', PostViewSet)


app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/', PostDetailView.as_view(), name="details"),
    path('<int:pk>/like/', PostLikeToggleView.as_view(), name="post-like"),
]
