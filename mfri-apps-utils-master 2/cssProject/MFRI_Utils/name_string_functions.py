
from MFRI_Utils.data_validate import valid_suffix_values, validate_last_name


def SplitName(full_name=None):
  
    if not full_name:
        return None, None, None, None
    
    SuffixValues = valid_suffix_values() # set(['JR', 'SR', 'I', 'II', 'III', 'IV', 'V'])

    NewFullName = full_name

    if NewFullName.find(',') >= 0: #name contains a comma (,) so is probably reversed
        NameParts = NewFullName.split(',', 2)
         
        NewFullName = NameParts[1].strip() + " " + NameParts[0].strip()

    NameTokens = NewFullName.split(' ')

    if len(NameTokens) == 1:
        last_name = NameTokens[0].strip()
        return None, None, last_name, None

    first_name = NameTokens[0].strip()
    middle_name = NameTokens[1].strip()
    last_name = ''
    suffix = ''
    
    if NameTokens[-1].upper().replace('.', ' ').strip() in SuffixValues:
        suffix = NameTokens[-1].upper().replace('.', ' ').strip()
        last_name = " ".join(NameTokens[2: -1])
        #assert False
    else:
        last_name = " ".join(NameTokens[2:])
        #assert False
    
    if middle_name == suffix:
        middle_name = ''
    
    if len(last_name) == 0:
        if len(middle_name) > 0:
            last_name = middle_name
            middle_name = ''
        else:
            last_name = first_name
            first_name = ''

    return first_name, middle_name, last_name, suffix

def JoinName(RawFirstName, RawMiddleName, RawLastName, RawSuffix, ReturnLastNameFirst):

    FullName = ""
    FirstName = ""
    MiddleName = ""
    LastName = ""
    Suffix = ""
    
    
    if len(RawFirstName) == 0 and len(RawMiddleName) == 0:
        NameParts = SplitName(full_name=RawLastName)

        if NameParts.count < 1:
            return ""
            
        LastName = NameParts.LastName
        FirstName = ""
        MiddleName = ""
        Suffix = ""
    
    
    if 1 == ReturnLastNameFirst:
        FullName = LastName.strip()
        
        if len(Suffix.strip()) > 1:
            if len(FullName.strip()) > 1:
                FullName += " "
            FullName += Suffix.strip() + ","
        else:
            FullName += ","

        if len(FirstName.strip()) > 1:
            if len(FullName.strip()) > 1:
                FullName += " "
            FullName += FirstName.strip()

        if len(MiddleName.strip()) > 1:
            if len(FullName.strip()) > 1:
                FullName += " "
            FullName += MiddleName.strip()

    else:
        FullName = FirstName.strip()
        
        if len(FirstName.strip()) > 1:
            if len(FullName.strip()) > 1:
                FullName += " "
            FullName += FirstName.strip()

        if len(MiddleName.strip()) > 1:
            if len(FullName.strip()) > 1:
                FullName += " "
            FullName += MiddleName.strip()

        if len(LastName.strip()) > 1:
            if len(FullName.strip()) > 1:
                FullName += " "
            FullName += LastName.strip()
        
        if len(Suffix.strip()) > 1:
            if len(FullName.strip()) > 1:
                FullName += " "
            FullName += Suffix.strip()

    return FullName

def validate_name(full_name=None, first_name=None, middle_name=None, last_name=None, suffix=None): 

    show_name_part_errors = True
    if full_name:
        show_name_part_errors = False
        first_name, middle_name, last_name, suffix = SplitName(full_name=full_name)
    
    if suffix:
        last_name = u'%s %s' % (last_name, suffix)

    first_name_error = None
    middle_name_error = None
    last_name_error = None
    
    first_name_validate_result = validate_first_name(first_name=first_name)
    
    first_name_error = first_name_validate_result.get('StatusMessage', None)

    middle_name_validate_result = validate_middle_name(middle_name=middle_name) #20210722 was first_name ?
    
    middle_name_error = middle_name_validate_result.get('StatusMessage', None)
    
    last_name_validate_result = validate_last_name(lastname=last_name)

    last_name_error = last_name_validate_result.get('StatusMessage', None)
    
    if not show_name_part_errors:
        
        response_code = 1
        
        if response_code > first_name_validate_result.get('ResponseCode', 0):
            response_code = first_name_validate_result.get('ResponseCode', 0)
        
        if response_code > middle_name_validate_result.get('ResponseCode', 0):
            response_code = middle_name_validate_result.get('ResponseCode', 0)

        if response_code > last_name_validate_result.get('ResponseCode', 0):
            response_code = last_name_validate_result.get('ResponseCode', 0)
        
        return {'ResponseCode': response_code, 'status_message': u'%s %s %s' % (first_name_error, middle_name_error, last_name_error)}
    
    return {
           'first_name_validate_result': first_name_validate_result,
           'middle_name_validate_result': middle_name_validate_result,
           'last_name_validate_result': last_name_validate_result,
           }


def validate_first_name(first_name=None): 
    return validate_name_string(name_string=first_name, string_label=u'First Name')

def validate_middle_name(middle_name=None, force_middle_initial=False): 

    max_length = 80
    name_label = u'Middle Name'
    if force_middle_initial:
        max_length = 1
        name_label = u'Middle Initial'

    return validate_name_string(name_string=middle_name, string_label=name_label, min_length=1, max_length=max_length)
    
def validate_name_string(name_string=None, string_label=u'name', min_length=2, max_length=80): 
    """
    Last Name must be at least 2 characters long and less than 80 characters long.  Only alphanumeric characters, single quotes (') and dashes (-) allowed
    returns 1 if last name passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }

    if not name_string:
        data_to_return['StatusMessage'] = u'No %s.' % (string_label)
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    NameTokens = name_string.strip()
    
    if len(name_string) < min_length:
        data_to_return['StatusMessage'] = u'%s must be at least %d characters long.' % (string_label, min_length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    if len(name_string) > max_length:
        data_to_return['StatusMessage'] = u'%s can not be longer than %d characters.' % (string_label, max_length)
        data_to_return['ResponseCode'] = 0

        return data_to_return
#1-zA-Z0-1@#.,'/\-\s
#"^([a-zA-Z'/\-])$"
#    bob = re.compile("^[a-z]$").search(name_string)

    if not re.compile("^([a-zA-Z'/\- ]+)$").search(name_string):
        data_to_return['StatusMessage'] = u'%s (%s) must only contain alphanumeric characters, single quotes (\') and dashes (-) allowed.' % (string_label, name_string)
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    return data_to_return

def build_name_query(first_name_label='firstname', middle_name_label='middlename', last_name_label='lastname', suffix_label='suffix', full_name=None, first_name=None, middle_name=None, last_name=None, suffix=None):
    if full_name:
        (first_name, middle_name, last_name, suffix) = SplitName(full_name)
        
    search_kwargs = {}
    if first_name:
        if len(first_name) == 1:
            search_kwargs[ '%s__istartswith' % (first_name_label) ] = first_name
        else:
            if first_name.find('*'): 
                search_kwargs[ '%s__icontains' % (first_name_label) ] = first_name
            else:
                search_kwargs[ '%s__iexact' % (first_name_label) ] = first_name

    if middle_name:
        if len(middle_name) == 1:
            search_kwargs[ '%s__istartswith' % (middle_name_label) ] = middle_name
        else:
            if middle_name.find('*'): 
                search_kwargs[ '%s__icontains' % (middle_name_label) ] = middle_name
            else:
                search_kwargs[ '%s__iexact' % (middle_name_label) ] = middle_name

    if last_name:
        if len(last_name) == 1:
            search_kwargs[ '%s__istartswith' % (last_name_label) ] = last_name
        else:
            if last_name.find('*'): 
                search_kwargs[ '%s__icontains' % (last_name_label) ] = last_name
            else:
                search_kwargs[ '%s__iexact' % (last_name_label) ] = last_name

    if suffix:
        search_kwargs[ '%s__iexact' % (suffix_label) ] = suffix

    return search_kwargs

