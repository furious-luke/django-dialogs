(function($){

  $.fn.dialog_trigger = function(options) {

    return this.each(function() {

	var dialog = $($(this).attr('target'));
	var modal = Boolean($(this).attr('modal'));
	if(modal == undefined)
	    modal = true;

	var settings = $.extend({'autoOpen': false, 'modal': modal}, options);
	dialog.dialog(settings);

	$(this).click(function() {
	    // Hide all panes...
	    dialog.children('div').hide();
	    // ... then show the first one.
	    dialog.children('div#' + dialog.attr('first')).show();
	    dialog.dialog('open');
	});

    });

  }

  $.fn.ajax_dialog_trigger = function(options) {

    return this.each(function() {

	var content = $('<div class="dialog" style="display:none"></div>');
	$('body').append(content);

	var url = $(this).attr('target');
	var modal = Boolean($(this).attr('modal'));
	if(modal == undefined)
	    modal = true;

	var settings = $.extend({'autoOpen': false, 'modal': modal}, options);

	settings.open = function(event, ui) {
	    content.load(url, function() {
		if(options.open)
		    options.open(event, ui, content);
	    });
	}

	settings.close = function(event, ui) {
	    if(options.close)
	        close(event, ui, content);
	    content.remove();
	}

	$(this).click(function() {
	    content.dialog(settings);
	});

    });

  }

})( jQuery );
