from django.conf.urls import url
from vk.views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^allusers/$', allusers, name='allusers'),
    url(r'^delete_post/(?P<p_id>\d+)/$', delete_post, name='delete_post'),
    url(r'^friends/$', friends, name='friends'),
    url(r'^guest/$', guest, name='guest'),
    url(r'^home/$', home, name='home'),
    url(r'^insertpost/(?P<w_id>\d+)/$', insertpost, name='insertpost'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^notification/(?P<header>\d+)/$', notification, name='notification'),
    url(r'^news/$', news, name='news'),
    url(r'^profile/$', myprofile, name='myprofile'),
    url(r'^profile/id(?P<p_id>\d+)/$', profile, name='profile_with_id'),
    url(r'^register/$', register, name='register'),
    url(r'^upload_photo/$', upload_photo, name='upload_photo'),
    url(r'^query_registration/$', query_registration, name='query_registration'),
]


