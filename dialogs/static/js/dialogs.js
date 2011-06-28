$('.dialogs-html').dialog_trigger();
$('.dialogs-ajax').ajax_dialog_trigger();

function dialogs_next(btn) {
    var cur = btn.closest('div.dialogs-pane');
    var dialog = cur.closest('div.dialogs-dialog');
    var next = dialog.children('div#' + btn.attr('next'));
    cur.hide();
    next.show();
    next.attr('dialogs-prev', cur.attr('id'));
}

function dialogs_prev(btn) {
    var cur = btn.closest('div.dialogs-pane');
    var dialog = cur.closest('div.dialogs-dialog');
    var content = dialog.children(':first').appendTo('body').hide();
    var prev = $(dialog.children('div.dialogs-prev').attr('prev')).prependTo(dialog).show();
}

// Handle static buttons.
$('.dialogs-button').click(function() {
    var actions = $(this).attr('action').split(',');
    for(action in actions) {
	var act = $.trim(action);
	if(act == 'CLOSE') {
	    dialogs_close();
	}
	else {
	    var func = act.split(':');
	    if(func.length > 1) {
		if(func[0] == 'SCRIPT') {
		    func = func[1];
		    // Call function somehow...
		}
	    }
	    else {
		dialogs_next($(this));
	    }
	}
    }
});

// Handle AJAX buttons.
$('.dialogs-prev-button').click(function() {

});
