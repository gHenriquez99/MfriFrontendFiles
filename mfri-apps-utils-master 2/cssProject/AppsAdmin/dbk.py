#import re
#import datetime
#import os
#import codecs
#import string
#import json
#import time
#import base64 # urlsafe_b64encode, urlsafe_b64decode
#from cStringIO import StringIO
#
#from django.http import HttpResponse
#from django.template import RequestContext
#from django.template.loader import get_template
#from django.contrib.auth.models import User, Group, Permission
#from django.contrib.contenttypes.models import ContentType

#from AppsAdmin.models import LegacyPermissions, Applications

def RegEncryptKey():
    return 'hereisakeyvalue'
    
def RegEncryptKeyS():
    return RegEncryptKey()

def RegEncryptKeyE():
    return RegEncryptKey()

def RegEncryptKeyB():
    return RegEncryptKey()

def SRecEncryptKey():
    return RegEncryptKey()

def SRecEncryptKeyS():
    return SRecEncryptKey()

def SRecEncryptKeyE():
    return SRecEncryptKey()

def SRecEncryptKeyB():
    return SRecEncryptKey()

def MESSAEncryptKey():
    return RegEncryptKey()

def MESSAEncryptKeyS():
    return MESSAEncryptKey()

def MESSAEncryptKeyE():
    return MESSAEncryptKey()

def MESSAEncryptKeyB():
    return MESSAEncryptKey()

def TranscriptEncryptKey():
    return RegEncryptKey()

def TranscriptEncryptKeyS():
    return TranscriptEncryptKey()

def TranscriptEncryptKeyE():
    return TranscriptEncryptKey()

def TranscriptEncryptKeyB():
    return TranscriptEncryptKey()

def QualificationsEncryptKey():
    return RegEncryptKey()

def SMedEncryptKey():
    return RegEncryptKey()

def SMedEncryptKeyS():
    return SMedEncryptKey()

def SMedEncryptKeyB():
    return SMedEncryptKey()

def StaffEncryptKey():
    return RegEncryptKey()

def StaffEncryptKeyU():
    return StaffEncryptKey()

def StaffEncryptKeyS():
    return StaffEncryptKey()

def ZoneEncryptKey():
    return RegEncryptKey()

def MTESEncryptKey():
    return ZoneEncryptKey()

