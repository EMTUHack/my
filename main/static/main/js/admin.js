function import_hackers() {
    var text = $("#batch_hackers").val();
    if (text.length == 0)
        return;
    $.ajax(
    {
        url: import_hackers_url,
        type: 'post',
        data: {
            data: text,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#batch_anchor").show();

            $("#batch_content_1").empty();
            $("#batch_title_1").text("Sucesso(" + data['success'].length + ")");
            if (data['success'].length > 0)
                for (i in data['success'])
                    $("#batch_content_1").append("<p class='transition hidden'>" + data['success'][i]['name'] + "</p>");

                $("#batch_content_2").empty();
                $("#batch_title_2").text("Existentes(" + data['repeated'].length + ")");
                if (data['repeated'].length > 0)
                    for (i in data['repeated'])
                        $("#batch_content_2").append("<p class='transition hidden'>" + data['repeated'][i]['name'] + "</p>");

                    $("#batch_content_3").empty();
                    $("#batch_title_3").text("Erros(" + data['fail'].length + ")");
                    if (data['fail'].length > 0)
                        for (i in data['fail'])
                            $("#batch_content_3").append("<p class='transition hidden'>" + data['fail'][i]['name'] + " - " + data['fail'][i]['error'] + "</p>");
                    }
                })
}

function import_staff() {
    var text = $("#batch_staff").val();
    if (text.length == 0)
        return;
    $.ajax(
    {
        url: import_staff_url,
        type: 'post',
        data: {
            data: text,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#batch_anchor_staff").show();

            $("#batch_content_1_staff").empty();
            $("#batch_title_1_staff").text("Sucesso(" + data['success'].length + ")");
            if (data['success'].length > 0)
                for (i in data['success'])
                    $("#batch_content_1_staff").append("<p class='transition hidden'>" + data['success'][i]['name'] + "</p>");

                $("#batch_content_2_staff").empty();
                $("#batch_title_2_staff").text("Existentes(" + data['repeated'].length + ")");
                if (data['repeated'].length > 0)
                    for (i in data['repeated'])
                        $("#batch_content_2_staff").append("<p class='transition hidden'>" + data['repeated'][i]['name'] + "</p>");

                    $("#batch_content_3_staff").empty();
                    $("#batch_title_3_staff").text("Erros(" + data['fail'].length + ")");
                    if (data['fail'].length > 0)
                        for (i in data['fail'])
                            $("#batch_content_3_staff").append("<p class='transition hidden'>" + data['fail'][i]['name'] + " - " + data['fail'][i]['error'] + "</p>");
                    }
                })
}



$('#regopen').calendar({
    ampm: false,
    endCalendar: $('#regclose'),
    onChange: function (date, text, mode) {
        registration_open(date.toGMTString());
    }
});
$('#regopen').calendar('set date', regopen_date);
$('#regclose').calendar({
    ampm: false,
    startCalendar: $('#regopen'),
    onChange: function (date, text, mode) {
        registration_close(date.toGMTString());
    }
});
$('#regclose').calendar('set date', regclose_date);
$('#confby').calendar({
    ampm: false,
    onChange: function (date, text, mode) {
        confirm_by(date.toGMTString());
    }
});
$('#confby').calendar('set date', confby_date);
$('#hackstart').calendar({
    ampm: false,
    endCalendar: $('#hackend'),
    onChange: function (date, text, mode) {
        hackathon_start(date.toGMTString());
    }
});
$('#hackstart').calendar('set date', hackstart_date);
$('#hackend').calendar({
    ampm: false,
    startCalendar: $('#hackstart'),
    onChange: function (date, text, mode) {
        hackathon_end(date.toGMTString());
    }
});
$('#hackend').calendar('set date', hackend_date);


$('#event_create_start').calendar({
    endCalendar: $('#event_create_end'),
    ampm: false
});
$('#event_create_end').calendar({
    startCalendar: $('#event_create_start'),
    ampm: false
});



function registration_open(date) {
    $.ajax(
    {
        url: registration_open_url,
        type: 'post',
        data: {
            date: date,
            csrfmiddlewaretoken: csrf
        }
    })
}
function registration_close(date) {
    $.ajax(
    {
        url: registration_close_url,
        type: 'post',
        data: {
            date: date,
            csrfmiddlewaretoken: csrf
        }
    })
}
function confirm_by(date) {
    $.ajax(
    {
        url: confirm_by_url,
        type: 'post',
        data: {
            date: date,
            csrfmiddlewaretoken: csrf
        }
    })
}
function hackathon_start(date) {
    $.ajax(
    {
        url: hackathon_start_url,
        type: 'post',
        data: {
            date: date,
            csrfmiddlewaretoken: csrf
        }
    })
}
function hackathon_end(date) {
    $.ajax(
    {
        url: hackathon_end_url,
        type: 'post',
        data: {
            date: date,
            csrfmiddlewaretoken: csrf
        }
    })
}
function max_hackers(number) {
    $.ajax(
    {
        url: max_hackers_url,
        type: 'post',
        data: {
            number: number,
            csrfmiddlewaretoken: csrf
        }
    })
}

$('#max_hackers').on('input', function() {
    max_hackers($(this).val());
});

$(document).ready(function() {
    $('#schedule_table').DataTable({
        "language": {
            "lengthMenu": "Mostrar _MENU_ Eventos por página",
            "zeroRecords": "Sem eventos nessa pesquisa :(",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "Sem eventos por enquanto",
            "infoFiltered": "(Filtrado de _MAX_ eventos totais)",
            "oPaginate": {
                "sFirst":    "Primeiro",
                "sPrevious": "Anterior",
                "sNext":     "Seguinte",
                "sLast":     "Último"
            },
            "sSearch":       "Procurar:",
        },
        "ajax": fetch_schedule_simple_url,
    });
});
