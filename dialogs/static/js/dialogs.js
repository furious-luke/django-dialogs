$(document).ready(function() {

function dialogs_next(btn, next) {
    var cur = btn.closest('div.dialogs-pane');
    var dialog = cur.closest('div.dialogs-dialog');
    var next = dialog.children('div#pane-' + next);
    cur.hide();
    next.show();
    next.attr('prev', cur.attr('id'));
}

function dialogs_prev(btn) {
    var cur = btn.closest('div.dialogs-pane');
    var dialog = cur.closest('div.dialogs-dialog');
    var prev = dialog.children('div#' + cur.attr('prev'));
    cur.hide();
    prev.show();
}

function dialogs_close(btn) {
    var dialog = btn.closest('div.dialogs-dialog');
    dialog.dialog('close');
}

function dialogs_handle_actions(btn, action_str) {
    var actions = action_str.split(',');
    for(var ii = 0; ii < actions.length; ++ii) {
	var act = $.trim(actions[ii]);
	if(act == 'CLOSE') {
	    dialogs_close(btn);
	}
	if(act == 'PREV') {
	    dialogs_prev(btn);
	}
	else {
	    var func = act.split(':');
	    if(func.length > 1) {
		if(func[0] == 'NEXT') {
		    dialogs_next(btn, func[1]);
		}
		else if(func[0] == 'SCRIPT') {
		    func = func[1];
		    // Call function somehow...
		    alert('can\'t call scripts yet');
		}
	    }
	    else
		alert('Unrecognised action: "' + act + '"');
	}
    }
}

$('.dialogs-html').dialog_trigger();
$('.dialogs-ajax').ajax_dialog_trigger();

// Handle static buttons.
$('.dialogs-button').click(function() {
    dialogs_handle_actions($(this), $(this).attr('action'));
});

// Handle AJAX buttons.
$('.dialogs-ajaxbutton').click(function() {
    var btn = $(this);
    var url = $(this).attr('target');
    var form = $(this).attr('form');
    var success = $(this).attr('success');
    var error = $(this).attr('error');

    // If no form specified, find the first form in the pane.
    if(form == undefined)
	form = $(this).closest('div.dialog-pane').children('form').first();
    else
	form = $(form).first();

    // If no success actions given, just close the dialog.
    if(success == undefined)
	success = 'CLOSE';

    // If no error given, just alert the user.
    if(error == undefined)
	error = 'SCRIPT:dialogs_alert';

    // Pack our data if there is any.
    if(form.length > 0)
	send_data = form.serialize();
    else
	send_data = '';

    // Submit our AJAX request, note that we're using the jqXHR
    // system, so we need jQuery 1.5+.
    $.post(url, send_data)
    .success(function(data) {
	data = $.parseJSON(data);
	if(data.status == 'success') {
	    dialogs_handle_actions(btn, success);
	}
	else if(data.status == 'error') {
	    dialogs_handle_actions(btn, error);
	}
	else {
	    alert('Unhandled status "' + data.status + '".');
	}
    })
    .error(function() {
	alert('AJAX request failed.');
    });
});

});
