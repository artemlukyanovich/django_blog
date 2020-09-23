from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'blogs', views.BlogViewSet)
router.register(r'bloggers', views.BloggerViewSet)
router.register(r'comments', views.CommentViewSet)


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogs/$', views.BlogListView.as_view(), name='blogs'),
    url(r'^blogs/(?P<pk>\d+)$', views.BlogDetailView.as_view(), name='blog-detail'),
    url(r'^bloggers/$', views.BloggerListView.as_view(), name='bloggers'),
    url(r'^bloggers/(?P<pk>\d+)$', views.BloggerDetailView.as_view(), name='blogger-detail'),
    url(r'^blogs/(?P<pk>\d+)/create/$', views.CommentCreate.as_view(), name='comment-create'),
    
    # url(r'^profiles/new/$', views.NewProfileView.as_view(), name="new-user-profile"),
    url(r'^profile/$', views.EditProfileView.as_view(), name='edit-user-profile'),
    
    # path('api/blogs/', views.BlogView.as_view({'get': 'list'})),
    # path('api/blogs/<int:pk>', views.BlogView.as_view({'get': 'retrieve'})),
    url(r'^api/', include((router.urls, 'api-miniblog'))),
    
]

# swagger
urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', views.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', views.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', views.schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# urlpatterns += router.urls

