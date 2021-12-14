
import re
import datetime
import json
import base64

from MFRI_Utils.data_validate import validate_address

from MStaff.utils import SplitName, validate_name, validate_first_name
from MFRI_Utils.data_validate import validate_ssn, validate_last_name, validate_state_provider_number, validate_nfa_sid_number, validate_birth_date, validate_student_address, validate_student_email_address

from SRec.utils import Student_Record_SSN_Query, GetDefaultStudentFlagStatus, find_student_by_name, FindDuplicateStudent

def ValidateStudentRecord(student_record=None, look_for_duplicate_mfri_student_number=True, look_for_duplicate_ssn=True, look_for_duplicate_nfa_sid=True, look_for_duplicate_state_provider_number=True):
    
    if not student_record:
        return {
               'name_error': u'',
               'ssn_error': u'',
               'state_provider_number_error': u'',
               'nfa_sid_number_error': u'',
               'birth_date_error': u'',
               'address1_error': u'',
               'address2_error': u'',
               'city_error': u'',
               'state_error': u'',
               'postcode_error': u'',
               'country_error': u'',
               'email_address_error': u'',
               'duplicate_ssn_list': u'',
               'duplicate_state_provider_number_list': u'',
               'duplicate_nfa_sid_number_list': u'',
               'merge_ssn_record_id_string': u'',
               'merge_state_provider_number_record_id_string': u'',
               'merge_nfa_sid_number_record_id_string': u'',
               'note': u'',
               'error_found': True,
               #'user_read_permission': user_read_permission,
               #'user_write_permission': user_write_permission,
               #'user_grade_read_permission': user_grade_read_permission,
               }

    error_found = False
    
    name_validation_result = validate_name(full_name=student_record.full_name)

    if name_validation_result.get('ResponseCode', 0) < 1:
        error_found = True

    ssn_validation_result = validate_ssn(ssn=student_record.ssn_clear, accept_last_five=False, accept_null_ssn=False)

    if ssn_validation_result.get('ResponseCode', 0) < 1:
        error_found = True

    state_provider_number_validation_result = validate_state_provider_number(epins=student_record.epins_clear)

    if state_provider_number_validation_result.get('ResponseCode', 0) < 1:
        error_found = True

    nfa_sid_number_validation_result = validate_nfa_sid_number(nfa_sid_number=student_record.nfa_sid)

    if nfa_sid_number_validation_result.get('ResponseCode', 0) < 1:
        error_found = True

    birth_date_validation_result = validate_birth_date(birth_date=student_record.birth_date)

    if birth_date_validation_result.get('ResponseCode', 0) < 1:
        error_found = True

    address_validation_result = validate_student_address(address1=student_record.address1, 
                                                 address2=student_record.address2, 
                                                 city=student_record.city, 
                                                 state=student_record.state, 
                                                 post_code=student_record.postcode, 
                                                 country=student_record.country)
    
    if len(address_validation_result.get('address1_error', u'')) > 0 or len(address_validation_result.get('address2_error', u'')) > 0 or len(address_validation_result.get('city_error', u'')) > 0 or len(address_validation_result.get('country_error', u'')) > 0 or len(address_validation_result.get('postcode_error', u'')) > 0 or len(address_validation_result.get('state_error', u'')) > 0:
        error_found = True

    email_address_validation_result = validate_student_email_address(email_address=student_record.email_address.get('Primary', student_record.email_address.get('Secondary', None)))

    if email_address_validation_result.get('ResponseCode', 0) < 1:
        error_found = True

    previous_registration_list = []

    duplicate_ssn_list = []
    merge_ssn_record_id_string = None

    if look_for_duplicate_ssn:
        if ssn_validation_result.get('ResponseCode', False):
            duplicate_ssn_list = FindDuplicateStudent(value_to_search=u'ssn', student_record=student_record) 
    
            merge_ssn_record_id_list = []
            merge_ssn_record_id_string = u''
            if duplicate_ssn_list:
                for duplicate_student_record in duplicate_ssn_list:
                    merge_ssn_record_id_list.append(str(duplicate_student_record.id))
                merge_ssn_record_id_string = ','.join(merge_ssn_record_id_list)
                error_found = True


    duplicate_state_provider_number_list = []
    merge_state_provider_number_record_id_string = None
    if look_for_duplicate_state_provider_number:
        if state_provider_number_validation_result.get('ResponseCode', False):
            duplicate_state_provider_number_list = FindDuplicateStudent(value_to_search=u'epins', student_record=student_record) 

            merge_state_provider_number_record_id_list = []
            merge_state_provider_number_record_id_string = u''
            if duplicate_state_provider_number_list:
                for duplicate_student_record in duplicate_state_provider_number_list:
                    merge_state_provider_number_record_id_list.append(str(duplicate_student_record.id))
                merge_state_provider_number_record_id_string = ','.join(merge_state_provider_number_record_id_list)
                error_found = True


    duplicate_nfa_sid_number_list = []
    merge_nfa_sid_number_record_id_string = None
    if look_for_duplicate_nfa_sid:
        if nfa_sid_number_validation_result.get('ResponseCode', False):
            duplicate_nfa_sid_number_list = FindDuplicateStudent(value_to_search=u'nfasid', student_record=student_record) 

            merge_nfa_sid_number_record_id_list = []
            merge_nfa_sid_number_record_id_string = u''
            if duplicate_nfa_sid_number_list:
                for duplicate_student_record in duplicate_nfa_sid_number_list:
                    merge_nfa_sid_number_record_id_list.append(str(duplicate_student_record.id))
                merge_nfa_sid_number_record_id_string = ','.join(merge_nfa_sid_number_record_id_list)
                error_found = True

    return {
            'name_error': name_validation_result.get('StatusMessage', u''),
            'ssn_error': ssn_validation_result.get('StatusMessage', u''),
            'state_provider_number_error': state_provider_number_validation_result.get('StatusMessage', u''),
            'nfa_sid_number_error': nfa_sid_number_validation_result.get('StatusMessage', u''),
            'birth_date_error': birth_date_validation_result.get('StatusMessage', u''),
            'address1_error': address_validation_result.get('address1_error', u''),
            'address2_error': address_validation_result.get('address2_error', u''),
            'city_error': address_validation_result.get('city_error', u''),
            'state_error': address_validation_result.get('state_error', u''),
            'postcode_error': address_validation_result.get('postcode_error', u''),
            'country_error': address_validation_result.get('country_error', u''),
            'email_address_error': email_address_validation_result.get('StatusMessage', u''),
            'duplicate_ssn_list': duplicate_ssn_list,
            'duplicate_state_provider_number_list': duplicate_state_provider_number_list,
            'duplicate_nfa_sid_number_list': duplicate_nfa_sid_number_list,
            'merge_ssn_record_id_string': merge_ssn_record_id_string,
            'merge_state_provider_number_record_id_string': merge_state_provider_number_record_id_string,
            'merge_nfa_sid_number_record_id_string': merge_nfa_sid_number_record_id_string,
            'note': u'',
            'error_found': error_found,
            #'user_read_permission': user_read_permission,
            #'user_write_permission': user_write_permission,
            #'user_grade_read_permission': user_grade_read_permission,
           }

def UpdateFormFieldErrorList(form_errors=None, field_name=None, new_error_list=None):

    if not field_name:
        return form_errors
    
    if not new_error_list:
        return form_errors
    
    if field_name in form_errors:
        field_error_list = form_errors.get(field_name, [])

        field_error_list.extend(new_error_list)

        form_errors[field_name] = field_error_list
    else:
        form_errors[field_name] = new_error_list
        
    return form_errors
    
    
    
    


