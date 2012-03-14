from django import forms
from django.utils.safestring import mark_safe


__all__ = ('ManyToManySelect',)


class ModelChoiceIterator(forms.models.ModelChoiceIterator):

    def __init__(self, field, ids=None):
        super(ModelChoiceIterator, self).__init__(field)
        if ids is not None:
            self.queryset = self.queryset.filter(id__in=ids)


class ManyToManySelect(forms.CheckboxSelectMultiple):

    # class Media:
    #     js = ('js/jquery.min.js', 'address/js/address.js',)

    def __init__(self, dialog, *args, **kwargs):
        self.dialog = dialog
        super(ManyToManySelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        if value is None:
            value = []

        trigger_html = self.dialog.trigger_as_submit({
            'value': 'Select',
            'class': ['m2mselect-select', 'submit', 'submitButton'],
        })

        intro = u'\n'.join([
            u'<ul>',
            u'<li>%s</li>'%trigger_html,
        ])
        outro = u'</ul>'

        # Replace the global choices with only the currently selected set, then
        # call the parent render function. Swap back afterwards.
        old_choices = self.choices
        self.choices = ModelChoiceIterator(self.choices.field, value)
        html = super(ManyToManySelect, self).render(name, value, attrs, **kwargs)
        self.choices = old_choices

        return mark_safe(u'\n'.join([intro, html, outro]))

    # def value_from_datadict(self, data, files, name):
    #     return data
