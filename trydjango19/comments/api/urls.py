from django.conf.urls import url
from django.contrib import admin
from .views import CommentListAPIView, CommentDetailAPIView,CommentCreateAPIView

urlpatterns = [
    # url(r'^$', posts_list, name='list'),
    url(r'^create/$', CommentCreateAPIView.as_view(),name="create"),
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', comment_delete),
]
