
import re
import json
import base64
import datetime

from AppsAdmin.models import Studentrecordspreferences

from SRec.models import Studentflagassignments

def legacy_app_permission(user=None):
    
    if not user:
        return False
    
    user_profile = user.profile
    
    if not user_profile:
        return False

    if not user_profile.LegacyUserData:
        return False
    
    return {'ReadPermission': True, 
            'CreatePermission': True, 
            'ModifyPermission': True, 
            'DeletePermission': True, 
            'ApprovePermission': False, 
            'OverridePermission': False, 
           }
     

def old_app_permissions(user=None):

    default_value = False
    
    if user and user.is_superuser:
        default_value = True
        
    app_permissions =  {'admin_read_permission'        : default_value, 
                        'admin_write_permission'       : default_value, 
                        'id_read_permission'             : default_value, 
                        'id_write_permission'            : default_value, 
                        'private_read_permission'        : default_value, 
                        'private_write_permission'       : default_value, 
                        'contact_read_permission'        : default_value, 
                        'contact_write_permission'       : default_value, 
                        'affiliation_read_permission'    : default_value, 
                        'affiliation_write_permission'   : default_value, 
                        'flags_read_permission'          : default_value, 
                        'flags_write_permission'         : default_value, 
                        'import_permission'            : default_value, 
                        'export_permission'            : default_value
                       }

    if not user:
        return app_permissions

    if not user.profile:
        return app_permissions

    if not user.profile.LegacyUserData:
        return app_permissions

    try:
        registration_permissions = Studentrecordspreferences.objects.get(userid__exact=user.profile.LegacyUserData.id)
    except:
        return app_permissions
    for permission_name in app_permissions:
        permission_value = getattr(registration_permissions,permission_name)
        if permission_value:
            app_permissions[permission_name] = True
        else:
            app_permissions[permission_name] = False
            
    return app_permissions


def get_student_record_permission(user=None, permission_name=None):

    if not user:
        return False

    if user.is_superuser:
       return True
    
    if not permission_name:
        return False
    
    app_permissions = old_app_permissions(user=user)

    return app_permissions.get(permission_name, False)

def get_student_record_read_permission(user=None):
    record_read_permission = get_student_record_id_read_permission(user=user) & get_student_record_private_read_permission(user=user) & get_student_record_contact_read_permission(user=user) & get_student_record_affiliation_read_permission(user=user) 

    return record_read_permission

def get_student_record_write_permission(user=None):
    record_write_permission = get_student_record_id_write_permission(user=user) & get_student_record_private_write_permission(user=user) & get_student_record_contact_write_permission(user=user) & get_student_record_affiliation_write_permission(user=user) 

    return record_write_permission

def get_student_record_id_read_permission(user=None):
    return get_student_record_permission(user=user, permission_name='id_read_permission')

def get_student_record_id_write_permission(user=None):
    return get_student_record_permission(user=user, permission_name='id_write_permission')

def get_student_record_private_read_permission(user=None):
    return get_student_record_permission(user=user, permission_name='private_read_permission')

def get_student_record_private_write_permission(user=None):
    return get_student_record_permission(user=user, permission_name='private_write_permission')

def get_student_record_contact_read_permission(user=None):
    return get_student_record_permission(user=user, permission_name='contact_read_permission')

def get_student_record_contact_write_permission(user=None):
    return get_student_record_permission(user=user, permission_name='contact_write_permission')

def get_student_record_affiliation_read_permission(user=None):
    return get_student_record_permission(user=user, permission_name='affiliation_read_permission')

def get_student_record_affiliation_write_permission(user=None):
    return get_student_record_permission(user=user, permission_name='affiliation_write_permission')

def get_student_record_flags_read_permission(user=None):
    return get_student_record_permission(user=user, permission_name='flags_read_permission')

def get_student_record_flags_write_permission(user=None):
    return get_student_record_permission(user=user, permission_name='flags_write_permission')

def get_student_record_import_permission(user=None):
    return get_student_record_permission(user=user, permission_name='import_permission')

def get_student_record_export_permission(user=None):
    return get_student_record_permission(user=user, permission_name='export_permission')






    


