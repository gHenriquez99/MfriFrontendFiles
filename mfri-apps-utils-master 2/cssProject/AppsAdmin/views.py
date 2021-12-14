import os
import codecs
import string
import json
#20180918+
import inspect
import re
import warnings
#20180918-


from django.db import connections


#from os import environ
from socket import gethostname
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group, Permission
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators import csrf 
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_list_or_404, render 
from django.core.mail import send_mail



from MFRI_Utils.js_functions_for_templates import JSOnClickEvent 
from AppBase.utils_exception import ExceptionRedirect 

from AppsAdmin.models import *
from AppsAdmin.forms import *

from MOffices.models import MfriOffices
from MSchedule.models import Scheduledcourses

from django.contrib.auth.models import User
                               


def UserAppsList():

    AppsList = []

    AppsList.append({'Name': u'Course Schedule Maintenance', 'Link': None})
    AppsList.append({'Name': u'Student Records Maintenance', 'Link': None})

    return AppsList


from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare
from django.utils.deprecation import RemovedInDjango21Warning
from django.utils.module_loading import import_string
from django.utils.translation import LANGUAGE_SESSION_KEY


SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'

@login_required
@csrf_protect
def user_home(request=None, template_name=None):

    RequestedCount = 0
    ApprovedCount = 0
    ReviewCount = 0

    if request.GET.has_key('FormButton'):
        form = UserHomeForm(request.GET)
        
        if form.is_valid():
            searchform = form.cleaned_data
            
            search_button_value = request.GET['FormButton']
            search_field_value = searchform['InputSearchField']
            
            CourseSearchButtons = ['Search Courses', 'Edit Course', 'PreRegistration', 'Registration', 'MESSA', 'Transcript', 'Online Registrations Received'] #20210426
            PersonSearchButtons = ['Student', 'Student Transcript', 'Instructor / Staff']
            
            if search_button_value in CourseSearchButtons:
                if search_button_value == "Search Courses":
                    return HttpResponseRedirect('/cgi-bin/coursesearch.cgi?HPS=1&LogNumberToFind=' + search_field_value + '&FormButton=Search')
                elif search_button_value == "Online Registrations Received":
                    try:
                        return HttpResponseRedirect(reverse('onlinereg_approved_reg_fs', kwargs={ 'log_number': search_field_value }))
                    except:
                        return ExceptionRedirect(log_number=None, office_code=None,
                                    exception_label=u'Search Error',
                                    exception_message=u'E901 Invalid Log Number.')
                else:
                    return HttpResponseRedirect('/cgi-bin/find_course.cgi?LogNumberToFind=' + search_field_value + '&FormButton=' + search_button_value )
            else:
                if search_button_value in PersonSearchButtons:
                    if search_button_value == 'Student Transcript':
                        return HttpResponseRedirect('/cgi-bin/find_person.cgi?NameToFind=' + search_field_value + '&FormButton=Transcript' )
                    else:
                        return HttpResponseRedirect('/cgi-bin/find_person.cgi?NameToFind=' + search_field_value + '&FormButton=' + search_button_value )
                else:
                    return HttpResponseRedirect(reverse('user_home'))
    else:
        HostName = gethostname()
        
        try:
            profile = UserProfile.objects.get(user=request.user)
            

        except UserProfile.DoesNotExist:
            logout(request)
            return HttpResponseRedirect('/accounts/invalid/')

        try:
            LegacyUserDetails = profile.LegacyUserData
        except:#user account not connected to legacy profile, so log user out and redirect to page that will report the error to the user.
            logout(request)
            return HttpResponseRedirect('/accounts/invalid/')

        if not profile.LegacyUserData:
            logout(request)
            return HttpResponseRedirect('/accounts/invalid/')
            
        
        form = UserHomeForm(initial={'InputSearchField': ''})
        
        schedule_permissions = None
        
        try:
            schedule_permissions = Schedpreferences.objects.get(userid__exact=LegacyUserDetails.id)
        except:
            permission_funding_approver = False
            permission_schedule_approver = False
            
        if schedule_permissions:
            permission_funding_approver = schedule_permissions.fundingapprover
            permission_schedule_approver = schedule_permissions.scheduleapprover
        else:
            permission_funding_approver = False
            permission_schedule_approver = False

        permission_read_student_registration = None
        permission_read_instructor_list = None
        permission_read_transcript = None
        permission_read_course_registration = None
        permission_edit_course_registration = None
        permission_read_scheduled_course = None
        permission_edit_scheduled_course = None
        
        try:                  
            permission_read_student_registration = LegacyPermissions.objects.Permission_Student_Registration(user_id=LegacyUserDetails.id).readpermission
        except:
            permission_read_student_registration = None
            
        try:                  
            permission_read_instructor_list = LegacyPermissions.objects.Permission_Instructor_List(user_id=LegacyUserDetails.id).readpermission
        except:
            permission_read_instructor_list = None
            
        try:                  
            permission_read_transcript = LegacyPermissions.objects.Permission_Transcript(user_id=LegacyUserDetails.id).readpermission
            permission_read_transcript = True
        except:
            permission_read_transcript = None

        try:                  
            permission_read_course_registration = LegacyPermissions.objects.Permission_Course_Registration(user_id=LegacyUserDetails.id).readpermission
        except:
            permission_read_course_registration = None
            
        try:                  
            permission_edit_course_registration = LegacyPermissions.objects.Permission_Course_Registration(user_id=LegacyUserDetails.id).modifypermission
        except:
            permission_edit_course_registration = None
            
        try:                  
            permission_read_scheduled_course = LegacyPermissions.objects.Permission_Scheduled_Course(user_id=LegacyUserDetails.id).readpermission
        except:
            permission_read_scheduled_course = None

        try:                  
            permission_edit_scheduled_course = LegacyPermissions.objects.Permission_Scheduled_Course(user_id=LegacyUserDetails.id).modifypermission
        except:
            permission_edit_scheduled_course = None

        if 2 == profile.WorkingOffice.id: #SPS
            MFRIOffices = [profile.WorkingOffice,]

            RequestedCount = Scheduledcourses.objects.requested_courses(MfriOffices=MFRIOffices).count()
            ApprovedCount = Scheduledcourses.objects.approved_courses(MfriOffices=MFRIOffices).count()

            form.RequestedCount = RequestedCount # + ApprovedCount
            form.ApprovedCount = ApprovedCount
        else:
            if 3 == profile.WorkingOffice.id: #FPS
                MFRIOffices = [3, 5, 6, 7, 8, 9, 10, 11, 18, 19]#20200721
                RequestedCount = Scheduledcourses.objects.requested_courses(MfriOffices=MFRIOffices).count()
                
                ApprovedCount = Scheduledcourses.objects.approved_courses(MfriOffices=MFRIOffices).count() #test

                form.RequestedCount = RequestedCount
                form.ApprovedCount = ApprovedCount
            elif 15 == profile.WorkingOffice.id: #IDS
                MFRIOffices = [15]
                RequestedCount = Scheduledcourses.objects.requested_courses(MfriOffices=MFRIOffices).count()
                
                ApprovedCount = Scheduledcourses.objects.approved_courses(MfriOffices=MFRIOffices).count() #test
                
                form.RequestedCount = RequestedCount
                form.ApprovedCount = ApprovedCount
            
            else:

                MFRIOffices = [profile.WorkingOffice,]
            
                if permission_funding_approver or permission_schedule_approver:
                    RequestedCount = Scheduledcourses.objects.requested_courses(MfriOffices=MFRIOffices, legacy_section=LegacyUserDetails.legacy_section, legacy_region=LegacyUserDetails.legacy_region).count()

                    ApprovedCount = Scheduledcourses.objects.approved_courses(MfriOffices=MFRIOffices).count() #test


                    form.RequestedCount = RequestedCount
                    form.ApprovedCount = ApprovedCount
                else:
                    form.RequestedCount = 0
                    form.ApprovedCount = 0
                    

        ApplicationsList = UserAppsList()
        
        form.label_suffix = ' '
        
        profile.ServerName = request.get_host() #HostName #Site.objects.get_current().domain

        request.session['max_age'] = 3600
           
        request.session['userid'] = 'qqq' + str(LegacyUserDetails.id) + 'qqq'#UserDetails.id
        request.session['username'] = 'qqq' + LegacyUserDetails.username + 'qqq' #UserDetails.username

        user_permissions = {'funding_approver': permission_funding_approver, 
                            'schedule_approver': permission_schedule_approver, 
                            'read_student_registration': permission_read_student_registration,
                            'read_instructor_list': permission_read_instructor_list,
                            'read_transcript': permission_read_transcript,
                            'read_course_registration': permission_read_course_registration,
                            'edit_course_registration': permission_edit_course_registration,
                            'read_scheduled_course': permission_read_scheduled_course,
                            'edit_scheduled_course': permission_edit_scheduled_course,
                            }

        UserHomeTemplate = get_template('userhome.html')

        server_name_port = request.get_host()
        protocol = u'https://'
        if u':' in server_name_port:
            server_name, port = server_name_port.split(u':')
            protocol = u'http://'
        else:
            server_name = server_name_port
            port = u''

        UserHomeContext = {'form': form, 
                           'current_user': profile, 
                           'protocol' : protocol, 
                           'server_name' : server_name, 
                           'port' : port, 
                           'AppsMenu': ApplicationsList, 
                           'user_permissions': user_permissions
                           }
        UserHomeHtml = UserHomeTemplate.render(request=request, context=UserHomeContext)
        
        ResponseWithExtraCookie = HttpResponse(UserHomeHtml)
        
        CookieValue = 'userid:' + str(LegacyUserDetails.id) + ',username:' + LegacyUserDetails.username + ',realname:' + LegacyUserDetails.fullname.replace(' ', '=')
        
        ResponseWithExtraCookie.set_cookie('CGISESSID', value=codecs.encode(CookieValue, 'rot13'))
        
        return ResponseWithExtraCookie
    

