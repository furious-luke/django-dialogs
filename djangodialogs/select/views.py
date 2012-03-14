from django.shortcuts import render, get_object_or_404
from djangoutils.decorators import called


def many_to_many_select(request, dialog_class, form_class, *args, **kwargs):
    ctx = {}
    model = form_class.Meta.model
    results = model.objects.none()

    # If we have post data we are either filtering or selecting.
    if request.method == 'POST':

        # Check for a valid form first.
        form = form_class(model, request.POST)
        if form.is_valid():

            # If 'filter' can be found in the POST data then perform the filtering.
            if 'filter' in request.POST:

                # Create a query from the model field names.
                exclude = set('token', 'object_select')
                for field_name, value in form.cleaned_data:
                    if field_name in exclude:
                        continue
                    query[field.name + '__icontains'] = form.cleaned_data[field.name]

                # Apply the filter.
                results = model.objects.filter(**query)

            # If 'select' can be found in the POST data then return the selection.
            elif 'select' in request.POST:

                # The user may not have actually selected anything.
                selected = {}
                cleaned_id = form.cleaned_data['id']
                if cleaned_id is not None:
                    obj = get_object_or_404(model, id=cleaned_id)
                    selected['many_to_many_selected'] = obj
                return resume_deferred(request, **selected)

    # Anything other than POST means we just display the form.
    else:
        form = form_class()

    # Update the choices.
    form.update_choices(results)

    # Create the dialog.
    dialog = dialog_class(request, ctx)

    ctx.update({
        'form': form,
        'dialog': dialog,
    })
    return render(request, 'dialogs/current_pane.html', ctx)
