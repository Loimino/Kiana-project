from django.urls import  path
from django.urls import re_path

from . import views
urlpatterns=[
    re_path(r'^login_page', views.login_page, name='login_page')  #
, re_path(r'^login_check', views.login_check, name='login_check')
, re_path(r'^supervise_home', views.supervise_home, name='supervise_home')
, re_path(r'^show_machine_detail', views.show_machine_detail, name='show_machine_detail')
, re_path(r'^show_employees_nearby', views.show_employees_nearby, name='show_employees_nearby')
, re_path(r'^show_machine_history', views.show_machine_history, name='show_machine_history')
, re_path(r'^maintenance_home', views.maintenance_home, name='maintenance_home')
, re_path(r'^return_first', views.return_first, name='return_first')
]


