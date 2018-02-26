from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="/main")),
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^travels/destination/(?P<number>\d+)$', views.destination),
    url(r'^travels/add$', views.add),
    url(r'^logout$', views.logout),
    url(r'^new$', views.new),
    url(r'^join/(?P<id>\d+)$', views.join)
]