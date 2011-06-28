from django.test import TestCase
from dialogs import *


class EmptyDialog(Dialog):
    pass


def setup_panes(inst):
    inst.buttons={
        'Login': ('/accounts/login/', {
            'success': 'CLOSE,SCRIPT:login_complete',
            'error': 'login',
        }),
        'Cancel': 'CLOSE',
    }

    inst.pane_empty = Pane('')

    inst.pane_login = Pane(
        'dialogs/login/login.html',
        method='post',
        buttons=inst.buttons,
    )


def setup_bound_panes(inst):
    setup_panes(inst)
    inst.bound_empty = BoundPane(EmptyDialog(), inst.pane_empty, 'empty')
    inst.bound_login = BoundPane(EmptyDialog(), inst.pane_login, 'login')


class PaneTest(TestCase):

    def setUp(self):
        setup_panes(self)

    def test_construct_empty(self):
        self.assertEqual(self.pane_empty.template, '')
        self.assertIs(self.pane_empty.method, None)
        self.assertIs(self.pane_empty.buttons, None)

    def test_construct_login(self):
        self.assertEqual(self.pane_login.template, 'dialogs/login/login.html')
        self.assertEqual(self.pane_login.method, 'post')
        self.assertDictEqual(self.pane_login.buttons, self.buttons)


class BoundPaneTest(TestCase):

    def setUp(self):
        setup_bound_panes(self)

    def test_render_empty(self):
        html = self.bound_empty.render()
        self.assertEqual(html, u'')

    def test_render_login_no_form(self):
        html = self.bound_login.render()

        # Should have returned an empty form.
        bi = html.find('<form>') + len('<form>')
        ei = html.find('</form>')
        self.assertEqual(html[bi:ei].strip(), u'')

    def test_render_login(self):
        # Set the context up with a form value.
        self.bound_login.dialog.request = {}
        self.bound_login.dialog.context = {'login_form': 'DUMMY'}
        html = self.bound_login.render()

        # Should have returned the word DUMMY in the form.
        bi = html.find('<form>') + len('<form>')
        ei = html.find('</form>')
        self.assertEqual(html[bi:ei].strip(), u'DUMMY')


class LoginTest(TestCase):

    def setUp(self):
        self.dialog_login = LoginDialog()

    def test_construct(self):
        dlg = self.dialog_login
        self.assertEqual(len(dlg.base_panes), 1)
        self.assertIn('login', dlg.base_panes)

    def test_render(self):
        html = self.dialog_login.render()
        # TODO: Improve this check.
        self.assertNotIn(html, [u'', None])
