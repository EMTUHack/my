from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^token/(?P<token>[\w]+)', views.login_from_token, name='login_from_token'),
    url(r'^token/', views.login_from_token, name='login_from_token2'),
    url(r'^change_token/', views.change_token, name='change_token'),
    url(r'^recover_token/', views.recover_token, name='recover_token'),

    url(r'facebook/remove_facebook/$', views.remove_facebook, name='remove_facebook'),
    url(r'facebook/login/$', views.facebook_login, name='facebook_login'),
    url(r'facebook/login_response/$', views.facebook_login_response, name='facebook_login_response'),
    url(r'github/remove_facebook/$', views.remove_github, name='remove_github'),
    url(r'github/login/$', views.github_login, name='github_login'),
    url(r'github/login_response/$', views.github_login_response, name='github_login_response'),
]
