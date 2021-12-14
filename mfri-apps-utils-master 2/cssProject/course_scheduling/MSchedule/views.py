import os
import codecs
import string
import json
import time
import datetime
from decimal import *
import base64

import sys, traceback

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.conf import settings
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render 

from AppBase.views import JSDatePicker

from MLocations.utils import GetLocationFromPK, GetLocationsforCounty 

from MCourses.utils import GetCurrentCourses, GetCourseDescriptionFromCategoryAndLevel

from MSchedule.models import *
from MSchedule.forms import ScheduledCourseEditForm, ScheduledCourseEditTabForm, ScheduledCourseEditTabTemplate, ConfirmScheduleExportForm 
from MSchedule.utils import legacy_app_permission, ScheduledCourseRecord, UnpackCourseListContext, FormatCourseDetailsForInstructorZone, GetCourseListForInstructor, FormatCourseDetailsForCourseRegistration, GetScheduledCourseStatus, GetActiveScheduledCourses, GetPublicScheduleFromName, GetPublicScheduledCourses, BuildCourseListJSON, BuildCourseDescriptionJSON, BuildScheduledCourseJSON, BuildLocationJSON, BuildLocationListJSON, ScheduledCourseFlier, GetCourseDescriptionsForPublicSchedule 
from MSchedule.utils_legacy_urls import CourseEditUrl

from MTrainingPortal.utils import GetOfficeFromAbbreviation, GetJurisdictionFromID 

from MSchedule.utils_tabs import ScheduleEditListTabs, FieldsForTab, CurrentScheduleEditTab


@login_required 
def EditRegistrationRules(request, log_number=None, template_name=None):
    scheduled_course = None
    update_message = u''
    user_read_permission = legacy_app_permission(user=request.user)

    if not user_read_permission:
        raise Http404
        
    
    if log_number:
        if not request.user.has_perm('MSchedule.change_scheduledcourses'):
            raise Http404
        scheduled_course = ScheduledCourseRecord(log_number=log_number)
    else:
        raise Http404

    if not scheduled_course:
        raise Http404

    parent_form_url = CourseEditUrl(scheduled_course=scheduled_course)


    if request.method == u'POST': 
        if request.POST['FormButton'] == 'Cancel':
            return HttpResponseRedirect(parent_form_url)
        
        form = ScheduledCourseEditForm(request.POST, request.FILES, instance=scheduled_course) 

        if form.is_valid():
            form.instance.user = request.user
            
            try:
                if scheduled_course.legacy_link == 0:
                    scheduled_course.legacy_link = None
            except:
                scheduled_course.legacy_link = None

            form.save()
            
            if scheduled_course.require_training_officer_approval:
                if not scheduled_course.use_web_registration:
                    scheduled_course.use_web_registration = True
                    scheduled_course.save(update_fields=['use_web_registration'])
            
            update_message = u'Rules Updated'
    else: 
        form = ScheduledCourseEditForm(instance=scheduled_course)
        
    return render(request=request, template_name=template_name, context={'form': form, 
                                         'update_message': update_message,
                                         'scheduled_course': scheduled_course, 
                                         })

@login_required 
def ViewRegistrationRules(request, log_number=None, template_name=None):
    
    scheduled_course = None

    user_read_permission = legacy_app_permission(user=request.user)
    
    if not user_read_permission:
        raise Http404
    
    if log_number:
        scheduled_course = ScheduledCourseRecord(log_number=log_number)
    else:
        raise Http404

    if not scheduled_course:
        raise Http404

    return render(request=request, template_name=template_name, context={
                                          'scheduled_course': scheduled_course, 
                                         })



def GetCourseList(request, instructor_uid=None, context=None):# mfri_office_abbreviation=None, 

    mimetype = 'application/json'
    
    if instructor_uid:
        context_decoded = {'instructor_uid':instructor_uid}
        context_decoded_json = json.dumps(context_decoded)
        context = base64.urlsafe_b64encode(context_decoded_json).strip('=')

    course_list_context = UnpackCourseListContext(context=context)

    if course_list_context['ResponseCode'] < 1:
        return HttpResponse(json.dumps( {  'StatusMessage': course_list_context['StatusMessage'],
                                           'ResponseCode': course_list_context['ResponseCode'],
                                        },mimetype))


    
    get_course_list_result = GetCourseListForInstructor(
                                                        lead_instructor = course_list_context.get('instructor', None),
                                                        schedule_view_window_days = course_list_context.get('window_days_length', 30),
                                                        fiscal_year = course_list_context.get('fiscal_year', None),
                                                       )

    return HttpResponse(json.dumps(get_course_list_result),mimetype)

def ReturnPDF404(request, error_message=u'File Not Found.'): #20200520
    PDF404Template = get_template('transcript/pdf404.html')

    PDF404Context = {'error_message': u'file not found.'}

    PDF404Html = PDF404Template.render(PDF404Context)

    return HttpResponse(PDF404Html)

def ReturnScheduledCourseFlier(request, category=None, level=None, funding_source_code=None, section_number=None, fiscal_year=None, return_file=False, template_name=None):
    
    scheduled_course = ScheduledCourseRecord(category=category, level=level, funding_source_code=funding_source_code, section_number=section_number, fiscal_year=fiscal_year)

    if not scheduled_course:
        return ReturnPDF404(request)

    scheduled_course_flier = None
    file_label = None
    file_url = None
    file_type = None

    scheduled_course_attachment = ScheduledCourseFlier(scheduled_course=scheduled_course)
    
    scheduled_course_flier = scheduled_course_attachment.get('scheduled_course_flier', None)
    file_label = scheduled_course_attachment.get('file_label', None)
    file_url = scheduled_course_attachment.get('file_url', None)
    file_type = scheduled_course_attachment.get('file_type', None)

    if not scheduled_course_flier:
        return ReturnPDF404(request)

    if len(file_url) == 0:
        return ReturnPDF404(request)

    file_name_parts = file_url.split('/')

    file_name = file_name_parts[-1]

    file_socket = open(u'/export/software/web/html/%s' % (file_url), 'rb')

    response = HttpResponse(content=file_socket)
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = u'attachment; filename=%s' % (file_name)

    return response
