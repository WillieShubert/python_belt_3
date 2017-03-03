from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^process_quote$', views.process_quote),
    url(r'^user/(?P<id>\d+)$', views.user_details),
    url(r'^like/(?P<quote_id>\d+)$', views.like_quote),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    ]
