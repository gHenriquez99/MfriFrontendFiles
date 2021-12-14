from django.conf.urls import  include, url 
from django.views.generic import TemplateView, ListView, FormView, CreateView, DeleteView, UpdateView

from django.contrib.auth.decorators import login_required

from django.views.generic import RedirectView 
from AppsAdmin.models import *

from MSchedule.models import *
from MSchedule.views import EditRegistrationRules

urlpatterns = [
    url(r'^registration/rules/edit/(?P<log_number>\w{2,4}\-\d{3}\-\w{0,1}\d{2,3}\-\d{2,4})$', EditRegistrationRules, {'template_name': 'mschedule/msched_reg_rules_edit.html'}, name='msched_reg_rules_edit'),
]


