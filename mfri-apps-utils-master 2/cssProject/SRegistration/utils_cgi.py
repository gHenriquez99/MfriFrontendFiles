import os
import codecs
import string
import json
import time
import datetime
import re
import base64
import urllib2
import sys


SERVER_NAME = u'https://mfridev.umd.edu' 

def StudentRegistrationCGIURL(scheduled_course_id=None, sreg_id=None):
    if not scheduled_course_id:
        return None
    
    if not sreg_id:
        return None
    
    return u'%s/cgi-bin/stureg_edit.cgi?RED=0&SRID=%s&SCID=%s' % (SERVER_NAME, sreg_id, scheduled_course_id)

def CourseRegistrationCGIURL(scheduled_course_id=None):
    if not scheduled_course_id:
        return None

    return u'%s/cgi-bin/stureg_reg.cgi?SCID=%s' % (SERVER_NAME, scheduled_course_id)


