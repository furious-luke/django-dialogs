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

function dialogs_handle_actions(btn, action_str, data) {
    var actions = action_str.split(',');
    for(var ii = 0; ii < actions.length; ++ii) {
	var act = $.trim(actions[ii]);
	if(act == 'CLOSE') {
	    dialogs_close(btn);
	}
	else if(act == 'PREV') {
	    dialogs_prev(btn);
	}
	else {
	    var func = act.split(':');
	    if(func.length > 1) {
		if(func[0] == 'NEXT') {
		    if(func[1][0] == '$') {
			// Use a value returned in the data to move to the
			// next pane.
			next = data[func[1].slice(1)];
		    }
		    else
			next = func[1];
		    dialogs_next(btn, next);
		}
		else if(func[0] == 'SCRIPT') {
		    func = func[1];
		    if(eval('typeof ' + func) == 'function')
			eval(func + '(btn, data);');
		}
	    }
	    else
		alert('Unrecognised action: "' + act + '"');
	}
    }
}

function dialogs_alert(obj, msg) {
    alert(msg);
}

function dialogs_show_form_errors(obj, data) {
    form_errors = data.form_errors;
    if(form_errors == undefined || form_errors == null)
        return;
    var pane = obj.closest('div.dialogs-pane');
    for(var field_name in form_errors) {
       var field = pane.find('#id_' + field_name);
       if(field.length == 0)
           continue;
       var errors = form_errors[field_name];
       if(errors.length == 0)
           continue;
       html = '<ul class="dialogs-formerrors">';
       for(var error in errors) {
           html += '<li>' + error + '</li>';
       html += '</ul>';
       field.before(html);
    }
}

function dialogs_clear_form_errors(obj) {
    var pane = obj.closest('div.dialogs-pane');
    pane.find('ul.dialogs-formerrors').remove();
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

    // Clear out any form errors before we begin.
    dialogs_clear_form_errors(btn);

    // If there is no form specified, first try and find a form in
    // the local pane.
    if(form == undefined || form == null) {
	form = $(this).closest('div.dialogs-pane').find('form').first();

	// If we still couldn't find a form, look for one as a child of
	// dialog itself.
	if(form.length == 0)
	    form = $(this).closest('div.dialogs-dialog').children('form').first();
    }
    else
	form = $(form).first();

    // If no success actions given, just close the dialog.
    if(success == undefined || success == null)
	success = 'CLOSE';

    // If no error given just run any form error processing.
    if(error == undefined || error == null)
	error = 'SCRIPT:dialogs_show_form_errors';

    // Pack our data if there is any.
    var send_data = '';
    if(form.length > 0)
	send_data = form.serialize();

    // Submit our AJAX request, note that we're using the jqXHR
    // system, so we need jQuery 1.5+.
    $.post(url, send_data).complete(function(xhr, status) {
	if(status == 'error' || !xhr.responseText) {
    	    alert('AJAX request failed.');
	}
	else {
    	    var data = $.parseJSON(xhr.responseText);
    	    if(data.status == 'success') {
    		dialogs_handle_actions(btn, success, data);
    	    }
    	    else if(data.status == 'error') {
    		dialogs_handle_actions(btn, error, data);
    	    }
    	    else {
    		alert('Unhandled status "' + data.status + '".');
    	    }
	}
    });
});

// Handle AJAX panes.
$('.dialogs-ajaxpane').click(function() {
    var pane = $(this);
    var url = $(this).attr('target');
    var form = $(this).attr('form');
    var error = $(this).attr('error');

    // If no error given, just alert the user.
    if(error == undefined || error == null)
	error = 'SCRIPT:dialogs_alert';

    // Pack our data if there is any.
    var send_data = '';
    if(form.length > 0)
	send_data = form.serialize();

    // Submit our AJAX request, note that we're using the jqXHR
    // system, so we need jQuery 1.5+.
    $.post(url, send_data).complete(function(xhr, status) {
	if(status == 'error' || !xhr.responseText) {
    	    alert('AJAX request failed.');
	}
	else {
	    pane.children('div.dialogs-ajaxpanecontent').html(data);
	}
    });
});

});
