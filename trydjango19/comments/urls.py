from django.conf.urls import url
from django.contrib import admin
from .views import  comment_thread,comment_delete
urlpatterns = [
    #url(r'^$', posts_list, name='list'),
    #url(r'^create/$', posts_create),
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    url(r'^(?P<id>\d+)/delete/$', comment_delete,name="delete"),
    #url(r'^(?P<slug>[\w-]+)/delete/$', comment_delete),
]
