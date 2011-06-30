from ..dialogs import *


##
#
class LoginDialog(Dialog):
    login = Pane(
        'dialogs/login/login.html',
        buttons=(
            AjaxButton('Login', '/accounts/login/ajax/', success='CLOSE,SCRIPT:dialogs_login_complete'),
            Button('Cancel', 'CLOSE'),
        )
    )


##
#
class RegisterDialog(Dialog):
    register = Pane(
        'dialogs/login/register.html',
        buttons=(
            AjaxButton('Register', '/accounts/register/ajax/', success='NEXT:complete'),
            Button('Cancel', 'CLOSE'),
        )
    )
    complete = Pane(
        'dialogs/login/register_deferred.html',
        buttons=(
            Button('OK', 'CLOSE,SCRIPT:dialogs_register_deferred'),
        )
    )
