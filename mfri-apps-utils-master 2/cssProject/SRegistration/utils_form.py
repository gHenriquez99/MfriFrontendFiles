
import re
import datetime
import json
import base64

from MFRI_Utils.data_encode import decode_context, encode_context


def BuildRadioButtonCourseChoices(online_course_list=None):
    
    if not online_course_list:
        return []
    
    list_box_options = []

    for course in online_course_list:
        course_name = course.get('Name', None)
        if course_name and len(course_name.strip()) > 0:
            course_log_number = course.get('ExternalId', None)
            show_log_number = False
            if course_log_number and len(course_log_number.strip()) > 0:
                log_number_index = course_name.find(course_log_number)
                if log_number_index < 0:
                    show_log_number = True
                    course_name = course_name.title()
                    course_log_number = course_log_number.upper()
                else:
                    course_name_part_1 = course_name[:log_number_index]
                    course_name_part_2 = course_name[log_number_index:]
                    course_name = course_name_part_1.title() + course_name_part_2.upper()
                
            if show_log_number:
                list_box_options.append([course.get('Id', u''), u'%s %s' % (course_name, course_log_number)])
            else:
                list_box_options.append([course.get('Id', u''), course_name])

    return list_box_options

def GetAdminAccountToken():
    return u'lms_admin_2017'

def GetInstructorAccountToken():
    return u'inst_lms_2017'

def GetAccountToken(encode_token=True, is_admin=True, is_instructor=False):
    
    if is_admin:
        token_value = GetAdminAccountToken()
    elif is_instructor:
        token_value = GetInstructorAccountToken()
    else:
        return None
    
    if encode_token:
        return encode_context(context_data=token_value)

    return token_value


def ValidateInstructorToken(token=None, encode_token=True, is_admin=True, is_instructor=False):

    if not token or len(token) == 0:
        return None

    token_value = None
    if encode_token:
        token_value = decode_context(raw_context=encode_token)
    else:
        token_value = encode_token
    
    if is_admin:
        if token_value == GetAdminAccountToken():
            return True
        else:
            return False
    elif is_instructor:
        if token_value == GetInstructorAccountToken():
            return True
        else:
            return False

    return False
    
#def is_duplicate_vehicle_name(current_vehicle_record=None, vehicle_name=None):
#    
#    if not vehicle_name:
#        return False
#    
#    conflicting_vehicles = []
#    
#    if current_vehicle_record:
#        try:
#            conflicting_vehicles = RegistrationEvocVehicleType.objects.filter(name__iexact=vehicle_name ).exclude(pk=current_vehicle_record.id)
#        except RegistrationEvocVehicleType.DoesNotExist:
#            return False
#    else:
#        try:
#            conflicting_vehicles = RegistrationEvocVehicleType.objects.filter(name__iexact=vehicle_name )
#        except RegistrationEvocVehicleType.DoesNotExist:
#            return False
#    
#    if conflicting_vehicles.count() > 0:
#        return True
#    
#    return False
#

#def validate_vehicle_name(current_vehicle_record=None, vehicle_name=None, check_for_duplicate=True): 
#    """
#    vehicle name must be a unique identifier, must not contain the word "delete".  Max be 255 characters long.  Mixed digits and numbers.
#    returns True if name passes and 0 if there is an error.
#    """
#    data_to_return = {  'description': '',
#                        'has_error': False,
#                     }    
#
#    if not vehicle_name:
#        data_to_return['description'] = u'No Name Given.'
#        data_to_return['has_error'] = True
#
#        return data_to_return
#
#
#    vehicle_name_max_length = 255
#    
#    if findWholeWord(u'Delete')(vehicle_name):
#        data_to_return['description'] = u'This not a valid name. A name can not cantain the word "delete".  If there is an error with this record or if it is a duplicate mark the appropriate options.'
#        data_to_return['has_error'] = True
#
#        return data_to_return
#    
#    if len(vehicle_name) > vehicle_name_max_length:
#        data_to_return['description'] = u'Name must be less than %d characters.' % (vehicle_name_max_length)
#        data_to_return['has_error'] = True
#        
#        return data_to_return
##^[a-zA-Z0-9]$
##[0-9]{2}[0-9]{4}
#    if not re.compile("^[0-9a-zA-Z\-\&\,\.\: \'\(\)\/\#]+$").search(vehicle_name):
#        data_to_return['description'] = u'Name must only contain letters, numbers and certain punctuation such as "-&,.:\'()".'
#        data_to_return['has_error'] = True
#
#        return data_to_return
#    
#    if check_for_duplicate and is_duplicate_vehicle_name(current_vehicle_record=current_vehicle_record, vehicle_name=vehicle_name):
#        data_to_return['description'] = u'Name must be unique. This name is already being used by another listing.'
#        data_to_return['has_error'] = True
#        
#        return data_to_return
#    
#    return data_to_return
