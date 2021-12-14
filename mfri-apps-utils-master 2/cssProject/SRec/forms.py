from django import forms
from django.forms import widgets
from django.forms import ValidationError

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.forms import ModelForm

from SRec.models import *

from AppBase.forms import baseForm

from SRec.utils import ReferenceDate, CalculateStudentAge

from SRec.utils_msn import validate_mfri_student_number, AssignNewMFRIStudentNumber, GetStudentRecordByStudentNumber 
from SRec.utils_form import UpdateFormFieldErrorList

from MFRI_Utils.data_validate import validate_email_address, parse_last_name_suffix, validate_university_id_number, validate_ssn, validate_last_name, validate_address, validate_date, validate_birth_date, validate_student_address, validate_student_email_address, validate_bool, validate_string
from MFRI_Utils.name_string_functions import validate_first_name, validate_middle_name, 

SUFFIX_VALUES = (
                  ('', u''),
                  ('JR', 'JR'),
                  ('SR', 'SR'),
                  ('I', 'I'),
                  ('II', 'II'),
                  ('III', 'III'),
                  ('IV', 'IV'),
                  ('V', 'V'),
                )


class StudentRecordEditForm(baseForm):

    birthdate = forms.DateField(input_formats=('%m-%d-%Y',), label='Birth Date', required=False,  
                                    widget=forms.DateInput(format='%m-%d-%Y', attrs={
                                        'class':'input',
                                        'readonly':'readonly',
                                        'size':'12'
                                    }))

    no_bulletin_email = forms.BooleanField(required=False, label='Email Opt Out', help_text=u'Opt Out of Bulletin Email')
    
    id_number = forms.CharField(required=False, max_length=9, label= u'SSN')

    umid = forms.CharField(required=False, max_length=10, label= u'UMID')

    epins = forms.CharField(required=False, max_length=7, label= u'State Provider Number')

    nfa_sid = forms.CharField(required=False, max_length=10, label= u'NFA SID')

    certificationexpirationdate = forms.DateField(input_formats=('%m-%d-%Y',), label='EMT Certification Expiration Date', required=False,  
                                    widget=forms.DateInput(format='%m-%d-%Y', attrs={
                                        'class':'input',
                                        'readonly':'readonly',
                                        'size':'12'
                                    }))


    class Meta:
        model = Studentrecords
        exclude = ('primaryphonenumbertypeid', 'secondaryphonenumbertypeid', 'createdby','firstname','idnumber','lastchangeby','lastname','lms_user_account_password','middlename','nfa_sid_number','show_name_as_is','suffix','umd_canvas_lms_user_account_identifier','umd_canvas_lms_user_account_password','umd_canvas_lms_user_name','umd_canvas_lms_user_name_created_date','universityidnumber','title', 'ssn', 'old_mfri_student_number', 'mfri_student_number', 'affiliatedcompanynumber', 'gender', 'race', 'hispanic', 'gradelevel', 'collegelevel', 'county', 'email', 'secondaryemail', 'adaflag', 'noshowflag', 'studentstatusid', 'recordstatusid', 'lms_user_name', 'lms_user_account_password ', 'lms_user_account_identifier', 'lms_user_name_created_date', 'lastchange', 'created')
 
    def __init__(self, *args, **kwargs): 
    
        super(StudentRecordEditForm, self).__init__(*args, **kwargs)
    
        if u'instance' in kwargs:
            instance = kwargs['instance']

            if instance:
                try:
                    suffix = instance.suffix
                except:
                    suffix = None
            
                try:
                    self.fields['id_number'].initial = instance.ssn_clear
                except:
                    pass
            
                try:
                    self.fields['umid'].initial = instance.umid_clear
                except:
                    pass
            
                try:
                    self.fields['epins'].initial = instance.epins_clear
                except:
                    pass
            
                try:
                    self.fields['nfa_sid'].initial = instance.nfa_sid
                except:
                    pass


    def clean_birthdate(self):
        birthdate = self.cleaned_data['birthdate'] 

        validate_string_results = validate_birth_date(birth_date=birthdate)

        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        student_age = CalculateStudentAge(reference_date=ReferenceDate(), birth_date=birthdate) 
        
        if student_age < 14:
            raise forms.ValidationError(u'Students must be over 14 years old.')
        
        return birthdate

    def clean_country(self):
        country = self.cleaned_data['country'] 
    
        if len(country) == 0:
            return country

        validate_string_results = validate_string(string_to_validate=country, is_required=False, string_type='Country', min_Length=2, max_Length=3, validate_rule="^([a-zA-Z]+)$")
        
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        return country

    def clean_primaryemail(self):
        primaryemail = self.cleaned_data['primaryemail'] 
    
        if len(primaryemail) == 0:
            return primaryemail

        if not validate_email_address(email_address=primaryemail):
            raise forms.ValidationError(u'Invalid email address.')
    
        return primaryemail

    def clean_id_number(self): 
        
        ssn = self.cleaned_data['id_number'].strip()

        ssn_valudation_result = validate_ssn(ssn=ssn, accept_last_five=False, accept_null_ssn=False)

        if ssn_valudation_result['ResponseCode'] < 1:
            raise forms.ValidationError(ssn_valudation_result['StatusMessage'])

        return ssn

    def clean(self):
        
        address_validation_result = validate_address(address1=self.cleaned_data.get("address1", None), 
                                                         address2=self.cleaned_data.get("address2", None), 
                                                         city=self.cleaned_data.get("city", None), 
                                                         state=self.cleaned_data.get("state", None), 
                                                         post_code=self.cleaned_data.get("postcode", None), 
                                                         country=self.cleaned_data.get("country", None))
                                                         
            
        if not address_validation_result['address1']['empty']:
            if address_validation_result['address1']['invalid']:
                msg = address_validation_result['address1']['description'] 
                self._errors["address1"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'address1' in self.cleaned_data:
                    del self.cleaned_data["address1"]
        
            if address_validation_result['address2']['invalid']:
                msg = address_validation_result['address2']['description'] 
                self._errors["address2"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'address2' in self.cleaned_data:
                    del self.cleaned_data["address2"]
        
            if address_validation_result['city']['invalid'] or address_validation_result['city']['empty']:
                msg = address_validation_result['city']['description'] 
                self._errors["city"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'city' in self.cleaned_data:
                    del self.cleaned_data["city"]
        
            if address_validation_result['state']['invalid'] or address_validation_result['state']['empty']:
                msg = address_validation_result['state']['description'] 
                self._errors["state"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'state' in self.cleaned_data:
                    del self.cleaned_data["state"]
        
            if address_validation_result['post_code']['invalid'] or address_validation_result['post_code']['empty']:
                msg = address_validation_result['post_code']['description'] 
                self._errors["postcode"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'postcode' in self.cleaned_data:
                    del self.cleaned_data["postcode"]
        

        return self.cleaned_data    

class StudentRecordNewForm(baseForm):

    suffix = forms.ChoiceField(choices=SUFFIX_VALUES, required=False)

    birthdate = forms.DateField(input_formats=('%m-%d-%Y',), label='Birth Date', required=False,  
                                    widget=forms.DateInput(format='%m-%d-%Y', attrs={
                                        'class':'input',
                                        'size':'12'
                                    }))

    no_bulletin_email = forms.BooleanField(required=False, label='Email Opt Out', help_text=u'Opt Out of Bulletin Email')
    
    id_number = forms.CharField(required=False, max_length=9, label= u'SSN')

    umid = forms.CharField(required=False, max_length=10, label= u'UMID')

    epins = forms.CharField(required=False, max_length=7, label= u'State Provider Number')

    nfa_sid = forms.CharField(required=False, max_length=10, label= u'NFA SID')

    certificationexpirationdate = forms.DateField(input_formats=('%m-%d-%Y',), label='EMT Certification Expiration Date', required=False,  
                                    widget=forms.DateInput(format='%m-%d-%Y', attrs={
                                        'class':'input',
                                        'readonly':'readonly',
                                        'size':'12'
                                    }))


    class Meta:
        model = Studentrecords
        exclude = ('primaryphonenumbertypeid', 'secondaryphonenumbertypeid', 'createdby','idnumber','lastchangeby','lms_user_account_password','nfa_sid_number','umd_canvas_lms_user_account_identifier','umd_canvas_lms_user_account_password','umd_canvas_lms_user_name','umd_canvas_lms_user_name_created_date','universityidnumber','title', 'ssn', 'old_mfri_student_number', 'mfri_student_number', 'affiliatedcompanynumber', 'gender', 'race', 'hispanic', 'gradelevel', 'collegelevel', 'county', 'email', 'secondaryemail', 'adaflag', 'noshowflag', 'studentstatusid', 'recordstatusid', 'lms_user_name', 'lms_user_account_password ', 'lms_user_account_identifier', 'lms_user_name_created_date', 'lastchange', 'created')

 
    def __init__(self, *args, **kwargs): 
    
        super(StudentRecordNewForm, self).__init__(*args, **kwargs)
    
        if u'instance' in kwargs:
            instance = kwargs['instance']

            if instance:
                try:
                    suffix = instance.suffix
                except:
                    suffix = None
            
                try:
                    self.fields['id_number'].initial = instance.ssn_clear
                except:
                    pass
            
                try:
                    self.fields['umid'].initial = instance.umid_clear
                except:
                    pass
            
                try:
                    self.fields['epins'].initial = instance.epins_clear
                except:
                    pass
            
                try:
                    self.fields['nfa_sid'].initial = instance.nfa_sid
                except:
                    pass

                suffix = None
                try:
                    suffix = instance.suffix
                except:
                    suffix = None

                if suffix:
                    self.fields['suffix'].initial = suffix
                else:
                    self.fields['suffix'].initial = u''


    def clean_firstname(self):
        firstname = self.cleaned_data['firstname'] 
    
        validate_string_results = validate_first_name(first_name=firstname)
        
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        return firstname

    def clean_middlename(self):
        middlename = self.cleaned_data['middlename'] 
    
        validate_string_results = validate_middle_name(middle_name=middlename)
        
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        return middlename

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname'] 
    
        validate_string_results = validate_last_name(lastname=lastname)
        
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        return lastname

    def clean_suffix(self):
        suffix = self.cleaned_data['suffix'] 
    
        if len(suffix) == 0:
            return suffix
    
        validate_string_results = validate_string(string_to_validate=suffix, is_required=False, string_type='Suffix', min_Length=1, max_Length=3, validate_rule="^([a-zA-Z]+)$")
    
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
       
        suffix_values_list = []
        
        for suffix_option in SUFFIX_VALUES:
            if len(suffix_option[0]) == 0:
                continue
            suffix_values_list.append(suffix_option[0])

        if suffix not in suffix_values_list:
            raise forms.ValidationError(u'Invalid Suffix')
            
        return suffix

    def clean_birthdate(self):
        birthdate = self.cleaned_data['birthdate'] 
    
        validate_string_results = validate_birth_date(birth_date=birthdate)

        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        student_age = CalculateStudentAge(reference_date=ReferenceDate(), birth_date=birthdate)
        
        if student_age < 14:
            raise forms.ValidationError(u'Students must be over 14 years old.')
        
        return birthdate

    def clean_country(self):
        country = self.cleaned_data['country'] 
    
        if len(country) == 0:
            return country

        validate_string_results = validate_string(string_to_validate=country, is_required=False, string_type='Country', min_Length=2, max_Length=3, validate_rule="^([a-zA-Z]+)$")
        
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        return country

    def clean_primaryemail(self):
        primaryemail = self.cleaned_data['primaryemail'] 
    
        if len(primaryemail) == 0:
            return primaryemail

        if not validate_email_address(email_address=primaryemail):
            raise forms.ValidationError(u'Invalid email address.')
    
        return primaryemail

    def clean_id_number(self): 
        
        ssn = self.cleaned_data['id_number'].strip()

        ssn_valudation_result = validate_ssn(ssn=ssn, accept_last_five=False, accept_null_ssn=False)

        if ssn_valudation_result['ResponseCode'] < 1:
            raise forms.ValidationError(ssn_valudation_result['StatusMessage'])

        return ssn

    def clean(self):
        
        last_name_validation = parse_last_name_suffix(lastname=self.cleaned_data.get("lastname", None).strip(), validate_suffix=True)

        if last_name_validation.get('suffix', None):
            suffix = last_name_validation.get('suffix', None)
            suffix_values_list = []

            for suffix_option in SUFFIX_VALUES:
                if len(suffix_option[0]) == 0:
                    continue
                suffix_values_list.append(suffix_option[0])

            if suffix in suffix_values_list:
                msg = u'The last name field contains the suffix value (%s), please use the suffix drop down list instead of entering it in the last name field.' % (suffix)
                self._errors["lastname"] = self.error_class([msg])
                # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'lastname' in self.cleaned_data:
                    del self.cleaned_data["lastname"]
        
        address_validation_result = validate_address(address1=self.cleaned_data.get("address1", None), 
                                                         address2=self.cleaned_data.get("address2", None), 
                                                         city=self.cleaned_data.get("city", None), 
                                                         state=self.cleaned_data.get("state", None), 
                                                         post_code=self.cleaned_data.get("postcode", None), 
                                                         country=self.cleaned_data.get("country", None))
                                                         
            
        if not address_validation_result['address1']['empty']:
            if address_validation_result['address1']['invalid']:
                msg = address_validation_result['address1']['description'] 
                self._errors["address1"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'address1' in self.cleaned_data:
                    del self.cleaned_data["address1"]
        
            if address_validation_result['address2']['invalid']:
                msg = address_validation_result['address2']['description'] 
                self._errors["address2"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'address2' in self.cleaned_data:
                    del self.cleaned_data["address2"]
        
            if address_validation_result['city']['invalid'] or address_validation_result['city']['empty']:
                msg = address_validation_result['city']['description'] 
                self._errors["city"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'city' in self.cleaned_data:
                    del self.cleaned_data["city"]
        
            if address_validation_result['state']['invalid'] or address_validation_result['state']['empty']:
                msg = address_validation_result['state']['description'] 
                self._errors["state"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'state' in self.cleaned_data:
                    del self.cleaned_data["state"]
        
            if address_validation_result['post_code']['invalid'] or address_validation_result['post_code']['empty']:
                msg = address_validation_result['post_code']['description'] 
                self._errors["postcode"] = self.error_class([msg])
                 # These fields are no longer valid. Remove them from the
                # cleaned data.
                if 'postcode' in self.cleaned_data:
                    del self.cleaned_data["postcode"]
        

        return self.cleaned_data    



class StudentNameEditForm(baseForm):
    suffix = forms.ChoiceField(choices=SUFFIX_VALUES, required=False)

    class Meta:
        model = Studentrecords
        exclude = ('address1', 'address2', 'city', 'country', 'createdby', 'idnumber', 'lastchangeby', 'lms_user_account_password', 'nfa_sid_number', 'note', 'postcode', 'primaryemail', 'primaryphonenumber', 'secondaryphonenumber', 'state', 'stateprovidernumber', 'umd_canvas_lms_user_account_identifier', 'umd_canvas_lms_user_account_password', 'umd_canvas_lms_user_name', 'umd_canvas_lms_user_name_created_date', 'universityidnumber', 'affiliation', 'primaryphonenumbertypeid', 'secondaryphonenumbertypeid', 'certificationexpirationdate', 'no_bulletin_email', 'birthdate', 'title', 'ssn', 'old_mfri_student_number', 'mfri_student_number', 'affiliatedcompanynumber', 'gender', 'race', 'hispanic', 'gradelevel', 'collegelevel', 'county', 'email', 'secondaryemail', 'adaflag', 'noshowflag', 'studentstatusid', 'recordstatusid', 'lms_user_name', 'lms_user_account_password ', 'lms_user_account_identifier', 'lms_user_name_created_date', 'lastchange', 'created')


    def __init__(self, *args, **kwargs): 
    
        super(StudentNameEditForm, self).__init__(*args, **kwargs)
    
        if u'instance' in kwargs:
            instance = kwargs['instance']

        suffix = None
        if instance:
            try:
                suffix = instance.suffix
            except:
                suffix = None

        if suffix:
            self.fields['suffix'].initial = suffix
        else:
            self.fields['suffix'].initial = u''

    def clean_firstname(self):
        firstname = self.cleaned_data['firstname'] 
    
        validate_string_results = validate_first_name(first_name=firstname)
        
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        return firstname

    def clean_middlename(self):
        middlename = self.cleaned_data['middlename'] 
    
        validate_string_results = validate_middle_name(middle_name=middlename)
        
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        return middlename

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname'] 
    
        validate_string_results = validate_last_name(lastname=lastname)
        
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
    
        return lastname

    def clean_suffix(self):
        suffix = self.cleaned_data['suffix'] 
    
        if len(suffix) == 0:
            return suffix
    
        validate_string_results = validate_string(string_to_validate=suffix, is_required=False, string_type='Suffix', min_Length=1, max_Length=3, validate_rule="^([a-zA-Z]+)$")
    
        if validate_string_results['ResponseCode'] < 0:
            raise forms.ValidationError(validate_string_results['StatusMessage'])
       
        suffix_values_list = []
        
        for suffix_option in SUFFIX_VALUES:
            if len(suffix_option[0]) == 0:
                continue
            suffix_values_list.append(suffix_option[0])

        if suffix not in suffix_values_list:
            raise forms.ValidationError(u'Invalid Suffix')
            
        return suffix

    def clean(self):
        last_name_validation = parse_last_name_suffix(lastname=self.cleaned_data.get("lastname", None).strip(), validate_suffix=True)

        if last_name_validation.get('suffix', None):
            suffix = last_name_validation.get('suffix', None)
            suffix_values_list = []

            for suffix_option in SUFFIX_VALUES:
                if len(suffix_option[0]) == 0:
                    continue
                suffix_values_list.append(suffix_option[0])

            if suffix in suffix_values_list:
                msg = u'The last name field contains the suffix value (%s), please use the suffix drop down list instead of entering it in the last name field.' % (suffix)
                self._errors["lastname"] = self.error_class([msg])
                # These fields are no longer valid. Remove them from the
                                                                                                                                                                                                                                                                                                                                                                                cleaned data.
                if 'lastname' in self.cleaned_data:
                    del self.cleaned_data["lastname"]
            
        return self.cleaned_data    
    
class StudentNumberEditForm(baseForm):

    ssn = forms.CharField(required=False, widget=forms.HiddenInput(), label= u'')

    class Meta:
        model = Studentrecords
        exclude = ('firstname', 'middlename', 'lastname', 'suffix', 'address1', 'address2', 'city', 'country', 'createdby', 'idnumber', 'lastchangeby', 'lms_user_account_password', 'nfa_sid_number', 'note', 'postcode', 'primaryemail', 'primaryphonenumber', 'secondaryphonenumber', 'show_name_as_is', 'state', 'stateprovidernumber', 'umd_canvas_lms_user_account_identifier', 'umd_canvas_lms_user_account_password', 'umd_canvas_lms_user_name', 'umd_canvas_lms_user_name_created_date', 'universityidnumber', 'affiliation', 'primaryphonenumbertypeid', 'secondaryphonenumbertypeid', 'certificationexpirationdate', 'no_bulletin_email', 'birthdate', 'title', 'ssn', 'old_mfri_student_number', 'affiliatedcompanynumber', 'gender', 'race', 'hispanic', 'gradelevel', 'collegelevel', 'county', 'email', 'secondaryemail', 'adaflag', 'noshowflag', 'studentstatusid', 'recordstatusid', 'lms_user_name', 'lms_user_account_password ', 'lms_user_account_identifier', 'lms_user_name_created_date', 'lastchange', 'created')

    def __init__(self, *args, **kwargs): 
        student_record = kwargs.get('instance', None)
        
        if student_record:
            ssn = student_record.ssn_clear

        super(StudentNumberEditForm, self).__init__(*args, **kwargs)

        self.fields['ssn'].initial = ssn



    def clean_mfri_student_number(self):
        mfri_student_number = self.cleaned_data['mfri_student_number'] 
    
        mfri_student_number_validation_result = validate_mfri_student_number(mfri_student_number=mfri_student_number)

        if mfri_student_number_validation_result['ResponseCode'] < 1:
            raise forms.ValidationError(mfri_student_number_validation_result['StatusMessage'])
    
        return mfri_student_number

    def clean(self):
        mfri_student_number = self.cleaned_data.get("mfri_student_number", None)

        found_student_record = GetStudentRecordByStudentNumber(mfri_student_number=mfri_student_number)

        if found_student_record and len(found_student_record) > 1:
            msg = u'This MFRI Student Number is in use by more than one student record.'
            self._errors["mfri_student_number"] = self.error_class([msg])
            # These fields are no longer valid. Remove them from the
            # cleaned data.
            if 'mfri_student_number' in self.cleaned_data:
                del self.cleaned_data["mfri_student_number"]

        if found_student_record and len(found_student_record) == 1 and (found_student_record[0].ssn_clear != self.cleaned_data["ssn"]):
            msg = u'This MFRI Student Number is in use by another student.'
            self._errors["mfri_student_number"] = self.error_class([msg])
            # These fields are no longer valid. Remove them from the
            # cleaned data.
            if 'mfri_student_number' in self.cleaned_data:
                del self.cleaned_data["mfri_student_number"]

        return self.cleaned_data    

class StudentNumberInitConfirmForm(forms.Form):

    pk = forms.IntegerField(required=False, widget=forms.HiddenInput(), label= u'')

    def __init__(self, *args, **kwargs): 
        initial_vars = kwargs.get('initial', None)
        
        super(StudentNumberInitConfirmForm, self).__init__(*args, **kwargs)

        if initial_vars:
            self.fields['pk'].initial = initial_vars.get('pk', None)

