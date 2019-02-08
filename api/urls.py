""" api/urls.py """

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateView, DetailsView, UserView, UserDetailView

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'^users/(?P<pk>[0-9+])/$', UserDetailView.as_view(), name="users_details"),
    url(r'^get-token/', obtain_auth_token),
    url(r'^bucketlist/$', CreateView.as_view(), name="create"),
    url(r'^bucketlist/(?P<pk>[0-9+])/$', DetailsView.as_view(), name="details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
