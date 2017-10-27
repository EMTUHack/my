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
