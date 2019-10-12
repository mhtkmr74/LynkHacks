from django.conf.urls import url
from . import views

urlpatterns = [
    url('volunteer/signup$', views.signup),
    url('supplier/login', views.login),
    url('supplier/[0-9]+/goods', views.insert_goods),
]
