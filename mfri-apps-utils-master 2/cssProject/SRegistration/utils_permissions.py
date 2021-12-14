
import re
import json
import base64
import datetime

def legacy_app_permission(user=None):

    return True


def get_registration_permission(user=None, permission_name=None):
    return True

def get_registration_read_permission(user=None):
    return get_registration_permission(user=user, permission_name='registration_read_permission')

def get_registration_write_permission(user=None):
    return get_registration_permission(user=user, permission_name='registration_write_permission')

def get_registration_grade_read_permission(user=None):
    return get_registration_permission(user=user, permission_name='grades_read_permission')

def get_registration_grade_write_permission(user=None):
    return get_registration_permission(user=user, permission_name='grades_write_permission')

def get_registration_import_permission(user=None):
    return get_registration_permission(user=user, permission_name='import_permission')

def get_registration_export_permission(user=None):
    return get_registration_permission(user=user, permission_name='export_permission')



















    
