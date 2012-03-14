from django import forms

from djangoutils.decorators import called
from djangoutils.uniform import UniFormMedia, make_helper

from ..dialogs import Dialog, Pane, Button, SubmitButton, CancelButton
from .views import many_to_many_select


__all__ = ('make_select_form', 'make_select_dialog')


def make_select_form(model):

    def update_choices(self, queryset):
        self.fields['object_select'].choices = queryset

    @property
    def helper(self):
        return make_helper(self, (('search', 'Search'), ('create', 'Create new')), (('cancel', 'Cancel'),))

    model_name = model.__name__
    meta_class = type('Meta', (object,), {'model': model})
    form_class = type('M2MSelectForm%s'%model_name, (forms.ModelForm, UniFormMedia), {
        'object_select': forms.ChoiceField(widget=forms.RadioSelect, choices=[]),
        'Meta': meta_class,
        'update_choices': update_choices,
        'helper': helper,
    })
    return form_class


def make_select_dialog(model):
    form_class = make_select_form(model)
    model_name = model.__name__
    dialog_class = type('M2MSelectDialog%s'%model_name, (Dialog,), {
        'name': model_name,
        'select': Pane(
            'dialogs/select/many_to_many_select.html',
            buttons=(
                SubmitButton('Select', 'CLOSE'),
                CancelButton('Cancel', 'CLOSE'),
            ),
        ),
        'form_class': form_class,
    })

    # In constructing the view function, we have to use the "called" decorator instead of
    # "is_dialog" because of a cyclic dependency issue.
    view = staticmethod(called(('cancel',), use_background=True)(lambda x,*y,**z: many_to_many_select(x, dialog_class, form_class, *y, **z)))

    # In order to use Django's "reverse" function I need to make sure the static view
    # method is only attached to one class (the dialog).
    dialog_class.view = view
    dialog_class.base_panes['select'].view = dialog_class.view

    return dialog_class
