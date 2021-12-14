import os
import codecs
import string
import json
import time
import datetime
import re


from AppsAdmin.dbk import SRecEncryptKeyS

from SRec.models import *
from MStaff.utils import validate_ssn, parse_last_name_suffix, validate_last_name, split_name, build_name_query

def validate_mfri_student_number(mfri_student_number=None): 
    """
    MFRI Student Number must be 8 digits long.  Only digits allowed.
    7 digits with 1 check sum
    it is an EAN-8 barcode
    returns 1 if msn passes and 0 if there is an error.
    """
    data_to_return = {  'StatusMessage': '',
                        'ResponseCode': 1,
                     }    

    if not mfri_student_number:
        data_to_return['StatusMessage'] = u'Null MFRI Student Number.'
        data_to_return['ResponseCode'] = 0

        return data_to_return


    msn_length = 8

    if len(mfri_student_number) != msn_length:
        data_to_return['StatusMessage'] = u'MFRI Student Number must be %d digits.' % (msn_length)
        data_to_return['ResponseCode'] = 0
        
        return data_to_return

    if not re.compile("^\d+$").search(mfri_student_number):
        data_to_return['StatusMessage'] = u'MFRI Student Number must only contain digits.'
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    if not ValidateEAN8CheckSum(mfri_student_number=mfri_student_number):
        data_to_return['StatusMessage'] = u'Checksum error in MFRI Student Number.'
        data_to_return['ResponseCode'] = 0

        return data_to_return
    
    return data_to_return

def StudentRecordSearchMFRIStudentNumber(mfri_student_number=None, last_name=None):
    if not mfri_student_number:
        return None

    mfri_student_number_validation_result = validate_mfri_student_number(mfri_student_number=mfri_student_number)

    if mfri_student_number_validation_result['ResponseCode'] < 1:
        return None

    response_list = None

    if not last_name:
        try:
            response_list = Studentrecords.objects.get(mfri_student_number__exact=mfri_student_number)
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
            response_list = Studentrecords.objects.get(mfri_student_number__exact=mfri_student_number, lastname__iexact=last_name)
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

def HighestMFRIStudentNumberSeed():
    
    student_records_count_min = 1000110
    
    starting_number = AssignEAN8CheckSum(first_7_digits=str(student_records_count_min))

    student_records_list = Studentrecords.objects.filter(mfri_student_number__gte=starting_number).order_by('-mfri_student_number')

    if not student_records_list:
        return str(student_records_count_min)

    highest_mfri_student_number = student_records_list[0].mfri_student_number

    print u'highest_mfri_student_number %s\n' % (highest_mfri_student_number)
    return highest_mfri_student_number[:7]

def GetStudentRecordByStudentNumber(mfri_student_number=None):
    
    if not mfri_student_number:
        return None

    try:
        student_record = Studentrecords.objects.filter(mfri_student_number__exact=mfri_student_number.strip())
    except Studentrecords.MultipleObjectsReturned:
        return None
    except Studentrecords.DoesNotExist:
        return None
            
    return student_record

def DoesMFRIStudentNumberExist(mfri_student_number=None):
    
    if not mfri_student_number:
        return False

    try:
        does_exist = Studentrecords.objects.filter(mfri_student_number__exact=mfri_student_number).exists()
    except Studentrecords.MultipleObjectsReturned:
        return True
    
    except Studentrecords.DoesNotExist:
        return False
            
    return does_exist

def ValidateEAN8CheckSum(mfri_student_number=None):
    
    if not mfri_student_number:
        return False
    
    first_7_digits = mfri_student_number[:7]
    found_checksum_digit = int(mfri_student_number[7:8])

    sum1 = int(first_7_digits[1] + first_7_digits[3] + first_7_digits[5]) 
    sum2 = int(3 * (first_7_digits[0] + first_7_digits[2] + first_7_digits[4] + first_7_digits[6]))
    checksum_value = sum1 + sum2

    calculated_checksum_digit = 10 - (checksum_value % 10);
    if (calculated_checksum_digit == 10):
        calculated_checksum_digit = 0;

    if found_checksum_digit == calculated_checksum_digit:
        return True

    return False
    

def AssignEAN8CheckSum(first_7_digits=None):
    
    if not first_7_digits:
        return None

    sum1 = int(first_7_digits[1] + first_7_digits[3] + first_7_digits[5]) 
    sum2 = int(3 * (first_7_digits[0] + first_7_digits[2] + first_7_digits[4] + first_7_digits[6]))
    checksum_value = sum1 + sum2

    checksum_digit = 10 - (checksum_value % 10);
    if (checksum_digit == 10):
        checksum_digit = 0;
    
    return u'%s%d' % (first_7_digits, checksum_digit)
    
    
def AssignNewMFRIStudentNumber(user=None, student_record=None, prior_number=None, force_new_number=False): 
    print u'AssignNewMFRIStudentNumber to %d\n' % (student_record.id)

    if not student_record:
        print u'no student record\n'
        return None

    if not student_record.id:
        try:
            student_record.save(user=user) 
        except:
            print u'did not save student record\n'
            return None
    
    print u'student record ssn %s\n' % (student_record.ssn_clear)
    ssn_valudation_result = validate_ssn(ssn=student_record.ssn_clear)

    if ssn_valudation_result['ResponseCode'] < 1:
        print u'did not save student record %s\n' % (ssn_valudation_result.get('StatusMessage', u'no message'))
        return None
        
    found_mfri_student_number = GetMFRIStudentNumberForSSN(ssn=student_record.ssn_clear)

    if found_mfri_student_number and len(found_mfri_student_number.strip()) > 0 and not force_new_number:
        mfri_student_number_validation_result = validate_mfri_student_number(mfri_student_number=found_mfri_student_number)

        if mfri_student_number_validation_result['ResponseCode'] < 1:
            found_mfri_student_number = None
    
    if found_mfri_student_number:
        print u'found_mfri_student_number\n'
        if ((not student_record.mfri_student_number) or len(student_record.mfri_student_number) == 0) or (found_mfri_student_number != student_record.mfri_student_number):
            
            record_msn = student_record.mfri_student_number
            
            student_record.lock()
            try:
               student_record.mfri_student_number = found_mfri_student_number
               student_record.save(update_fields=['mfri_student_number'])
            finally:
                student_record.unlock()
        return student_record.mfri_student_number
        
    if student_record.mfri_student_number and len(student_record.mfri_student_number) > 0 and not force_new_number:
        print u'student record has number, skipping %s\n' % (student_record.mfri_student_number)
        saved_mfri_student_number = SetMFRIStudentNumberForSSN(ssn=student_record.ssn_clear, mfri_student_number=student_record.mfri_student_number)

        return student_record.mfri_student_number
        
    student_records_count_min = 1000111
    student_records_count_max = 9999999

    if prior_number:
        student_records_count = int(prior_number[:7]) + 1 
    else:
        student_records_count = int(HighestMFRIStudentNumberSeed()) + 1 

    if str(student_records_count)[5:7] == u'00':
        student_records_count += 1

    mfri_student_number = None
    student_record.lock()
    try:
        while student_records_count >= student_records_count_min and student_records_count < student_records_count_max:

            mfri_student_number = AssignEAN8CheckSum(first_7_digits=str(student_records_count))
            
            if not DoesMFRIStudentNumberExist(mfri_student_number=mfri_student_number):
                break
            
            student_records_count += 1
            
            if str(student_records_count)[5:7] == u'00':
                student_records_count += 1

        if mfri_student_number:
           student_record.mfri_student_number = mfri_student_number
           student_record.save(update_fields=['mfri_student_number'])
    finally:
        student_record.unlock()

    saved_mfri_student_number = SetMFRIStudentNumberForSSN(ssn=student_record.ssn_clear, mfri_student_number=student_record.mfri_student_number)

    print u'check saved msn %s\n' % (GetMFRIStudentNumberForSSN(ssn=student_record.ssn_clear))
    
    print u'returning saved_mfri_student_number %s\n' % (saved_mfri_student_number)
    return student_record.mfri_student_number
    

def GetMFRIStudentNumberLookupRecordForSSN(ssn=None):
    
    if not ssn:
        return None
    
    ssn_valudation_result = validate_ssn(ssn=ssn)

    if ssn_valudation_result['ResponseCode'] < 1:
        return None

    try:
        response_list = MFRIStudentNumberLookup.objects.raw('SELECT id FROM MFRIStudentNumberLookup WHERE (AES_DECRYPT(ssn, %s) like %s)', (SRecEncryptKeyS(), ssn))
    except MFRIStudentNumberLookup.MultipleObjectsReturned:
        return None

    except MFRIStudentNumberLookup.DoesNotExist:
        return None
        
    if not response_list: 
        return None

    try:
        first_record = response_list[0]
    except:
        return None

    if not first_record:
        return None

    return first_record

def GetMFRIStudentNumberForSSN(ssn=None):
    
    if not ssn:
        assert False
        return None
    
    found_lookup_record = GetMFRIStudentNumberLookupRecordForSSN(ssn=ssn)
    
    if not found_lookup_record:
        return None
    print u'ssn on file for %s is %s' % (found_lookup_record.mfri_student_number, found_lookup_record.ssn_clear)
    return found_lookup_record.mfri_student_number
    
def SetMFRIStudentNumberForSSN(ssn=None, mfri_student_number=None, force_new_number=False):

    print u'SetMFRIStudentNumberForSSN for %s\n' % (ssn)
    
    if not ssn:
        print u'no ssn\n'
        return None
    
    ssn_valudation_result = validate_ssn(ssn=ssn)

    if ssn_valudation_result['ResponseCode'] < 1:
        print u'ssn validation error %s\n' % (ssn_valudation_result.get('StatusMessage', u'no ssn validate error message found.'))
        return None

    mfri_student_number_validation_result = validate_mfri_student_number(mfri_student_number=mfri_student_number)

    if mfri_student_number_validation_result['ResponseCode'] < 1:
        return None

    found_lookup_record = GetMFRIStudentNumberLookupRecordForSSN(ssn=ssn)
    
    if found_lookup_record:
        print u'found lookup record %d\n' % (found_lookup_record.id)
        if force_new_number:
            print u'force_new_number\n'
            found_lookup_record.mfri_student_number = mfri_student_number
            try:
                found_lookup_record.save()
            except Exception as e:
                print u'error saving lookup record %s\n' % (e)
                return None
            print u'forced new msn %s\n' % (mfri_student_number)
            return mfri_student_number
        else:
            print u'not force_new_number\n'
            
            mfri_student_number_validation_result = validate_mfri_student_number(mfri_student_number=found_lookup_record.mfri_student_number)

            if mfri_student_number_validation_result['ResponseCode'] > 0:
                print u'msn validation error %s\n' % (mfri_student_number_validation_result.get('StatusMessage', u'no msn validate error message found.'))
                return found_lookup_record.mfri_student_number
            else:
                print u'possible msn validation error %d %s\n' % (mfri_student_number_validation_result.get('ResponseCode', u'no msn validate error number found.'), mfri_student_number_validation_result.get('StatusMessage', u'no msn validate error message found.'))
                print u'replacing found msn (%s) with new one %s' % (found_lookup_record.mfri_student_number, new_student_number)
                found_lookup_record.mfri_student_number = mfri_student_number
                try:
                    found_lookup_record.save()
                except Exception as e:
                    print u'error saving lookup record %s\n' % (e)
                    return None
        print u'updated msn %s\n' % (mfri_student_number)
        return found_lookup_record.mfri_student_number

    new_mfri_student_number_lookup_record = MFRIStudentNumberLookup(
                                                                    mfri_student_number = mfri_student_number,
                                                                   )

    try:
        new_mfri_student_number_lookup_record.save()
    except Exception as e:
        print u'error saving lookup record %s\n' % (e)
        return None

    try:
        new_mfri_student_number_lookup_record.ssn_clear = ssn

        new_mfri_student_number_lookup_record.save()
    except Exception as e:
        print u'error saving lookup ssn to record %s\n' % (e)
        return None

    #finally:
    #    new_mfri_student_number_lookup_record.unlock()
    print u'return new msn %s\n' % (mfri_student_number)

    return mfri_student_number
