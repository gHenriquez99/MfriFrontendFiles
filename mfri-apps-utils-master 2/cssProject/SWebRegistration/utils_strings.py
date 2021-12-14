

from MFRI_Utils.name_string_functions import SplitName


def FixName(student_record=None):

    if not student_record:
        return False

    try:
        if not student_record.name or len(student_record.name.strip()) == 0:
            student_record.name = u'%s %s %s %s' % (student_record.first_name, student_record.middle_name, student_record.last_name, student_record.suffix)
            student_record.name = student_record.name.strip()
            student_record.save(update_fields=['name'])
            return True
    except:
        return False

    try:
        if (student_record.first_name and len(student_record.first_name.strip()) > 0) and (student_record.last_name and len(student_record.last_name.strip()) > 0):
            return True
    except:
        return False

    return UpdateNameFields(web_registration_record=student_record) 

def UpdateNameFields(web_registration_record=None):
    
    if not web_registration_record:
        return False
    
    if not web_registration_record.name and len(web_registration_record.name.strip()) == 0:
        return False
    
    try:
        (first_name, middle_name, last_name, suffix) = split_name(web_registration_record.name)
    except:
        return False

    update_field_list = []
    try:
        if not web_registration_record.first_name and len(web_registration_record.first_name.strip()) == 0:
            web_registration_record.first_name = first_name
            update_field_list.append('first_name')
    except:
        return False

    try:
        if not web_registration_record.middle_name and len(web_registration_record.middle_name.strip()) == 0:
            web_registration_record.middle_name = middle_name
            update_field_list.append('middle_name')
    except:
        return False

    try:
        if not web_registration_record.last_name and len(web_registration_record.last_name.strip()) == 0:
            web_registration_record.last_name = last_name
            update_field_list.append('last_name')
    except:
        return False

    try:
        if not web_registration_record.suffix and len(web_registration_record.suffix.strip()) == 0:
            web_registration_record.suffix = suffix
            update_field_list.append('suffix')
    except:
        return False

    try:
        self.save(update_fields=update_field_list)
    except:
        return False

    return True


