from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^schedule/', views.schedule, name='schedule'),
    url(r'^submit_feedback/', views.submit_feedback, name='submit_feedback'),
    url(r'^toggle_attendance/', views.toggle_attendance, name='toggle_attendance'),
]
