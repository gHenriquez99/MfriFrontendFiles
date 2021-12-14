import re
import datetime, decimal

from django import forms
from django.forms import widgets, ModelForm, ValidationError
from AppsAdmin.models import *

from django.utils.html import escape
from django.utils.safestring import mark_safe


from SRegistration.models import *

from MAffiliations.models import Affiliations
from MOffices.models import Jurisdictions
from MLocations.models import Locations

from MSchedule.utils_search import FindCourseFromLogNumber

from MFRI_Utils.data_validate import validate_email_address, ValidateTableIndex

class DynamicChoiceField(forms.ChoiceField):
  # The only thing we need to override here is the validate function.  
  def validate(self, value):
      if self.required and not value:
          raise ValidationError(self.error_messages['required'])


class DynamicMultipleChoiceField(forms.MultipleChoiceField):
  # The only thing we need to override here is the validate function.  
  def validate(self, value):
      if self.required and not value:
          raise ValidationError(self.error_messages['required'])

class CopyRegisteredStudentsForm(forms.Form):


    student_registrations_to_copy = DynamicMultipleChoiceField(choices=[], required=False, widget=forms.CheckboxSelectMultiple())

    student_registrations_to_confirm = DynamicMultipleChoiceField(choices=[], required=False, widget=forms.CheckboxSelectMultiple())

    from_log_number = forms.CharField(max_length=25, label= u'From Course Log Number', required=True)
    to_log_number = forms.CharField(max_length=25, label= u'To Course Log Number', required=True)

    student_registration_ids_to_copy = forms.CharField(required=False, widget=forms.HiddenInput(), label= u'')

    copy_step = forms.CharField(required=False, widget=forms.HiddenInput(), label= u'')

    TO_TABLE_CHOICES=[('Preregistrations','Pre-Registration'),
                      ('Studentregistration','Seated')]

    to_table = forms.ChoiceField(choices=TO_TABLE_CHOICES, widget=forms.RadioSelect(), initial='Studentregistration') #attrs={'id': 'value'}

    def __init__(self, *args, **kwargs): #request=None,

        registration_list = kwargs.pop('student_registrations_to_copy', [])
        from_scheduled_course = kwargs.pop('from_scheduled_course', None)
        init_form = kwargs.pop('init_form', False)


        super(CopyRegisteredStudentsForm, self).__init__(*args, **kwargs)
        

        if not init_form and not registration_list:# and len(self.fields['student_registrations_to_copy'].choices) > 0:
            form_data = args[0]
            
            self.fields['student_registrations_to_copy'].choices = []
            from_log_number = form_data['from_log_number']
            from_scheduled_course = ScheduledCourseRecord(log_number=from_log_number)
            
            registration_list = Studentregistration.objects.filter(scheduled_course__exact=from_scheduled_course).order_by('student_record__lastname', 'student_record__firstname', 'student_record__middlename', 'student_record__suffix')


        if from_scheduled_course:
            if init_form:
                self.fields['student_registrations_to_copy'].choices = []

            self.fields['from_log_number'].initial = from_scheduled_course.log_number

            if len(self.fields['student_registrations_to_copy'].choices) == 0:
                for student_registration in registration_list:
                    self.fields['student_registrations_to_copy'].choices.append((student_registration.id, student_registration))

                self.fields['student_registrations_to_copy'].initial = [c.id for c in registration_list]



    def clean(self):
        cleaned_data = self.cleaned_data

        to_log_number = cleaned_data.get('to_log_number')

        from_log_number = cleaned_data.get('from_log_number')

        if from_log_number == to_log_number:
            msg = u'You can not copy students to the same class they are currently in.  The From and To log numbers must be different.'

            self._errors['to_log_number'] = self.error_class([msg])

            del cleaned_data['to_log_number']
        
             
        # Always return the full collection of cleaned data.
        return cleaned_data    


    def clean_to_log_number(self): 

        to_log_number = self.cleaned_data['to_log_number'] 

        if len(to_log_number) == 0:
            return to_log_number

        verify_result = FindCourseFromLogNumber(log_number=to_log_number, check_in_use=True)

        if verify_result['ResponseCode'] < 1:
            raise forms.ValidationError(verify_result['StatusMessage'])

        return to_log_number


class ConfirmCopyRegisteredStudentsForm(forms.Form):

    student_registration_ids_to_copy = forms.CharField(required=False, widget=forms.HiddenInput(), label= u'')

    from_log_number = forms.CharField(max_length=25, label= u'From Course Log Number', required=True)
    to_log_number = forms.CharField(max_length=25, label= u'To Course Log Number', required=True)

    to_table = forms.CharField(required=False, widget=forms.HiddenInput(), label= u'')

    def __init__(self, *args, **kwargs): 
        
        student_registrations_to_confirm = kwargs.pop('student_registration_ids_to_copy', [])
        
        from_log_number = kwargs.pop('from_log_number', None)
        to_log_number = kwargs.pop('to_log_number', None)
        to_table = kwargs.pop('to_table', 'Studentregistration')
        
        
        
        super(ConfirmCopyRegisteredStudentsForm, self).__init__(*args, **kwargs)

        self.fields['student_registration_ids_to_copy'].initial = student_registrations_to_confirm

        self.fields['from_log_number'].initial = from_log_number
        self.fields['to_log_number'].initial = to_log_number
        self.fields['to_table'].initial = to_table


