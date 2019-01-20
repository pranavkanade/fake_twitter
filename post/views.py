from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from core.models import Post
from post.serializers import PostSerializer, PostDetailSerializer, PostLikeSerializer


class PostViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        """Return objs for the current authenticated users only"""
        return self.queryset.all().order_by('-id')

    def perform_create(self, serializer):
        """Create new obj"""
        serializer.save(user=self.request.user)


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostLikeToggleView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer

    def patch(self, request, *args, **kwargs):
        post_obj = get_object_or_404(Post, pk=kwargs['pk'])
        if post_obj.user.id != request.user.id:
            if request.user not in post_obj.liked_by.all():
                post_obj.liked_by.add(request.user)
                if request.user in post_obj.disliked_by.all():
                    post_obj.disliked_by.remove(request.user)
            else:
                post_obj.liked_by.remove(request.user)
                if request.user not in post_obj.disliked_by.all():
                    post_obj.disliked_by.add(request.user)

        payload = {
            'liked_by': post_obj.liked_by,
            'disliked_by': post_obj.disliked_by
        }
        return self.partial_update(request, payload)


class PostPrivateViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
