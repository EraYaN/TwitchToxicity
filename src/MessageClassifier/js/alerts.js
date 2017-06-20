$(document).ready(function () {
	//alert hiding
	$("[data-hide]").on("click", function () {
		//$("#" + $(this).data("hide")).hide();
		//console.log('Closing 2', this);
		// -or-, see below
		$(this).closest("." + $(this).data("hide")).hide();
	});
});

function hideAlerts() {
	$('.alert').hide();
}

function alertDanger(text) {
	if (text.length > 0) {
		$('#dangerdiv').show();
		$.scrollTo($('#dangerdiv'));
		$('#dangerdivcontent').html(text);
	} else {
		$('#dangerdiv').hide();
		$('#dangerdivcontent').html('');
	}
}
function alertWarning(text) {
	if (text.length > 0) {
		$('#warningdiv').show();
		$.scrollTo($('#warningdiv'));
		$('#warningdivcontent').html(text);
	} else {
		$('#warningdiv').hide();
		$('#warningdivcontent').html('');
	}
}
function alertInfo(text) {
	if (text.length > 0) {
		$('#infodiv').show();
		$.scrollTo($('#infodiv'));
		$('#infodivcontent').html(text);
	} else {
		$('#infodiv').hide();
		$('#infodivcontent').html('');
	}
}
function alertSuccess(text) {
	if (text.length > 0) {
		$('#successdiv').show();
		$.scrollTo($('#successdiv'));
		$('#successdivcontent').html(text);
	} else {
		$('#successdiv').hide();
		$('#successdivcontent').html('');
	}
}