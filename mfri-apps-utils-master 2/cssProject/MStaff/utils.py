
import re
import json
import base64
import time #20210828
import datetime #20210828
from decimal import Decimal #20190815

from AppsAdmin.dbk import StaffEncryptKeyU

from MStaff.models import *

from MFRI_Utils.data_validate import validate_last_name, validate_university_id_number

def ValidateStaffIdentifier(uid=None, last_name=None): 
    """
    Validate staff UID and Last Name, return dictionary with status message
    
    'StatusMessage': 'text of message',
    'ResponseCode': return code < 0 on error. > 0 if correct
    """
    
    if not uid:
        data_to_return = {  'StatusMessage': 'No University ID given',
                            'ResponseCode': -10,
                            'no_uid': True,
                            'no_last_name': False,
                        }    
            
        return data_to_return
    
    uid_validation_result = validate_university_id_number(uid)

    if uid_validation_result['ResponseCode'] != 1:
        data_to_return = {  'StatusMessage': uid_validation_result['StatusMessage'],
                            'ResponseCode': -11,
                            'no_uid': True,
                            'no_last_name': False,
                        }    
            
        return data_to_return
    
    if not last_name:
        data_to_return = {  'StatusMessage': 'No last name given',
                            'ResponseCode': -12,
                            'no_uid': False,
                            'no_last_name': True,
                        }    
    
        return data_to_return

    lastname_validation_result = validate_last_name(last_name)

    if lastname_validation_result['ResponseCode'] != 1:
        data_to_return = {  'StatusMessage': lastname_validation_result['StatusMessage'],
                            'ResponseCode': -13,
                            'no_uid': False,
                            'no_last_name': True,
                         }
        
        return data_to_return

    data_to_return = {  'StatusMessage': 'No Errors',
                        'ResponseCode': 1,
                        'no_uid': False,
                        'no_last_name': False,
                     }

    return data_to_return



def GetStaffObj(uid=None, last_name=None):
    
    if not uid:
        return None
    
    if not last_name or len(last_name) == 0:
        try:
            response_obj = MfriInstructors.objects.raw('SELECT id FROM MfriInstructors WHERE (AES_DECRYPT(UniversityIDNumber, %s) like %s)', [StaffEncryptKeyU(), uid])

        except MfriInstructors.MultipleObjectsReturned:
            return None

        except MfriInstructors.DoesNotExist:
            return None
    else:
        try:
            response_obj = MfriInstructors.objects.raw('SELECT id FROM MfriInstructors WHERE (AES_DECRYPT(UniversityIDNumber, %s) like %s) AND (LastName like %s)', [StaffEncryptKeyU(), uid,last_name])
        
        except MfriInstructors.MultipleObjectsReturned:
            return None
        
        except MfriInstructors.DoesNotExist:
            return None

    return response_obj
    

def GetStaffRecord(uid=None, last_name=None):
    """
    return staff object in dict.
    
    'StatusMessage': 'text of message',
    'ResponseCode': return code < 0 on error. staff record ID if correct
    'StaffData': StaffObject or None on error
    """

    validation_result = ValidateStaffIdentifier(uid=uid, last_name=last_name)

    if validation_result['ResponseCode'] < 1 and validation_result['no_uid']:
        data_to_return = {  'StatusMessage': 'Error, invalid UID: %s' % (validation_result['StatusMessage']),
                            'ResponseCode': -24,
                            'StaffData': None
                         }    

        return data_to_return

    response_obj = GetStaffObj(uid, last_name)

    if not response_obj:
        data_to_return = {  'StatusMessage': 'Error, the database server did not find a matching record in employee database',
                            'ResponseCode': -20,
                            'StaffData': None
                         }    
        return data_to_return
    
    found_record = None
    if len(list(response_obj)) > 0:
        found_record = response_obj[0]
    else: #'Error, no matching record found in employee database, one was expected but the list was empty',
        data_to_return = {  'StatusMessage': 'No matching record found in employee database',
                            'ResponseCode': -22,
                            'StaffData': None
                         }    
        return data_to_return
        
    if not found_record:
        data_to_return = {  'StatusMessage': 'Error, no matching record found in employee database but one was expected',
                            'ResponseCode': -23,
                            'StaffData': None
                            }
        return data_to_return

    found_status_message = found_record.employmentstatus.name
    record_count = len(list(response_obj))
    

    if record_count > 1:
        found_status_message = u'%s Warning: %d records were found with this UID and Last Name' % (found_record.employmentstatus.name, record_count)

    data_to_return = {  'StatusMessage': found_status_message,
                        'ResponseCode': found_record.id,
                        'StaffData': found_record
                        }
    
    return data_to_return


