
import re
import json
import base64
import datetime

from MOffices.models import Jurisdictions
from MAffiliations.models import Affiliations
from MOffices.models import Jurisdictions
from MSchedule.models import *

from MSchedule.utils_search import ScheduledCourseRecord

def format_start_end_date(start_date=None, end_date=None, show_labels=True, if_no_date_show_underlines=False):
    
    date_label = u''
    if show_labels:
        date_label = u'Date: '
    
    if start_date and end_date:
        if start_date != end_date:
            if show_labels:
                date_label = u'Start/End Dates: '
            return u'%s%s/%s' % (date_label, start_date, end_date)
        else:
            return u'%s%s' % (date_label, start_date)
    elif start_date:
        return u'%s%s' % (date_label, start_date)
    elif end_date:
        return u'%s%s' % (date_label, end_date)
    else:
        if if_no_date_show_underlines:
            return u'%s____-____-________ / ____-____-________' % (date_label)
        else:
            return u'%s' % (date_label)
            

def mfri_report_header_data(scheduled_course=None, log_number=None, show_date_labels=True):

    log_number = u''
    course_name = u''
    mfri_office_name = u''
    lead_instructor_name = u''
    lead_instructor_uid = u''
    location_name = u''
    course_dates = u''

    if not scheduled_course:
        if log_number:
            scheduled_course = ScheduledCourseRecord(log_number=log_number)

    if scheduled_course:
        log_number = scheduled_course.log_number
        course_name = scheduled_course.course_name
        mfri_office_name = scheduled_course.mfri_office_name
        lead_instructor_name = scheduled_course.lead_instructor_name
        lead_instructor_uid = scheduled_course.lead_instructor_uid
        location_name = scheduled_course.location_name
        course_dates = format_start_end_date(start_date=scheduled_course.start_date_MMDDYYY, end_date=scheduled_course.end_date_MMDDYYY, show_labels=show_date_labels)

    return {
            'log_number':             log_number,
            'course_name':            course_name,
            'mfri_office_name':       mfri_office_name,
            'lead_instructor_name':   lead_instructor_name,
            'lead_instructor_uid':    lead_instructor_uid,
            'location_name':          location_name,
            'course_dates':           course_dates,
           }

