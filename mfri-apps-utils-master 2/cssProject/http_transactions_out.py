#import re
#import datetime
#import time
import json
import base64
#import urllib2
#from cStringIO import StringIO
#from io import StringIO
#from decimal import *

import requests

#from reportlab.pdfgen import canvas
#from reportlab.lib import colors
#from reportlab.lib.pagesizes import letter
#from reportlab.lib.units import inch
#from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
#from reportlab.pdfbase.pdfmetrics import stringWidth

#from django.http import HttpResponse
#from django.conf import settings
#from django.core.urlresolvers import reverse
#from django.utils.safestring import mark_safe
#from django.template.loader import get_template
#from django.template import Context, RequestContext

#from MOffices.models import MfriOffices
#from MOffices.utils import validate_office_abbreviation
#from MCourses.utils import validate_course_category

from mfri.utils.data_encode import encode_context
from mfri.utils.data_encrypt import CreateEncryptKey, EncryptContext, DecryptContext

def SZ_Local_Testing():
    return False #settings.DEBUG

def Remote_Server_Registration_Path():
    return u'registration' 

def Remote_Server_Transcript_Path():
    return u'izone/student/transcript' 
    #return u'transcript' 

def Transaction_Server_Protocol(local_test=False):

    if local_test:
        return u'http'
    
    return 'https'

def Transaction_Server_Name(local_test=False):

    if local_test:
        return u'localhost:8000'
    
    return 'zone.mfri.org'

def Send_Transaction(transaction_data=None, encode_data=False, transaction_url=None, extra_data=None, return_raw_response=False, server_url=Transaction_Server_Name(), transaction_protocol='https://', testing_before=False, testing_after=False, encrypt_data=False, spec_test=False):#20211011 #20211012

#    contact_details = None
#    StatusMessage = 'No Status Found'

    if not transaction_data:
        return {'ResponseCode': -10, 'StatusMessage': 'Null transaction data'}
    
    if len(transaction_data) == 0:
        return {'ResponseCode': -12, 'StatusMessage': 'No transaction data'}

    if not transaction_url:
        return {'ResponseCode': -14, 'StatusMessage': 'Null Transaction'}

    if len(transaction_url) == 0:
        return {'ResponseCode': -15, 'StatusMessage': 'No Transaction'}

    #20211011+
    if spec_test:
        server_response_raw = u'gAAAAABhZZ6mznVmGXQ2HX4NZWhkLOpnwyyUpe5ItcLn1iWmw44wLCwzb9CK0gUf6RgB1leycp3nXiDimMbITi3VrfwUPd37e6ck3qvuytKkhPOwLzH6PzQnKoY2jEjuQG5p96CRRTtx9ZFUYjOMhrHELI2PAqCaEr6Lhe2vWLC2qwEi8cNiQOUoxOag8Auy9bQZ-eld96DvGmUrO6kYLYfWc321Weub7YQazYd9sa7DqFzINvl78a7gFUM3ZYs5BNgE2caC-9wMfAvjxgF7xSc_-W3RGeVHWsHcFRnz92Zr_GhfzKi4GQXF4R9g0u0y6ZryblyjgQtatPlrz8B4F9fK-qAepEdiZUP0zMZ5wU2HSxxhivUzZe5Npk6dwhRb3tnwYQDCkMsjZ41SnxUIoeKMWxTx8ViSEKgDntv3yBoeBtJWDCzgHzbllTRLPDsoepHfceJFoPe5y_OVmwtDmMwO3DWMfutUK1VnSdbbVfYSN2OJUzUgtJjA-Iijue9YRADNp0TmIlK0S9yYooMpSmjjgXDGCun5zXEsamooHwFZWiVdqtWNbAhfGNNtfBqXo54-H6OVYvZhyHnk8sUoKmr01ynyyUYcrSld2jdiZJ-J8ZeYXDv7EqYYojNtb08u3eu0geBsixycCfNKfxjGBhNgZ7HM-FIoZVW485SaYYbdqXHKUCer4DYDAXf1z9T6-p8K5tELT6lHqe1PzTRFLHWGJEq7I1dKUEzPHUkaevMPwgpmy46yROJDeMaC-weIYCUk1H0umgTzWPVqlVZMWAqxsvRJ8mTSbVz-XscE96pSRapw5RakcaqE740NLFGjsVbcrKegv1WnTXPHuPjqslECEg--dopPon4iubstLik64xNMKqm-PQoPA7L5OeSXg7q3dRWH0pe-pjcZqdWuVJGFd6cPmDzjorGo3gd5kNI1cKqq0qR9v2jt-TwwmSJQzqezDqfYxr_uLMnyfETG1IvOhp5-yuNhwpUP7efj-KT96s6V-X_KcK4XSLS8zm3_XSEInNTTLD26MkqYDWdKUxQJ5V82RTngbHtz7tx3ILWzraoxymdonELpQDIPKdZl-3RWVaL9jJss_vLCD247cgvYTp8J9bi9cw=='
        if encrypt_data:
            server_response_raw = DecryptContext(encrypted_context=server_response_raw, encryption_key=CreateEncryptKey(), decode_data_after=encrypt_data)
        
        if return_raw_response: #transaction_url == '/mtes/getform':
            return server_response_raw
            
        server_response_json = server_response_raw
        #server_response_json = json.loads(server_response_raw)
        #try:
        #    server_response_json = server_response_raw.json() #json.loads(server_response_raw)
        #except ValueError: 
        #    return False
        
        struct_to_return = {}
        #assert False
        if extra_data:
            for ed_key, ed_value in extra_data.items():
                if ed_key in server_response_json:
                    struct_to_return[ed_key] = server_response_json[ed_key]
        
        if 'StatusMessage' in server_response_json:
            struct_to_return['StatusMessage'] = server_response_json['StatusMessage']
        
        if 'ResponseCode' in server_response_json:
            struct_to_return['ResponseCode'] = server_response_json['ResponseCode']
        
        #20211012+
        if 'e_d' in server_response_json:
            struct_to_return['e_d'] = server_response_json['e_d']
        #20211012-

        return struct_to_return
        
    #20211011-
        


    #20211011transaction_data_json = json.dumps(transaction_data)
    transaction_data_json = transaction_data

    if encode_data:
        #transaction_data_json_base64 = base64.urlsafe_b64encode(transaction_data_json).strip('=')
        
        if encrypt_data:
            transaction_data_json_base64 = EncryptContext(context_data=transaction_data_json, encryption_key=CreateEncryptKey(), encode_data_before=encode_data)
        else:
            transaction_data_json_base64 = encode_context(context_data=transaction_data_json)
    else:
        if encrypt_data:
            transaction_data_json_base64 = EncryptContext(context_data=transaction_data_json, encryption_key=CreateEncryptKey(), encode_data_before=encode_data)
        else:
            transaction_data_json_base64 = transaction_data_json
        
    fully_qualified_transaction_url = u'%s%s%s/%s' % (transaction_protocol, server_url, transaction_url, transaction_data_json_base64)

    #20211012+
    if testing_before:
        assert False
    #20211012-
    
    try:
        server_response_raw = requests.get(fully_qualified_transaction_url).json()
    except Exception: #, e:
        if server_response_raw:
            return server_response_raw
        else:
            return False
#    try:
#        server_response_raw = urllib2.urlopen(fully_qualified_transaction_url).read()
#    except urllib2.HTTPError, error:
#        #bob = error.read()
#        return {'StatusMessage': u'Remote Server Error: %s' % (error.msg),
#                'ResponseCode': -98}
#    except Exception, e:
#        if transaction_url != '/mtes/getform':
#            return {'StatusMessage': u'Remote Server Error: %s' % (e),
#                    'ResponseCode': -99}
#        else:
#            if server_response_raw:
#                return server_response_raw
#            else:
#                return {'StatusMessage': u'No Remote Server response but one was expected. Error: %s' % (e),
#                        'ResponseCode': -99}

    #20211012if encrypt_data:
    #20211012    server_response_raw = DecryptContext(encrypted_context=server_response_raw, encryption_key=CreateEncryptKey(), decode_data_after=encrypt_data)

    #20211012+
    if testing_after:
        assert False
    #20211012-
    
    if return_raw_response: #transaction_url == '/mtes/getform':
        return server_response_raw
        

    #server_response_json = json.loads(server_response_raw)
    try:
        server_response_json = server_response_raw #json.loads(server_response_raw)
    except ValueError: 
        return False

    struct_to_return = {}
    #assert False
    if extra_data:
        for ed_key, ed_value in extra_data.items():
            if ed_key in server_response_json:
                struct_to_return[ed_key] = server_response_json[ed_key]
#        assert False
#    extra_data = {'course_detail': 
#                      {'name': '',
#                        'location': '',
#                        'start_datetime': '',
#                        'end_datetime': '',
#                        'hours': 0,
#                        'total_hours': 0
#                       },
#                 }


    if 'StatusMessage' in server_response_json:
        struct_to_return['StatusMessage'] = server_response_json['StatusMessage']

    if 'ResponseCode' in server_response_json:
        struct_to_return['ResponseCode'] = server_response_json['ResponseCode']

    #20211012+
    if 'e_d' in server_response_json:
        struct_to_return['e_d'] = server_response_json['e_d']
    #20211012-

    return struct_to_return




