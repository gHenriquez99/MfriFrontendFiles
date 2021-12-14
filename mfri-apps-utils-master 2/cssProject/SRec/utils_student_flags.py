import os
import codecs
import string
import json
import time
import datetime
import re

from AppsAdmin.dbk import SRecEncryptKeyS

from SRec.models import *
from SRec.utils import GetStudentRecord

def GetStudentFlagsList(student_record=None, pk=None):
    
    if not student_record:
        student_record = GetStudentRecord(pk=pk)
    
    if not student_record:
        return []

    student_flags = Studentflagassignments.objects.filter(student_record__exact=student_record) 

    if not student_flags:
        return []

    flag_list_to_return = []
    for flag_record in student_flags:
        if flag_record.expiration_date and flag_record.expiration_date.strftime('%Y-%m-%d') != u'0000-00-00':
            if flag_record.expiration_date <= datetime.datetime.today():
                continue
                
        flag_list_to_return.append(flag_record)
        

    return flag_list_to_return

