from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/import_staff/$', views.import_staff, name='batch_import_staff'),
]
