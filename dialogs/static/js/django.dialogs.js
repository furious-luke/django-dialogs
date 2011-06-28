$('.dialogs-html').dialog_trigger();
$('.dialogs-ajax').ajax_dialog_trigger();

// Next and previous buttons.
$('.dialogs-next-button').click(function() {
    var cur = $(this).closest('div.dialogs-pane');
    var dialog = cur.closest('div.dialogs-dialog');
    var next = dialog.children('div#' + $(this).attr('next'));
    cur.hide();
    next.show();
    next.attr('dialogs-prev', cur.attr('id'));
});
$('.dialogs-prev-button').click(function() {
    var cur = $(this).closest('div.dialogs-pane');
    var dialog = cur.closest('div.dialogs-dialog');
    var content = dialog.children(':first').appendTo('body').hide();
    var prev = $(dialog.children('div.dialogs-prev').attr('prev')).prependTo(dialog).show();
});
