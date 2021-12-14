
from MSchedule.utils import ScheduledCourseRecord

#This returns a url to the perl script cgi 

def CourseEditUrl(log_number=None, scheduled_course=None):

    if not scheduled_course:
        if log_number:
            scheduled_course = ScheduledCourseRecord(log_number=log_number)

    if scheduled_course:
        return u'/cgi-bin/schedule_edit.cgi?FormButton=Go&SchedID=%d' % (scheduled_course.id)
    else:
        return None
        
