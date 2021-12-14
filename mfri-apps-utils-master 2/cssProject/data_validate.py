import re

#from cStringIO import StringIO

#import random
#import json
#import base64
#import time
import datetime
from dateutil.relativedelta import relativedelta

#from mfri.org.utils_log_number import SplitLogNumber

#from mfri.org.utils_course import GetCourseDescription

EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain


def validate_bool(bool_to_check=None):
    
    if type(bool_to_check) != bool:
        if bool_to_check in ['True', 'False']:
            return True
        
        return False
        
    if len(str(bool_to_check)) == 0:
        return False

    if bool_to_check in [True, False]:
        return True

    return False

def validate_ssn(ssn=None, accept_last_four=False, accept_last_five=False): 
    """
    SSN must be 9 digits long.  Only digits allowed.
    returns 1 if SSN passes and 0 if there is an error.
    """
    
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    
    
    if not ssn:
        data_to_return['StatusMessage'] = u'No SSN given.'
        data_to_return['ResponseCode'] = 0
        
        return data_to_return
        
    ssn = ssn.replace('-', '')
    ssn = ssn.strip()
    
    SSN_Length = 9
    
    if len(ssn) != SSN_Length:
        if accept_last_four:
            if len(ssn) != 4:
                data_to_return['StatusMessage'] = u'SSN must be 4 or %d digits.' % (SSN_Length)
                data_to_return['ResponseCode'] = 0
                return data_to_return
        elif accept_last_five:
            if len(ssn) != 5:
                data_to_return['StatusMessage'] = u'SSN must be 5 or %d digits.' % (SSN_Length)
                data_to_return['ResponseCode'] = 0
                return data_to_return
        else:
            data_to_return['StatusMessage'] = u'SSN must be %d digits.' % (SSN_Length)
            data_to_return['ResponseCode'] = 0
            return data_to_return

    #20210323+
    if ssn == u'000000000':
        data_to_return['StatusMessage'] = u'SSN can not be all zeros.  You must provide a valid SSN.' 
        data_to_return['ResponseCode'] = 0
        return data_to_return
    #20210323-

#    bob = ssn[0:3].upper()

    if ssn[0:3].upper() != u'MSN':
        if not re.compile("^\d+$").search(ssn):
            data_to_return['StatusMessage'] = u'SSN must only contain digits.'
            data_to_return['ResponseCode'] = 0
            return data_to_return
    else:
        if not re.compile("^\d+$").search(ssn[3:]):
            data_to_return['StatusMessage'] = u'SSN must only contain digits.'
            data_to_return['ResponseCode'] = 0
            return data_to_return

    return data_to_return
    
def validate_mfri_student_number(mfri_student_number=None): 
    """
    mfri_student_number must be 8 digits long.  Only digits allowed.
    returns 1 if mfri_student_number passes and 0 if there is an error.
    """
    
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    
    
    if not mfri_student_number:
        data_to_return['StatusMessage'] = u'No MFRI Student Number given.'
        data_to_return['ResponseCode'] = 0
        
        return data_to_return
        
    mfri_student_number = mfri_student_number.strip('-')
    mfri_student_number = mfri_student_number.strip()
    
    mfri_student_number_Length = 8
    
    if len(mfri_student_number) != mfri_student_number_Length:
        data_to_return['StatusMessage'] = u'MFRI Student Number must be %d digits.' % (mfri_student_number_Length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    #old mfri student number started with MSN
    if mfri_student_number[0:3].upper() != u'MSN':
        if not re.compile("^\d+$").search(mfri_student_number):
            data_to_return['StatusMessage'] = u'MFRI Student Number must only contain digits.'
            data_to_return['ResponseCode'] = 0

            return data_to_return
    else:
        if not re.compile("^\d+$").search(mfri_student_number[3:]):
            data_to_return['StatusMessage'] = u'MFRI Student Number must only contain digits.'
            data_to_return['ResponseCode'] = 0

            return data_to_return
    
    return data_to_return

def validate_state_provider_number(epins=None): #Also known as EPINS number
    """
    State Provider Number must be 7 digits long.  Only digits allowed.
    returns 1 if epins passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    

    if not epins:
        data_to_return['StatusMessage'] = u'Null State Provider Number.'
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

def validate_nfa_sid_number(nfa_sid_number=None): #Also known as nfa_sid_number number
    """
    State Provider Number must be 10 digits long.  Only digits allowed.
    returns 1 if nfa_sid_number passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    

    if not nfa_sid_number:
        data_to_return['StatusMessage'] = u'Null NFA SID Number.'
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

def validate_university_id_number(uid=None): 
    """
    University ID Number must be 9 digits long.  Only digits allowed.
    returns 1 if UID passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    

    if not uid:
        data_to_return['StatusMessage'] = u'Null University ID Number.'
        data_to_return['ResponseCode'] = 0

        return data_to_return


    UID_Length = 9
    
    if len(uid) != UID_Length:
        data_to_return['StatusMessage'] = u'University ID Number must be %d digits.' % (UID_Length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    if not re.compile("^\d+$").search(uid):
        data_to_return['StatusMessage'] = u'University ID Number must only contain digits.'
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    return data_to_return

def valid_suffix_values():
    return set(['JR', 'SR', 'I', 'II', 'III', 'IV', 'V', 'VI'])

def parse_last_name_suffix(lastname=None, validate_suffix=True, message_label=u'Last Name'):
    
    if not lastname:
        data_to_return = {  'StatusMessage': u'Null %s.' % (message_label),
                            'ResponseCode': 0
                         }

        return data_to_return

    NameTokens = lastname.split(' ')
    
    suffix = u''
    
    if len(NameTokens) > 1:
        SuffixValues = valid_suffix_values()
    
        if NameTokens[-1].upper().replace('.', ' ').strip() in SuffixValues:
            suffix = NameTokens[-1].upper().replace('.', ' ').strip()
            lastname = u' '.join(NameTokens[0: -1])
        elif validate_suffix:
            if len(NameTokens[-1].upper().replace('.', ' ').strip()) < 3:
                data_to_return = {  'StatusMessage': u'Invalid Suffix %s in name %s' % (NameTokens[-1].upper().replace('.', ' ').strip(), lastname),
                                    'ResponseCode': 0
                                 }
    
                return data_to_return

    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                        'last_name': lastname,
                        'suffix': suffix,
                     }    

    return data_to_return

def validate_last_name(lastname=None, allow_suffix=False, min_Length=2, max_Length=80, message_label=u'Last Name'): 
    """
    Last Name must be at least 2 characters long and less than 80 characters long.  Only alphanumeric characters, single quotes (') and dashes (-) allowed
    returns 1 if last name passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }

    if not lastname:
        data_to_return['StatusMessage'] = u'Null %s.' % (message_label)
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    NameTokens = lastname.split(' ')

    if len(NameTokens) > 1:
        data_to_return = parse_last_name_suffix(lastname=lastname, validate_suffix=allow_suffix, message_label=message_label)
        
        if data_to_return['ResponseCode'] < 1:
            return data_to_return
        
        lastname = data_to_return['last_name']
        if not allow_suffix:
            suffix = data_to_return['suffix']
            
            if suffix and len(suffix) > 0:
                data_to_return['StatusMessage'] = u'No suffix, only use %s.' % (message_label)
                data_to_return['ResponseCode'] = 0

                return data_to_return
        
    
#    assert False
    if len(lastname) < min_Length:
        data_to_return['StatusMessage'] = u'%s must be at least %d characters long.' % (message_label, min_Length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    if len(lastname) > max_Length:
        data_to_return['StatusMessage'] = u'%s can not be longer than %d characters.' % (message_label, max_Length)
        data_to_return['ResponseCode'] = 0

        return data_to_return

    if not re.compile("^([a-zA-Z\'\- ]+)$").search(lastname):
        data_to_return['StatusMessage'] = u'%s (%s) must only contain alphanumeric characters, single quotes (\') and dashes (-) allowed.' % (message_label, lastname)
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    return data_to_return

def validate_first_name(firstname=None, min_Length=1, max_Length=80, message_label=u'First Name'): 
    """
    First Name must be at least 1 characters long and less than 80 characters long.  Only alphanumeric characters, single quotes (') and dashes (-) allowed
    returns 1 if first name passes and 0 if there is an error.
    also used for middle name.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }

    if not firstname:
        data_to_return['StatusMessage'] = u'Null %s.' % (message_label)
        data_to_return['ResponseCode'] = 0

        return data_to_return
        
    if len(firstname) < min_Length:
        data_to_return['StatusMessage'] = u'%s must be at least %d characters long.' % (message_label, min_Length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    if len(firstname) > max_Length:
        data_to_return['StatusMessage'] = u'%s can not be longer than %d characters.' % (message_label, max_Length)
        data_to_return['ResponseCode'] = 0

        return data_to_return

    if not re.compile("^([a-zA-Z\'\- ]+)$").search(firstname):
        data_to_return['StatusMessage'] = u'%s (%s) must only contain alphanumeric characters, single quotes (\') and dashes (-) allowed.' % (message_label, firstname)
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    return data_to_return

def validate_date(date_to_check=None, date_format='YMD'):
    
    if not date_to_check:
        return False
        
    date_parts = date_to_check.replace('/','-').split('-')
        
    date_parts_count = len(date_parts) 
    
    if date_parts_count != 3:
        return False

    if date_format == 'YMD':
        year = date_parts[0]
        month = date_parts[1]
        day = date_parts[2]
    elif date_format == 'MDY':
        month = date_parts[1]
        day = date_parts[2]
        year = date_parts[0]
    else:
        return False
    
    try:
        t1 = (int(year), int(month), int(day), 0, 0, 0, 0, 0, -1)
        d = time.mktime(t1)
        t2 = time.localtime(d)
        if t1[:3] != t2[:3]:
            return False
        else:
            return True
    except (OverflowError, ValueError):
        return False

def validate_date_field(date_to_check=None, date_label=u'Birth Date'): 
    
    if not validate_date(date_to_check=date_to_check):
        return {   'StatusMessage': 'Invalid %s.' % (date_label),
               'ResponseCode': 0
           }

    return {   'StatusMessage': '%s Ok' % (date_label),
                  'ResponseCode': 1
              }

def validate_email_address(email_address=None, email_label=u'Email'):

    if not email_address:
        return {   'StatusMessage': 'Invalid %s.' % (email_label), 
               'ResponseCode': 0
           }

    if EMAIL_RE.search(email_address):
        return {   'StatusMessage': '%s Ok.' % (email_label),
                   'ResponseCode': 1
               }

    return {   'StatusMessage': 'Invalid %s.' % (email_label),
               'ResponseCode': 0
           }

state_name_list = [(u'AL', u'Alabama'),
(u'AK', u'Alaska'),
(u'AZ', u'Arizona'),
(u'AR', u'Arkansas'),
(u'CA', u'California'),
(u'CO', u'Colorado'),
(u'CT', u'Connecticut'),
(u'DE', u'Delaware'),
(u'FL', u'Florida'),
(u'GA', u'Georgia'),
(u'HI', u'Hawaii'),
(u'ID', u'Idaho'),
(u'IL', u'Illinois'),
(u'IN', u'Indiana'),
(u'IA', u'Iowa'),
(u'KS', u'Kansas'),
(u'KY', u'Kentucky'),
(u'LA', u'Louisiana'),
(u'ME', u'Maine'),
(u'MD', u'Maryland'),
(u'MA', u'Massachusetts'),
(u'MI', u'Michigan'),
(u'MN', u'Minnesota'),
(u'MS', u'Mississippi'),
(u'MO', u'Missouri'),
(u'MT', u'Montana'),
(u'NE', u'Nebraska'),
(u'NV', u'Nevada'),
(u'NH', u'New Hampshire'),
(u'NJ', u'New Jersey'),
(u'NM', u'New Mexico'),
(u'NY', u'New York'),
(u'NC', u'North Carolina'),
(u'ND', u'North Dakota'),
(u'OH', u'Ohio'),
(u'OK', u'Oklahoma'),
(u'OR', u'Oregon'),
(u'PA', u'Pennsylvania'),
(u'RI', u'Rhode Island'),
(u'SC', u'South Carolina'),
(u'SD', u'South Dakota'),
(u'TN', u'Tennessee'),
(u'TX', u'Texas'),
(u'UT', u'Utah'),
(u'VT', u'Vermont'),
(u'VA', u'Virginia'),
(u'WA', u'Washington'),
(u'WV', u'West Virginia'),
(u'WI', u'Wisconsin'),
(u'WY', u'Wyoming'),
(u'AS', u'American Samoa'),
(u'DC', u'District of Columbia'),
(u'FM', u'Federated States of Micronesia'),
(u'GU', u'Guam'),
(u'MH', u'Marshall Islands'),
(u'MP', u'Northern Mariana Islands'),
(u'PW', u'Palau'),
(u'PR', u'Puerto Rico'),
(u'VI', u'Virgin Islands'),
(u'AE', u'Armed Forces Africa'),
(u'AA', u'Armed Forces Americas'),
(u'AE', u'Armed Forces Canada'),
(u'AE', u'Armed Forces Europe'),
(u'AE', u'Armed Forces Middle East'),
(u'AP', u'Armed Forces Pacific'),]

def is_valid_us_state(state_to_check=None):
    
    #assert False
    if is_string_empty(string_to_check=state_to_check):
        #assert False
        return False
    
    try:
        state_name = dict(state_name_list)[state_to_check.upper()]
    except KeyError:
        state_name = None
    
    if is_string_empty(string_to_check=state_name):
        #assert False
        return False

    #assert False
    return True

def is_string_empty(string_to_check=None, allow_end_spaces=False):
    
    if not string_to_check:
        return True

    if allow_end_spaces:
        if len(string_to_check) == 0:
            return True
    else:
        if len(string_to_check.strip()) == 0:
            return True

    return False

def validate_address(address1=None, address2=None, city=None, state=None, post_code=None, country=None, use_country=False, require_zip_plus_4_post_code=False, require_us_post_code=True): 
    """
    make sure address is basically in a legal format.
    
    """    
    
    validation_results = {
                          'address1':{'description':u'', 'has_error': False, 'empty': False, 'invalid': False},
                          'address2':{'description':u'', 'has_error': False, 'empty': False, 'invalid': False},
                          'city':{'description':u'', 'has_error': False, 'empty': False, 'invalid': False},
                          'state':{'description':u'', 'has_error': False, 'empty': False, 'invalid': False},
                          'post_code':{'description':u'', 'has_error': False, 'empty': False, 'invalid': False},
                          'country':{'description':u'', 'has_error': False, 'empty': False, 'invalid': False},
                         }

    if is_string_empty(string_to_check=address1):
        validation_results['address1']['description'] = u'No address line 1.'
        validation_results['address1']['has_error'] = True
        validation_results['address1']['empty'] = True
        validation_results['address1']['invalid'] = False


    if is_string_empty(string_to_check=address2):
        validation_results['address2']['description'] = u'No address line 2.'
        validation_results['address2']['has_error'] = False
        validation_results['address2']['empty'] = True
        validation_results['address2']['invalid'] = False

    if is_string_empty(string_to_check=city):
        validation_results['city']['description'] = u'No city.'
        validation_results['city']['has_error'] = True
        validation_results['city']['empty'] = True
        validation_results['city']['invalid'] = False

    if country.strip().upper()[0:1] == u'US' or is_string_empty(string_to_check=country):
        if not is_valid_us_state(state_to_check=state):
            validation_results['state']['description'] = u'Invalid state.'
            validation_results['state']['has_error'] = True
            validation_results['state']['empty'] = False
            validation_results['state']['invalid'] = True
        
        if is_string_empty(string_to_check=post_code):
            validation_results['post_code']['description'] = u'No zip code.'
            validation_results['post_code']['has_error'] = True
            validation_results['post_code']['empty'] = True
            validation_results['post_code']['invalid'] = False

        if not re.compile("^[0-9]{5}(?:-[0-9]{4})?$").search(post_code):
            validation_results['post_code']['description'] = u'Zip code is not in correct format, must be 12345 or 12345-1234.'
            validation_results['post_code']['has_error'] = True
            validation_results['post_code']['empty'] = False
            validation_results['post_code']['invalid'] = True
            
        if require_zip_plus_4_post_code:
            if len(post_code) < 10:
                validation_results['post_code']['description'] = u'Must use zip+4: 12345-1234.'
                validation_results['post_code']['has_error'] = True
                validation_results['post_code']['empty'] = False
                validation_results['post_code']['invalid'] = True
                
    else:
        if is_string_empty(string_to_check=state):
            validation_results['state']['description'] = u'No state.'
            validation_results['state']['has_error'] = True
            validation_results['state']['empty'] = True
            validation_results['state']['invalid'] = False

        if is_string_empty(string_to_check=post_code):
            validation_results['post_code']['description'] = u'No zip code.'
            validation_results['post_code']['has_error'] = True
            validation_results['post_code']['empty'] = True
            validation_results['post_code']['invalid'] = False
    
    return validation_results

def YearsBetweenDates(start_date=None, end_date=datetime.datetime.now().date()):
    
    if not start_date:
        return 0
        
    return relativedelta(end_date, start_date).years


def IsUnder18(birth_date=None, class_start_date=datetime.datetime.now().date()):
    
    if not birth_date:
        return False
        
    age = YearsBetweenDates(start_date=birth_date, end_date=class_start_date)
    
    if age < 18:
        return True
    
    return False
    
def ValidateTableIndex(index_to_check=None, max_length=8, min_value=1, max_value=99999999, look_up=False, table=None):
    
    if not index_to_check:
        #assert False
        return False

    if not index_to_check.isdigit():
        #assert False
        return False

    if len(index_to_check) > max_length:
        #assert False
        return False

    int_index_to_check = int(index_to_check)
    
    if int_index_to_check < min_value:
        #assert False
        return False

    if int_index_to_check > max_value:
        #assert False
        return False

    if look_up:
        found_record = None

        try:
            found_record = table.objects.get(pk=int_index_to_check)
        except:
            return False

        if not found_record:
            #assert False
            return False
    
    return True

    
