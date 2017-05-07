from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^add/plan$', views.add),
    url(r'^add_new$', views.add_plans),
    url(r'^logout$', views.logout),
    url(r'^info/(?P<id>\d+)$', views.show_info),
    url(r'^join$', views.join)
]
