

from AppBase.utils_exception import ExceptionRedirect 

def IsLockedOut(is_superuser=False):
    
    if is_superuser:
        return False
    
    return False  #change to True to lock out access


def LockOutRedirect(#profile=None, 
                    log_number=None, 
                    office_code=None,
                    exception_label=None,
                    exception_message=None):

    site_label = u'MFRI Apps Server'

    if not exception_label:
        exception_label = u'The %s is Temporarily Unavailable' % (site_label)

    if not exception_message:
        exception_message = u'The %s is undergoing a maintenance update.'  % (site_label)

    return ExceptionRedirect(
                             log_number=log_number, 
                             office_code=office_code,
                             exception_label=exception_label,
                             exception_message=exception_message)

