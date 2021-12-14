
import re
import json
import base64
import datetime

#from AppsAdmin.models import Studentregistrationpreferences
#from AppsAdmin.utils import legacy_app_read_permission

from SRegistration.models import *
from SRec.models import Studentflagassignments
from MOffices.models import Jurisdictions
from MAffiliations.models import Affiliations
from MOffices.models import Jurisdictions

from AppBase.utils_json import UnpackJson, PackJson, IsDuplicateElement, ReplaceElement, AppendElement, RemoveElementFromList

from MSchedule.utils import CourseTitle, CourseDetails
from MStaff.utils import DecodeStaffContext #, GetStaffObj

def FiscalYears():
    return ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022',]


def ListStudentsForAffiliation(affiliation=None, affiliation_county=None, location=None, location_county=None, start_date=None, end_date=None, fiscal_year=None): 
    """
      list student registrations with the given affiliation in the date range or fiscal year.
    """

    if not affiliation and not affiliation_county:
        return {'result_message':u'No affiliation or county given.', 'list': []}

    if not start_date and not end_date and not fiscal_year:
        return {'result_message':u'No module name given.', 'list': []}

    location_id = 164
    affiliation = None

    if fiscal_year:
        registration_record_list = Studentregistration.objects.filter(affiliation__exact=affiliation, scheduled_course__fiscal_year__eq=fiscal_year).order_by('scheduled_course', 'student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
    else:
        if affiliation:
            registration_record_list = Studentregistration.objects.filter(
                                                                        affiliation__id__exact=affiliation, 
                                                                        scheduled_course__start_date__gte=start_date, 
                                                                        scheduled_course__start_date__lt=end_date
                                                                     ).order_by('affiliation', 'scheduled_course', 'student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
        elif affiliation_county:
            registration_record_list = Studentregistration.objects.filter(
                                                                    affiliation__county__exact=affiliation_county, 
                                                                    scheduled_course__start_date__gte=start_date, 
                                                                    scheduled_course__start_date__lt=end_date
                                                                 ).order_by('affiliation', 'scheduled_course', 'student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
        elif location_id:
            registration_record_list = Studentregistration.objects.filter(
                                                                scheduled_course__location__exact=location_id, 
                                                                scheduled_course__start_date__gte=start_date, 
                                                                scheduled_course__start_date__lt=end_date
                                                             ).order_by('affiliation', 'scheduled_course', 'student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
        elif location_county:
            registration_record_list = Studentregistration.objects.filter(
                                                                scheduled_course__location__county__exact=location_county, 
                                                                scheduled_course__start_date__gte=start_date, 
                                                                scheduled_course__start_date__lt=end_date
                                                             ).order_by('affiliation', 'scheduled_course', 'student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
        
    if not registration_record_list:
        return {'result_message':u'No records found.', 'list': []}


    return {'result_message':u'Students found.', 'list': registration_record_list}


def CountStudentsForAffiliation(affiliation=None, start_date=None, end_date=None, fiscal_year=None, return_count_by_affiliation=False, return_count_by_course=False): 

    list_return = ListStudentsForAffiliation(affiliation=affiliation, start_date=start_date, end_date=end_date)

    registration_list = list_return.get('list', None)
    
    if not registration_list:
        return {'result_message':list_return.get('result_message', u'No records found.'), 'course_count': 0, 'registration_count': 0, 'list': []}
    
    
    course_count = 0
    registration_per_course_count = 0
    registration_count = 0
    last_scheduled_course = None
    
    course_counts = {}
    agency_counts = {}
    
    agency_list = []
    
    results_list = []
    
    
    for registration in registration_list:
        if registration.scheduled_course.log_number not in course_counts:
            course_counts[registration.scheduled_course.log_number] = {'total': 0}
        if registration.affiliation.name not in course_counts[registration.scheduled_course.log_number]:
            course_counts[registration.scheduled_course.log_number][registration.affiliation.name] = 0
        
        course_counts[registration.scheduled_course.log_number]['total'] += 1
        course_counts[registration.scheduled_course.log_number][registration.affiliation.name] += 1

        if registration.affiliation.name not in agency_counts:
            agency_counts[registration.affiliation.name] = 0
            
        agency_counts[registration.affiliation.name] += 1
        
    for affiliation_name in sorted(agency_counts):
        agency_list.append({'affiliation': affiliation_name, 'tally': agency_counts[affiliation_name]})
        
    assert False
    
    
    return {'result_message': u'report results', 'course_count': course_count, 'registration_count': registration_count, 'list': results_list}
    
    

def ListRegistrationRecordsForStudent(student_record=None, mfri_student_number=None, show_seated=True, show_pre_reg=True, show_webreg=True):  #ssn=None, 

    registration_record_list = []
    preregistration_records = []
    online_registration_record_list = []

    if show_seated:
        registration_record_list = Studentregistration.objects.filter(student_record__exact=student_record).order_by('scheduled_course__start_date')

    if show_pre_reg:
        preregistration_records = Preregistrations.objects.filter(student_record__exact=student_record).exclude(scheduled_course__end_date__lt=datetime.datetime.today()).exclude(status=7).order_by('scheduled_course__start_date') #20210722

    if show_webreg and mfri_student_number: #20210722
        online_registration_record_list = WebRegHold.objects.filter(mfri_student_number__exact=mfri_student_number).exclude(scheduled_course__end_date__lt=datetime.datetime.today()).exclude(status=4).order_by('scheduled_course__start_date') #20210722

    return {
            'registration_record_list': registration_record_list,
            'preregistration_records': preregistration_records,
            'online_registration_record_list': online_registration_record_list,
           }
