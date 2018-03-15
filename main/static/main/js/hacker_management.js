function load_data_into_modal(data) {
    $("#hacker_name").text(data['Primeiro Nome'] + ' ' + data['Sobrenome']);
    $("#hacker_email").text(data['Email']);
    $("#hacker_phone").text(data['Celular']);
    $("#hacker_age").text(data['Idade']);
    $("#hacker_gender").text(data['Gênero']);
    $("#hacker_university").text(data['Universidade']);
    $("#hacker_enroll_year").text(data['Ano de Ingresso']);
    $("#hacker_shirt_size").text(data['Tamanho da Camisa']);
    $("#hacker_shirt_style").text(data['Tipo da Camisa']);
    $("#hacker_cv_type").text(data['Tipo do Currículo']);
    if (data['Transporte de SP'] == true) {
        $("#hacker_bus_sp").text("Sim");
    }
    else {
        $("#hacker_bus_sp").text("Não");
    }
    if (data['Transporte de SC'] == true) {
        $("#hacker_bus_sc").text("Sim");
    }
    else {
        $("#hacker_bus_sc").text("Não");
    }
    $("#hacker_cv").text(data['Currículo']);
    $("has_other_cv").hide();
    if (data['Tipo do Currículo 2'] != null) {
        $("has_other_cv").show();
        $("#hacker_cv2_type").text(data['Tipo do Currículo 2']);
        $("#hacker_cv2").text(data['Currículo 2']);
    }
    $('#hacker_description').text(data['Descrição']);
    $('#hacker_essay').text(data['Motivação']);
}

function show_pending(id) {
    $.ajax(
    {
        url: get_hacker_application_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            load_data_into_modal(data);
            hide_modal_actions();
            $('#pending_actions').show();
            $('.ui.modal').modal({
                'onApprove': function() {
                    swal(data['Primeiro Nome'] + ' ' + data['Sobrenome'], "Aprovar Hacker?", "warning", {
                        buttons: {
                            check: {
                                text: "Sim!",
                            },
                            cancel: "Deixa pra lá!",
                        },
                    }).then((value) => {
                        switch (value) {

                            case "check":
                            $.ajax(
                            {
                                url: admit_hacker_url,
                                type: 'post',
                                data: {
                                    id: id,
                                    csrfmiddlewaretoken: csrf
                                },
                                success: function(data) {
                                    swal("Pronto!", "Hacker admitido!", "success");
                                    reload_pending_hackers();
                                }
                            });
                            break;
                        }
                    });
                },
                'onDeny': function() {
                    swal(data['Primeiro Nome'] + ' ' + data['Sobrenome'], "Rejeitar Hacker?", "warning", {
                        buttons: {
                            check: {
                                text: "Sim!",
                            },
                            cancel: "Deixa pra lá!",
                        },
                    }).then((value) => {
                        switch (value) {

                            case "check":
                            $.ajax(
                            {
                                url: decline_hacker_url,
                                type: 'post',
                                data: {
                                    id: id,
                                    csrfmiddlewaretoken: csrf
                                },
                                success: function(data) {
                                    swal("Pronto!", "Hacker recusado!", "success");
                                    reload_pending_hackers();
                                }
                            });
                            break;
                        }
                    });
                }
            });
            $('.ui.modal').modal('show');
        }
    });
};

function show_admitted(id) {
    $.ajax(
    {
        url: get_hacker_application_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            load_data_into_modal(data);
            hide_modal_actions();
            $('#admitted_actions').show();
            $('.ui.modal').modal({
                'onDeny': function() {
                    swal(data['Primeiro Nome'] + ' ' + data['Sobrenome'], "Rejeitar Hacker?", "warning", {
                        buttons: {
                            check: {
                                text: "Sim!",
                            },
                            cancel: "Deixa pra lá!",
                        },
                    }).then((value) => {
                        switch (value) {

                            case "check":
                            $.ajax(
                            {
                                url: decline_hacker_url,
                                type: 'post',
                                data: {
                                    id: id,
                                    csrfmiddlewaretoken: csrf
                                },
                                success: function(data) {
                                    swal("Pronto!", "Hacker recusado!", "success");
                                    reload_admitted_hackers();
                                }
                            });
                            break;
                        }
                    });
                },
            });
            $('.ui.modal').modal('show');
        }
    });
};
function show_declined(id) {
    $.ajax(
    {
        url: get_hacker_application_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            load_data_into_modal(data);
            hide_modal_actions();
            $('#declined_actions').show();
            $('.ui.modal').modal({
                'onApprove': function() {
                    swal(data['Primeiro Nome'] + ' ' + data['Sobrenome'], "Aprovar Hacker?", "warning", {
                        buttons: {
                            check: {
                                text: "Sim!",
                            },
                            cancel: "Deixa pra lá!",
                        },
                    }).then((value) => {
                        switch (value) {

                            case "check":
                            $.ajax(
                            {
                                url: admit_hacker_url,
                                type: 'post',
                                data: {
                                    id: id,
                                    csrfmiddlewaretoken: csrf
                                },
                                success: function(data) {
                                    swal("Pronto!", "Hacker admitido!", "success");
                                    reload_declined_hackers();
                                }
                            });
                            break;
                        }
                    });
                },
            });
            $('.ui.modal').modal('show');
        }
    });
};
function show_waitlist(id) {
    $.ajax(
    {
        url: get_hacker_application_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            load_data_into_modal(data);
            hide_modal_actions();
            $('#waitlist_actions').show();
            $('.ui.modal').modal({
                'onApprove': function() {
                    swal(data['Primeiro Nome'] + ' ' + data['Sobrenome'], "Tirar da Fila?", "warning", {
                        buttons: {
                            check: {
                                text: "Sim!",
                            },
                            cancel: "Deixa pra lá!",
                        },
                    }).then((value) => {
                        switch (value) {

                            case "check":
                            $.ajax(
                            {
                                url: unwaitlist_hacker_url,
                                type: 'post',
                                data: {
                                    id: id,
                                    csrfmiddlewaretoken: csrf
                                },
                                success: function(data) {
                                    swal("Pronto!", "Hacker tirado da fila!", "success");
                                    reload_waitlist_hackers();
                                }
                            });
                            break;
                        }
                    });
                },
            });
            $('.ui.modal').modal('show');
        }
    });
};
function show_checkedin(id) {
    $.ajax(
    {
        url: get_hacker_application_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            load_data_into_modal(data);
            hide_modal_actions();
            $('.ui.modal').modal('show');
        }
    });
};

function hide_modal_actions() {
    $('#pending_actions').hide();
    $('#admitted_actions').hide();
    $('#declined_actions').hide();
    $('#waitlist_actions').hide();
}

function reload_pending_hackers() {
    $('#pending_hackers').DataTable().ajax.reload();
};
function reload_admitted_hackers() {
    $('#admitted_hackers').DataTable().ajax.reload();
};
function reload_declined_hackers() {
    $('#declined_hackers').DataTable().ajax.reload();
};
function reload_waitlist_hackers() {
    $('#waitlist_hackers').DataTable().ajax.reload();
};
function reload_checkedin_hackers() {
    $('#checkedin_hackers').DataTable().ajax.reload();
};

$(document).ready(function() {
    $('#pending_hackers').DataTable({
        "order": [[ 1, "asc" ]],
        "columnDefs": [
            {'orderData':[5], 'targets': [1] },
            {
                'targets': [5],
                'visible': false,
                'searchable': false
            },
        ],

        "language": {
            "lengthMenu": "Mostrar _MENU_ Hackers por página",
            "zeroRecords": "Sem hackers nessa pesquisa :(",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "Sem Hackers por enquanto",
            "infoFiltered": "(Filtrado de _MAX_ Hackers totais)",
            "oPaginate": {
                "sFirst":    "Primeiro",
                "sPrevious": "Anterior",
                "sNext":     "Seguinte",
                "sLast":     "Último"
            },
            "sSearch":       "Procurar:",
        },
        "ajax": fetch_submitted_hackers_url,
    });
    $('#admitted_hackers').DataTable({
        "order": [[ 1, "desc" ]],

        "language": {
            "lengthMenu": "Mostrar _MENU_ Hackers por página",
            "zeroRecords": "Sem hackers nessa pesquisa :(",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "Sem Hackers por enquanto",
            "infoFiltered": "(Filtrado de _MAX_ Hackers totais)",
            "oPaginate": {
                "sFirst":    "Primeiro",
                "sPrevious": "Anterior",
                "sNext":     "Seguinte",
                "sLast":     "Último"
            },
            "sSearch":       "Procurar:",
        },
        "ajax": fetch_admitted_hackers_url,
    });
    $('#declined_hackers').DataTable({
        "order": [[ 1, "desc" ]],

        "language": {
            "lengthMenu": "Mostrar _MENU_ Hackers por página",
            "zeroRecords": "Sem hackers nessa pesquisa :(",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "Sem Hackers por enquanto",
            "infoFiltered": "(Filtrado de _MAX_ Hackers totais)",
            "oPaginate": {
                "sFirst":    "Primeiro",
                "sPrevious": "Anterior",
                "sNext":     "Seguinte",
                "sLast":     "Último"
            },
            "sSearch":       "Procurar:",
        },
        "ajax": fetch_declined_hackers_url,
    });
    $('#waitlist_hackers').DataTable({
        "order": [[ 1, "asc" ]],
        "columnDefs": [
            {'orderData':[5], 'targets': [1] },
            {
                'targets': [5],
                'visible': false,
                'searchable': false
            },
        ],

        "language": {
            "lengthMenu": "Mostrar _MENU_ Hackers por página",
            "zeroRecords": "Sem hackers nessa pesquisa :(",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "Sem Hackers por enquanto",
            "infoFiltered": "(Filtrado de _MAX_ Hackers totais)",
            "oPaginate": {
                "sFirst":    "Primeiro",
                "sPrevious": "Anterior",
                "sNext":     "Seguinte",
                "sLast":     "Último"
            },
            "sSearch":       "Procurar:",
        },
        "ajax": fetch_waitlist_hackers_url,
    });
    $('#checkedin_hackers').DataTable({
        "order": [[ 1, "desc" ]],

        "language": {
            "lengthMenu": "Mostrar _MENU_ Hackers por página",
            "zeroRecords": "Sem hackers nessa pesquisa :(",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "Sem Hackers por enquanto",
            "infoFiltered": "(Filtrado de _MAX_ Hackers totais)",
            "oPaginate": {
                "sFirst":    "Primeiro",
                "sPrevious": "Anterior",
                "sNext":     "Seguinte",
                "sLast":     "Último"
            },
            "sSearch":       "Procurar:",
        },
        "ajax": fetch_checkedin_hackers_url,
    });
    $('.menu .item').tab({
        'onLoad': function(path, array, hist) {
            arr = {
                'first': reload_pending_hackers(),
                'second': reload_admitted_hackers(),
                'third': reload_declined_hackers(),
                'fourth': reload_waitlist_hackers(),
                'fifth': reload_checkedin_hackers(),
            }
        }
    });
} );
