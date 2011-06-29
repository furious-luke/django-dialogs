from django.template import loader
from django.forms.widgets import MediaDefiningClass
from django.utils.itercompat import is_iterable
from django.template import RequestContext
from django.template.loader import render_to_string


__all__ = ['Pane']


def is_iter(value):
    return is_iterable(value) and not isinstance(value, (basestring, dict))


def to_iter(value):
    if value is None:
        return []
    elif is_iter(value):
        return value
    else:
        return [value]


def flatten_attrs(attrs):
    if attrs is not None:
        return u' '.join([u'%s="%s"'%(k, ' '.join(to_iter(v))) for k, v in attrs.iteritems()])
    else:
        return u''


def update_attrs(attrs, more):
    if more is not None:
        for k, v in more.iteritems():
            if k in attrs:
                if not is_iter(attrs[k]):
                    if is_iter(v):
                        attrs[k] = [attrs[k]]
                        attrs[k].extend(v)
                    else:
                        attrs[k] = [attrs[k], v]
                else:
                    if isiter(v):
                        attrs[k].extend(v)
                    else:
                        attrs[k].append(v)
            else:
                attrs[k] = v
    return attrs


class BasePane(object):
    __metaclass__ = MediaDefiningClass

    creation_counter = 0

    def __init__(self, buttons=None):
        self.buttons = buttons

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Pane.creation_counter
        Pane.creation_counter += 1

    def render_buttons(self):
        if self.buttons:
            html = [u'<div class="dialogs-buttons">']
            for btn in self.buttons:
                html.append(btn.render())
            html.append(u'</div>')
            return u'\n'.join(html)
        else:
            return u''


class Pane(BasePane):

    def __init__(self, template, buttons=None):
        super(Pane, self).__init__(buttons)
        self.template = template

    def render(self, dialog, name, attrs=None):
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
        final_attrs = update_attrs({'class': 'dialogs-pane'}, attrs)
        html = u'<div id="pane-%s"%s>\n'%(name, flatten_attrs(final_attrs)) + html + u'</div>\n'
        return html


class AjaxPane(BasePane):

    def __init__(self, url, buttons=None):
        super(Pane, self).__init__(buttons)
        self.url = url

    def render(self, dialog, name, attrs=None):
        html = u'<div class="dialogs-ajaxpanecontent"></div>\n'
        html += self.render_buttons()
        final_attrs = update_attrs({'class': 'dialogs-ajaxpane'}, attrs)
        html = u'<div id="pane-%s"%s>\n'%(name, flatten_attrs(final_attrs)) + html + u'</div>\n'
        return html + self.render_buttons()
