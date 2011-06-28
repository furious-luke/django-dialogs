__all__ = ['BaseButton', 'Button', 'AjaxButton']


class BaseButton(object):

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.render()

    def _render_html(self, **kwargs):
        final_attrs = {'type': 'button'}
        final_attrs.update(kwargs)
        attrs_str = (u' ' + u' '.join([u'%s="%s"'%(k, v) for k, v in final_attrs.iteritems()])) if final_attrs else u''
        return u'<button%s>%s</button>'%(attrs_str, self.name)


class Button(BaseButton):

    def __init__(self, name, action):
        super(Button, self).__init__(name)
        self.action = action

    def render(self):
        attrs = {}
        if self.action:
            attrs['action'] = self.action
        return self._render_html(**attrs)


class AjaxButton(BaseButton):

    def __init__(self, name, url, success=None, error=None):
        super(AjaxButton, self).__init__(name)
        self.url = url
        self.success = success
        self.error = error

    def render(self):
        attrs = {}
        if self.url:
            attrs['target'] = self.url
        if self.success:
            attrs['success'] = self.success
        if self.error:
            attrs['error'] = self.error
        return self._render_html(**attrs)
