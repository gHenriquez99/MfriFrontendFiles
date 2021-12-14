from django.conf.urls import  include, url #20180904 patterns,
from django.views.generic import RedirectView 
from django.views.generic import TemplateView, ListView, FormView, CreateView, DeleteView, UpdateView

from SRegistration.models import *
from SRegistration.views import *

urlpatterns = [
    url(r'^copy/from/(?P<from_log_number>[-\w]+)$', CopyStudentRegistrationsStart, {'template_name': 'schedule/student_registration/copy_registrations_form.html'},name='copy_student_registrations_start'),




]
