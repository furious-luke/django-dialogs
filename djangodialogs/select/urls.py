from django.conf.urls.defaults import *
from views import *


urlpatterns = patterns('',
    url(r'^select/m2m/$', many_to_many_select),
)
