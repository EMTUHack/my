from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^schedule/', views.schedule, name='schedule'),
    url(r'^submit_feedback/', views.submit_feedback, name='submit_feedback'),
    url(r'^toggle_attendance/', views.toggle_attendance, name='toggle_attendance'),

    url(r'^api/fetch_schedule_simple/', views.fetch_schedule_simple, name='fetch_schedule_simple'),
    url(r'^api/fetch_schedule_full/', views.fetch_schedule_full, name='fetch_schedule_full'),
    url(r'^api/create_or_edit_event/', views.create_or_edit_event, name='create_or_edit_event'),
    url(r'^api/delete_event/', views.delete_event, name='delete_event'),

]
