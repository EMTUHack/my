from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^application/$', views.application, name='application'),
    url(r'^withdraw/$', views.toggle_withdraw, name='toggle_withdraw'),
    url(r'^confirm_presence/$', views.confirm_presence, name='confirm_presence'),
    url(r'^notify_checkin/$', views.notify_check_in_hacker, name='notify_check_in_hacker'),

    url(r'^api/enter_team', views.enter_team, name='api_enter_team'),
    url(r'^api/leave_team', views.leave_team, name='api_leave_team'),
    url(r'^api/update_project', views.update_project, name='api_update_project'),
    url(r'^api/update_location', views.update_location, name='api_update_location'),
    url(r'^api/update_github_url', views.update_github_url, name='api_update_github_url'),
    url(r'^api/update_allow_new', views.update_allow_new_members, name='api_update_allow_new'),

    url(r'^api/import_hackers/$', views.import_hackers, name='batch_import_hackers'),
    url(r'^api/search_hackers/$', views.search_hacker, name='search_hackers'),
    url(r'^api/check_in_hacker/$', views.check_in_hacker, name='check_in_hacker'),
    url(r'^api/get_hacker_check_in/$', views.get_hacker_check_in, name='get_hacker_check_in'),
    url(r'^api/resend_email/$', views.check_in_hacker, name='check_in_hacker'),
]
