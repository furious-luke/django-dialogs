from inspect import isclass

from djangoutils.decorators import deferrable, called
# from djangoutils.decorators import post_to_dict
# from djangoutils.tokens import token_generator


__all__ = ('uses_dialogs', 'is_dialog')


def uses_dialogs(dialogs):

    # Make sure we're dealing with a list or tuple.
    if not isinstance(dialogs, (list, tuple)):
        dialogs = (dialogs,)

    # Make a dictionary of actions.
    actions = []
    for dlg in dialogs:
        if isclass(dlg):
            dlg = dlg()
        if dlg.first_pane:
            actions.append((dlg.trigger_name, dlg.first_pane.view))
    actions = dict(actions)

    # Return the deferrable view.
    return deferrable(actions, store_background=True)


# def uses_dialogs(dialogs):

#     # Make sure we're dealing with a list or tuple.
#     if not isinstance(dialogs, (list, tuple)):
#         dialogs = [dialogs]

#     # Make a dictionary of actions.
#     actions = []
#     for dlg in dialogs:
#         if isclass(dlg):
#             dlg = dlg()
#         if dlg.first_pane:
#             actions.append((dlg.trigger_name, dlg.first_pane.view))
#     actions = dict(actions)

#     # We return this function.
#     def uses_dialogs_inner(view):
#         def uses_dialogs_view(request, *args, **kwargs):

#             # Check for a resumed view.
#             retoken = request.GET.get('retoken', None)
#             if retoken:

#                 # There must be a matching token in the session.
#                 try:
#                     post = request.session[retoken]['post']
#                 except:
#                     raise Http404

#                 # Add a flag indicating a resume and provide the post data.
#                 request.defer_resumed = True
#                 request.defer_post = post
#                 return view(request, *args, **kwargs)

#             else:
#                 request.defer_resumed = False

#             # Check if an action has been requested. This generally happens as a result
#             # of submitting a form using a submit button named appropriately.
#             if request.method == 'POST':
#                 for name, action in actions.iteritems():
#                     if name in request.POST:

#                         # We need to convert the request method to GET.
#                         old_method = request.method
#                         request.method = 'GET'

#                         # Render the background first. Do this by swapping out the POST
#                         # method for GET, setting the inital content and calling the original
#                         # view.
#                         request.defer_post = request.POST
#                         background = view(request, *args, **kwargs)

#                         # Now render the foreground. We need to use a token to store the current
#                         # POST data on the request.
#                         token = token_generator.make_token(request.user)
#                         request.session[token] = {
#                             'token': token,
#                             'return_to': request.path,
#                             'post': post_to_dict(request.POST),
#                         }
#                         request.GET = {'token': token}
#                         foreground = action(request, *args, **kwargs)

#                         # Reset the request method.
#                         request.method = old_method

#                         # To combine the two, we need to hunt down the end of the body tag of
#                         # the background and insert the foreground into it.
#                         idx = background.content.rfind('</body>')
#                         background.content.insert(idx, foreground.content)

#                         # Shade the background and make the foreground modal.
#                         # TODO

#                         # Return the background, as it contains the foreground now.
#                         return background

#             # Nothing fancy going on, render the view as usual.
#             request.defer_post = {}
#             return view(request, *args, **kwargs)

#         return uses_dialogs_view
#     return uses_dialogs_inner


def is_dialog(dialog):
    if isclass(dialog):
        dialog = dialog()
    return called(dialog.cancel_trigger_names, use_background=True)
