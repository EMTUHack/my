var stat = false;
function toggle_sidebar() {
    if (stat == false)
    {
        $('#stat_x').removeClass('hide-X ng-hide');
        $("#stat_icon").addClass('hide-X ng-hide');
        $("#sidebar").addClass("open");
    }
    else
    {
        $('#stat_x').addClass('hide-X ng-hide');
        $("#stat_icon").removeClass('hide-X ng-hide');
        $("#sidebar").removeClass("open");
    }
    stat = !stat;
}
