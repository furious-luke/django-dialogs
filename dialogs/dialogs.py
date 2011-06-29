from django.utils.copycompat import deepcopy
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.forms.widgets import Media, media_property
from django.utils.encoding import StrAndUnicode
from panes import *
from buttons import *


__all__ = ['Pane',
           'Button', 'AjaxButton',
           'Dialog', 'LoginDialog']


##
# Refer to django/forms/forms.py for the original.
def get_declared_panes(bases, attrs, with_base_panes=True):

    # Pull the panes and order them using a counter on the Pane class.
    panes = [(pane_name, attrs.pop(pane_name)) for pane_name, obj in attrs.items() if isinstance(obj, Pane)]
    panes.sort(key=lambda x: x[1].creation_counter)

    # Grab base class panes.
    if with_base_panes:
        for base in bases[::-1]:
            if hasattr(base, 'base_panes'):
                panes = base.base_panes.items() + panes
    else:
        for base in bases[::-1]:
            if hasattr(base, 'declared_panes'):
                panes = base.declared_panes.items() + panes

    # Store in a Django sorted dictionary.
    return SortedDict(panes)


##
# This is used to build a set of panes on Dialog classes. Refer to
# django/forms/forms.py for the original.
class DeclarativePanesMetaclass(type):

    def __new__(cls, name, bases, attrs):
        attrs['base_panes'] = get_declared_panes(bases, attrs)
        new_class = super(DeclarativePanesMetaclass, cls).__new__(cls, name, bases, attrs)
        if 'media' not in attrs:
            new_class.media = media_property(new_class)
        return new_class


##
# Based on Django's BaseForm class. Refer to django/forms/forms.py for 
# the original.
class BaseDialog(StrAndUnicode):

    def __init__(self, request, name='', context={}):
        self.name = unicode(name)
        self.panes = deepcopy(self.base_panes)
        self.trigger_name = None
        self.first_pane = None
        self.request = request
        self.context = context
        self._type = None

    def __unicode__(self):
        return self.render()

    def __iter__(self):
        for name, pane in self.panes.items():
            yield BoundPane(self, pane, name)

    def __getitem__(self, name):
        try:
            pane = self.panes[name]
        except KeyError:
            raise KeyError('Key %r not found in Dialog'%name)
        return BoundPane(self, pane, name)

    def render(self):

        # Which pane to show first.
        if len(self.panes) > 0:
            if self.first_pane is not None:
                first_pane = self.first_pane
            else:
                first_pane = self.panes.keys()[0]

        html = u'<div%s class="dialogs-dialog">\n'%(' id="dialog-%s"'%self.name if self.name else '')
        for pane in self:
            classes = []
            if pane.name == first_pane:
                classes.append('first')
            html += pane.render({'class': classes})
        html += '</div>\n'
        return mark_safe(unicode(html))

    def trigger_as_a(self):
        if self.trigger_name is None:
            name = self.name
        else:
            name = self.trigger_name
        return mark_safe(u'<a class="dialogs-%s" target="dialog-%s">%s</a>'%(self._type, self.name, name))

    def trigger_as_button(self):
        if self.trigger_name is None:
            name = self.name
        else:
            name = self.trigger_name
        return mark_safe(u'<button type="button" class="dialogs-%s" target="dialog-%s">%s</button>'%(self._type, self.name, name))

    @property
    def media(self):
        media = Media()

        # Add the appropriate dialog media; this will depend on which
        # client-side dialog library is chosen.
        media.add_js(['js/jquery.min.js', 'js/jquery-ui.min.js'])

        # Add the dialogs scripts.
        media.add_js(['js/dialogs/jquery.dialogs.js', 'js/dialogs/dialogs.js'])

        for pane in self.panes.values():
            media = media + pane.media
        return media


##
#
class Dialog(BaseDialog):
    __metaclass__ = DeclarativePanesMetaclass

    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self._type = 'html'


##
#
class BoundPane(StrAndUnicode):

    def __init__(self, dialog, pane, name):
        self.dialog = dialog
        self.pane = pane
        self.name = name

    def render(self, attrs=None):
        return self.pane.render(self.dialog, self.name, attrs)


##
#
class LoginDialog(Dialog):
    login = Pane(
        'dialogs/login/login.html',
        buttons=(
            AjaxButton('Login', '/accounts/login/ajax/', success='CLOSE,SCRIPT:login_complete', error='SCRIPT:login_error'),
            Button('Cancel', 'CLOSE'),
        )
    )


##
#
class RegisterDialog(Dialog):
    register = Pane(
        'dialogs/login/register.html',
        buttons=(
            AjaxButton('Register', '/accounts/register/ajax/', success='CLOSE,SCRIPT:login_complete', error='login'),
            Button('Cancel', 'CLOSE'),
        )
    )
