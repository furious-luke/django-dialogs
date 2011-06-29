from django.conf.urls.defaults import *
from views import *


urlpatterns = patterns('',
    url(r'^accounts/login/ajax/$', login),
)
