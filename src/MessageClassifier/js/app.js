$(document).ready(function () {

    Handlebars.registerHelper({
        eq: function (v1, v2) {
            return v1 == v2;
        },
        ne: function (v1, v2) {
            return v1 != v2;
        },
        lt: function (v1, v2) {
            return v1 < v2;
        },
        gt: function (v1, v2) {
            return v1 > v2;
        },
        lte: function (v1, v2) {
            return v1 <= v2;
        },
        gte: function (v1, v2) {
            return v1 >= v2;
        },
        and: function (v1, v2) {
            return v1 && v2;
        },
        or: function (v1, v2) {
            return v1 || v2;
        }
    });

    //ajax
    $(document).ajaxStart(function () {
        $('body').addClass('ajaxbusy');
    });
    $(document).ajaxStop(function () {
        $('body').removeClass('ajaxbusy');
    });

    console.log('Ready!');   

    if (document.getElementById('classifier') != null) {
        console.log('Classifier loaded.')
        messageTemplate = Handlebars.compile($("#message-template").html());
        refresh();
    }
});

function refresh() {
    empty_messages();
    var count = $('#num_entries').val()
    var context = $('#context_num').val()
    if (count < 10) count = 10
    if (count > 200) count = 200
    if (context < 0) context = 0
    if (context > 50) context = 50
    load_messages(count, context);
}

function empty_messages() {
    var box = document.getElementById('messages_container');
    while (box.firstChild) {
        box.removeChild(box.firstChild);
    }
}

function submit_classification(message_id, classification) {

    hideAlerts();
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
        //alertSuccess(data.success);
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
    if (data.result) {
        if (data.data) {
            if ($('#full_update:checked').length > 0) {
                refresh();
            } else {
                set_message_HTML(data.data);
            }
        }
    }
}

function load_messages(count,context) {

    hideAlerts();
    var data = 'count=' + String(count) + '&context=' + String(context)
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

function generate_message_HTML(message) {
    var diff = JsDiff.diffChars(message.message_data['message'], message.message_data['message-filtered']);
    var fragment = document.createDocumentFragment();
    var color = '',
        span = null;
    diff.forEach(function (part) {
        // green for additions, red for deletions
        // grey for common parts
        color = part.added ? 'green' :
            part.removed ? 'red' : 'inherit';
        span = document.createElement('span');
        span.style.color = color;
        span.appendChild(document
            .createTextNode(part.value));
        fragment.appendChild(span);
    });
    message.message_data['message-diff'] = $('<div>').append(fragment).html();
    return messageTemplate(message);
}

function set_message_HTML(message) {
    var html = generate_message_HTML(message);

    if ($("#message" + String(message.message_id)).length > 0)
        $("#message" + String(message.message_id)).replaceWith(html)
    else
        $("#messages_container").append(html);
}

function submitDoneM(data, textStatus, jqXHR) {    
    if (!data.success.isEmpty()) {
        //alertSuccess(data.success);
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
    if (data.result) {
        for (message in data.data) {
            set_message_HTML(data.data[message]);
        }
    }
}