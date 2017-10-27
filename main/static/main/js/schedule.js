console.log("test");
function toggle_attendance(id) {
        $.ajax(
        {
            url: toggle_attendance_url,
            type: 'post',
            data: {
                id: id,
                csrfmiddlewaretoken: csrf
            },
            success: function(data) {

                if (data['resp'] == true) {
                    $("#att_" + id).removeClass("green");
                    $("#att_" + id).addClass("red");
                    $("#att_" + id).html('<i class="remove icon"></i> Desistir');
                }
                else {
                    $("#att_" + id).removeClass("red");
                    $("#att_" + id).addClass("green");
                    $("#att_" + id).html('<i class="check icon"></i> Se inscrever');
                }
            },
            error: function(data) {
                console.log("error");
                console.log(data);
            }
        })
    }


    function submit_feedback() {
        var star = $("#star_" + v_id).rating('get rating');
        var feedback = $("#feedback_" + v_id).val();
        $.ajax(
        {
            url: submit_feedback_url,
            type: 'post',
            data: {
                id: v_id,
                rating: star,
                feedback: feedback,
                csrfmiddlewaretoken: csrf
            },
            success: function(data) {

            },
            error: function(data) {
                console.log("error");
                console.log(data);
            }
        })
    }

    $('.rating').rating({
        maxRating: 5,
        clearable: true,
    });

    $('.rating').rating('setting', 'onRate', function(data) {
        proc_feedback($(this).data('id'));
    });

    var v_id;

    function proc_feedback(id) {
        v_id = id;
        on_feedback_up();
    }

var typingTimer;                //timer identifier
var doneTypingInterval = 500;  //time in ms (2 seconds)

//on keyup, start the countdown
function on_feedback_up() {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(submit_feedback, doneTypingInterval);
}
