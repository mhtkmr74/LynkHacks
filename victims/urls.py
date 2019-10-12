from django.conf.urls import url
from . import views

urlpatterns = [
    url('/supplier/signup$', views.signup),
    url('/victim/login', views.login),
    # url('/victim/requirement/[0-9]+$', views.requirement_status)
]
