function search_hackers() {
    var text = $("#search_hackers").val();
    if (text.length == 0)
        return;
    $.ajax(
    {
        url: search_hackers_url,
        type: 'post',
        data: {
            data: text,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#example").empty();
            $('#example').DataTable( {
                data: data,
                columns: [
                { title: "Nome" },
                { title: "Email" },
                { title: "Extras" },
                { title: "Check-in" },
                ],
                responsive: true,
                searching: false,
                lengthChange: false,
                destroy: true,
                paging: false
            } );
            console.log(data);
        }
    })
}


function check_hacker(id) {
    $.ajax(
    {
        url: check_in_hacker_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            if (data['res'] == true)
            {
                console.log("Dispatching Notifier")
                swal("Pronto!", "Check-In feito!", "success");
                notify_check_in(id);
                console.log("Notifier dispatched")
            }
            else
                swal("Pronto!", "Check-In desfeito!", "success");
        }
    })
}

function notify_check_in(id) {
    $.ajax(
    {
        url: notify_check_in_hacker_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            console.log("Email para " + id + " enviado!");
        },
        error: function(data) {
            console.log("ERRO ao enviar email para " + id + "!");
        }
    })
}

function sweet(name, id) {
    $.ajax(
    {
        url: get_hacker_check_in_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            if (data['data'] == true) {
                var text1 = "Já fez o check-in";
                var text2 = "Desfazer check-in";
            }
            else {
                var text1 = "Não fez o check-in";
                var text2 = "Fazer check-in";
            }
            swal(name, text1, "warning", {
                buttons: {
                    check: {
                        text: text2,
                    },
                    cancel: "Deixa pra lá!",
                },
            }).then((value) => {
                switch (value) {

                    case "check":
                    check_hacker(id);
                    break;
                }
            });
        }
    })
}


function search_late_hackers() {
    var text = $("#search_late_hackers").val();
    if (text.length == 0)
        return;
    $.ajax(
    {
        url: search_late_hackers_url,
        type: 'post',
        data: {
            data: text,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#example_late").empty();
            $('#example_late').DataTable( {
                data: data,
                columns: [
                { title: "Nome" },
                { title: "Email" },
                { title: "Liberar" },
                ],
                responsive: true,
                searching: false,
                lengthChange: false,
                destroy: true,
                paging: false
            } );
            console.log(data);
        }
    })
}


function give_second_chance(id) {
    $.ajax(
    {
        url: give_second_chance_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            if (data['res'] == true)
            {
                console.log("Dispatching Notifier")
                swal("Pronto!", "Hacker liberado!", "success");
                notify_late(id);
                console.log("Notifier dispatched")
            }
            else
                swal("Pronto!", "Hacker bloqueado!", "success");
        }
    })
}

function notify_late(id) {
    $.ajax(
    {
        url: notify_late_hacker_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            console.log("Email para " + id + " enviado!");
        },
        error: function(data) {
            console.log("ERRO ao enviar email para " + id + "!");
        }
    })
}


function sweet_late(name, id) {
    $.ajax(
    {
        url: get_hacker_second_chance_url,
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            if (data['data'] == true) {
                var text1 = "Já está liberado";
                var text2 = "Bloquear";
            }
            else {
                var text1 = "Não está liberado";
                var text2 = "Liberar";
            }
            swal(name, text1, "warning", {
                buttons: {
                    check: {
                        text: text2,
                    },
                    cancel: "Deixa pra lá!",
                },
            }).then((value) => {
                switch (value) {

                    case "check":
                    give_second_chance(id);
                    break;
                }
            });
        }
    })
}
