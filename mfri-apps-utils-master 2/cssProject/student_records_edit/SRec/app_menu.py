
from django.core.urlresolvers import reverse

from AppsAdmin.models import Applications

def legacy_app_id():
    return 0

def app_name(app_id=legacy_app_id(), default_name=u'Student Records'):
    
    return default_name
    
