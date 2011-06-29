from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import simplejson


@csrf_protect
@never_cache
def login(request):
    response = {}
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        response['status'] = 'success'
    else:
        response['status'] = 'error'
    return HttpResponse(simplejson.dumps(response), mimetype='application/javascript')
