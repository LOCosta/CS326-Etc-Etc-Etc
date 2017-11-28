from django.conf.urls import url

from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'create-project/', views.create_project, name='create-project'),
    url(r'project/(?P<id>[\d\w]+)/$', views.project, name='view-project'),
    url(r'project/(?P<pk>[\d\w]+)/update/$', views.ProjectUpdate.as_view(), name='update-project'),
    # url(r'user/', views.profile, name='view-current-user-profile'),  # Requires sessions to be implemented
    url(r'project/$', views.ProjectListView.as_view(), name='project-list'),
    url(r'user/$', views.ProfileListView.as_view(), name='user-list'),
    url(r'user/(?P<id>[\d\w]+)/$', views.profile, name='view-user-profile'),
    url(r'advanced-search/', views.search, name='advanced-search',),
    url(r'user/(?P<pk>[-\w]+)/update/$', views.ProfileUpdate.as_view(), name='edit-profile-user')
  
]
