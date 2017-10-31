from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'create-project/', views.CREATE-PROJECT, name='create-project'),
    url(r'project/(?P<id>\d+)/$', views.PROJECT, name='view-project'),
    url(r'user/(?P<id>\d+)/$', views.USER, name='view-user-profile'),
    url(r'advanced-search/', views.search, name='advanced-search',),
]
