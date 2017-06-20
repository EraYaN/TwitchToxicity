$(document).ready(function () {
    //ajax
    $(document).ajaxStart(function () {
        $('body').addClass('ajaxbusy');
    });
    $(document).ajaxStop(function () {
        $('body').removeClass('ajaxbusy');
    });

    console.log('Ready!');   

    if ($('#classifier')) {
        console.log('Classifier loaded.')
        load_messages(50);
    }
});

function submit_classification(message_id,classification) {
    var data = 'message_id='+String(message_id)+'&classification='+String(classification)
    var jqXHR = $.ajax({
        type: 'POST',
        url: 'ajax.php?submit_classification=1',
        data: data,
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        }
    }).done(submitDoneC).fail(submitFailC);
}

function submitFailC(jqXHR, textStatus, errorThrown) {
    alertDanger('Submitting classification failed.<br>' + errorThrown);
}
function submitDoneC(data, textStatus, jqXHR) {
    if (!data.success.isEmpty()) {
        alertSuccess(data.success);
    }
    if (!data.danger.isEmpty()) {
        alertDanger(data.danger);
    }
    if (!data.warning.isEmpty()) {
        alertWarning(data.warning);
    }
    if (!data.info.isEmpty()) {
        alertInfo(data.info);
    }
}

function load_messages(count) {
    var data = 'count='+String(count)
    var jqXHR = $.ajax({
        type: 'POST',
        url: 'ajax.php?get_messages=1',
        data: data,
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        }
    }).done(submitDoneM).fail(submitFailM);
}

function submitFailM(jqXHR, textStatus, errorThrown) {
    alertDanger('Getting messages for classification failed.<br>' + errorThrown);
}
function submitDoneM(data, textStatus, jqXHR) {
    if (!data.success.isEmpty()) {
        alertSuccess(data.success);
    }
    if (!data.danger.isEmpty()) {
        alertDanger(data.danger);
    }
    if (!data.warning.isEmpty()) {
        alertWarning(data.warning);
    }
    if (!data.info.isEmpty()) {
        alertInfo(data.info);
    }
    if(data.result){
        alert('Got messages!');
    }
}