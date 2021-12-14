from django.conf.urls import  include, url 
from AppsAdmin.models import *

from AppsAdmin.views import *

urlpatterns = [
     url(r'^$', user_home, name='user_home_root'),
     url(r'^userhome/$', user_home, {'template_name': 'userprofile.html'}, name='user_home'),

]
