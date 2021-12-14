import os
#import sys
#import codecs
import string
#import json
#import time
import datetime
#import base64


from django.core.urlresolvers import reverse


from MAffiliations.models import Affiliations

from MOffices.models import MfriOffices, Jurisdictions

from MSchedule.models import *

schedule_edit_tab_list =[
                {'value': 'overview',  'label': 'Course Overview',  'help': 'Course Overview'  , 'link': ''}, 
                {'value': 'course',  'label': 'Course Management',  'help': 'Course Management'  , 'link': 'course'}, 
                {'value': 'workflow',  'label': 'Work Flow',  'help': 'Course Work Flow'  , 'link': 'workflow'}, 
                {'value': 'scheduling',  'label': 'Scheduling',  'help': 'Course Scheduling'  , 'link': 'scheduling'}, 
                {'value': 'registration',  'label': 'Registration',  'help': 'Course Registration'  , 'link': 'registration'}, 
                {'value': 'fees',  'label': 'Fees',  'help': 'Course Fees'  , 'link': 'fees'}, 
                {'value': 'files',  'label': 'Brochure',  'help': 'File Uploads'  , 'link': 'files'}, 
                ]

fields_per_tab ={
                    'overview':     [],
                    'course':       ['course_description', 'funding_source_code', 'section_number', 'fiscal_year', 'lognumber_suffix', 'old_format_log_number_section_and_fiscal_year', 'miemss_log_number', 'short_log_number', 'schedule_type', 'is_seminar', 'notes', 'location', 'legacy_host_region', 'legacy_host_section', 'client', 'mfri_office', 'host_agency', 'jurisdiction', 'hostreservations', 'hostregistrations', 'use_host_agency_priority', 'use_jurisdiction_priority', 'use_legacy_region_priority', 'use_instate_priority', 'use_emt_certification_expiration_priority', 'coordinator', 'instructor', ],
                    'workflow':     ['schedule_status', 'sent_to_transcript', 'saved_in_transcript', 'mark_as_deleted', 'class_folder_sent_date', 'class_folder_sent_by', 'class_folder_received_date', 'class_folder_received_by', 'class_folder_closed_date', 'class_folder_closed_by', 'class_folder_note', 'show_on_transcript', 'transcript_note', 'require_program_evaluations', 'program_evaluation_note', ], 
                    'scheduling':   ['registration_open_date', 'registration_close_date', 'start_date', 'end_date', 'recurring_days', 'alert_msg', 'special_alert', 'registration_note', 'post_on_schedule_list', ],  
                    'registration': ['min_students', 'max_students', 'use_wait_list', 'use_web_registration', 'registered_count', 'dropped_count', 'require_epins', 'require_ssn', 'require_mfri_student_number', 'require_birth_date', 'require_emt_expiration_date', 'require_address', 'require_affiliation', 'require_email_address', 'require_primary_phone', 'require_cell_phone', 'require_training_officer_approval', 'require_mfri_office_approval', 'registration_alert_text', 'registration_header_text', 'registration_special_instructions_text', 'registration_footer_text', 'registration_message', 'registration_email_text', 'use_host_agency_priority', 'use_jurisdiction_priority', 'use_legacy_region_priority', 'use_instate_priority', 'use_emt_certification_expiration_priority',],  #20200916  'require_book_fee_acknowledgment', 'require_rules_and_regulations_acknowledgement', 'require_release_statement_acknowledgement', 'show_msfa_acknowledgement',#20200921
                    'fees':         ['out_of_state_fee', 'in_state_fee', 'resource_fee', 't_code', 'umd_term', 'books_and_resources_list',],  
                    'files':       ['legacy_link', ],
                }




def LegalTabCodes():
    
    tab_code_list = []
    for tab in schedule_edit_tab_list:
        tab_code_list.append(tab['value'])

    return tab_code_list
    
def ScheduleEditHomeTabs():
    return schedule_edit_tab_list

def FieldsForTab(tab_name=u'course'):
    return fields_per_tab.get(tab_name, fields_per_tab['course'])

def ScheduleEditListTabs():
    
    Tab_List = []

    for tab_options in ScheduleEditHomeTabs():

        Tab_List.append({'value': tab_options['value'], 'label': u'%s' % (tab_options['label']), 'help': tab_options['help'], 'link': tab_options['link']})

    return Tab_List


def IsLegalScheduleEditTab(tab_name_to_check=None):
    
    if not tab_name_to_check:
        return False
    
    tab_code_list = LegalTabCodes()
    if tab_name_to_check in tab_code_list:
        return True
    
    return False

def CurrentScheduleEditTab(current_tab='course'):
    
    
    if not IsLegalScheduleEditTab(current_tab):
        return schedule_edit_tab_list[0]
    
    for tab in schedule_edit_tab_list:
        if tab['value'] == current_tab:
            return tab
        
    return schedule_edit_tab_list[0]

