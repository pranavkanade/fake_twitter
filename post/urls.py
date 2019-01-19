from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post.views import PostViewSet, PostDetailView, PostCreateView

router = DefaultRouter()
router.register('', PostViewSet)


app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/', PostDetailView.as_view(), name="details"),
]
