from django.template import loader


__all__ = ['Pane']


class Pane(object):

    creation_counter = 0

    def __init__(self, template, method=None, buttons=None):
        self.template = template
        self.method = method
        self.buttons = buttons

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Pane.creation_counter
        Pane.creation_counter += 1
