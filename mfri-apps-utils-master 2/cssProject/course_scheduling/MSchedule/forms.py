import datetime

from django import forms
from django.forms import widgets
from django.forms import ValidationError
#from AppHome.models import *
#20180904from django.contrib.auth.models import User, check_password
from django.utils.html import escape
from django.utils.safestring import mark_safe
#20180904from django.forms.util import flatatt
from django.forms import ModelForm

from AppBase.forms import baseForm

from MSchedule.models import *



DEFAULT_REG_EMAIL_CHOICES=[('none','No email alert'),
                           ('before','At time of registration before training officer approval'),
                           ('after','After training officer approval')]



def ScheduledCourseEditTabTemplate(tab_name='overview'):
    
    if tab_name == 'overview':
        return 'mschedule/msched_edit_overview.html'
    if tab_name == 'course':
        return 'mschedule/msched_edit_course.html'
    if tab_name == 'workflow':
        return 'mschedule/msched_edit_workflow.html'
    if tab_name == 'scheduling':
        return 'mschedule/msched_edit_schedule.html'
    if tab_name == 'registration':
        return 'mschedule/msched_edit_registration.html'
    if tab_name == 'fees':
        return 'mschedule/msched_edit_fees.html'
    if tab_name == 'files':
        return 'mschedule/msched_edit_files.html'
    return 'mschedule/msched_edit_course.html'

def ScheduledCourseEditTabForm(tab_name='overview'):
    
    if tab_name == 'overview':
        return OverviewEditForm
    if tab_name == 'course':
        return CourseEditForm
    if tab_name == 'workflow':
        return WorkFlowEditForm
    if tab_name == 'scheduling':
        return SchedulingEditForm
    if tab_name == 'registration':
        return RegistrationEditForm
    if tab_name == 'fees':
        return FeesEditForm
    if tab_name == 'files':
        return FilesEditForm
        
    return CourseEditForm

class ScheduledCourseEditForm(baseForm):

    when_to_send_registration_alert_email = forms.ChoiceField(choices=DEFAULT_REG_EMAIL_CHOICES, required=False, label='Send Registration Request Email Alert')#, widget=forms.RadioSelect)
    
    class Meta:
        model = Scheduledcourses
        fields = ('send_alert_email_to_office_before_approval', 'send_alert_email_to_office_after_approval', 'require_training_officer_approval', 'require_epins', 'require_nfasid', 'require_emt_expiration_date', 'require_payment', 'allow_late_registration', 'require_birth_date', 'require_ssn', 'require_mfri_student_number' ) #20170823 #20171103 #20190912 #20200916 #20210927

    def __init__(self, *args, **kwargs):
        field_list = kwargs.pop('field_list', None)
        
        super(ScheduledCourseEditForm, self).__init__(*args, **kwargs)

        if u'instance' in kwargs:
            instance = kwargs['instance']

            if instance:
                try:
                    send_alert_email_to_office_before_approval = instance.send_alert_email_to_office_before_approval
                    send_alert_email_to_office_after_approval = instance.send_alert_email_to_office_after_approval 
                except:
                    send_alert_email_to_office_before_approval = False
                    send_alert_email_to_office_after_approval = False

                if send_alert_email_to_office_before_approval:
                    self.fields['when_to_send_registration_alert_email'].initial = u'before'
                elif send_alert_email_to_office_after_approval:
                    self.fields['when_to_send_registration_alert_email'].initial = u'after'
                else:
                    self.fields['when_to_send_registration_alert_email'].initial = u'none'

    def save(self, *args, **kwargs):
        kwargs['commit']=False

        try:
            cleaned_data = self.cleaned_data
            when_to_send_registration_alert_email = cleaned_data.get('when_to_send_registration_alert_email', None)
        except:
            when_to_send_registration_alert_email = None
        
        send_alert_email_to_office_before_approval = False
        send_alert_email_to_office_after_approval = False
        
        if when_to_send_registration_alert_email == u'before':
            send_alert_email_to_office_before_approval = True
            send_alert_email_to_office_after_approval = False
        elif when_to_send_registration_alert_email == u'after':
            send_alert_email_to_office_before_approval = False
            send_alert_email_to_office_after_approval = True
        else:
            send_alert_email_to_office_before_approval = False
            send_alert_email_to_office_after_approval = False

        obj = super(ScheduledCourseEditForm, self).save(*args, **kwargs)

        obj.send_alert_email_to_office_before_approval = send_alert_email_to_office_before_approval
        obj.send_alert_email_to_office_after_approval =  send_alert_email_to_office_after_approval 

        obj.save()
        return obj

class CourseEditForm(baseForm):
    
    class Meta:
        model = Scheduledcourses
        fields = ('course_description', 'funding_source_code', 'section_number', 'fiscal_year', 'old_format_log_number_section_and_fiscal_year', 'miemss_log_number', 'short_log_number', 'schedule_type', 'is_seminar', 'notes', 'location', 'legacy_host_region', 'legacy_host_section', 'client', 'mfri_office', 'host_agency', 'jurisdiction', 'hostreservations', 'hostregistrations', 'use_host_agency_priority', 'use_jurisdiction_priority', 'use_legacy_region_priority', 'use_instate_priority', 'use_emt_certification_expiration_priority', 'coordinator', 'instructor',)
    
    def clean(self):
        
        if self.cleaned_data.get("require_training_officer_approval", False):
            if not self.cleaned_data.get("require_affiliation", True):
                msg = u"If you are using trainig officer approval for this class you must require students to indicate their departmental affiliation." 
                self._errors["require_training_officer_approval"] = self.error_class([msg])
                self._errors["require_affiliation"] = self.error_class([msg])
                # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'require_training_officer_approval' in self.cleaned_data:
                    del self.cleaned_data["require_training_officer_approval"]
                
                if 'require_affiliation' in self.cleaned_data:
                    del self.cleaned_data["require_affiliation"]
            

        # Always return the full collection of cleaned data.
        return self.cleaned_data    


    def __init__(self, *args, **kwargs):
        #field_list = kwargs.pop('field_list', None)
        
        super(CourseEditForm, self).__init__(*args, **kwargs)

    def save(self, file_type, *args, **kwargs):
        kwargs['commit']=False

        obj = super(standard_form, self).save(*args, **kwargs)

        obj.save()
        return obj

class OverviewEditForm(baseForm):
    
    class Meta:
        model = Scheduledcourses
        fields = []

class WorkFlowEditForm(baseForm):
    
    class Meta:
        model = Scheduledcourses
        fields = ('schedule_status', 'sent_to_transcript', 'saved_in_transcript', 'mark_as_deleted', 'class_folder_sent_date', 'class_folder_sent_by', 'class_folder_received_date', 'class_folder_received_by', 'class_folder_closed_date', 'class_folder_closed_by', 'class_folder_note', 'show_on_transcript', 'transcript_note', 'require_program_evaluations', 'program_evaluation_note',)
    

class SchedulingEditForm(baseForm):
    #post_on_schedule_list
    class Meta:
        model = Scheduledcourses
        fields = ('registration_open_date', 'registration_close_date', 'start_date', 'end_date', 'recurring_days',)


class RegistrationEditForm(baseForm):
    
    class Meta:
        model = Scheduledcourses
        fields = ('min_students', 'max_students', 'use_wait_list', 'use_web_registration', 'registered_count', 'dropped_count', 'require_epins', 'require_ssn', 'require_mfri_student_number', 'require_nfasid', 'require_birth_date', 'require_emt_expiration_date', 'require_address', 'require_affiliation', 'require_email_address', 'require_primary_phone', 'require_cell_phone', 'require_training_officer_approval', 'require_mfri_office_approval', 'alert_msg', 'special_alert', 'registration_note', 'registration_alert_text', 'registration_header_text', 'registration_special_instructions_text', 'registration_footer_text', 'registration_message', 'registration_email_text', 'use_host_agency_priority', 'use_jurisdiction_priority', 'use_legacy_region_priority', 'use_instate_priority', 'use_emt_certification_expiration_priority',) #20200916

class FeesEditForm(baseForm):
    #books_and_resources_list
    class Meta:
        model = Scheduledcourses
        fields = ('out_of_state_fee', 'in_state_fee', 'resource_fee', 't_code', 'umd_term',)


class FilesEditForm(baseForm):
    #books_and_resources_list
    class Meta:
        model = Scheduledcourses
        fields = ('legacy_link', )



class ConfirmScheduleExportForm(forms.Form):

    schedule_name = forms.CharField(required=False, widget=forms.HiddenInput(), label= u'')
    office_abbreviation = forms.CharField(required=False, widget=forms.HiddenInput(), label= u'')
    location_pk = forms.CharField(required=False, widget=forms.HiddenInput(), label= u'')

    start_date = forms.DateField(input_formats=('%m-%d-%Y',), label='Start Date', required=False,  
                                    widget=forms.DateInput(format='%m-%d-%Y', attrs={
                                        'class':'input',
                                        'readonly':'readonly',
                                        'size':'12'
                                    }))

