import os
import codecs
import string
import json
import time
import datetime

from socket import gethostname
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.shortcuts import render 

from django.shortcuts import get_object_or_404, get_list_or_404, render #20180904render_to_response

from AppBase.forms import AppBaseExceptionForm

from MFRI_Utils.data_encode import decode_context

def appBaseExceptionView(request, template_name=None, context=None):

    try:
        context_decoded = decode_context(raw_context=context.encode("utf-8"))
        
        if not context_decoded:
            context_decoded={
                         'log_number': u'',
                         'office_code': u'stp',
                         'exception_label': u'MFRI Apps Error',
                         'exception_message': u'E901 Unknown Error.',
                        }
    except:
        context_decoded={
                     'log_number': u'',
                     'office_code': u'stp',
                     'exception_label': u'MFRI Apps Error',
                     'exception_message': u'E902 Unknown Error.',
                    }

    log_number = context_decoded.get('log_number', None)

    exception_label = context_decoded.get('exception_label', u'MFRI Apps Error')

    exception_message = context_decoded.get('exception_message', u'There has been an unexpected error.')

    form = AppBaseExceptionForm()

    return render(request, 
        template_name, 
        {'form': form, 
         'exception_label'  :  exception_label,
         'exception_message':  exception_message,
         'log_number':         log_number,
         #'contact':            contact,
        })


