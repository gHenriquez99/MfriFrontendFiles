
import re
import json
import base64
import datetime
from operator import attrgetter 


from SRegistration.models import *
from SRec.models import Studentflagassignments
from MOffices.models import Jurisdictions

from MAffiliations.models import Affiliations
from MOffices.models import Jurisdictions

from SRec.utils import student_age_at_date

from MSchedule.utils_search import FindCourseFromLogNumber
from MStaff.utils import DecodeStaffContext
from MFRI_Utils.data_validate import validate_ssn, validate_last_name


def diff_month(d1, d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month

def GetRegistrationPriorityIncrement(rule_name=None):
    
    if not rule_name:
        return 0

    try:
        legacy_rule = Registrationpriorityrules.objects.get(name__exact=rule_name)
    except Registrationpriorityrules.DoesNotExist:
        return 0

    if not legacy_rule:
        return 0

    return legacy_rule.priorityincrement

def CalculateStudentPriority(current_priority=0, affiliation=None, emt_certification_expiration_date=None, student_record=None, student_jurisdiction=None, scheduled_course=None):


    if not affiliation:
        if student_record:
            affiliation = student_record.affiliation
        if not affiliation:
            return current_priority

    if not scheduled_course:
        return current_priority
        

    student_affiliation_number = affiliation.miemss_number

    if not student_jurisdiction:
        try:
            student_jurisdiction = Jurisdictions.objects.get(number__exact=student_affiliation_number[:2])
        except Jurisdictions.DoesNotExist:
            student_jurisdiction = None
        
    if not student_jurisdiction:
        return current_priority
        
    if affiliation.name == u'Affiliation Unknown': 
        return current_priority

    student_region_number = student_jurisdiction.mfri_region_number

    if scheduled_course.use_legacy_region_priority and student_region_number == scheduled_course.legacy_host_region.regionnumber:
        current_priority += GetRegistrationPriorityIncrement(rule_name=u'Region')
        
    if scheduled_course.use_host_agency_priority and affiliation == scheduled_course.host_agency:

        host_registrations = []
        if scheduled_course.hostregistrations < scheduled_course.hostreservations: 

            try:
                host_registrations = Preregistrations.objects.filter(scheduled_course__exact=scheduled_course, affiliation__exact=affiliation) 
            except Preregistrations.DoesNotExist:
                host_registrations = []

        if host_registrations and len(host_registrations) > 0:
            if scheduled_course.hostregistrations < scheduled_course.hostreservations: 
                current_priority += GetRegistrationPriorityIncrement(rule_name=u'Host Agency')
        else:
            current_priority += GetRegistrationPriorityIncrement(rule_name=u'Host Agency')


    if scheduled_course.use_jurisdiction_priority and student_jurisdiction == scheduled_course.jurisdiction:
        current_priority += GetRegistrationPriorityIncrement(rule_name=u'Jurisdiction')

    if scheduled_course.use_instate_priority and affiliation.county.id not in (27,28,29,30,31):
        current_priority += GetRegistrationPriorityIncrement(rule_name=u'In State')


    if scheduled_course.category_and_level == u'EMS-203' and emt_certification_expiration_date:
        if diff_month(emt_certification_expiration_date, scheduled_course.start_date) <= 6:
            current_priority += GetRegistrationPriorityIncrement(rule_name=u'EMTB Expiration in 6 Months')

    if scheduled_course.use_emt_certification_expiration_priority:
        outstanding_flags = Studentflagassignments.objects.filter(student_record__exact=student_record).exclude(expiration_date__lte=datetime.datetime.now())

        if len(outstanding_flags) > 0:
            current_priority += GetRegistrationPriorityIncrement(rule_name=u'Student Flagged')
        
    return current_priority


def GetPreRegistrationStatus(status_id=None, status_name=None):
    
    if status_id:
        try:
            default_status = Preregistrationstatus.objects.get( pk=status_id )
            return default_status
        except Preregistrationstatus.DoesNotExist:
            pass
    elif status_name:
        try:
            default_status = Preregistrationstatus.objects.get( name__iexact=status_name )
            return default_status
        except Preregistrationstatus.DoesNotExist:
            pass
    
    try:
        default_status = Preregistrationstatus.objects.get( pk=2 )
    except Preregistrationstatus.DoesNotExist:
        return None
    return default_status


def GetCounty(county_id=None, county_name=None):
    
    if county_id:
        try:
            default_county = Jurisdictions.objects.get( pk=county_id )
            return default_county
        except Jurisdictions.DoesNotExist:
            pass
    elif county_name:
        try:
            default_county = Jurisdictions.objects.get( name__iexact=county_name )
            return default_county
        except Jurisdictions.DoesNotExist:
            pass
    
    try:
        default_county = Jurisdictions.objects.get( pk=30 )
    except Jurisdictions.DoesNotExist:
        return None
    return default_county

def GetStudentgradeOption(option_id=None, option_name=None):
    
    if option_id:
        try:
            default_option = Studentgradeoptions.objects.get( pk=option_id )
            return default_option
        except Studentgradeoptions.DoesNotExist:
            pass
    elif option_name:
        try:
            default_option = Studentgradeoptions.objects.get( name__iexact=option_name )
            return default_option
        except Studentgradeoptions.DoesNotExist:
            pass
    
    try:
        default_option = Studentgradeoptions.objects.get( pk=1 )
    except Studentgradeoptions.DoesNotExist:
        return None
    return default_option

def GetRegistrationStatusForGrade(grade=None):
    if not grade:
        return GetRegistrationStatus(status_id=1)
    
    if grade.is_passing:
        return GetRegistrationStatus(status_id=9)
    else:
        return GetRegistrationStatus(status_id=19)

def GetRegistrationStatus(status_id=None, status_name=None):
    
    if status_id:
        try:
            default_status = Registrationstatus.objects.get( pk=status_id )
            return default_status
        except Registrationstatus.DoesNotExist:
            pass
    elif status_name:
        try:
            default_status = Registrationstatus.objects.get( name__iexact=status_name )
            return default_status
        except Registrationstatus.DoesNotExist:
            pass
    
    try:
        default_status = Registrationstatus.objects.get( pk=3 )
    except Registrationstatus.DoesNotExist:
        return None
    return default_status

def GetRegisteredStudents(scheduled_course=None, pk=None, log_number=None):

    if log_number:
        find_course_result = FindCourseFromLogNumber(log_number=log_number, check_in_use=True)
        
        scheduled_course = None
        if find_course_result:
            scheduled_course_list = find_course_result.get('scheduled_courses', None)
            if scheduled_course_list:
                scheduled_course = scheduled_course_list[0]
    elif pk:
        try:
            scheduled_course = Scheduledcourses.objects.get(pk=pk)
        except Scheduledcourses.DoesNotExist:
            return []

    if not scheduled_course:
        return []
        
    try:
        registered_students = Studentregistration.objects.filter(scheduled_course__exact=scheduled_course).order_by('student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')
    except Studentregistration.DoesNotExist:
        registered_students = []

    return registered_students


def GetToScheduledCourse(log_number=None):

    if not log_number:
        return {'student_registration_record': None, 'message': u'No to log number'}

    find_course_result = FindCourseFromLogNumber(log_number=log_number, check_in_use=True)

    to_scheduled_course = None
    if find_course_result:
        scheduled_course_list = find_course_result.get('scheduled_courses', None)
        if scheduled_course_list:
            to_scheduled_course = scheduled_course_list[0]

    return to_scheduled_course


def CreateNewStudentRegistrationFromRegistration(user=None, old_student_registration_id=None, to_scheduled_course=None, update_registered_count=True):

    if not user:
        return {'student_registration_record': None, 'message': u'No user record'}

    if not old_student_registration_id:
        return {'student_registration_record': None, 'message': u'No from student registration'}

    if not to_scheduled_course:
        return {'student_registration_record': None, 'message': u'No to scheduled course'}

    try:
        old_student_registration = Studentregistration.objects.get(pk=old_student_registration_id)
    except Studentregistration.DoesNotExist:
        old_student_registration = None

    if not old_student_registration:
        return {'student_registration_record': None, 'message': u'Can not find from student registration record'}

        
    new_student_registration_record = Studentregistration(
        student_record = old_student_registration.student_record,
        scheduled_course = to_scheduled_course,
        affiliation = old_student_registration.affiliation, 
        status = GetRegistrationStatus(),
        grade = GetStudentgradeOption(),
        grade_text = GetStudentgradeOption().name,
        percentage_score = u'',
        grade_note = u'',
        registration_status  = GetRegistrationStatus(),
        lastchangeby = user, 
        lastchange = datetime.datetime.now(), 
        createdby = user, 
        created = datetime.datetime.now()
        ) 

    try:
        new_student_registration_record.save()
    except Exception as e:
        return {'student_registration_record': None, 'message': u'Student registration record not created: %s' % (e)}

    if update_registered_count:
        to_scheduled_course.registered_count += 1
        to_scheduled_course.save()
        
    return {'student_registration_record': new_student_registration_record, 'message': u'Record created'}



def CreateNewStudentPreRegistrationFromRegistration(user=None, old_student_registration_id=None, to_scheduled_course=None):

    if not user:
        return {'student_registration_record': None, 'message': u'No user record'}

    if not old_student_registration_id:
        return {'student_registration_record': None, 'message': u'No from student registration'}

    if not to_scheduled_course:
        return {'student_registration_record': None, 'message': u'No to scheduled course'}

    try:
        old_student_registration = Studentregistration.objects.get(pk=old_student_registration_id)
    except Studentregistration.DoesNotExist:
        old_student_registration = None

    if not old_student_registration:
        return {'student_registration_record': None, 'message': u'Can not find from student registration record'}

    
    priority = CalculateStudentPriority(affiliation=old_student_registration.affiliation, 
                                        emt_certification_expiration_date=old_student_registration.student_record.certificationexpirationdate, 
                                        student_record=old_student_registration.student_record, 
                                        student_jurisdiction=old_student_registration.affiliation.county, 
                                        scheduled_course=to_scheduled_course)
        
    new_student_registration_record = Preregistrations(
        student_record = old_student_registration.student_record,
        scheduled_course = to_scheduled_course,
        log_number = to_scheduled_course.log_number,

        birth_date = old_student_registration.student_record.birthdate,


        title         = old_student_registration.student_record.title,
        firstname     = old_student_registration.student_record.firstname,
        middlename    = old_student_registration.student_record.middlename,
        lastname      = old_student_registration.student_record.lastname,
        suffix        = old_student_registration.student_record.suffix,

        address1 = old_student_registration.student_record.address1,
        address2 = old_student_registration.student_record.address2,
#        apt      = old_student_registration.student_record.apt,
        city     = old_student_registration.student_record.city,
        state    = old_student_registration.student_record.state,
        postcode = old_student_registration.student_record.postcode,

        county = old_student_registration.student_record.county,

        primary_phone_number = old_student_registration.student_record.primaryphonenumber,
        secondary_phone_number = old_student_registration.student_record.secondaryphonenumber,

        email = old_student_registration.student_record.primaryemail,

        status = GetPreRegistrationStatus(),

        student_registration = None,
        
        priority = priority,
        affiliation = old_student_registration.affiliation, 
        emt_certification_expiration_date = old_student_registration.student_record.certificationexpirationdate,

        lastchangeby = user, 
        lastchange = datetime.datetime.now(), 
        createdby = user, 
        created = datetime.datetime.now()
        ) 

    new_student_registration_record.ssn_clear = old_student_registration.student_record.ssn_clear
    new_student_registration_record.epins_clear = old_student_registration.student_record.epins_clear

    try:
        new_student_registration_record.save()
    except Exception as e:
        return {'student_registration_record': None, 'message': u'Student pre-registration record not created: %s' % (e)}

    return {'student_registration_record': new_student_registration_record, 'message': u'Record created'}


def GetStudentRegistration(scheduled_course=None, student_record=None):

    if not scheduled_course:
        return None

    if not student_record:
        return None

    try:
        student_registration = Studentregistration.objects.get(scheduled_course__exact=scheduled_course, student_record__exact=student_record)
    except Studentregistration.DoesNotExist:
        return None
    except Studentregistration.MultipleObjectsReturned:
        return None

    return student_registration
    
def CheckIfStudentRegisteredInCourse(scheduled_course=None, student_record=None):


    if GetStudentRegistration(scheduled_course=scheduled_course, student_record=student_record):
        return True
    
    return False


def BuildStudentRegistrationDict(course_registrations=None):

    if not course_registrations:
        return {}
        
    registration_dict = {}

    for student_registration in course_registrations:
    
        try:
            if not student_registration.student_record:
                continue
        except Studentrecords.DoesNotExist:
            continue
            
        record_key = student_registration.student_record.ssn_clear

        if not record_key:
            continue

        registration_dict[record_key] = {
        'registration_record': student_registration
        }
        
    return registration_dict

def CheckForDuplicateStudentRegistrations(from_course_registrations=None, to_course_registrations=None):

    from_registrations_dict = BuildStudentRegistrationDict(course_registrations=from_course_registrations)
    to_registrations_dict = BuildStudentRegistrationDict(course_registrations=to_course_registrations)
    
    from_duplicate_registration_flag = []
    to_duplicate_registration_flag = []

    for from_student_record in from_course_registrations:
        if to_registrations_dict.get(from_student_record.student_record.ssn_clear, None):
            from_duplicate_registration_flag.append(True)
        else:
            from_duplicate_registration_flag.append(False)

    for to_student_record in to_course_registrations:
        if from_registrations_dict.get(to_student_record.student_record.ssn_clear, None):
            to_duplicate_registration_flag.append(True)
        else:
            to_duplicate_registration_flag.append(False)

    return {'from_duplicate_registration_flag': from_duplicate_registration_flag, 'to_duplicate_registration_flag': to_duplicate_registration_flag}



def GetPreRegisteredList(scheduled_course=None, sort_by_name=False):

    student_list = Preregistrations.objects.filter(scheduled_course__exact=scheduled_course,  status__in=['2', '6', '7']).order_by('status__sortorder', '-priority', 'created')

    pre_reg_counter = 1
    pre_reg_list = []
    pre_reg_wait_list = []

    for pre_registered_student in student_list:
        if pre_registered_student.status.id != 1:
            if pre_reg_counter > scheduled_course.max_students:
                pre_reg_wait_list.append(pre_registered_student)
            else:
                pre_reg_list.append(pre_registered_student)
        pre_reg_counter += 1

    if sort_by_name:
        pre_reg_list = sorted(pre_reg_list, key=attrgetter('lastname', 'firstname', 'middlename', 'suffix')) 
        pre_reg_wait_list = sorted(pre_reg_wait_list, key=attrgetter('lastname', 'firstname', 'middlename', 'suffix')) 

    return {'registered': pre_reg_list, 'wait': pre_reg_wait_list}

def StudentRegistrationSearch(scheduled_course=None, student_registration=None):

    if not scheduled_course:
        return None

    if not student_registration:
        return None

    if not student_registration.student_record:
        return None

    try:
        response_list = list(Studentregistration.objects.raw('SELECT SReg.ID as id FROM CourseDescriptions AS CD, ScheduledCourses AS SC, StudentRegistration AS SReg, StudentRecords AS SRec, StudentGradeOptions AS SGO, RegistrationStatus AS RS WHERE (AES_DECRYPT(SRec.IDNumber, %s) like %s) AND (SReg.SchedCourseID = SC.ID) AND (SC.CourseID = CD.ID) AND (CD.Category = %s) AND (CD.Level = %s) AND (SReg.StudentID = SRec.ID) AND (SReg.GradeID = SGO.ID) AND (SReg.StatusID = RS.ID) AND (SReg.StatusID != 9) AND (SReg.SchedCourseID != %s)', (SRecEncryptKeyS(), student_registration.student_record.ssn_clear, scheduled_course.category, scheduled_course.level, scheduled_course.id))) #20210222
    except Studentregistration.DoesNotExist:
        return None
            
    if not response_list: 
        return None


    return response_list

def SavePreRegistrationRecord(user=None, scheduled_course=None, existing_student_record=None, new_registration_record=None, priority=0):
    
    new_student_registration_record = Preregistrations(
        student_record = existing_student_record,
        scheduled_course = scheduled_course,
        log_number = scheduled_course.log_number,

        birth_date = new_registration_record.birth_date,

        #title         = new_registration_record.title,
        firstname     = new_registration_record.first_name_tc,
        middlename    = new_registration_record.middle_name_tc,
        lastname      = new_registration_record.last_name_tc,
        suffix        = new_registration_record.suffix_tc,

        address1 = new_registration_record.address1,
        address2 = new_registration_record.address2,
#        apt      = old_student_registration.student_record.apt,
        city     = new_registration_record.city,
        state    = new_registration_record.state,
        postcode = new_registration_record.postcode,

        county = new_registration_record.affiliation.county,

        country = new_registration_record.country,

        primary_phone_number = new_registration_record.primary_phone_number,
        secondary_phone_number = new_registration_record.secondary_phone_number,

        email = new_registration_record.email_address,

        status = GetPreRegistrationStatus(),


        is_web_reg = True, 
        is_late_registration = new_registration_record.is_late_registration,
        owes_course_fee = new_registration_record.owes_course_fee,
        registration_approved_by = new_registration_record.approved_by,
        registration_approved_by_username = new_registration_record.approved_by_username,
        registration_approved_on = new_registration_record.approved_on,
        book_fee_acknowledged = new_registration_record.book_fee_acknowledged,
        book_fee_agency_pay = new_registration_record.book_fee_agency_pay,


        student_registration = None,
        
        priority = priority,
        affiliation = new_registration_record.affiliation, 
        emt_certification_expiration_date = new_registration_record.emt_expiration_date,

        lastchangeby = user, 
        lastchange = datetime.datetime.now(), 
        createdby = user, 
        created = datetime.datetime.now()
        ) 

    new_student_registration_record.ssn_clear = new_registration_record.ssn_clear
    new_student_registration_record.epins_clear = new_registration_record.epins_clear
    new_student_registration_record.mfri_student_number = new_registration_record.mfri_student_number #20210405


    try:
        new_student_registration_record.save()
    except Exception as e:
        return {'student_registration_record': None, 'message': u'Student pre-registration record not created: %s' % (e)}

    return {'student_registration_record': new_student_registration_record, 'message': u'Student pre-registration record created'}

