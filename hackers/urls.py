from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^application/$', views.application, name='application'),
    url(r'^withdraw/$', views.toggle_withdraw, name='toggle_withdraw'),
    url(r'^notify_checkin/$', views.notify_check_in_hacker, name='notify_check_in_hacker'),
    url(r'^notify_late/$', views.notify_late_hacker, name='notify_late_hacker'),

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
    url(r'^api/search_late_hackers/$', views.search_late_hacker, name='search_late_hackers'),
    url(r'^api/give_second_chance/$', views.give_second_chance, name='give_second_chance'),
    url(r'^api/get_hacker_second_chance/$', views.get_hacker_second_chance, name='get_hacker_second_chance'),
]
