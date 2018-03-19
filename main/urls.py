from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^token/(?P<token>[\w]+)', views.login_from_token, name='login_from_token'),
    url(r'^token/', views.login_from_token, name='login_from_token2'),
    url(r'^change_token/', views.change_token, name='change_token'),
    url(r'^recover_token/', views.recover_token, name='recover_token'),
    url(r'^verify_email/(?P<code>[\w]+)', views.check_verify_email, name='verify_email'),
    url(r'^resend_verify_email', views.send_verify_email, name='send_verify_email'),

    url(r'facebook/remove_facebook/$', views.remove_facebook, name='remove_facebook'),
    url(r'facebook/login/$', views.facebook_login, name='facebook_login'),
    url(r'facebook/login_response/$', views.facebook_login_response, name='facebook_login_response'),
    url(r'github/remove_github/$', views.remove_github, name='remove_github'),
    url(r'github/login/$', views.github_login, name='github_login'),
    url(r'github/login_response/$', views.github_login_response, name='github_login_response'),

    url(r'api/get_hacker_application/$', views.get_hacker_application, name='get_hacker_application'),
    url(r'api/change_registration_open/$', views.change_registration_open, name='registration_open'),
    url(r'api/change_registration_close/$', views.change_registration_close, name='registration_close'),
    url(r'api/change_confirmation/$', views.change_confirmation, name='confirm_by'),
    url(r'api/change_hackathon_start/$', views.change_hackathon_start, name='hackathon_start'),
    url(r'api/change_hackathon_end/$', views.change_hackathon_end, name='hackathon_end'),
    url(r'api/change_max_hackers/$', views.change_max_hackers, name='max_hackers'),
    url(r'api/admit_hacker/$', views.admit_hacker, name='admit_hacker'),
    url(r'api/nag_hacker/$', views.nag_hacker, name='nag_hacker'),
    url(r'api/decline_hacker/$', views.decline_hacker, name='decline_hacker'),
    url(r'api/unwaitlist_hacker/$', views.unwaitlist_hacker, name='unwaitlist_hacker'),
    url(r'api/fetch_submitted_hackers/$', views.fetch_submitted_hackers, name='fetch_submitted_hackers'),
    url(r'api/fetch_admitted_hackers/$', views.fetch_admitted_hackers, name='fetch_admitted_hackers'),
    url(r'api/fetch_declined_hackers/$', views.fetch_declined_hackers, name='fetch_declined_hackers'),
    url(r'api/fetch_waitlist_hackers/$', views.fetch_waitlist_hackers, name='fetch_waitlist_hackers'),
    url(r'api/fetch_checkedin_hackers/$', views.fetch_checkedin_hackers, name='fetch_checkedin_hackers'),
    url(r'^api/manual_cycle_waitlist', views.manual_cycle_waitlist, name='manual_cycle_waitlist'),
]
