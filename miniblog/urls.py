from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogs/$', views.BlogListView.as_view(), name='blogs'),
    url(r'^blog/(?P<pk>\d+)$', views.BlogDetailView.as_view(), name='blog-detail'),
    url(r'^bloggers/$', views.BloggerListView.as_view(), name='bloggers'),
    url(r'^blogger/(?P<pk>\d+)$', views.BloggerDetailView.as_view(), name='blogger-detail'),
    url(r'^blog/(?P<pk>\d+)/create/$', views.CommentCreate.as_view(), name='comment-create'),
    path('api/blogs/', views.BlogView.as_view()),
]

