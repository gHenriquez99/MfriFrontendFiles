
import json
import base64
import time
import datetime

from MOffices.models import MfriOffices

from MSchedule.models import *

from MFRI_Utils.log_number_validation import validate_log_number_parts, parse_log_number

def ScheduledCourseRecord(log_number=None, category=None, level=None, funding_source_code=None, section_number=None, fiscal_year=None):#20200114

    scheduled_course = None
    
    find_course_result = FindCourseFromLogNumber(log_number=log_number, category=category, level=level, funding_source_code=funding_source_code, section_number=section_number, fiscal_year=fiscal_year)
       
    if find_course_result:
        if find_course_result['ResponseCode'] > 0:
            course_list = find_course_result.get('scheduled_courses',  [None,])
            scheduled_course = course_list[0]
            
    return scheduled_course

def FindCourseFromLogNumber(log_number=None, category=None, level=None, funding_source_code=None, section_number=None, fiscal_year=None, course_code=None, check_in_use=True):
    """
    Tests log number for correct syntax and then checks to see if it is currently in use.
    """
    
    if log_number:
        log_number = log_number.upper()
        log_number_parse_response = parse_log_number(log_number=log_number)
        course_code=log_number_parse_response.get('course_code')
        category=log_number_parse_response.get('category')
        level=log_number_parse_response.get('level')
        funding_source_code=log_number_parse_response.get('funding_source_code')
        section_number=log_number_parse_response.get('section_number')
        fiscal_year=log_number_parse_response.get('fiscal_year')
    else:
        if not (category or level or funding_source_code or section_number or fiscal_year or course_code):
            return {'ResponseCode': 0, 'StatusMessage': 'No Log Number given.'}
        
        if course_code:
            course_code = course_code.upper()
            
        if category:
            category = category.upper()
            
        if level:
            level = level.upper()

        if funding_source_code:
            funding_source_code = funding_source_code.upper()
            
        validate_response = validate_log_number_parts(category=category, level=level, funding_source_code=funding_source_code, section_number=section_number, fiscal_year=fiscal_year, course_code=course_code)
        log_number_parse_response = {'ResponseCode': validate_response['ResponseCode'], 'StatusMessage': validate_response['StatusMessage'], 'category': category, 'level': level, 'funding_source_code': funding_source_code, 'section_number': section_number, 'fiscal_year': fiscal_year, 'course_code': course_code}
    
    if log_number_parse_response['ResponseCode'] < 1:
        return {'ResponseCode': log_number_parse_response['ResponseCode'], 'StatusMessage': log_number_parse_response['StatusMessage']}


    if not check_in_use:
        return {'ResponseCode': log_number_parse_response['ResponseCode'], 'StatusMessage': log_number_parse_response['StatusMessage']}

    try:
        if course_code:
            scheduled_courses = Scheduledcourses.objects.filter(course_description__course_code__iexact=course_code, section_number = section_number, fiscal_year = fiscal_year)
        else:
            scheduled_courses = Scheduledcourses.objects.filter(course_description__category__iexact=category, course_description__level__iexact=level, section_number = section_number, fiscal_year = fiscal_year)
    except Exception as e:
        return {'StatusMessage': u'Log Number Validation Error: %s' % (e),
                'ResponseCode': -99}
        
    if len(scheduled_courses) == 1:
        return {'ResponseCode': len(scheduled_courses), 'StatusMessage': 'One Course Found ', 'scheduled_courses': scheduled_courses}
    elif len(scheduled_courses) > 1:
        return {'ResponseCode': len(scheduled_courses), 'StatusMessage': 'Multiple Courses Found ', 'scheduled_courses': scheduled_courses}

    return {'ResponseCode': -1, 'StatusMessage': 'Log Number Not Found'}

