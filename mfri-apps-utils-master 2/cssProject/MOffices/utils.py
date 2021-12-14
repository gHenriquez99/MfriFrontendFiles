
import re

from MOffices.models import *


def ValidateOfficeAbbreviation(abbreviation=None): 
    """
    Abbreviation must be at least 2 characters long and less than 8 characters long.  Only upper case alphanumeric characters
    returns 1 if abbreviation passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    

    min_Length = 2
    max_Length = 8

    if len(abbreviation) < min_Length:
        data_to_return['StatusMessage'] = u'Abbreviation must be at least %d characters long.' % (min_Length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    if len(abbreviation) > max_Length:
        data_to_return['StatusMessage'] = u'Abbreviation can not be longer than %d characters.' % (max_Length)
        data_to_return['ResponseCode'] = 0

        return data_to_return

    if not re.compile("^([A-Za-z]+)$").search(abbreviation): 
        data_to_return['StatusMessage'] = u'Abbreviation must only contain alphanumeric characters, single quotes (\') and dashes (-) allowed.'
        data_to_return['ResponseCode'] = 0

        return data_to_return

    try:
        office_list = MfriOffices.objects.all().values()
    except Exception as e:
        data_to_return['StatusMessage'] = u'No offices found: %s' % (e)
        data_to_return['ResponseCode'] = 0

        return data_to_return

    for office in office_list:

        try:
            if office['abbreviation'].upper() == abbreviation.upper(): 
                return data_to_return
        except Exception as e:
            data_to_return['StatusMessage'] = u'Invalid office record: %s' % (e)
            data_to_return['ResponseCode'] = 0

    data_to_return['StatusMessage'] = u'Abbreviation does not match an office.'
    data_to_return['ResponseCode'] = 0

    
    return data_to_return



def GetDefaultPrimaryPhoneNumberType():
    try:
        default_type = Phonenumbertypes.objects.get( name__iexact='Primary' )
    except Phonenumbertypes.DoesNotExist:
        return None
    return default_type

def GetDefaultSecondaryPhoneNumberType():
    try:
        default_type = Phonenumbertypes.objects.get( name__iexact='Secondary' )
    except Phonenumbertypes.DoesNotExist:
        return None
    return default_type


def UnknownJurisdictionDefault():
    try:
        default_value = Jurisdictions.objects.get( pk=30 ) #30 unkown Jurisdiction
    except Jurisdictions.DoesNotExist:
        return None
    except Jurisdictions.MultipleObjectsReturned:
        return None
    return default_value

def GetDefaultJurisdiction(pk=None):
    
    if pk:
        default_value_list = Jurisdictions.objects.filter( pk=pk )
            
        if default_value_list:
            return default_value_list[0]
    
    return UnknownJurisdictionDefault()

def GetOfficeCodeFromSectionID( legacy_section_id = None ):

    default_office_code = u'fo'

    if not legacy_section_id.isdigit():
        return default_office_code

    if not legacy_section_id:
        return default_office_code

    try:
        legacy_mfri_section = LegacyCoursesection.objects.get(pk = legacy_section_id)
    except LegacyCoursesection.DoesNotExist:
        return default_office_code

    try:
        legacy_mfri_section_abbreviation = legacy_mfri_section.abbreviation
    except:
        return default_office_code
    
    office_code = default_office_code
    
    if legacy_mfri_section_abbreviation == u'SPS':
        office_code = (legacy_mfri_section_abbreviation).lower()
    elif legacy_mfri_section_abbreviation == u'FO ':
        office_code = legacy_mfri_section_abbreviation.lower()
    elif legacy_mfri_section_abbreviation == u'ALL':
        office_code = u'hq'
    elif legacy_mfri_section_abbreviation == u'OTH':
        office_code = u'hq'
    elif legacy_mfri_section_abbreviation == u'ALS':
        office_code = legacy_mfri_section_abbreviation.lower()
    elif legacy_mfri_section_abbreviation == u'ADS':
        office_code = legacy_mfri_section_abbreviation.lower()
    elif legacy_mfri_section_abbreviation == u'LSS':
        office_code = legacy_mfri_section_abbreviation.lower()
    elif legacy_mfri_section_abbreviation == u'DIR':
        office_code = legacy_mfri_section_abbreviation.lower()
    elif legacy_mfri_section_abbreviation == u'IDS':
        office_code = legacy_mfri_section_abbreviation.lower()
    elif legacy_mfri_section_abbreviation == u'TCS':
        office_code = legacy_mfri_section_abbreviation.lower()
    else:
        office_code = default_office_code
    
    return office_code



