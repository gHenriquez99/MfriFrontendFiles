import os
import codecs
import string
import json
import time
import datetime


from SRegistration.models import *

from SRegistration.utils_cgi import CourseRegistrationCGIURL 


def GetFeeBatchesForStudent(student_record=None):

    if not student_record:
        return None
    
    student_registration_list = Studentregistration.objects.filter(student_record=student_record).order_by('scheduled_course__start_date')
    
    student_fee_batch_list = []
    for student_registration in student_registration_list:
        

        if student_registration.pidn_batch:
            student_fee_batch_list.append(student_registration.pidn_batch)
        
        if student_registration.invoice_batch:
            student_fee_batch_list.append(student_registration.invoice_batch)

        if student_registration.credit_batch:
            student_fee_batch_list.append(student_registration.credit_batch)


    return student_fee_batch_list

def FormatFeeBatchesForStudent(fee_batch_list=None, student_record=None):
    
    if not student_record:
        return u''

    if not fee_batch_list:
        fee_batch_list = GetFeeBatchesForStudent(student_record=student_record)
    
    if not fee_batch_list:
        return u'' #return {'student_record': student_record, 'is_cleared': False, 'clearance_type':u'No Medical Clearance on File', 'clearance_message':u'Not cleared for MFRI Classes', 'determination_date':None, 'exam_date':None, 'clearance_note': None} #20210322

    formatted_batch_list = []
    for fee_batch in fee_batch_list:
        
        scheduled_course = None
        scheduled_course_id = None
        log_number = u''
        tcode = u'Address only batch. No charges.'
        
        if fee_batch.scheduled_course:
            scheduled_course = fee_batch.scheduled_course
            scheduled_course_id = fee_batch.scheduled_course.id
            log_number = fee_batch.scheduled_course.log_number

        if fee_batch.batch_type.batch_type_abbreviation != u'PIDN':
            tcode = fee_batch.tcode.full_name

        
        formatted_batch_list.append({
            'course_edit_url': CourseRegistrationCGIURL(scheduled_course_id=scheduled_course_id),
            'fee_batch': fee_batch, 
            'student_record': student_record, 
            'scheduled_course': scheduled_course, 
            'log_number': log_number, 
            'date_sent_to_accounting': fee_batch.date_sent_to_accounting, 
            'date_sent_to_bursar': fee_batch.date_sent_to_bursar, 
            'tcode': tcode, 
            'umd_term':  fee_batch.umd_term.full_name, 
            'item_reference':  fee_batch.item_reference, 
            'status':  fee_batch.status.name, 
            'batch_type':  fee_batch.batch_type.batch_type_abbreviation, 
           })
    
    return formatted_batch_list

















