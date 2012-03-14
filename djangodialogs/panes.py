from django.template import loader
from django.forms.widgets import MediaDefiningClass
from django.utils.itercompat import is_iterable
from django.template import RequestContext
from django.template.loader import render_to_string
from pythonutils.html import AttrDict


__all__ = ['Pane']


class BasePane(object):
    __metaclass__ = MediaDefiningClass

    creation_counter = 0

    def __init__(self, buttons=None, view=None):
        self.view = view
        self.buttons = buttons

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Pane.creation_counter
        Pane.creation_counter += 1

    def render_buttons(self):
        if self.buttons:
            html = [u'<div class="dialogs-buttons buttonHolder">']
            for btn in self.buttons:
                html.append(btn.render())
            html.append(u'</div>')
            return u'\n'.join(html)
        else:
            return u''


class Pane(BasePane):

    def __init__(self, template, buttons=None, view=None):
        super(Pane, self).__init__(buttons, view)
        self.template = template

    def render(self, dialog, name, attrs=None):
        final_attrs = AttrDict({'class': 'dialogs-pane'}, attrs, ['class'])
        if not self.template:
            return u''
        if dialog.request is not None:
            ctx = RequestContext(dialog.request, dialog.context)
        else:
            ctx = None
        html = render_to_string(self.template, context_instance=ctx)
        if html:
            html += u'\n'
        html += self.render_buttons()
        html = u'<div id="pane-%s"%s>\n'%(name, unicode(final_attrs)) + html + u'</div>\n'
        return html


class AjaxPane(BasePane):

    def __init__(self, url, buttons=None):
        super(Pane, self).__init__(buttons)
        self.url = url

    def render(self, dialog, name, attrs=None):
        final_attrs = AttrDict({'class': 'dialogs-ajaxpane'}, attrs, ['class'])
        html = u'<div class="dialogs-ajaxpanecontent"></div>\n'
        html += self.render_buttons()
        html = u'<div id="pane-%s"%s>\n'%(name, unicode(final_attrs)) + html + u'</div>\n'
        return html + self.render_buttons()
