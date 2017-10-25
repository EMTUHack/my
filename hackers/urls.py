from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^token/(?P<token>[\w]+)', views.login_from_token, name='login_from_token'),
    url(r'^token/', views.login_from_token, name='login_from_token2'),
    url(r'^change_token/', views.change_token, name='change_token'),
    url(r'^recover_token/', views.recover_token, name='recover_token'),
    url(r'^application/$', views.application, name='application'),
    url(r'^withdraw/$', views.toggle_withdraw, name='toggle_withdraw'),
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

    url(r'facebook/remove_facebook/$', views.remove_facebook, name='remove_facebook'),
    url(r'facebook/login/$', views.facebook_login, name='facebook_login'),
    url(r'facebook/login_response/$', views.facebook_login_response, name='facebook_login_response'),
    url(r'github/remove_facebook/$', views.remove_github, name='remove_github'),
    url(r'github/login/$', views.github_login, name='github_login'),
    url(r'github/login_response/$', views.github_login_response, name='github_login_response'),
]
