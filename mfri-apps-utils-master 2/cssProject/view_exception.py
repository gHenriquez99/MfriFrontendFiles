
#import sys, getopt
#import json
#import base64
#import datetime 

#import urllib2

from django.http import HttpResponseRedirect #Http404, HttpResponse, 
#from django.shortcuts import render
from django.urls import reverse

from mfri.utils.data_encode import encode_context #, decode_context

def ExceptionRedirect(schedule_code=u'msfs', 
                   log_number=None, 
                   office_code=None, 
                   exception_label=u'System Error',
                   exception_message=u'E001 Unknown Error.'):
                  
    error_context_encoded = encode_context(context_data={'schedule_code': schedule_code, 
                                                         'office_code': office_code,
                                                         'log_number': log_number,
                                                         'exception_label': exception_label,
                                                         'exception_message': exception_message,
                                                         })
    return HttpResponseRedirect(reverse('exception_report', kwargs={'context':error_context_encoded}))
