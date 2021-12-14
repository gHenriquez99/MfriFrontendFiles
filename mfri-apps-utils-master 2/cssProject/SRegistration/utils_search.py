
import re
import json
import base64
import datetime
from operator import attrgetter 

from SRegistration.models import *
from SRec.utils import student_record_id_number_query 

from MSchedule.utils_search import FindCourseFromLogNumber



def FindStudentRecord(partial_ssn=None, full_ssn=None, state_provider_number=None, nfa_sid_number=None, last_name=None):

    if not partial_ssn:
        partial_ssn = full_ssn
        
        if not partial_ssn and not state_provider_number and not nfa_sid_number:
            return None

    if partial_ssn: 
        if partial_ssn[0:3].upper() != u'MSN':
            if partial_ssn[0:3] == u'000':
                partial_ssn = str(int(partial_ssn))

    ssn_matches = student_record_id_number_query(epins=state_provider_number, nfa_sid=nfa_sid_number, ssn=partial_ssn, last_name=last_name, allow_partial_ssn=True)#20171102

    if ssn_matches:
        student_record = ssn_matches[0]
    else:
        if not partial_ssn and not full_ssn:
            return None
        
        ssn_matches = Student_Record_SSN_Query(ssn=partial_ssn)
        if ssn_matches:
            student_record = ssn_matches[0]
        else:
            if full_ssn and u'MSN' == full_ssn[0:3]:
                ssn_matches = Student_Record_SSN_Query(ssn=full_ssn)

                if ssn_matches:
                    student_record = ssn_matches[0]
                else:
                    student_record = None
            elif full_ssn and str(int(full_ssn)) > 0:
                ssn_matches = Student_Record_SSN_Query(ssn=full_ssn)

                if ssn_matches:
                    student_record = ssn_matches[0]
                else:
                    student_record = None
            else:
                student_record = None
                
    return student_record








