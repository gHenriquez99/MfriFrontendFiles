from django.conf.urls import  include, url 

from AppsAdmin.models import *

from SRec.models import *
from SRec.forms import *
from SRec.views import *

urlpatterns = [
    url(r'^new$', StudentDataEdit, {'template_name': 'srec/srec_student_edit.html'}, name='srec_new_student_data_pk'),

    url(r'^edit/(?P<pk>\d+)$', StudentDataEdit, {'template_name': 'srec/srec_student_edit.html'}, name='srec_edit_student_data_pk'),
    url(r'^edit/(?P<context_encoded>[-\w]+)$', StudentDataEdit, {'template_name': 'srec/srec_student_edit.html'}, name='srec_edit_student_data_context'),

    url(r'^edit/name/(?P<pk>\d+)$', StudentNameEdit, {'template_name': 'srec/srec_name_edit.html'}, name='srec_edit_student_name_pk'),
    url(r'^edit/msn/(?P<pk>\d+)$', StudentNumberEdit, {'template_name': 'srec/srec_msn_edit.html'}, name='srec_edit_student_number_pk'),

    url(r'^edit/msn/new/(?P<pk>\d+)$', StudentNumberInitConfirm, { 'template_name': 'srec/srec_msn_init_confirm.html'}, name='srec_init_confirm_student_number_pk'),
    url(r'^edit/msn/new/done/(?P<pk>\d+)$', StudentNumberInitConfirmDone, { 'template_name': 'srec/srec_msn_init_confirm_done.html'}, name='srec_init_confirm_done_student_number_pk'),

    ]




