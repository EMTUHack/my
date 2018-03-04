"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout

from main import views
from hackers import views as h_views

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
handler403 = 'main.views.handler500'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('hackers.urls', namespace='hackers')),
    url(r'^', include('main.urls', namespace='main')),
    url(r'^', include('staff.urls', namespace='staff')),
    url(r'^', include('schedule.urls', namespace='schedule')),
    url(r'^$', views.index, name='index'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^team$', views.team, name='team'),
    url(r'^godmode/$', views.admin, name='admin'),
    url(r'^godmode/hackers$', views.manage_hackers, name='manage_hackers'),
    url(r'^godmode/stats$', views.stats, name='stats'),
    url(r'^godmode/checkin$', views.checkin, name='checkin'),
    url(r'^godmode/export/basic$', views.export_basic_info, name='export_basic_info'),
    url(r'^godmode/export/basic_confirmed$', views.export_basic_info_confirmed, name='export_basic_info_confirmed'),
    url(r'^godmode/export/basic_unconfirmed$', views.export_basic_info_unconfirmed, name='export_basic_info_unconfirmed'),
    url(r'^godmode/export/advanced$', views.export_advanced_info, name='export_advanced_info'),
    url(r'^godmode/export/advanced_checkedin$', views.export_advanced_checkedin_info, name='export_advanced_checkedin_info'),
    url(r'^godmode/export/teams$', views.export_teams, name='export_teams'),
    url(r'^godmode/export/teams_after$', views.export_teams_after, name='export_teams_after'),
    url(r'^godmode/export/staff$', views.export_staff, name='export_staff'),
    url(r'^godmode/export/events$', views.export_events, name='export_events'),
    url(r'^godmode/error$', views.test_error, name='test_error'),

    url(r'^godmode/batch_confirm$', h_views.batch_confirm_hackers, name='batch_confirm'),
]
