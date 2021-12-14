
import sys, getopt
import json
import base64
import datetime 

import urllib2

from django.http import HttpResponseRedirect #Http404, HttpResponse, 

from django.core.urlresolvers import reverse

from MFRI_Utils.data_encode import encode_context

def ExceptionRedirect(
                   log_number=None, 
                   office_code=None, 
                   exception_label=u'System Error',
                   exception_message=u'E001 Unknown Error.'):
                  
    error_context_encoded = encode_context(context_data={
                                                         'office_code': office_code,
                                                         'log_number': log_number,
                                                         'exception_label': exception_label,
                                                         'exception_message': exception_message,
                                                         })
    return HttpResponseRedirect(reverse('apps_exception', kwargs={'context':error_context_encoded}))
