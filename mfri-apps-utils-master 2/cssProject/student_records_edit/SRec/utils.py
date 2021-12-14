import os
import codecs
import string
import json
import time
import datetime
import re

from AppsAdmin.dbk import SRecEncryptKeyS

from SRec.models import *
from MSchedule.utils_search import validate_log_number_parts 
from MStaff.utils import validate_ssn, parse_last_name_suffix, validate_last_name, split_name, build_name_query

def validate_state_provider_number(epins=None): #Also known as EPINS number
    """
    State Provider Number must be 7 digits long.  Only digits allowed.
    returns 1 if epins passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    

    if not epins:
        data_to_return['StatusMessage'] = u'No State Provider Number.'
        data_to_return['ResponseCode'] = 0

        return data_to_return


    epins_length = 7

    if len(epins) != epins_length:
        data_to_return['StatusMessage'] = u'State Provider Number must be %d digits.' % (epins_length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    if not re.compile("^\d+$").search(epins):
        data_to_return['StatusMessage'] = u'State Provider Number must only contain digits.'
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    return data_to_return

def validate_nfa_sid_number(nfa_sid_number=None): 
    """
    State Provider Number must be 10 digits long.  Only digits allowed.
    returns 1 if nfa_sid_number passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    

    if not nfa_sid_number:
        data_to_return['StatusMessage'] = u'No NFA SID Number.'
        data_to_return['ResponseCode'] = 0

        return data_to_return


    nfa_sid_number_length = 10
    
    if len(nfa_sid_number) != nfa_sid_number_length:
        data_to_return['StatusMessage'] = u'NFA SID Number must be %d digits.' % (nfa_sid_number_length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    if not re.compile("^\d+$").search(nfa_sid_number):
        data_to_return['StatusMessage'] = u'NFA SID Number must only contain digits.'
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    return data_to_return

def Student_Record_SSN_Query(ssn=None, last_name=None, allow_partial_ssn=False):
    if not ssn:
        return None

    ssn_valudation_result = validate_ssn(ssn=ssn)

    if ssn_valudation_result['ResponseCode'] < 1:
        return None

    response_list = None
    
    if not last_name:
        try:
            if len(ssn) < 9:
                return None
            else:
                response_list = Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(IDNumber, %s) like %s)', (SRecEncryptKeyS(), ssn))
        except Studentrecords.MultipleObjectsReturned:
            return None

        except Studentrecords.DoesNotExist:
            return None
            
        if not response_list: 
            return None

        try:
            first_record = response_list[0]
        except:
            return None
            
    else:
        lastname_validation_result = validate_last_name(last_name)

        if lastname_validation_result['ResponseCode'] != 1:
            return None
        
        try:
            if allow_partial_ssn and len(ssn) < 9:
                response_list = Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (RIGHT(AES_DECRYPT(IDNumber, %s), %s) like %s) AND (LastName like %s)', (SRecEncryptKeyS(), len(ssn), ssn, last_name))
            elif len(ssn) == 9:
                response_list = Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(IDNumber, %s) like %s) AND (LastName like %s)', (SRecEncryptKeyS(), ssn, last_name))
            else:
                return None
        except Studentrecords.MultipleObjectsReturned:
            return None
        
        except Studentrecords.DoesNotExist:
            return None

    if not response_list: 
        return None

    #triggers the query to see if a record was found
    try:
        first_record = response_list[0]
    except:
        return None

    return response_list
    
def student_search_by_state_provider_number(epins=None, last_name=None):
    if not epins:
        return None

    epins_valudation_result = validate_state_provider_number(epins=epins)

    if epins_valudation_result['ResponseCode'] < 1:
        return None

    response_list = None
    
    if not last_name:
        try:
            response_list = Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(StateProviderNumber, %s) like %s)', (SRecEncryptKeyS(), epins))
        except Studentrecords.MultipleObjectsReturned:
            return None

        except Studentrecords.DoesNotExist:
            return None
            
        if not response_list: 
            return None

        try:
            first_record = response_list[0]
        except:
            return None
            
    else:
        lastname_validation_result = validate_last_name(last_name)

        if lastname_validation_result['ResponseCode'] != 1:
            return None
        
        try:
            response_list = Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(StateProviderNumber, %s) like %s) AND (LastName like %s)', (SRecEncryptKeyS(), epins, last_name))
        except Studentrecords.MultipleObjectsReturned:
            return None
        
        except Studentrecords.DoesNotExist:
            return None

    if not response_list: 
        return None

    #triggers the query to see if a record was found
    try:
        first_record = response_list[0]
    except:
        return None

    return response_list

def student_search_by_nfa_sid_number(nfa_sid_number=None, last_name=None):
    if not nfa_sid_number:
        return None

    nfa_sid_number_valudation_result = validate_nfa_sid_number(nfa_sid_number=nfa_sid_number)

    if nfa_sid_number_valudation_result['ResponseCode'] < 1:
        return None

    response_list = None
    
    if not last_name:
        try:
            response_list = Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(nfa_sid_number, %s) like %s)', (SRecEncryptKeyS(), nfa_sid_number))
        except Studentrecords.MultipleObjectsReturned:
            return None

        except Studentrecords.DoesNotExist:
            return None
            
        if not response_list: 
            return None

        try:
            first_record = response_list[0]
        except:
            return None
            
    else:
        lastname_validation_result = validate_last_name(last_name)

        if lastname_validation_result['ResponseCode'] != 1:
            return None
        
        try:
            response_list = Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(nfa_sid_number, %s) like %s) AND (LastName like %s)', (SRecEncryptKeyS(), nfa_sid_number, last_name))
        except Studentrecords.MultipleObjectsReturned:
            return None
        
        except Studentrecords.DoesNotExist:
            return None

    if not response_list: 
        return None

    #triggers the query to see if a record was found
    try:
        first_record = response_list[0]
    except:
        return None

    return response_list


def student_record_id_number_query(epins=None, nfa_sid=None, ssn=None, last_name=None, allow_partial_ssn=False):

    if ssn:
        return Student_Record_SSN_Query(ssn=ssn, last_name=last_name, allow_partial_ssn=allow_partial_ssn)

    if epins:
        return student_search_by_state_provider_number(epins=epins, last_name=last_name)

    if nfa_sid:
        return student_search_by_nfa_sid_number(nfa_sid_number=nfa_sid, last_name=last_name)

    return None


def GetDefaultStudentFlagStatus():
    try:
        default_status = Studentflagstatus.objects.get( name__iexact='No Flags' )
    except Studentflagstatus.DoesNotExist:
        return None
    return default_status


def find_student_by_name(prefix_search_kwargs={}, full_name=None, first_name=None, middle_name=None, last_name=None, suffix=None):

    search_kwargs = build_name_query(full_name=full_name, first_name=first_name, middle_name=middle_name, last_name=last_name, suffix=suffix)

    if prefix_search_kwargs:
        search_kwargs.update(prefix_search_kwargs)
    
    
    if not search_kwargs:
        return None

    found_list = Studentrecords.objects.filter(**search_kwargs)

    if not found_list:
        if full_name:
            (first_name, middle_name, last_name, suffix) = split_name(full_name)
        
        search_kwargs = build_name_query(full_name=None, first_name=first_name, middle_name=None, last_name=last_name, suffix=None)
        if prefix_search_kwargs:
            search_kwargs.update(prefix_search_kwargs)
        
        found_list = Studentrecords.objects.filter(**search_kwargs)
        
    if not found_list:
        if full_name:
            (first_name, middle_name, last_name, suffix) = split_name(full_name)
        
        if first_name and (len(first_name) > 0):

            search_kwargs = build_name_query(full_name=None, first_name=first_name[0:1], middle_name=None, last_name=last_name, suffix=None)
            if prefix_search_kwargs:
                search_kwargs.update(prefix_search_kwargs)
            
            found_list = Studentrecords.objects.filter(**search_kwargs)

    if not found_list:
    
        if full_name:
            (first_name, middle_name, last_name, suffix) = split_name(full_name)

        search_kwargs = build_name_query(full_name=None, first_name=None, middle_name=None, last_name=last_name, suffix=None)
        if prefix_search_kwargs:
            search_kwargs.update(prefix_search_kwargs)
        
        found_list = Studentrecords.objects.filter(**search_kwargs)
        
    if not found_list:
        
        search_kwargs = build_name_query(first_name_label='public_first_name', middle_name_label='public_middle_name', last_name_label='public_last_name', suffix_label='public_suffix', full_name=full_name, first_name=first_name, middle_name=middle_name, last_name=last_name, suffix=suffix)
        if prefix_search_kwargs:
            search_kwargs.update(prefix_search_kwargs)
        
        search_kwargs[ 'use_public_name__exact' ] = True
        found_list = Studentrecords.objects.filter(**search_kwargs)

    if not found_list:
        
        if full_name:
            (first_name, middle_name, last_name, suffix) = split_name(full_name)
        search_kwargs = build_name_query(first_name_label='public_first_name', middle_name_label='public_middle_name', last_name_label='public_last_name', suffix_label='public_suffix', full_name=None, first_name=first_name, middle_name=None, last_name=last_name, suffix=None)
        if prefix_search_kwargs:
            search_kwargs.update(prefix_search_kwargs)
        
        search_kwargs[ 'use_public_name__exact' ] = True

        found_list = Studentrecords.objects.filter(**search_kwargs)

    if not found_list:
        
        if full_name:
            (first_name, middle_name, last_name, suffix) = split_name(full_name)
        search_kwargs = build_name_query(first_name_label='public_first_name', middle_name_label='public_middle_name', last_name_label='public_last_name', suffix_label='public_suffix', full_name=None, first_name=None, middle_name=None, last_name=last_name, suffix=None)
        if prefix_search_kwargs:
            search_kwargs.update(prefix_search_kwargs)
        
        search_kwargs[ 'use_public_name__exact' ] = True

        found_list = Studentrecords.objects.filter(**search_kwargs)

    return found_list

def ReferenceDate():
    return datetime.datetime.now().date()

def reorder_date_to_ymd(date_string=None, separater=u'-'):
    
    if not date_string or len(date_string) == 0:
        return None
    
    if not separater:
        separater = u'-'
    
    (year, month, day) = date_string.split(separater)
    
    if len(day) == 4 and len(year) == 2:
        temp_year = day
        temp_month = year
        temp_day = month
        
        month = temp_month
        day = temp_day
        year = temp_year

    return u'%s-%s-%s' % (year, month, day)

def CalculateStudentAge(reference_date=ReferenceDate(), birth_date=None):
    
    if not birth_date:
        return None

    if type(reference_date) != datetime.datetime and type(reference_date) != datetime.date: 
        if len(reference_date) == 0:
            reference_date = datetime.datetime.now().strftime('%Y-%m-%d')

        if reference_date == u'0000-00-00':
            reference_date = datetime.datetime.now().strftime('%Y-%m-%d')

        reference_date = datetime.datetime.strptime(reorder_date_to_ymd(date_string=reference_date), '%Y-%m-%d').date()
    
    if type(birth_date) != datetime.date:
        if len(birth_date) == 0:
            return None

        if birth_date == u'0000-00-00':
            return None

        birth_date = datetime.datetime.strptime(reorder_date_to_ymd(date_string=birth_date), '%Y-%m-%d').date()

    (reference_year_string, reference_month_string, reference_day_string) = reference_date.strftime(u'%Y-%m-%d').split('-')
    
    (student_year_string, student_month_string, student_day_string) = birth_date.strftime(u'%Y-%m-%d').split('-')

    reference_year  = int(reference_year_string)
    reference_month = int(reference_month_string)
    reference_day   = int(reference_day_string)

    student_year  = int(student_year_string)
    student_month = int(student_month_string)
    student_day   = int(student_day_string)
    

    student_age = 0
    if reference_year > student_year:
        student_age = reference_year - student_year
        if reference_month < student_month:
            student_age -= 1
        elif reference_month == student_month:
            if reference_day < student_day:
                student_age -= 1
    else:
        return 0

    return student_age
    
def student_age_at_date(student_record=None, target_date=None):

    if not student_record:
        return 0

    if not student_record.birthdate:
        return 0
    
    if not target_date:
        return 0
        
    try:
        return target_date.year - student_record.birthdate.year - ((target_date.month, target_date.day) < (student_record.birthdate.month, student_record.birthdate.day))
    except:
        return 0

    return 0

def GetStudentRecord(pk=None):
    student_record = None
    
    if pk:

        try:
            student_record = Studentrecords.objects.get(pk=pk)
        except Studentrecords.DoesNotExist:
            return None
        except Studentrecords.MultipleObjectsReturned:
            return None

    return student_record

def StudentRecordSSNSearch(ssn=None, last_name=None, current_record=None, allow_partial_ssn=False):

    if not ssn:
        return None

    ssn_valudation_result = validate_ssn(ssn=ssn)

    if ssn_valudation_result['ResponseCode'] < 1:
        return None

    response_list = None
    
    if not last_name:
        try:
            if current_record:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(IDNumber, %s) like %s) AND (ID != %s) ORDER BY lastname, suffix, firstname, middlename', (SRecEncryptKeyS(), ssn, current_record.id)))
            else:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(IDNumber, %s) like %s) ORDER BY lastname, suffix, firstname, middlename', (SRecEncryptKeyS(), ssn)))

        except Studentrecords.DoesNotExist:
            return None
            
    else:
        lastname_validation_result = validate_last_name(last_name)

        if lastname_validation_result['ResponseCode'] != 1:
            return None
        
        try:
            if current_record:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(IDNumber, %s) like %s) AND (LastName like %s) AND (ID != %s) ORDER BY lastname, suffix, firstname, middlename', (SRecEncryptKeyS(), ssn, last_name, current_record.id)))
            else:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(IDNumber, %s) like %s) AND (LastName like %s) ORDER BY lastname, suffix, firstname, middlename', (SRecEncryptKeyS(), ssn, last_name)))
        
        except Studentrecords.DoesNotExist:
            return None

    if not response_list: 
        return None

    return response_list
    
def FindDuplicateStudent(table_name=u'StudentRecord', value_to_search=u'ssn', student_record=None):

    student_duplicate_list = []
    
    if value_to_search == u'ssn':
        if table_name == u'StudentRecord':
            student_duplicate_list = StudentRecordSSNSearch(ssn=student_record.ssn_clear,  current_record=student_record) 

    if value_to_search == u'epins':
        if table_name == u'StudentRecord':
            student_duplicate_list = StudentRecordStateProviderNumberSearch(state_provider_number=student_record.epins_clear,  current_record=student_record) 

    if value_to_search == u'nfasid':
        if table_name == u'StudentRecord':
            student_duplicate_list = StudentNFASIDNumberSearch(nfa_sid_number=student_record.nfa_sid,  current_record=student_record) 
                
    return student_duplicate_list
    
def StudentRecordStateProviderNumberSearch(state_provider_number=None, last_name=None, current_record=None):
    
    if not state_provider_number:
        return None

    state_provider_number_valudation_result = validate_state_provider_number(epins=state_provider_number)

    if state_provider_number_valudation_result['ResponseCode'] < 1:
        return None

    response_list = None
    
    if not last_name:
        try:
            if current_record:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(StateProviderNumber, %s) like %s) AND (ID != %s)', (SRecEncryptKeyS(), state_provider_number, current_record.id)))
            else:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(StateProviderNumber, %s) like %s)', (SRecEncryptKeyS(), state_provider_number)))

        except Studentrecords.DoesNotExist:
            return None
            
        if not response_list: 
            return None

    else:
        lastname_validation_result = validate_last_name(last_name)

        if lastname_validation_result['ResponseCode'] != 1:
            return None
        
        try:
            if current_record:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(StateProviderNumber, %s) like %s) AND (LastName like %s) AND (ID != %s)', (SRecEncryptKeyS(), state_provider_number, last_name, current_record.id)))
            else:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(StateProviderNumber, %s) like %s) AND (LastName like %s)', (SRecEncryptKeyS(), state_provider_number, last_name)))
        
        except Studentrecords.DoesNotExist:
            return None

    if not response_list: 
        return None

    return response_list

def StudentNFASIDNumberSearch(nfa_sid_number=None, last_name=None, current_record=None):
    
    if not nfa_sid_number:
        return None

    nfa_sid_number_valudation_result = validate_nfa_sid_number(nfa_sid_number=nfa_sid_number)

    if nfa_sid_number_valudation_result['ResponseCode'] < 1:
        return None

    response_list = None
    
    if not last_name:
        try:
            if current_record:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(nfa_sid_number, %s) like %s) AND (ID != %s)', (SRecEncryptKeyS(), nfa_sid_number, current_record.id)))
            else:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(nfa_sid_number, %s) like %s)', (SRecEncryptKeyS(), nfa_sid_number)))

        except Studentrecords.DoesNotExist:
            return None
            
        if not response_list: 
            return None

    else:
        lastname_validation_result = validate_last_name(last_name)

        if lastname_validation_result['ResponseCode'] != 1:
            return None
        
        try:
            if current_record:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(nfa_sid_number, %s) like %s) AND (LastName like %s) AND (ID != %s)', (SRecEncryptKeyS(), nfa_sid_number, last_name, current_record.id)))
            else:
                response_list = list(Studentrecords.objects.raw('SELECT id FROM StudentRecords WHERE (AES_DECRYPT(nfa_sid_number, %s) like %s) AND (LastName like %s)', (SRecEncryptKeyS(), nfa_sid_number, last_name)))
        except Studentrecords.MultipleObjectsReturned:
            return None
        
        except Studentrecords.DoesNotExist:
            return None

    if not response_list: 
        return None

    return response_list

def GetStudentRecordObj(ssn=None, last_name=None, suffix=None, maiden_name=None, birth_date='0000-00-00', require_birth_date=True):

    if not ssn:
        return None

    if not last_name and not maiden_name:
        return None

    if require_birth_date and birth_date == '0000-00-00':
        return None

    NameTokens = last_name.split(' ')

    if len(NameTokens) > 1:
        data_to_return = parse_last_name_suffix(lastname=last_name, validate_suffix=False)

        if data_to_return['ResponseCode'] < 1:
            return data_to_return

        last_name = data_to_return['last_name']
        suffix = data_to_return['suffix']

    student_record_list = StudentRecordSSNSearch(ssn=ssn, last_name=last_name, allow_partial_ssn=True)

    if maiden_name and not student_record_list:

        student_record_list = StudentRecordSSNSearch(ssn=ssn, last_name=maiden_name, allow_partial_ssn=True)

    if not student_record_list:
        return None
    else:
        try:
            first_record = student_record_list[0]
        except:
            return None

    if suffix:
        if suffix != student_record_list[0].suffix:
            return None
    else:
        if ( (not student_record_list[0].birth_date) and (student_record_list[0].birth_date != '0000-00-00') ) and student_record_list[0].suffix and len(student_record_list[0].suffix) > 0:
            return None

    if birth_date != '0000-00-00':
        if student_record_list[0].birth_date:
            student_record_birth_date = student_record_list[0].birth_date.strftime('%Y-%m-%d')
            if len(student_record_birth_date) == 0:
                student_record_birth_date = '0000-00-00'
        else:
            student_record_birth_date = '0000-00-00'
            
        if student_record_birth_date != '0000-00-00':
            if birth_date == student_record_birth_date:
                return student_record_list[0]
            else:
                return None
        else:
            student_record_list = StudentRecordSSNSearch(ssn=ssn, last_name=last_name, allow_partial_ssn=True)
            
            if maiden_name and not student_record_list:
                student_record_list = StudentRecordSSNSearch(ssn=ssn, last_name=maiden_name, allow_partial_ssn=True)

            if student_record_list:
                if student_record_list[0].birthdate:
                    student_record_birth_date = student_record_list[0].birthdate.strftime('%Y-%m-%d')

                    if len(student_record_birth_date) == 0:
                        student_record_birth_date = '0000-00-00'
                else:
                    student_record_birth_date = '0000-00-00'
                    
                    
                if student_record_birth_date != '0000-00-00':
                    if birth_date != student_record_birth_date:
                        return None
                    

    return student_record_list[0]


def FindMFRIStudentNumber(request, user=None, student_details=None): 
    """
      return mfri student number
    """

    if not student_details:
        data_to_return = {  'StatusMessage': 'Could not return transcript, no data',
                            'ResponseCode': -1,
                            'mfri_student_number': None,
                         }    
        return data_to_return

    if not 'ssn' in student_details:
        data_to_return = {  'StatusMessage': 'Social Security Number not found in request',
                            'ResponseCode': -2,
                            'mfri_student_number': None,
                         }    
        return data_to_return
        
    if not 'last_name' in student_details:
        data_to_return = {  'StatusMessage': 'Last Name not found in request',
                            'ResponseCode': -3,
                            'mfri_student_number': None,
                         }    
        return data_to_return

    if not 'birth_date' in student_details:
        data_to_return = {  'StatusMessage': 'Birth Date not found in request',
                            'ResponseCode': -4,
                            'mfri_student_number': None,
                         }    
        return data_to_return

    ssn_valudation_result = validate_ssn(ssn=student_details['ssn'], accept_last_five=True)

    if ssn_valudation_result['ResponseCode'] < 1:
        data_to_return = {  'StatusMessage': ssn_valudation_result['StatusMessage'],
                            'ResponseCode': -5,
                            'mfri_student_number': None,
                            }      
        return data_to_return

    last_name_valudation_result = validate_last_name(lastname=student_details['last_name'])

    if last_name_valudation_result['ResponseCode'] < 1 :
        data_to_return = {  'StatusMessage': last_name_valudation_result['StatusMessage'],
                            'ResponseCode': -254,
                            'mfri_student_number': None,
                            }      
        return data_to_return

    if 'maiden_name' in student_details and student_details['maiden_name'] and len(student_details['maiden_name']) > 0:
        if not validate_last_name(lastname=student_details['maiden_name']):
            data_to_return = {  'StatusMessage': 'Student maiden/former name invalid',
                                'ResponseCode': -6,
                                'mfri_student_number': None,
                                }      
            return data_to_return

    if not validate_date(date_to_check=student_details['birth_date']):
        data_to_return = {  'StatusMessage': 'Student birth date invalid',
                            'ResponseCode': -7,
                            'mfri_student_number': None,
                            }      
        return data_to_return
                        
    student_record = GetStudentRecordObj(ssn=student_details['ssn'].strip('-').strip(), last_name=student_details['last_name'], maiden_name=student_details['maiden_name'], birth_date=student_details['birth_date']) 

    if not student_record:
        data_to_return = {  'StatusMessage': u'No record found for this student.',
                            'ResponseCode': -8,
                            'mfri_student_number': None,
                            }      
        return data_to_return
        
    if student_record['ResponseCode'] < 0:
        return data_to_return
        
    if not 'StudentData' in student_record:
        data_to_return = {  'StatusMessage': u'There was an error retrieving the record for this student.',
                            'ResponseCode': -9,
                            'mfri_student_number': None,
                            }      
        return data_to_return

def FormatListRegistrationRecordsForDisplay(registration_record_list=None, preregistration_records=None, online_registration_record_list=None):
    
    registration_list = []
    preregistration_list = []
    onlineregistration_list = []

    seated_log_numbers = {}

    for registration_record in registration_record_list:
        
        validate_response = validate_log_number_parts(category=registration_record.scheduled_course.category, level=registration_record.scheduled_course.level, funding_source_code=registration_record.scheduled_course.funding_source_code, section_number=registration_record.scheduled_course.section_number, fiscal_year=registration_record.scheduled_course.fiscal_year, course_code=registration_record.scheduled_course.course_description.course_code)
        if validate_response['ResponseCode'] < 1:
            is_log_number_valid = False
        else:
            is_log_number_valid = True

        if registration_record.scheduled_course.fiscal_year == u'0000':
            is_log_number_valid = False

        if registration_record.scheduled_course.category == u'None':
            is_log_number_valid = False

        seated_log_numbers[registration_record.scheduled_course.log_number] = True
        registration_list.append({
                                  'log_number': registration_record.scheduled_course.log_number,
                                  'start_date': registration_record.scheduled_course.start_date,
                                  'end_date': registration_record.scheduled_course.end_date,
                                  'course_name': registration_record.scheduled_course.course_name,
                                  'fees': registration_record.resource_fee,
                                  'credit': registration_record.credit_amount,
                                  'location_name': registration_record.scheduled_course.location_name,
                                  'status': registration_record.status,
                                  'outcome': registration_record.grade,
                                  'created_date': registration_record.created,
                                  'scheduled_course_id': registration_record.scheduled_course.id,
                                  'record_id': registration_record.id,
                                  'is_log_number_valid': is_log_number_valid,
                                })
                            

    for registration_record in preregistration_records:
        if registration_record.scheduled_course.log_number in seated_log_numbers:
            continue

        validate_response = validate_log_number_parts(category=registration_record.scheduled_course.category, level=registration_record.scheduled_course.level, funding_source_code=registration_record.scheduled_course.funding_source_code, section_number=registration_record.scheduled_course.section_number, fiscal_year=registration_record.scheduled_course.fiscal_year, course_code=registration_record.scheduled_course.course_description.course_code)
        if validate_response['ResponseCode'] < 1:
            is_log_number_valid = False
        else:
            is_log_number_valid = True
            
        if registration_record.scheduled_course.fiscal_year == u'0000':
            is_log_number_valid = False

        if registration_record.scheduled_course.category == u'None':
            is_log_number_valid = False

        preregistration_list.append({
                                  'log_number': registration_record.scheduled_course.log_number,
                                  'start_date': registration_record.scheduled_course.start_date,
                                  'end_date': registration_record.scheduled_course.end_date,
                                  'course_name': registration_record.scheduled_course.course_name,
                                  'fees': 0,
                                  'credit': 0,
                                  'location_name': registration_record.scheduled_course.location_name,
                                  'status': registration_record.status.name,
                                  'outcome': None,
                                  'created_date': registration_record.created,
                                  'scheduled_course_id': registration_record.scheduled_course.id,
                                  'record_id': registration_record.id,
                                  'is_log_number_valid': is_log_number_valid,
                                })

    for registration_record in online_registration_record_list:
        if registration_record.scheduled_course.log_number in seated_log_numbers:
            continue
            
        validate_response = validate_log_number_parts(category=registration_record.scheduled_course.category, level=registration_record.scheduled_course.level, funding_source_code=registration_record.scheduled_course.funding_source_code, section_number=registration_record.scheduled_course.section_number, fiscal_year=registration_record.scheduled_course.fiscal_year, course_code=registration_record.scheduled_course.course_description.course_code)

        if validate_response['ResponseCode'] < 1:
            is_log_number_valid = False
        else:
            is_log_number_valid = True

        if registration_record.scheduled_course.fiscal_year == u'0000':
            is_log_number_valid = False
            
        if registration_record.scheduled_course.category == u'None':
            is_log_number_valid = False

        onlineregistration_list.append({
                                  'log_number': registration_record.scheduled_course.log_number,
                                  'start_date': registration_record.scheduled_course.start_date,
                                  'end_date': registration_record.scheduled_course.end_date,
                                  'course_name': registration_record.scheduled_course.course_name,
                                  'fees': 0,
                                  'credit': 0,
                                  'location_name': registration_record.scheduled_course.location_name,
                                  'status': registration_record.status.name,
                                  'outcome': None,
                                  'created_date': registration_record.created,
                                  'scheduled_course_id': registration_record.scheduled_course.id,
                                  'record_id': registration_record.id,
                                  'is_log_number_valid': is_log_number_valid,
                                })

    return {
            'registration_list': registration_list,
            'preregistration_list': preregistration_list,
            'onlineregistration_list': onlineregistration_list,
           }


