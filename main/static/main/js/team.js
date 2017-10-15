function create_team() {
    var text = $("#input_team_name").val();
    if (text.length == 0)
        return;
    $.ajax(
    {
        url: create_team_url,
        type: 'post',
        data: {
            team_name: text,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            switch_forms();
            $("#team_name").text(data['team']);
            for (mate in data['members'])
                $("#teammates_anchor").append("<p class='item'>" + data['members'][mate]['name'] + "</p>");
            $("#project").val(data['project']);
            $("#location").val(data['location']);
            if (data['new_blocked'] == true)
                $('#block_new').checkbox('attach events', '.check.button', 'check');
        },
        error: function(data) {
            console.log("error");
            $("#team_error").text(data['responseJSON']['error']);
            $("#team_error").show();
        }
    })
}

function leave_team() {
    $.ajax(
    {
        url: leave_team_url,
        type: 'post',
        data: {
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            switch_forms();
        },
        error: function(data) {
            if (data['status'] == 403)
            {
                $("#team_error").text("Fim do prazo de alteração das equipes!");
                $("#team_error").show();
            }
        }
    })
}

function allow_team() {
    $.ajax(
    {
        url: allow_team_url,
        type: 'post',
        data: {
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
        },
        error: function(data) {
            if (data['status'] == 403)
            {
                $("#team_error").text("Fim do prazo de alteração das equipes!");
                $("#team_error").show();
            }
        }
    })
}

function update_project() {
    var text = $("#project").val();
    $.ajax(
    {
        url: update_project_url,
        type: 'post',
        data: {
            project: text,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
        },
        error: function(data) {
            if (data['status'] == 403)
            {
                $("#team_error").text("Fim do prazo de alteração das equipes!");
                $("#team_error").show();
            }
        }
    })
}

function update_location() {
    var text = $("#location").val();
    $.ajax(
    {
        url: update_location_url,
        type: 'post',
        data: {
            location: text,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
        },
        error: function(data) {
            if (data['status'] == 403)
            {
                $("#team_error").text("Fim do prazo de alteração das equipes!");
                $("#team_error").show();
            }
        }
    })
}

jQuery.fn.swapWith = function(to) {
    return this.each(function() {
        var copy_to = $(to).clone(true);
        var copy_from = $(this).clone(true);
        $(to).replaceWith(copy_from);
        $(this).replaceWith(copy_to);
    });
};


function switch_forms() {
    // empty fields
    $("#teammates_anchor").empty();
    $("#input_team_name").val('');
    $("#project").val('');
    $("#location").val('');
    $("#team_name").empty();
    $("#team_error").empty();
    $("#team_error").hide();
    // Switch forms
    $("#anchor").swapWith("#substitute");
    // Toggle visibility
    $("#anchor").toggle();
    $("#substitute").toggle();
};


var typingTimer;                //timer identifier
var doneTypingInterval = 500;  //time in ms (2 seconds)

//on keyup, start the countdown
function on_project_up() {
    clearTimeout(typingTimer);
        typingTimer = setTimeout(update_project, doneTypingInterval);
}
function on_location_up() {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(update_location, doneTypingInterval);
}
