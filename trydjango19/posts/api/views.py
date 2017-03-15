from django.db.models import Q
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveDestroyAPIView,ListAPIView,RetrieveUpdateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly
from .serializers import PostListSerializer,PostDetailSerializer,PostCreateUpdateSerializer
from posts.models import Post
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser, IsAuthenticatedOrReadOnly

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [
        IsAuthenticated
    ]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    # lookup_url_kwarg = "abc"

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    lookup_field = "slug"
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    lookup_field = "slug"

class PostListAPIView(ListAPIView):
    # queryset =
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title","content","user__first_name"]
    pagination_class = PostPageNumberPagination #PageNumberPagination
    def get_queryset(self,*args,**kwargs):
        # queryset_list = super(PostListAPIView,self).get_query_set(*args,*kwargs)
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list

