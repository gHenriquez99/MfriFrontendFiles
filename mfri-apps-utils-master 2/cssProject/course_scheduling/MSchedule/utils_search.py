
import json
import base64
import time
import datetime

from AppsAdmin.utils import legacy_app_read_permission

from MOffices.models import MfriOffices

from MStaff.utils import GetStaffRecord

from MSchedule.models import *

def validate_log_number_parts(category=None, level=None, funding_source_code=None, section_number=None, fiscal_year=None, course_code=None):

    if not course_code:
        if not category:
            return {'ResponseCode': -1, 'StatusMessage': 'Null Category'}

        if len(category) < 2:
            return {'ResponseCode': -1, 'StatusMessage': 'No Category'}
        
        if len(category) > 4:
            return {'ResponseCode': -1, 'StatusMessage': 'Category too long'}
        
        if category.isdigit(): ####
            return {'ResponseCode': -1, 'StatusMessage': 'Category must be a be a text string'}
        
        if not level:
            return {'ResponseCode': -1, 'StatusMessage': 'Null Level'}
        
        if not level.isdigit(): ####
            return {'ResponseCode': -4, 'StatusMessage': 'Level must be a number'}
        
        if len(str(level)) != 3: 
            return {'ResponseCode': -5, 'StatusMessage': 'Level must be 3 digits long'}
        
        if funding_source_code and len(funding_source_code) > 0:
            if funding_source_code.isdigit(): ####
                return {'ResponseCode': -6, 'StatusMessage': 'Function Source Code Number must be a letter'}
    else:
        if len(course_code) < 1:
            return {'ResponseCode': -1, 'StatusMessage': 'No Category'}
        
        if len(course_code) > 11: #longest course code in course descriptions table
            return {'ResponseCode': -1, 'StatusMessage': 'Category too long'}
        
        
    if not section_number.isdigit(): ####
        return {'ResponseCode': -7, 'StatusMessage': 'Section Number must be a number'}
    
    if not fiscal_year:
        return {'ResponseCode': -1, 'StatusMessage': 'Null Fiscal Year'}

    if not fiscal_year.isdigit(): ####
        return {'ResponseCode': -8, 'StatusMessage': 'Fiscal Year must be a number'}
    
    if len(str(fiscal_year)) != 4:
        if len(str(fiscal_year)) == 2:
            if fiscal_year >= 30 and fiscal_year <= 99:
                fiscal_year = "19" + str(fiscal_year)
            else:
                fiscal_year = "20" + str(fiscal_year)
        else:
            return {'ResponseCode': -9, 'StatusMessage': 'Fiscal Year is an invalid value, must be either 2 or 4 digits'}
    
    return {'ResponseCode': 1, 'StatusMessage': 'Log Number Syntax OK'}
    

def parse_log_number(log_number=None):
    """
    split log number into parts return dict with parts
    """

    if not log_number:
        return {'ResponseCode': -1, 'StatusMessage': 'Null Log Number ID', 'category':'', 'level':'', 'funding_source_code':'', 'section_number':'', 'fiscal_year':'', 'course_code': ''}

    if len(log_number) == 0:
        return {'ResponseCode': -2, 'StatusMessage': 'No Log Number ID', 'category':'', 'level':'', 'funding_source_code':'', 'section_number':'', 'fiscal_year':'', 'course_code': ''}

    log_number_parts = log_number.split('-')

    log_number_parts_count = len(log_number_parts) 

    if log_number_parts_count > 2 and log_number_parts[0] == "ID" and log_number_parts[1].isalpha():
        log_number_parts[0] += "-" + log_number_parts[1]
        
        list_counter = 1

        while list_counter+1 < log_number_parts_count:
            log_number_parts.insert(list_counter, log_number_parts.pop(list_counter+1))
            list_counter += 1
        
        log_number_parts = log_number_parts[:log_number_parts_count-1]
        log_number_parts_count = len(log_number_parts) 
        #assert False
            
           
    if log_number_parts_count < 3 or log_number_parts_count > 4:
        return {'ResponseCode': -14, 'StatusMessage': u'Invalid Log Number format. Field Count %d' % (log_number_parts_count), 'category':'', 'level':'', 'funding_source_code':'', 'section_number':'', 'fiscal_year':'', 'course_code': ''}
    
    if log_number_parts_count == 4:
        category = log_number_parts[0]
        level = log_number_parts[1]
        funding_source_code_section_number = log_number_parts[2]
        fiscal_year = log_number_parts[3]
        
        
        if len(fiscal_year) == 2:
            if int(fiscal_year) >= 30 and int(fiscal_year) <= 99:
                fiscal_year = "19" + str(fiscal_year)
            else:
                fiscal_year = "20" + str(fiscal_year)
            
        if len(funding_source_code_section_number) > 3:
            funding_source_code = funding_source_code_section_number[0:1]
            section_number = funding_source_code_section_number[1:]
        else:
            funding_source_code = ''
            section_number = funding_source_code_section_number

        validate_response = validate_log_number_parts(category=category, level=level, funding_source_code=funding_source_code, section_number=section_number, fiscal_year=fiscal_year)

        return {'ResponseCode': validate_response['ResponseCode'], 'StatusMessage': validate_response['StatusMessage'], 'category': category, 'level': level, 'funding_source_code': funding_source_code, 'section_number': section_number, 'fiscal_year': fiscal_year, 'course_code': None}
            
    else:
        course_code = log_number_parts[0]
        section_number = log_number_parts[1]
        fiscal_year = log_number_parts[2]
        
        if len(fiscal_year) == 2:
            if int(fiscal_year) >= 30 and int(fiscal_year) <= 99:
                fiscal_year = "19" + str(fiscal_year)
            else:
                fiscal_year = "20" + str(fiscal_year)
            
        funding_source_code = None
        category = None
        level = None

        validate_response = validate_log_number_parts(course_code=course_code, section_number=section_number, fiscal_year=fiscal_year)

        return {'ResponseCode': validate_response['ResponseCode'], 'StatusMessage': validate_response['StatusMessage'], 'course_code': course_code, 'category': category, 'level': level, 'funding_source_code': funding_source_code, 'section_number': section_number, 'fiscal_year': fiscal_year}
        
        

def verify_log_number(log_number=None, category=None, level=None, funding_source_code=None, section_number=None, fiscal_year=None, course_code=None, check_in_use=True):
    """
    Tests log number for correct syntax and then checks to see if it is currently in use.
    """
    find_results = find_course_from_log_number(log_number=log_number, category=category, level=level, funding_source_code=funding_source_code, section_number=section_number, fiscal_year=fiscal_year, course_code=course_code, check_in_use=check_in_use)

    if not check_in_use:
        return {'ResponseCode': find_results['ResponseCode'], 'StatusMessage': find_results['StatusMessage']}

    if find_results['ResponseCode'] > 0:
        return {'ResponseCode': find_results['ResponseCode'], 'StatusMessage': 'Log Number Found'}

    return {'ResponseCode': -1, 'StatusMessage': 'Log Number Not Found'}

def find_course_from_log_number(log_number=None, category=None, level=None, funding_source_code=None, section_number=None, fiscal_year=None, course_code=None, check_in_use=True):
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

