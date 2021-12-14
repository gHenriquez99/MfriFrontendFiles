
from django.core.urlresolvers import reverse

from AppsAdmin.models import Applications


def legacy_app_id():
    return 33

def app_name(app_id=legacy_app_id(), default_name=u'Student Registration'):
    
    try:
        app_obj = Applications.objects.get(pk=app_id)
    except:
        app_obj = None

    if app_obj:
        return app_obj.name
    else:
        return default_name


