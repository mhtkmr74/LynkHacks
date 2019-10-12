from django.conf.urls import url
from . import views

urlpatterns = [
    url('/volunteer/signup$', views.signup),
    url('', views.login),
    url('volunteer/[0-9]+$/availability', views.update_volunteer)
]
