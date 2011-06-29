==============
django-dialogs
==============

Warning
=======

Still under heavy construction! Needs much more documentation.

Description
===========

I wanted a reusable application which would allow me to easily write
dialog chains (move through a sequence of dialogs depending on what
options the user picks). TODO

Dependencies
============

Currently requires jQuery 1.5+ and jQuery-UI. In the future the
dialog javascript library will be selectable.

Usage
=====

Defining a dialog
-----------------

Example::

  from dialogs import dialogs

  class InfoDialog(dialogs.Dialog)
    first = dialogs.Pane(
      'dialogs/info/first.html',
      buttons=(
        dialogs.Button('Next', 'NEXT:second'),
	dialogs.Button('Close', 'CLOSE'),
      )
    )
    second = dialogs.Pane(
      'dialogs/info/second.html',
      buttons=(
        dialogs.Button('Next', 'NEXT:third'),
	dialogs.Button('Close', 'CLOSE'),
      )
    )
    third = dialogs.Pane(
      'dialogs/info/third.html',
      buttons=(
        dialogs.Button('Done', 'SCRIPT:process_dialog'),
	dialogs.Button('Close', 'CLOSE'),
      )
    )

AjaxPane
--------

The standard ``Pane`` class renders static HTML into the dialog. If you
wish to include content from the server via AJAX you can use an ``AjaxPane``.
As an example::

  class DynamicInfoDialog(dialogs.Dialog)
    first = dialogs.AjaxPane(
      '/api/info/',
      buttons=(
	dialogs.Button('Close', 'CLOSE'),
      )
    )

Buttons
-------


Javascript/CSS
--------------

The dialog class uses the same mechanism for including media files
as form widgets. If you have a form and a dialog on a page, the
following can be used to merge all required javascript and CSS
files::

  {{ dialog.media + form.media }}

Including javascript in this fashion assumes that in your static
files folder you have ``js/jquery.min.js`` and ``js/jquery-ui.min.js``,
which will be included automatically.

At the moment the CSS for the dialogs must be included independently,
for example::

  <link href="{{ STATIC_URL }}css/jquery-ui.css" rel="stylesheet" type="text/css" media="screen" />
