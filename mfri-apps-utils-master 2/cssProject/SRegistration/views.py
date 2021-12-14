import os
import codecs
import string
import json
import time
import datetime
import base64

from socket import gethostname
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.template.defaultfilters import slugify
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404 

from django import forms

from AppBase.views import EditItem, DeleteItem
from AppsAdmin.models import *


from MFRI_Utils.data_validate import ValidateTableIndex

from MFRI_Utils.data_encode import decode_context, encode_context


from MSchedule.utils_search import ScheduledCourseRecord, GetConfirmedCourses

from SRec.models import *
from SRec.views import StudentRecordCGIURL

from MSchedule.models import *
from MSchedule.utils_legacy_urls import CourseEditUrl

from MStaff.utils import GetStaffRecord, find_staff_by_uid

from SRegistration.models import *
from SRegistration.forms import CopyRegisteredStudentsForm, ConfirmCopyRegisteredStudentsForm 
from SRegistration.utils import CreateNewStudentRegistrationFromRegistration, CreateNewStudentPreRegistrationFromRegistration, GetToScheduledCourse, CheckForDuplicateStudentRegistrations 
from SRegistration.utils_permissions import get_registration_read_permission, get_registration_write_permission, get_registration_grade_read_permission, get_registration_grade_write_permission

from SRegistration.utils_reports import CountStudentsForAffiliation
from SRegistration.utils_reports_pdf import report_error_pdf, create_resource_assignment_report_pdf

@login_required
def CopyStudentRegistrationsStart(request, from_log_number=None, template_name=None):

    from_scheduled_course = ScheduledCourseRecord(log_number=from_log_number)

    if not from_scheduled_course:
        raise Http404

    registered_students_1 = []


    init_form = True

    if request.method == u'POST': 
        init_form = False

        if request.POST['FormButton'] == 'Cancel': 
            return HttpResponseRedirect('/cgi-bin/stureg_reg.cgi?SCID=%d' % (from_scheduled_course.id))
        
        form = CopyRegisteredStudentsForm(request.POST) #, instance=from_scheduled_course) 

        if form.is_valid():
            #warn(u'form is valid\n')
            copy_registration_form_data = form.cleaned_data

            if request.POST['FormButton'] == 'Copy': 

                to_log_number = copy_registration_form_data.get('to_log_number', None)
                to_table = copy_registration_form_data.get('to_table', None)
                
                student_registrations_to_copy = copy_registration_form_data.get('student_registrations_to_copy', None)

                to_scheduled_course = GetToScheduledCourse(log_number=to_log_number)

                if not to_scheduled_course:
                    form.errors['to_log_number'] = u'Error finding to course record.'
                

                registration_copy_result_list = []
                

                student_registration_ids_to_copy = (",".join(student_registrations_to_copy))

                registered_students_selected = []
                for student_registration_id in student_registrations_to_copy:
                    
                    try:
                        selected_student = Studentregistration.objects.get(pk=student_registration_id)
                    except Studentregistration.DoesNotExist:
                        selected_student = None
                        
                    if selected_student:
                        registered_students_selected.append(selected_student)
                
                if to_table == u'Studentregistration':
                    try:
                        to_class_registered_students = Studentregistration.objects.filter(scheduled_course=to_scheduled_course).order_by('student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
                    except Studentregistration.DoesNotExist:
                        to_class_registered_students = []
                else:
                    try:
                        to_class_registered_students = Preregistrations.objects.filter(scheduled_course=to_scheduled_course).order_by('student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
                    except Studentregistration.DoesNotExist:
                        to_class_registered_students = []
                
                duplicate_registration_flag_list = CheckForDuplicateStudentRegistrations(from_course_registrations=registered_students_selected, to_course_registrations=to_class_registered_students)
                
                confirm_form = ConfirmCopyRegisteredStudentsForm(from_log_number=from_scheduled_course.log_number, to_log_number=to_scheduled_course.log_number, to_table=to_table, student_registration_ids_to_copy=student_registration_ids_to_copy)
                
                return render(request=request, template_name=u'schedule/student_registration/copy_registrations_form_confirm.html', context={ 'form': confirm_form, 
                                                         'from_scheduled_course': from_scheduled_course, 
                                                         'to_scheduled_course': to_scheduled_course,
                                                         'from_class_registered_students': registered_students_selected,
                                                         'to_class_registered_students': to_class_registered_students,
                                                         'duplicate_from_list': duplicate_registration_flag_list.get('from_duplicate_registration_flag', None),
                                                         'duplicate_to_list': duplicate_registration_flag_list.get('to_duplicate_registration_flag', None),
                                                        })

            elif request.POST['FormButton'] == 'Confirm':

                
                from_log_number = from_scheduled_course.log_number 
                to_log_number = copy_registration_form_data.get('to_log_number', None)
                to_table = copy_registration_form_data.get('to_table', None)
                student_registrations_to_copy = copy_registration_form_data.get('student_registration_ids_to_copy', None)

                form_errors = []
                student_registrations_to_copy_list = []

                if student_registrations_to_copy:
                    student_registrations_to_copy_list = student_registrations_to_copy.split(',')

                to_scheduled_course = GetToScheduledCourse(log_number=to_log_number)

                if not to_scheduled_course:
                    form_errors.append(u'Error finding course coping to record.')
                
                registration_copy_result_list = []

                if to_table == u'Studentregistration':
                    for from_student_registration in student_registrations_to_copy_list:
                        registration_copy_result_list.append( CreateNewStudentRegistrationFromRegistration(user=request.user, old_student_registration_id=from_student_registration, to_scheduled_course=to_scheduled_course, update_registered_count=False) )
                else:
                    for from_student_registration in student_registrations_to_copy_list:
                        registration_copy_result_list.append( CreateNewStudentPreRegistrationFromRegistration(user=request.user, old_student_registration_id=from_student_registration, to_scheduled_course=to_scheduled_course) )
                    
                try:
                    to_scheduled_course.registered_count += len(student_registrations_to_copy_list)
                    to_scheduled_course.save()
                except:
                    form_errors.append(u'Error updating to registered student count for course.')
                

                return render(request=request, template_name=u'schedule/student_registration/copy_registrations_form_results.html', context={
                                                         'from_scheduled_course': from_scheduled_course, 
                                                         'to_scheduled_course': to_scheduled_course,
                                                         'to_table': to_table,
                                                         'form_copy_results': form_errors,
                                                         'registration_copy_results': registration_copy_result_list,
                                                        })
            

    else: #if request.method != u'POST':# or not registered_students_1: 
        try:
            registered_students_1 = Studentregistration.objects.filter(scheduled_course__exact=from_scheduled_course).order_by('student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
        except Studentregistration.DoesNotExist:
            registered_students_1 = []

        form = CopyRegisteredStudentsForm(init_form=init_form, from_scheduled_course=from_scheduled_course, student_registrations_to_copy=registered_students_1) #, copy_step=u'Initial'

        
    return render(request=request, template_name=template_name, context={'form': form, 
                                         'from_scheduled_course': from_scheduled_course, 
                                        })





