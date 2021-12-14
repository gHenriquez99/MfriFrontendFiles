"""
tags used to simplify forms

"""

from django.template import Library

register = Library()

def phone_number_display(value, arg=u'-', split_exchange=False):
    """
    Returns a phone number separated by arg

    301-123-1234
    
    if split_exchange is true separte exchange with parens
    
    (301) 123-1234

    The separator can be changed by specifying as an argument
    """
    
    if not value or len(value) == 0:
        return u''

    phone_number = value.strip(':-() .')

    if not raw_phone_number or len(phone_number) == 0:
        return u''


    if split_exchange:
        formated_phone_number = u'(%s) %s%s%s' % (raw_phone_number[0:3], raw_phone_number[3:3], arg, raw_phone_number[6:3])
    else:
        formated_phone_number = u'%s%s%s%s%s' % (raw_phone_number[0:3], arg, raw_phone_number[3:3], arg, raw_phone_number[6:3])
        
    return formated_phone_number
phone_number_display.is_safe = False

register.filter(phone_number_display)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()