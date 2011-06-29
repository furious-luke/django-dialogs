from django.utils.copycompat import deepcopy
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.forms.widgets import Media, media_property
from django.utils.encoding import StrAndUnicode
from django.template import RequestContext
from django.template.loader import render_to_string
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

    def __init__(self, name='', request=None, context={}):
        self.name = unicode(name)
        self.panes = deepcopy(self.base_panes)
        self.first_pane = None
        self.request = request
        self.context = context

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
            classes = ['dialogs-pane']
            if pane.name == first_pane:
                classes.append('first')
            html += u'<div id="pane-%s" class="%s">\n'%(pane.name, ' '.join(classes))
            html += pane.render()
            html += '</div>\n'
        html += '</div>\n'
        return mark_safe(unicode(html))

    @property
    def media(self):
        media = Media()

        # Add the appropriate dialog media; this will depend on which
        # client-side dialog library is chosen.
        media.add_js('js/jquery.min.js', 'js/jquery-ui.min.js')

        # Add the dialogs scripts.
        media.add_js('js/dialogs/jquery.dialogs.min.js', 'js/dialogs/dialogs.min.js')

        for pane in self.panes.values():
            media = media + pane.media
        return media


##
#
class Dialog(BaseDialog):
    __metaclass__ = DeclarativePanesMetaclass


##
#
class BoundPane(StrAndUnicode):

    def __init__(self, dialog, pane, name):
        self.dialog = dialog
        self.pane = pane
        self.name = name

    def render(self):
        if not self.pane.template:
            return u''
        if self.dialog.request is not None:
            ctx = RequestContext(self.dialog.request, self.dialog.context)
        else:
            ctx = None
        html = render_to_string(self.pane.template, context_instance=ctx)
        if html:
            html += u'\n'
        return html + self.render_buttons()

    def render_buttons(self):
        if self.pane.buttons:
            html = [u'<div class="dialogs-buttons">']
            for btn in self.pane.buttons:
                html.append(btn.render())
            html.append(u'</div>')
            return u'\n'.join(html)
        else:
            return u''


##
#
class LoginDialog(Dialog):
    login = Pane(
        'dialogs/login/login.html',
        method='post',
        buttons=(
            AjaxButton('Login', '/accounts/login/', success='CLOSE,SCRIPT:login_complete', error='login'),
            Button('Cancel', 'CLOSE'),
        )
    )
