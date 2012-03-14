from pythonutils.html import AttrDict


_all__ = ('BaseButton', 'Button', 'SubmitButton', 'AjaxButton')


class BaseButton(object):

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.render()

    def _render_html(self, attrs={}):
        final_attrs = AttrDict({'type': 'button',
                                'value': self.name},
                               attrs,
                               ['class'])
        return u'<input%s></input>'%unicode(final_attrs)


class Button(BaseButton):

    def __init__(self, name, action):
        super(Button, self).__init__(name)
        self.action = action

    def render(self, attrs={}):
        defaults = {'class': 'dialogs-button'}
        if self.action:
            defaults['action'] = self.action
        return self._render_html(AttrDict(defaults, attrs, ['class']))


class SubmitButton(Button):

    def render(self, attrs={}):
        defaults = {'type': 'submit', 'class': ['submit', 'submitButton']}
        return super(SubmitButton, self).render(AttrDict(defaults, attrs, ['class']))


class CancelButton(SubmitButton):

    def render(self, attrs={}):
        defaults = {'class': 'secondaryAction'}
        return super(CancelButton, self).render(AttrDict(defaults, attrs, ['class']))


class AjaxButton(BaseButton):

    def __init__(self, name, url, success=None, error=None):
        super(AjaxButton, self).__init__(name)
        self.url = url
        self.success = success
        self.error = error

    def render(self):
        attrs = {'class': 'dialogs-ajaxbutton'}
        if self.url:
            attrs['target'] = self.url
        if self.success:
            attrs['success'] = self.success
        if self.error:
            attrs['error'] = self.error
        return self._render_html(**attrs)
