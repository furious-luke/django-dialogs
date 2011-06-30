from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import simplejson
from registration.backends.default import DefaultBackend


@csrf_protect
@never_cache
def login(request):
    response = {'status': 'error'}
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            response['status'] = 'success'
        else:
            response['form_errors'] = form.errors
    return HttpResponse(simplejson.dumps(response), mimetype='application/javascript')


@csrf_protect
@never_cache
def register(request):
    response = {'status': 'error'}
    backend = DefaultBackend()
    if backend.registration_allowed(request):
        form_class = backend.get_form_class(request)
        if request.method == 'POST':
            form = form_class(data=request.POST, files=request.FILES)
            if form.is_valid():
                new_user = backend.register(request, **form.cleaned_data)
                response['status'] = 'success'
            else:
                response['form_errors'] = form.errors
    return HttpResponse(simplejson.dumps(response), mimetype='application/javascript')
