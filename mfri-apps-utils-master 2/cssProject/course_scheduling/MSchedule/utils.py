
import json
import base64
import time
import datetime
import decimal 

from AppsAdmin.utils import legacy_app_read_permission

from MBooks.utils import GetResourcesForCourse, GetResourceListForCourse

from MCourses.models import Coursestatus, Coursedescriptions

from MOffices.models import MfriOffices

from MStaff.utils import GetStaffRecord

from MSchedule.utils_search import validate_log_number_parts, parse_log_number, verify_log_number, find_course_from_log_number

from MSchedule.models import *

def decode_context(raw_context=None):

    if not raw_context:
        return None

    context_decoded = base64.urlsafe_b64decode(raw_context.encode("utf-8") + '=' * (4 - len(raw_context) % 4))

    context_decoded_dict = json.loads(context_decoded)

    if type(context_decoded_dict) != dict:
        return context_decoded_dict

    for context_key in context_decoded_dict.iterkeys():
        
        if type(context_decoded_dict[context_key]) in (str, unicode):
            context_decoded_dict[context_key] = context_decoded_dict[context_key].strip()
    
    return context_decoded_dict

def encode_context(context_data=None):
    
    if not context_data:
        return None

    email_context_json = json.dumps(context_data)
    
    email_context_base64 = base64.urlsafe_b64encode(email_context_json).strip('=')

    return email_context_base64


def legacy_app_id():
    return 6

def legacy_app_permission(user=None):
    if not user:
        return False
    
    user_profile = user.profile
    
    if not user_profile:
        return False

    if not user_profile.LegacyUserData:
        return False
    

    return legacy_app_read_permission(legacy_user_id=user_profile.LegacyUserData.id, legacy_app_id=legacy_app_id())


def ScheduledCourseRecord(log_number=None, category=None, level=None, funding_source_code=None, section_number=None, fiscal_year=None):#20200114

    scheduled_course = None
    
    find_course_result = find_course_from_log_number(log_number=log_number, category=category, level=level, funding_source_code=funding_source_code, section_number=section_number, fiscal_year=fiscal_year)
       
    if find_course_result:
        if find_course_result['ResponseCode'] > 0:
            course_list = find_course_result.get('scheduled_courses',  [None,])
            scheduled_course = course_list[0]
            
    return scheduled_course

def CourseTitle(log_number=None):
    
    log_number_parse_response = parse_log_number(log_number=log_number)

    if log_number_parse_response['ResponseCode'] < 1:
        return ''
    if log_number_parse_response['category']:
        scheduled_courses = Scheduledcourses.objects.filter(course_description__category__contains=log_number_parse_response['category'], course_description__level__contains=log_number_parse_response['level'], section_number = log_number_parse_response['section_number'], fiscal_year = log_number_parse_response['fiscal_year'])
    else:
        scheduled_courses = Scheduledcourses.objects.filter(course_description__course_code__contains=log_number_parse_response['course_code'], section_number = log_number_parse_response['section_number'], fiscal_year = log_number_parse_response['fiscal_year'])
            
    if scheduled_courses:
        return scheduled_courses[0].course_description.name

    return u'Invalid Log Number, no scheduled course match.'

def CourseDetails(log_number=None):

    log_number_parse_response = parse_log_number(log_number=log_number)

    if log_number_parse_response['ResponseCode'] < 1:
        return {   'StatusMessage': log_number_parse_response['StatusMessage'],
                   'ResponseCode': log_number_parse_response['ResponseCode'],
                   'course_detail': {'name': '',
                                     'location': '',
                                     'mfri_office': '',
                                     'mfri_office_abbreviation': '', 
                                     'coordinator': '',
                                     'lead_instructor': '',
                                     'start_datetime': '',
                                     'end_datetime': '',
                                     'instructional_hours': '',
                                     'total_hours': '',
                                     'pay_override': '', 
                                     'is_als': '', 
                                    },
                }
                
                

    if log_number_parse_response['category']:
        scheduled_courses = Scheduledcourses.objects.filter(course_description__category__contains=log_number_parse_response['category'], course_description__level__contains=log_number_parse_response['level'], section_number = log_number_parse_response['section_number'], fiscal_year = log_number_parse_response['fiscal_year'])
    else:
        scheduled_courses = Scheduledcourses.objects.filter(course_description__course_code__contains=log_number_parse_response['course_code'], section_number = log_number_parse_response['section_number'], fiscal_year = log_number_parse_response['fiscal_year'])

    if scheduled_courses:
        
        try:
            mfri_office = scheduled_courses[0].mfriofficeid
        except:
            mfri_office = MfriOffices.objects.get(pk=1)

        try:
            if scheduled_courses[0].start_date:
                course_start_date = scheduled_courses[0].start_date.strftime('%m-%d-%Y %H:%M')
            else:
                course_start_date = None
        except:
                course_start_date = None

        try:
            if scheduled_courses[0].end_date:
                course_end_date = scheduled_courses[0].end_date.strftime('%m-%d-%Y %H:%M')
            else:
                course_end_date = None
        except:
                course_end_date = None

        try:
            if scheduled_courses[0].course_description.name:
                course_name = scheduled_courses[0].course_description.name
            else:
                course_name = None
        except:
                course_name = None

        try:
            if scheduled_courses[0].location.name:
                course_location = scheduled_courses[0].location.name
            else:
                course_location = None
        except:
                course_location = None

        try:
            if scheduled_courses[0].coordinator_name:
                coordinator_name = scheduled_courses[0].coordinator_name
            else:
                coordinator_name = None
        except:
                coordinator_name = None

        try:
            if scheduled_courses[0].lead_instructor_name:
                lead_instructor_name = scheduled_courses[0].lead_instructor_name
            else:
                lead_instructor_name = None
        except:
                lead_instructor_name = None

        try:
            if scheduled_courses[0].course_description.instructional_hours:
                instructional_hours = str(scheduled_courses[0].course_description.instructional_hours)
            else:
                instructional_hours = '0.00'
        except:
                instructional_hours = '0.00'

        try:
            if scheduled_courses[0].course_description.total_hours:
                total_hours = str(scheduled_courses[0].course_description.total_hours)
            else:
                total_hours = '0.00'
        except:
                total_hours = '0.00'

        try:
            is_als = scheduled_courses[0].course_description.is_als
        except:
            is_als = False

        hourly_rate_override_amount = decimal.Decimal(u'0.00')
        
        if scheduled_courses[0].course_description.pay_override:
            hourly_rate_override_amount = scheduled_courses[0].course_description.pay_override
        
        return {   'StatusMessage': 'Course Found',
                   'ResponseCode': 1,
                   'course_detail': {'name': course_name, 
                                     'location': course_location, 
                                     'mfri_office': mfri_office.name,
                                     'mfri_office_abbreviation': mfri_office.abbreviation,
                                     'coordinator': coordinator_name, 
                                     'lead_instructor': lead_instructor_name, 
                                     'start_datetime': course_start_date,
                                     'end_datetime': course_end_date,
                                     'instructional_hours': instructional_hours, 
                                     'total_hours': total_hours, 
                                     'pay_override': str(hourly_rate_override_amount), 
                                     'is_als': is_als, 
                                    },
                }

    return {   'StatusMessage': u'Invalid Log Number, no scheduled course match.',
               'ResponseCode': -99,
               'course_detail': {'name': '',
                                 'location': '',
                                 'mfri_office': '', 
                                 'mfri_office_abbreviation': '', 
                                 'coordinator': '', 
                                 'lead_instructor': '', 
                                 'start_datetime': '',
                                 'end_datetime': '',
                                 'instructional_hours': '',
                                 'total_hours': '',
                                 'pay_override': '', 
                                 'is_als': '', 
                                },
            }

def CourseDescription(log_number=None, category=None, level=None, section_number=None, fiscal_year=None, course_code=None):

    course_code = None
    category = None
    level = None
    section_number = None
    fiscal_year = None
    
    if log_number:
        log_number_parse_response = parse_log_number(log_number=log_number)

        if log_number_parse_response['ResponseCode'] == 1:
            course_code = log_number_parse_response['course_code']
            category = log_number_parse_response['category']
            level = log_number_parse_response['level']
            section_number = log_number_parse_response['section_number']
            fiscal_year = log_number_parse_response['fiscal_year']

    validate_response = validate_log_number_parts(category=category, level=level,  section_number=section_number, fiscal_year=fiscal_year, course_code=course_code)

    if validate_response['ResponseCode'] < 1:
        return None
    
    if course_code:
        scheduled_courses = Scheduledcourses.objects.filter(course_description__course_code__iexact=course_code, section_number = section_number, fiscal_year = fiscal_year)
    else:
        scheduled_courses = Scheduledcourses.objects.filter(course_description__category__contains=category, course_description__level__contains=level, section_number = section_number, fiscal_year = fiscal_year)
            
    if scheduled_courses:
        return scheduled_courses[0]

    return None

def GetActiveScheduledCourses(mfri_office_list=None, current_date=None): #, category=None, level=None, section_number=None, 


    if not current_date:
        current_date = datetime.datetime.now()
        
    if not mfri_office_list:
        confirmed_courses = Scheduledcourses.objects.confirmed_courses().filter(start_date__lt=current_date, end_date__gt=current_date).order_by('mfri_office__abbreviation', 'start_date', 'end_date')
            
    confirmed_courses = Scheduledcourses.objects.confirmed_courses(MfriOffices=mfri_office_list).filter(start_date__lt=current_date, end_date__gt=current_date).order_by('mfri_office__abbreviation', 'location__name', 'start_date', 'end_date')

    return confirmed_courses

def GetConfirmedCourses(): 

    confirmed_courses = Scheduledcourses.objects.confirmed_courses(MfriOffices=MfriOffices.objects.all()).order_by('mfri_office__abbreviation', 'start_date', 'end_date') #'location__name', 

    return confirmed_courses


def UnpackCourseListContext(context=None, validate_requesting_instructor=True):
    
    if not context:
        return {'StatusMessage': u'No data.', 
                'ResponseCode': -2,
               }

    course_list_context = decode_context(context)

    if validate_requesting_instructor:
        instructor_uid = course_list_context.get('instructor_uid', None)
        
        if not instructor_uid:
            return {  'StatusMessage': u'No instructor UID',
                      'ResponseCode': -1,
                    }    
        
        if instructor_uid == u'999999999':
            return {  'StatusMessage': u'Wrong instructor UID',
                      'ResponseCode': -11,
                    }    
        
        instructor_response = GetStaffRecord(uid=instructor_uid)
        
        if instructor_response['ResponseCode'] < 1:
            return {  'StatusMessage': instructor_response['StatusMessage'],
                      'ResponseCode': -2,
                    }    
            
        instructor_record = instructor_response.get('StaffData', None)
        if not instructor_record:
            return {  'StatusMessage': u'No instructor UID, but one was expected',
                      'ResponseCode': -3,
                    }    
    
    log_number = course_list_context.get('log_number', None)
    
    window_days_length = course_list_context.get('window_days_length', 30)
    
    fiscal_year = course_list_context.get('fiscal_year', None)
    
    return {
            'StatusMessage': u'',
            'ResponseCode': 1,
            'instructor_uid': instructor_uid,
            'instructor': instructor_record,
            'log_number': log_number,
            'window_days_length': window_days_length,
            'fiscal_year': fiscal_year,
            }

def FormatCourseDetailsForInstructorZone(scheduled_course=None, log_number=None):

    if not scheduled_course:
        if not log_number:
            return None

        scheduled_course = ScheduledCourseRecord(log_number=log_number)

    if not scheduled_course:
        return None

    resource_list = GetResourceListForCourse(course_description=scheduled_course.course_description)

    details_to_return = {
                                'pk': scheduled_course.id,
                                'log_number': scheduled_course.log_number,
                                'name': scheduled_course.course_name,
                                'start_date': scheduled_course.start_date_MMDDYYY,
                                'end_date': scheduled_course.end_date_MMDDYYY,
                                'location': scheduled_course.location_name,
                                'mfri_office': scheduled_course.mfri_office.facility_name,
                                'mfri_office_phone': scheduled_course.mfri_office.main_number,
                                'mfri_office_email': scheduled_course.mfri_office.primary_email_address,
                                'has_online_component': scheduled_course.has_online_component,
                                'lms_course_name': scheduled_course.lms_course_name,
                                'lms_course_identifier': scheduled_course.lms_course_identifier,
                                'registration_close_date': scheduled_course.registration_close_date.strftime('%m-%d-%Y'),
                                'registered_count': scheduled_course.registered_count,
                                'min_students': scheduled_course.min_students,
                                'max_students': scheduled_course.max_students,
                                'does_require_medical_clearance': scheduled_course.does_require_medical_clearance,
                                'medical_clearance_note': scheduled_course.medical_clearance_note,
                                'has_sim_center_component': scheduled_course.has_sim_center_component,
                                'coordinator_name': scheduled_course.coordinator_name,
                                'require_training_officer_approval': scheduled_course.require_training_officer_approval,
                                'lead_instructor_uid': scheduled_course.lead_instructor_uid,
                                'lead_instructor_name': scheduled_course.lead_instructor_name,
                                'lead_instrustor_email': scheduled_course.lead_instructor_email_address, 
                                'resource_list': resource_list,
                              }

    return details_to_return

def GetCourseListForInstructor(lead_instructor=None, fiscal_year=None, schedule_view_window_days=30):

    if not lead_instructor:
        return []

    if fiscal_year:
        scheduled_course_list = Scheduledcourses.objects.filter(
                                                                instructor__exact=lead_instructor, fiscal_year__exact=fiscal_year
                                                               ).order_by('course_description__category', 'course_description__level', 'section_number', 'fiscal_year')
    else:
        scheduled_course_list = Scheduledcourses.objects.filter(
                                                            instructor__exact=lead_instructor,
                                                           ).order_by('course_description__category', 'course_description__level', 'section_number', 'fiscal_year')
                                                           
    list_to_return = []

    for scheduled_course in scheduled_course_list:
        
        if not scheduled_course.end_date:
            continue

        if not fiscal_year:
            if scheduled_course.end_date + datetime.timedelta(days=schedule_view_window_days) < datetime.datetime.now():
                continue
        
        list_to_return.append(FormatCourseDetailsForInstructorZone(scheduled_course=scheduled_course))

    return list_to_return


def FormatCourseDetailsForCourseRegistration(scheduled_course=None, log_number=None):

    if not scheduled_course:
        if not log_number:
            return None

        scheduled_course = ScheduledCourseRecord(log_number=log_number)

    if not scheduled_course:
        return None

    resource_list = GetResourceListForCourse(course_description=scheduled_course.course_description)
    
    details_to_return = {
                                'pk': scheduled_course.id,
                                'log_number': scheduled_course.log_number,
                                'name': scheduled_course.course_name,
                                'start_date': scheduled_course.start_date_MMDDYYY,
                                'end_date': scheduled_course.end_date_MMDDYYY,
                                'registration_open_date'                  : scheduled_course.registration_open_date_MMDDYYYY,
                                'registration_close_date'                 : scheduled_course.registration_close_date_MMDDYYYY,
                                'registration_open_date_YMD'                  : scheduled_course.registration_open_date_YYYYMMDD,
                                'registration_close_date_YMD'                 : scheduled_course.registration_close_date_YYYYMMDD,
                                'location': scheduled_course.location_name,
                                'mfri_office': scheduled_course.mfri_office.facility_name,
                                'mfri_office_phone': scheduled_course.mfri_office.main_number,
                                'mfri_office_email': scheduled_course.mfri_office.primary_email_address,
                                'has_online_component': scheduled_course.has_online_component,
                                'does_require_medical_clearance': scheduled_course.does_require_medical_clearance,
                                'medical_clearance_note': scheduled_course.medical_clearance_note,
                                'alert_msg'                               : scheduled_course.alert_msg,
                                'special_alert'                           : scheduled_course.special_alert,
                                'registration_note'                       : scheduled_course.registration_note,
                                'registration_alert_text'                 : scheduled_course.registration_alert_text,
                                'registration_header_text'                : scheduled_course.registration_header_text,
                                'registration_special_instructions_text'  : scheduled_course.registration_special_instructions_text,
                                'registration_footer_text'                : scheduled_course.registration_footer_text,
                                'registration_message'                    : scheduled_course.registration_message,
                                'registration_email_text'                 : scheduled_course.registration_email_text,
                                'additional_course_prerequisite'          : scheduled_course.additional_course_prerequisite,
                                'require_epins'                           : scheduled_course.require_epins,
                                'require_ssn'                             : scheduled_course.require_ssn,
                                'require_mfri_student_number'             : scheduled_course.require_mfri_student_number, 
                                'require_nfasid'                          : scheduled_course.require_nfasid,
                                'require_birth_date'                      : scheduled_course.require_birth_date,
                                'require_emt_expiration_date'             : scheduled_course.require_emt_expiration_date,
                                'require_address'                         : scheduled_course.require_address,
                                'require_affiliation'                     : scheduled_course.require_affiliation,
                                'require_email_address'                   : scheduled_course.require_email_address,
                                'require_primary_phone'                   : scheduled_course.require_primary_phone,
                                'require_cell_phone'                      : scheduled_course.require_cell_phone,
                                'require_training_officer_approval'       : scheduled_course.require_training_officer_approval,
                                'require_mfri_office_approval'            : scheduled_course.require_mfri_office_approval,
                                'require_book_fee_acknowledgment'                 : scheduled_course.require_training_officer_approval, 
                                'require_rules_and_regulations_acknowledgement'   : scheduled_course.require_training_officer_approval, 
                                'require_release_statement_acknowledgement'       : scheduled_course.require_training_officer_approval, 
                                'show_msfa_acknowledgement'                      : scheduled_course.require_training_officer_approval,  
                                'use_wait_list'                           : scheduled_course.use_wait_list,
                                'use_web_registration'                    : scheduled_course.use_web_registration,
                                'out_of_state_fee'                        : str(scheduled_course.out_of_state_fee),
                                'in_state_fee'                            : str(scheduled_course.in_state_fee),
                                'resource_fee'                            : str(scheduled_course.resource_fee),
                                'is_seminar'                              : scheduled_course.is_seminar,
                                'needs_bls_approval'                      : scheduled_course.needs_bls_approval,
                                'needs_als_approval'                      : scheduled_course.needs_als_approval,
                                'needs_pdi_approval'                      : scheduled_course.needs_pdi_approval,
                                'needs_other_approval'                    : scheduled_course.needs_other_approval,
                                'late_registration_token'                 : scheduled_course.late_registration_token,
                                'resource_list': resource_list,
                              }

    return details_to_return

def GetCompletedCourseList(mfri_office=None, days_closed_threshold=30):

    if mfri_office:
        scheduled_course_list = Scheduledcourses.objects.filter(
                                                                mfri_office__exact=mfri_office,
                                                                schedule_status__in=(3, 4, 5, 11),
                                                               ).order_by('course_description__category', 'course_description__level', 'section_number', 'fiscal_year')
    else:
        scheduled_course_list = Scheduledcourses.objects.filter(
                                                                schedule_status__in=(3, 4, 5, 11),
                                                           ).order_by('course_description__category', 'course_description__level', 'section_number', 'fiscal_year')
                                                           
    list_to_return = []

    for scheduled_course in scheduled_course_list:
        
        if not scheduled_course.end_date:
            continue

        if scheduled_course.end_date + datetime.timedelta(days=days_closed_threshold) < datetime.datetime.now():
            continue
        
        list_to_return.append(scheduled_course)

    return list_to_return

def ScheduledCourseStatusDefault():
    try:
        default_value = ScheduledCourseStatus.objects.get( pk=2 )
    except ScheduledCourseStatus.DoesNotExist:
        return None
    except ScheduledCourseStatus.MultipleObjectsReturned:
        return None
    return default_value


def GetScheduledCourseStatus(pk=None, key_word=None):
    
    if key_word:
        if key_word == u'cancelled':
            pk = 6
        elif key_word == u'duplicate':
            pk = 7
        elif key_word == u'error':
            pk = 9
        elif key_word == u'requested':
            pk = 2
        elif key_word == u'confirmed':
            pk = 3
        elif key_word == u'approved':
            pk = 11
        elif key_word == u'closed':
            pk = 4
        else:
            pk = 2

    default_value_list = ScheduledCourseStatus.objects.filter( pk=pk )
            
    if default_value_list:
        return default_value_list[0]
    
    return ScheduledCourseStatusDefault()

def GetPublicScheduleFromName( public_schedule_short_name = None ):
    
    if public_schedule_short_name == u'msfs':
        public_schedule_short_name = u'mdfs'

    if not public_schedule_short_name:
        return None

    try:
        return Publicschedule.objects.get(code_name__iexact=public_schedule_short_name )
    except Publicschedule.DoesNotExist:
        return None

    return None

def build_query_kwargs(query_kwarg_list=None):

    if not query_kwarg_list:
        return None

    query_kwargs = {}

    for kwarg in query_kwarg_list:
        query_kwargs['%s__%s' % (kwarg['table_field_name'], kwarg['query_verb'])] = kwarg['field_value']
    
    return query_kwargs

def BuildPublicScheduleStruct(public_schedule=None, scheduled_course=None):
    
    schedule_entry = {
                        'ps_id': 0,
                        'public_schedule_name': '',
                        'name': '',
                        'course_id': 0,
                        'sc_id': 0,
                        'log_number': '',
                        'instructional_hours': 0,
                        'section_id': 0,
                        'section_name': '',
                        'region_id': 0,
                        'region_name': '',
                        'office_id': 0,
                        'office_name': '',
                        'office_abbreviation': '',
                        'office_email': '',
                        'start_date': '',
                        'start_time': '',
                        'end_date': '',
                        'end_time': '',
                        'registration_open_date': '',
                        'registration_close_date': '',
                        'meeting_days': '',
                        'location_id': 0,
                        'location_name': '',
                        'has_file' : False, 
                        'file_label': '',
                        'file_url': '',
                        'file_type': '',
                        'does_require_medical_clearance': False,
                        'medical_clearance_note'        : u'',
                        'has_sim_center_component'      : False,
                        'has_online_component'          : False,
                        'approximate_course_length': '',
                        'alert_msg'                               : '',
                        'special_alert'                           : '',
                        'registration_note'                       : '',
                        'registration_alert_text'                 : '',
                        'registration_header_text'                : '',
                        'registration_special_instructions_text'  : '',
                        'registration_footer_text'                : '',
                        'registration_message'                    : '',
                        'require_payment'                         : False,
                        'require_epins'                           : False,
                        'require_ssn'                             : False,
                        'require_mfri_student_number'         : False,            
                        'require_nfasid'                          : False,
                        'require_birth_date'                      : False,
                        'require_emt_expiration_date'             : False,
                        'require_address'                         : False,
                        'require_affiliation'                     : False,
                        'require_email_address'                   : False,
                        'require_primary_phone'                   : False,
                        'require_cell_phone'                      : False,
                        'require_training_officer_approval'	  : False,
                        'require_mfri_office_approval'            : False,
                        'use_wait_list'                           : False,
                        'use_web_registration'                    : False,
                        'allow_late_registration'                 : False,
                        'use_wait_list'                           : False,
                        'use_web_registration'                    : False,
                        'allow_late_registration'                 : False,
                        'require_book_fee_acknowledgment'                 : False, 
                        'require_rules_and_regulations_acknowledgement'   : False, 
                        'require_release_statement_acknowledgement'       : False, 
                        'show_msfa_acknowledgement'                      : False,  
                        'schedule_type' : u'', 
                        'is_seminar' : u'', 
                        'in_state_fee'      : u'0.00',
                        'out_of_state_fee'    : u'0.00',
                        'resource_fee'      : u'0.00',
                        'registered_count': 0, 
                        'min_students': 0, 
                        'max_students': 0, 
                     }
    
    if not scheduled_course:
        return schedule_entry
    
    public_schedule_name = ''
    ps_id = 0
    if public_schedule:
        public_schedule_name = public_schedule.name
        ps_id = public_schedule.id

    scheduled_course_flier = None
    file_label = None
    file_url = None
    file_type = None
    has_file = False 

    scheduled_course_attachment = ScheduledCourseFlier(scheduled_course=scheduled_course)

    if scheduled_course_attachment.get('scheduled_course_flier', None):
        file_label = scheduled_course_attachment.get('file_label', None)
        file_url = scheduled_course_attachment.get('file_url', None)
        file_type = scheduled_course_attachment.get('file_type', None)
        has_file = scheduled_course_attachment.get('has_file', False) 

    schedule_type_name = u''
    if scheduled_course.schedule_type:
        schedule_type_name = scheduled_course.schedule_type.name

    return {
              'ps_id': ps_id,
              'public_schedule_name': public_schedule_name,
              'name': scheduled_course.course_description.name,
              'course_id': scheduled_course.course_description.id,
              'sc_id': scheduled_course.id,
              'log_number': scheduled_course.log_number,
              'instructional_hours': str(scheduled_course.course_description.instructional_hours),
              'section_id': scheduled_course.legacy_host_section.id,
              'section_name': scheduled_course.legacy_host_section.name,
              'region_id': scheduled_course.legacy_host_region.id,
              'region_name': scheduled_course.legacy_host_region.name,
              'office_id': scheduled_course.mfri_office.id,
              'office_abbreviation': scheduled_course.mfri_office.abbreviation,
              'office_name': scheduled_course.mfri_office.name,
              'office_email': scheduled_course.mfri_office.primary_email_address,
              'start_date': scheduled_course.start_date_MMDDYYY,
              'start_time': scheduled_course.start_time,
              'end_date': scheduled_course.end_date_MMDDYYY,
              'end_time': scheduled_course.end_time,
              'registration_open_date': scheduled_course.registration_open_date_MMDDYYYY,
              'registration_close_date': scheduled_course.registration_close_date_MMDDYYYY,
              'meeting_days': scheduled_course.regular_meeting_days,
              'location_id': scheduled_course.location.id,
              'location_name': scheduled_course.location_name,
              'has_file' : has_file, 
              'file_label': file_label,
              'file_url': file_url,
              'file_type': file_type,
              'does_require_medical_clearance': scheduled_course.does_require_medical_clearance,
              'medical_clearance_note': scheduled_course.medical_clearance_note,
              'has_sim_center_component': scheduled_course.has_sim_center_component,
              'has_online_component': scheduled_course.has_online_component,
              'approximate_course_length': scheduled_course.approximate_course_length,
              'alert_msg'                               : scheduled_course.alert_msg,
              'special_alert'                           : scheduled_course.special_alert,
              'registration_note'                       : scheduled_course.registration_note,
              'registration_alert_text'                 : scheduled_course.registration_alert_text,
              'registration_header_text'                : scheduled_course.registration_header_text,
              'registration_special_instructions_text'  : scheduled_course.registration_special_instructions_text,
              'registration_footer_text'                : scheduled_course.registration_footer_text,
              'registration_message'                    : scheduled_course.registration_message,
              'require_payment'                         : scheduled_course.require_payment,
              'require_epins'                           : scheduled_course.require_epins,
              'require_ssn'                             : scheduled_course.require_ssn,
              'require_mfri_student_number'             : scheduled_course.require_mfri_student_number, 
              'require_nfasid'                          : scheduled_course.require_nfasid,
              'require_birth_date'                      : scheduled_course.require_birth_date,
              'require_emt_expiration_date'             : scheduled_course.require_emt_expiration_date,
              'require_address'                         : scheduled_course.require_address,
              'require_affiliation'                     : scheduled_course.require_affiliation,
              'require_email_address'                   : scheduled_course.require_email_address,
              'require_primary_phone'                   : scheduled_course.require_primary_phone,
              'require_cell_phone'                      : scheduled_course.require_cell_phone,
              'require_training_officer_approval'       : scheduled_course.require_training_officer_approval,
              'require_book_fee_acknowledgment'                 : scheduled_course.require_training_officer_approval, 
              'require_rules_and_regulations_acknowledgement'   : scheduled_course.require_training_officer_approval, 
              'require_release_statement_acknowledgement'       : scheduled_course.require_training_officer_approval, 
              'show_msfa_acknowledgement'                      : scheduled_course.require_training_officer_approval,  
              'require_mfri_office_approval'            : scheduled_course.require_mfri_office_approval,
              'use_wait_list'                           : scheduled_course.use_wait_list,
              'use_web_registration'                    : scheduled_course.use_web_registration,
              'allow_late_registration'                 : scheduled_course.allow_late_registration,
              'out_of_state_fee'                        : str(scheduled_course.out_of_state_fee),
              'in_state_fee'                            : str(scheduled_course.in_state_fee),
              'resource_fee'                            : str(scheduled_course.resource_fee),
              'schedule_type' : schedule_type_name, 
              'is_seminar' : scheduled_course.is_seminar, 
              'registered_count': scheduled_course.registered_count, 
              'min_students': scheduled_course.min_students, 
              'max_students': scheduled_course.max_students, 
            }

def GetPublicScheduledCourses(public_schedule=None, mfri_office=None, location=None, start_date=None, category=None, level=None): 

    query_kwargs = {}


    query_kwarg_list = []


    if public_schedule:
        query_kwarg_list.append({'table_field_name': 'public_schedule', 'query_verb': u'exact', 'field_value': public_schedule})


    if location:
        query_kwarg_list.append({'table_field_name': 'scheduled_course__location', 'query_verb': u'exact', 'field_value': location})

    if category:
        query_kwarg_list.append({'table_field_name': 'scheduled_course__course_description__category', 'query_verb': u'exact', 'field_value': category})

    if level:
        query_kwarg_list.append({'table_field_name': 'scheduled_course__course_description__level', 'query_verb': u'exact', 'field_value': level})

    if not start_date:
        start_date = datetime.datetime.today()
        
    query_kwarg_list.append({'table_field_name': 'scheduled_course__start_date', 'query_verb': u'gte', 'field_value': start_date})

    query_kwarg_list.append({'table_field_name': 'scheduled_course__mark_as_deleted', 'query_verb': u'exact', 'field_value': 0})
    query_kwarg_list.append({'table_field_name': 'scheduled_course__schedule_status', 'query_verb': u'exact', 'field_value': 3}) #course confirmed

    query_kwargs = build_query_kwargs(query_kwarg_list=query_kwarg_list)
    
    public_schedule_list = []

    if query_kwargs:
        public_schedule_list = Publicschedulelink.objects.filter(**query_kwargs).order_by(u'scheduled_course__start_date')

    schedule_list = []

    for public_schedule_entry in public_schedule_list:
        if not public_schedule_entry.public_schedule:
            continue

        if public_schedule_entry.public_schedule.code_name == u'none':
            continue

        if mfri_office:
            if public_schedule_entry.scheduled_course.mfri_office != mfri_office:
                if public_schedule_entry.scheduled_course.course_description.is_als:
                    if public_schedule_entry.scheduled_course.location.region.abbreviation != mfri_office.abbreviation:
                        continue
                else:
                    continue

        schedule_list.append(BuildPublicScheduleStruct(public_schedule=public_schedule, scheduled_course=public_schedule_entry.scheduled_course))

    return schedule_list


def ScheduledCourseFlier(scheduled_course=None):

    if not scheduled_course:

        return {
                'scheduled_course_flier': None,
                'has_file': False, 
                'file_type': None, 
                'file_label': None, 
                'file_url': None
                }

    scheduled_course_flier = None
    file_label = None
    file_url = None
    file_type = None

    try:
        if scheduled_course.legacy_link: 
            scheduled_course_flier = scheduled_course.legacy_link
            file_label = scheduled_course_flier.name
            file_url = scheduled_course_flier.url
            file_type = scheduled_course_flier.link_type.name

    except:

        return {
                'scheduled_course_flier': None,
                'has_file': False, 
                'file_type': None, 
                'file_label': None, 
                'file_url': None
                }
   
    return {
            'scheduled_course_flier': scheduled_course_flier,
            'has_file': True, 
            'file_type': file_type, 
            'file_label': file_label, 
            'file_url': file_url
            }

def BuildScheduledCourseJSON(scheduled_course=None):

    schedule_entry = {
                        'name': '',
                        'course_id': 0,
                        'sc_id': 0,
                        'log_number': '',
                        'instructional_hours': 0,
                        'section_id': 0,
                        'section_name': '',
                        'region_id': 0,
                        'region_name': '',
                        'office_id': 0,
                        'office_name': '',
                        'office_email': '',
                        'office_abbreviation': '', 
                        'office_code': '', 
                        'start_date': '',
                        'start_time': '',
                        'end_date': '',
                        'end_time': '',
                        'registration_open_date': '',
                        'registration_close_date': '',
                        'meeting_days': '',
                        'location_id': 0,
                        'location_name': '',
                        'file_label': '',
                        'file_url': '',
                        'file_type': '',
                        'does_require_medical_clearance': False,
                        'medical_clearance_note'        : u'',
                        'has_sim_center_component'      : False,
                        'has_online_component'          : False,
                        'approximate_course_length': '',
                        'alert_msg'                               : '',
                        'special_alert'                           : '',
                        'registration_note'                       : '',
                        'registration_alert_text'                 : '',
                        'registration_header_text'                : '',
                        'registration_special_instructions_text'  : '',
                        'registration_footer_text'                : '',
                        'registration_message'                    : '',
                        'require_payment'                         : False,
                        'require_epins'                           : False,
                        'require_ssn'                             : False,
                        'require_mfri_student_number'         : '', 
                        'require_nfasid'                          : False,
                        'require_birth_date'                      : False,
                        'require_emt_expiration_date'             : False,
                        'require_address'                         : False,
                        'require_affiliation'                     : False,
                        'require_email_address'                   : False,
                        'require_primary_phone'                   : False,
                        'require_cell_phone'                      : False,
                        'require_training_officer_approval'       : False,
                        'require_mfri_office_approval'            : False,
                        'require_book_fee_acknowledgment'                 : False, 
                        'require_rules_and_regulations_acknowledgement'   : False, 
                        'require_release_statement_acknowledgement'       : False, 
                        'show_msfa_acknowledgement'                      : False,  
                        'use_wait_list'                           : False,
                        'use_web_registration'                    : False,
                        'allow_late_registration'                 : False,
                        'out_of_state_fee'                        : '',
                        'in_state_fee'                            : '',
                        'resource_fee'                            : '',
                        'has_file' : False, 
                        'schedule_type' : u'', 
                        'is_seminar' : u'', 
                        'registered_count': 0, 
                        'min_students': 0, 
                        'max_students': 0, 
                        'course_description': BuildCourseDescriptionJSON(course_description=None, override_show_in_catalog=True),#20200115 #20200514
                     }

    if not scheduled_course:
        return schedule_entry

    scheduled_course_flier = None
    file_label = None
    file_url = None
    file_type = None
    has_file = False 

    scheduled_course_attachment = ScheduledCourseFlier(scheduled_course=scheduled_course)

    if scheduled_course_attachment.get('scheduled_course_flier', None):
        file_label = scheduled_course_attachment.get('file_label', None)
        file_url = scheduled_course_attachment.get('file_url', None)
        file_type = scheduled_course_attachment.get('file_type', None)
        has_file = scheduled_course_attachment.get('has_file', False) 

    schedule_type_name = u''
    if scheduled_course.schedule_type:
        schedule_type_name = scheduled_course.schedule_type.name

    return {
              'name': scheduled_course.course_description.full_name,
              'course_id': scheduled_course.course_description.id,
              'sc_id': scheduled_course.id,
              'log_number': scheduled_course.log_number,
              'instructional_hours': str(scheduled_course.course_description.instructional_hours),
              'section_id': scheduled_course.legacy_host_section.id,
              'section_name': scheduled_course.legacy_host_section.name,
              'region_id': scheduled_course.legacy_host_region.id,
              'region_name': scheduled_course.legacy_host_region.name,
              'office_id': scheduled_course.mfri_office.id,
              'office_name': scheduled_course.mfri_office.name,
              'office_email': scheduled_course.mfri_office.primary_email_address,
              'office_abbreviation': scheduled_course.mfri_office.abbreviation, 
              'office_code': scheduled_course.mfri_office.abbreviation.lower(), 
              'start_date': scheduled_course.start_date_MMDDYYY,
              'start_time': scheduled_course.start_time,
              'end_date': scheduled_course.end_date_MMDDYYY,
              'end_time': scheduled_course.end_time,
              'registration_open_date': scheduled_course.registration_open_date_MMDDYYYY,
              'registration_close_date': scheduled_course.registration_close_date_MMDDYYYY,
              'meeting_days': scheduled_course.regular_meeting_days,
              'location_id': scheduled_course.location.id,
              'location_name': scheduled_course.location_name,
              'does_require_medical_clearance': scheduled_course.does_require_medical_clearance,
              'medical_clearance_note': scheduled_course.medical_clearance_note,
              'has_sim_center_component': scheduled_course.has_sim_center_component,
              'has_online_component': scheduled_course.has_online_component,
              'approximate_course_length': scheduled_course.approximate_course_length,
              'alert_msg'                               : scheduled_course.alert_msg,
              'special_alert'                           : scheduled_course.special_alert,
              'registration_note'                       : scheduled_course.registration_note,
              'registration_alert_text'                 : scheduled_course.registration_alert_text,
              'registration_header_text'                : scheduled_course.registration_header_text,
              'registration_special_instructions_text'  : scheduled_course.registration_special_instructions_text,
              'registration_footer_text'                : scheduled_course.registration_footer_text,
              'registration_message'                    : scheduled_course.registration_message,
              'require_payment'                         : scheduled_course.require_payment,
              'require_epins'                           : scheduled_course.require_epins,
              'require_ssn'                             : scheduled_course.require_ssn,
              'require_mfri_student_number'             : scheduled_course.require_mfri_student_number, 
              'require_nfasid'                          : scheduled_course.require_nfasid,
              'require_birth_date'                      : scheduled_course.require_birth_date,
              'require_emt_expiration_date'             : scheduled_course.require_emt_expiration_date,
              'require_address'                         : scheduled_course.require_address,
              'require_affiliation'                     : scheduled_course.require_affiliation,
              'require_email_address'                   : scheduled_course.require_email_address,
              'require_primary_phone'                   : scheduled_course.require_primary_phone,
              'require_cell_phone'                      : scheduled_course.require_cell_phone,
              'require_training_officer_approval'       : scheduled_course.require_training_officer_approval,
              'require_book_fee_acknowledgment'                 : scheduled_course.require_training_officer_approval, 
              'require_rules_and_regulations_acknowledgement'   : scheduled_course.require_training_officer_approval, 
              'require_release_statement_acknowledgement'       : scheduled_course.require_training_officer_approval, 
              'show_msfa_acknowledgement'                      : scheduled_course.require_training_officer_approval,  
              'require_mfri_office_approval'            : scheduled_course.require_mfri_office_approval,
              'use_wait_list'                           : scheduled_course.use_wait_list,
              'use_web_registration'                    : scheduled_course.use_web_registration,
              'allow_late_registration'                 : scheduled_course.allow_late_registration,
              'out_of_state_fee'                        : str(scheduled_course.out_of_state_fee),
              'in_state_fee'                            : str(scheduled_course.in_state_fee),
              'resource_fee'                            : str(scheduled_course.resource_fee),
              'has_file' : has_file, 
              'file_label' : file_label, 
              'file_url'   : file_url, 
              'file_type ' : file_type, 
              'schedule_type' : schedule_type_name, 
              'is_seminar' : scheduled_course.is_seminar, 
              'registered_count': scheduled_course.registered_count, 
              'min_students': scheduled_course.min_students, 
              'max_students': scheduled_course.max_students, 
              'course_description': BuildCourseDescriptionJSON(course_description=scheduled_course.course_description, override_show_in_catalog=True),
            }

def BuildCourseDescriptionJSON(course_description=None, override_show_in_catalog=False):
    
    course_description_entry = {
                        'name': '',
                        'course_id': 0,
                        'category': '',
                        'level': '',
                        'instructional_hours': 0,
                        'description': '',
                        'medical_clearance_label' :  '',
                        'has_online_component_label' : '',
                        'ace_description'         :  '',
                        'prerequisites'           :  '',
                        'fp_specific_description' :  '',
                        'sp_specific_description' :  '',
                        'registration_message' : '',
                        'medical_clearance_note' : '',
                        'require_medical_clearance' : False, 
                        'has_online_component' : False, 
                        'resource_list': '', 
                     }
    
    if not course_description:
        return course_description_entry

    if not override_show_in_catalog:
        if not course_description.show_in_catalog:
            return course_description_entry

    resource_list = GetResourceListForCourse(course_description=course_description)

    return {
              'name': course_description.name,
              'edition': course_description.edition,
              'course_id': course_description.id,
              'category': course_description.category,
              'level': course_description.level,
              'instructional_hours': str(course_description.instructional_hours),
              'description': course_description.description,
              'medical_clearance_label' : course_description.medical_clearance_label,
              'has_online_component_label'    : course_description.has_online_component_label,
              'ace_description'         : course_description.ace_description,
              'prerequisites'           : course_description.prerequisites,
              'fp_specific_description' : course_description.fp_specific_description,
              'sp_specific_description' : course_description.sp_specific_description,
              'registration_message' : course_description.registration_message,
              'medical_clearance_note' : course_description.medical_clearance_note,
              'require_medical_clearance' : course_description.require_medical_clearance, 
              'has_online_component' : course_description.has_online_component,
              'resource_list': resource_list, 
            }


def BuildCourseListJSON(course_list=None):

    course_list_to_return = []
    
    if not course_list:
        return course_list_to_return

    for course_description in course_list:

        course_description_json = BuildCourseDescriptionJSON(course_description=course_description)
        if course_description_json.get('course_id', 0) == 0:
            continue
        course_list_to_return.append(course_description_json)

    return course_list_to_return


def BuildLocationJSON(location=None):
    
    location_entry = {
                        'name': '',
                        'region_abbreviation': '',
                        'region_name': '',
                        'county_name': '',
                        'county_pk': 0,
                        'address1': '',
                        'address2': '',
                        'city': '',
                        'state' : '',
                        'postcode' : '',
                        'country' : '',
                        'primary_phone_number' :  '',
                        'secondary_phone_number' :  '',
                        'fax_number' : '',
                        'email_address' : '',
                     }
    
    if not location:
        return location_entry
    
    region_abbreviation = u''
    region_name = u''

    if location.region:
        region_abbreviation = location.region.abbreviation
        region_name = location.region.name

    county_name = u''
    county_pk = 0

    if location.county:
        county_name = location.county.name
        county_pk = location.county.id

    return {
            'name': location.name,
            'region_abbreviation': region_abbreviation,
            'region_name': region_name,
            'county_name': county_name,
            'county_pk': county_pk,
            'address1': location.address1,
            'address2': location.address2,
            'city': location.city,
            'state' : location.state,
            'postcode' : location.postcode,
            'country' : location.country,
            'primary_phone_number' :  u'', #don't return phone number location.primary_phone_number,
            'secondary_phone_number' :  u'', #don't return phone number location.secondary_phone_number,
            'fax_number' : u'', #don't return phone number location.fax_number,
            'email_address' : u'', #don't return email address location.email_address,
            }

def BuildLocationListJSON(location_list=None):

    location_list_to_return = []
    
    if not location_list:
        return location_list_to_return

    for location_description in location_list:
        location_list_to_return.append(BuildLocationJSON(location=location_description))

    return location_list_to_return




def FormatResourcesForCourse(scheduled_course=None, log_number=None):

    if not scheduled_course:
        if not log_number:
            return None

        scheduled_course = ScheduledCourseRecord(log_number=log_number)

    if not scheduled_course:
        return None

    resource_list = GetResourceListForCourse(course_description=scheduled_course.course_description)
    
    return resource_list



def GetPublicScheduleCodeFromID( public_schedule_id = None ):

    default_schedule_code = u'mdfs'

    if not public_schedule_id.isdigit():
        return default_schedule_code

    if not public_schedule_id:
        return default_schedule_code

    try:
        public_schedule = Publicschedule.objects.get(pk=public_schedule_id )
    except Publicschedule.DoesNotExist:
        return default_schedule_code

    try:
        public_schedule_code = public_schedule.code_name
    except:
        return default_schedule_code
        
    return public_schedule_code


def GetCourseDescriptionsForPublicSchedule(public_schedule=None, category=None, start_date=None): 

    query_kwargs = {}


    query_kwarg_list = []


    if not public_schedule:
        return []

    query_kwarg_list.append({'table_field_name': 'public_schedule', 'query_verb': u'exact', 'field_value': public_schedule})

    if not start_date:
        start_date = datetime.datetime.today()

    if category:
        query_kwarg_list.append({'table_field_name': 'scheduled_course__course_description__category', 'query_verb': u'exact', 'field_value': category})

    query_kwarg_list.append({'table_field_name': 'scheduled_course__start_date', 'query_verb': u'gte', 'field_value': start_date})
    query_kwarg_list.append({'table_field_name': 'scheduled_course__mark_as_deleted', 'query_verb': u'exact', 'field_value': 0})
    query_kwarg_list.append({'table_field_name': 'scheduled_course__schedule_status', 'query_verb': u'exact', 'field_value': 3}) #course confirmed

    query_kwargs = build_query_kwargs(query_kwarg_list=query_kwarg_list)

    public_schedule_list = []

    if query_kwargs:
        public_schedule_list = Publicschedulelink.objects.filter(**query_kwargs).order_by(u'scheduled_course__course_description__category', u'scheduled_course__course_description__level') #.order_by(u'scheduled_course__start_date')
    
    result_count = len(public_schedule_list)

    category_level_found = {}
    course_list = []

    for public_schedule_entry in public_schedule_list:
        if not public_schedule_entry.public_schedule:
            continue
            
        if public_schedule_entry.public_schedule.code_name == u'none':
            continue

        if category_level_found.get(public_schedule_entry.scheduled_course.course_description.category_level, False):
            continue

        if public_schedule_entry.scheduled_course.course_description.category in (u'CD', u'PDI', u'EMSS', u'FIRS', u'HMS', u'INDS', u'MGTS', u'RESS', u'SES', u'SIM', u'TTT', u'NFA'):
            continue

        category_level_found[public_schedule_entry.scheduled_course.course_description.category_level] = True
        course_description_json = BuildCourseDescriptionJSON(course_description=public_schedule_entry.scheduled_course.course_description)
        if course_description_json.get('course_id', 0) == 0:
            continue
        course_list.append(course_description_json)

    return course_list

def UpdateEmailAlertOptionGetCompletedCourseList(mfri_office=None, send_alert_email_to_office_before_approval=False, send_alert_email_to_office_after_approval=False):

    if not mfri_office:
        return False

    scheduled_course_list = Scheduledcourses.objects.filter(
                                                                mfri_office__exact=mfri_office,
                                                                schedule_status__in=(3, 4, 5, 11),
                                                                start_date__gte=datetime.date.today()
                                                               ).order_by('course_description__category', 'course_description__level', 'section_number', 'fiscal_year')
                                            
    for scheduled_course in scheduled_course_list:
        
        try:
            scheduled_course.send_alert_email_to_office_before_approval = send_alert_email_to_office_before_approval
            scheduled_course.send_alert_email_to_office_after_approval = send_alert_email_to_office_after_approval
            scheduled_course.save(update_fields=['send_alert_email_to_office_before_approval', 'send_alert_email_to_office_after_approval'])
        except:
            continue

    return True










