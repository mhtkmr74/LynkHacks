from django.conf.urls import url
from . import views

urlpatterns = [
    url('/victim/signup$', views.signup),
]
