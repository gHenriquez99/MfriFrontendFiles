import datetime

from django.conf import settings
from django.db import models, connection

from AppsAdmin.dbk import RegEncryptKeyS, RegEncryptKeyE
from AppBase.models import AppBase

from AppLegacyBase.models import AppLegacyBase

from MAffiliations.models import Affiliations

from MOffices.models import MfriOffices, Jurisdictions, Phonenumbertypes

from SRec.models import TitleCaseName, Studentrecords
from MSchedule.models import Scheduledcourses

from SWebRegistration.utils_strings import FixName, UpdateNameFields 

class WebRegHoldStatus(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 

    class Meta:
        db_table = u'WebRegHoldStatus'
        verbose_name_plural = "WebRegHoldStatuses"
        ordering = ['name']

    def __unicode__(self):
        return self.name

class WebRegHold(AppLegacyBase):
    scheduled_course = models.ForeignKey(Scheduledcourses, db_column='ScheduledCourseID')
    
    fee = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='Fee', blank=True) 

    in_state_rate = models.IntegerField(null=True, db_column='InStateRate', blank=True) 
    
    priority = models.IntegerField(null=True, db_column='Priority', blank=True) 
    
    affiliation = models.ForeignKey(Affiliations, db_column='AffiliationID')
    
    affiliation_text = models.CharField(max_length=765, db_column='Affiliation', blank=True) 
    
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    
    first_name = models.CharField(max_length=255, db_column='first_name', blank=True) 
    middle_name = models.CharField(max_length=255, db_column='middle_name', blank=True) 
    last_name = models.CharField(max_length=255, db_column='last_name', blank=True) 
    suffix = models.CharField(max_length=255, db_column='suffix', blank=True) 

    id_number = models.BinaryField(db_column='IDNumber', blank=True) 
    
    state_provider_number = models.BinaryField(db_column='StateProviderNumber', blank=True) 
    
    mfri_student_number = models.CharField(max_length=255, blank=True) 

    nfa_sid_number = models.BinaryField(blank=True) 
    
    birth_date = models.DateField(default=None, null=True, blank=True, help_text='Birth Date') 
    emt_expiration_date = models.DateField(default=None, null=True, blank=True, help_text='EMT Certification Expiration Date. Usually only used for EMS Refresher classes.') 
    
    address1 = models.CharField(max_length=765, db_column='Address1', blank=True) 
    address2 = models.CharField(max_length=765, db_column='Address2', blank=True) 
    city = models.CharField(max_length=765, db_column='City', blank=True) 
    state = models.CharField(max_length=765, db_column='State', blank=True) 
    postcode = models.CharField(max_length=96, db_column='PostCode', blank=True) 
    country = models.CharField(max_length=765, db_column='Country', blank=True) 
    
    primary_phone_number = models.CharField(max_length=96, db_column='PrimaryPhoneNumber', blank=True) 
    secondary_phone_number = models.CharField(max_length=96, db_column='SecondaryPhoneNumber', blank=True) 
    mobile_phone_number = models.CharField(max_length=96, db_column='MobilePhoneNumber', blank=True) 

    email = models.CharField(max_length=765, db_column='Email', blank=True) 

    status = models.ForeignKey('WebRegHoldStatus', db_column='StatusID')

    is_late_registration = models.BooleanField(default=False, blank=True, help_text='Registration submitted after closed date.')

    owes_course_fee = models.BooleanField(default=False, blank=True, help_text='Student owes course fee.')

    book_fee_acknowledged = models.BooleanField(default=False, help_text='Student has acknowledged book fee at time of registration.')

    is_approved = models.BooleanField(default=False, help_text='This application has been approved.')
    has_been_reviewed = models.BooleanField(default=False, help_text='This application has been reviewed and approved or disapproved.')
    approved_on = models.DateTimeField(default='0000-00-00 00:00:00', help_text='Approval Timestamp.') 
    approved_by = models.CharField(max_length=255, blank=True, help_text='Who has approved the application.') 
    approved_by_username = models.CharField(max_length=80, blank=True, help_text='Username and system for approver.') 

    book_fee_agency_pay = models.BooleanField(default=False, help_text='Affiliation agency has affirmed they will pay all book fees at time of approval.')

    training_officer_note = models.TextField(blank=True, help_text='Optional note entered by training officer approving application.')
    student_note = models.TextField(blank=True, help_text='Optional note entered by student submitting application.')
    registrar_note = models.TextField(blank=True, help_text='Optional note entered by MFRI staff processing application.')


    student_registration = models.IntegerField(null=True, db_column='StudentRegID', blank=True) 

#    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
#    lastchange = models.DateTimeField(db_column='LastChange') 
#    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
#    created = models.DateTimeField(db_column='Created') 

    class Meta:
        db_table = u'WebRegHold'
        verbose_name_plural = "WebRegHolds"
        ordering = ['created']

    def __unicode__(self):
        
        top_message = u''
        if self.scheduled_course.require_training_officer_approval:
            if self.has_been_reviewed:
                top_message += u'TOP Reviewed'
            if self.is_approved:
                if len(top_message) > 0:
                    top_message += u' '
                top_message += u'Approved by %s on %s' % (self.approved_by, self.approved_on.strftime('%m-%d-%Y %H:%M:%S'))
            else:
                if self.approved_on:
                    top_message += u'Not approved by %s on %s' % (self.approved_by, self.approved_on.strftime('%m-%d-%Y %H:%M:%S'))

        created_date = u''
        if self.created:
            created_date = self.created.strftime('%m-%d-%Y %H:%M:%S')

        return u'%s %s %s %s %s %s' % (self.scheduled_course.log_number, created_date, self.name, self.status.name, self.affiliation.name, top_message)

    def _get_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(IDNumber, %s) as ssn FROM WebRegHold WHERE id=%s", [RegEncryptKeyS(), self.id])
        return cursor.fetchone()[0]
    
    def _set_ssn(self, ssn_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as ssn", [ssn_value, RegEncryptKeyS()])
        self.id_number = cursor.fetchone()[0]
    
    ssn = property(_get_ssn, _set_ssn)
    ssn_clear = property(_get_ssn, _set_ssn) #20210217

    def _get_partial_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(IDNumber, %s) as ssn FROM WebRegHold WHERE id=%s", [RegEncryptKeyS(), self.id])
        ssn_found = cursor.fetchone()[0]
        ssn_length=5
        fill_char='X'
        if ssn_found[0:3].upper() == u'MSN':
            return ssn_found
        else:
            if fill_char:
                return str(fill_char) * (len(ssn_found) - ssn_length) + str(ssn_found[-ssn_length:])
            else:
                return ssn_found[-ssn_length:]

    partial_ssn = property(_get_partial_ssn)

    def _get_epins(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(StateProviderNumber, %s) as epins FROM WebRegHold WHERE id=%s", [RegEncryptKeyE(), self.id])
        return cursor.fetchone()[0]
    
    def _set_epins(self, epins_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as epins", [epins_value, RegEncryptKeyE()])
        self.state_provider_number = cursor.fetchone()[0]
    
    epins = property(_get_epins, _set_epins)
    epins_clear = property(_get_epins, _set_epins) #20210217

    def _get_nfa_sid(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(nfa_sid_number, %s) as nfa_sid FROM WebRegHold WHERE id=%s", [RegEncryptKeyE(), self.id])
        return cursor.fetchone()[0]
    
    def _set_nfa_sid(self, nfa_sid_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as nfa_sid", [nfa_sid_value, RegEncryptKeyE()])
        self.nfa_sid_number = cursor.fetchone()[0]
    
    nfa_sid = property(_get_nfa_sid, _set_nfa_sid)

    def _get_full_name(self):
        "returns the full name FN MN LN S"
        
        FixName(student_record=self) 

        ReturnedName = ''
        if self.first_name and len(self.first_name) > 0:
            ReturnedName += TitleCaseName(self.first_name)
            #, no_title_case=self.show_name_as_is
    
        if self.middle_name and len(self.middle_name) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(self.middle_name)
    
        if self.last_name and len(self.last_name) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(self.last_name)
    
        if self.suffix and len(self.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.suffix.title() 
        
        return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')#20190502
    
    def _get_full_name_reversed(self):
        "returns the full name LN S, FN MN"

        FixName(student_record=self) #20210222

        ReturnedName = ''
        if self.last_name and len(self.last_name) > 0:
            ReturnedName += TitleCaseName(name=self.last_name)

        if self.suffix and len(self.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '

            ReturnedName += self.suffix.title() 
    
        if len(ReturnedName) > 0:
            ReturnedName += ','
    
        if self.first_name and len(self.first_name) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(name=self.first_name)
    
        if self.middle_name and len(self.middle_name) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(name=self.middle_name)

        return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')#20190502

    full_name_reversed = property(_get_full_name_reversed)

    def _set_full_name(self, RawFullName):
        "sets name parts with the given full name"
        NewFullName = RawFullName.strip()
    
        SuffixValues = set(['JR', 'SR', 'I', 'II', 'III', 'IV', 'V'])
    
        if NewFullName.find(',') >= 0: #name contains a comma (,) so is probably reversed
            NameParts = NewFullName.split(',', 1)
    
            NewFullName = NameParts[1].strip() + " " + NameParts[0].strip()
    
        NameTokens = NewFullName.split(' ')
    
        self.first_name = NameTokens[0].strip()
        self.middle_name = NameTokens[1].strip()
    
        if NameTokens[-1].upper().replace('.', ' ').strip() in SuffixValues:
            self.suffix = NameTokens[-1].upper().replace('.', ' ').strip()
            self.last_name = " ".join(NameTokens[2: -1])
        else:
            self.last_name = " ".join(NameTokens[2:])
    
        if not self.last_name:
            self.last_name = ''
        
        if len(self.last_name) == 0:
            if len(self.middle_name) > 0:
                self.last_name = self.middle_name
                self.middle_name = ''
            else:
                self.last_name = self.first_name
                self.first_name = ''
    
    full_name = property(_get_full_name, _set_full_name)

    def _get_first_name_title_case(self):
        "returns the title cased first name"

        UpdateNameFields(web_registration_record=self) #20210405

        if self.first_name and len(self.first_name.strip()) > 0:
            return TitleCaseName(name=self.first_name.strip()) 
    
        return u''
    
    first_name_tc = property(_get_first_name_title_case)

    def _get_middle_name_title_case(self):
        "returns the title cased middle name"

        UpdateNameFields(web_registration_record=self) #20210405

        if self.middle_name and len(self.middle_name.strip()) > 0:
            return TitleCaseName(name=self.middle_name.strip())
    
        return u''
    
    middle_name_tc = property(_get_middle_name_title_case)

    def _get_last_name_title_case(self):
        "returns the title cased last name"
        
        UpdateNameFields(web_registration_record=self) 

        if self.last_name and len(self.last_name.strip()) > 0:
            ReturnedName = TitleCaseName(name=self.last_name.strip()) 
            return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')

        return u''
    
    last_name_tc = property(_get_last_name_title_case)

    def _get_suffix_title_case(self):
        "returns the title cased Suffix"
        
        UpdateNameFields(web_registration_record=self) 

        if self.suffix and len(self.suffix.strip()) > 0:
            return self.suffix.strip().title().replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')
    
        return u''
        
    suffix_tc = property(_get_suffix_title_case)

    def _get_last_name_and_suffix_title_case(self):
        "returns the title cased last name and Suffix"
        
        ReturnedName = ''
        if self.last_name and len(self.last_name.strip()) > 0:
            ReturnedName += TitleCaseName(name=self.last_name.strip()) 

        if self.suffix and len(self.suffix.strip()) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '

            ReturnedName += self.suffix.strip().title() 

        return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')
        
    
    last_name_and_suffix_tc = property(_get_last_name_and_suffix_title_case)

    def _student_record(self):
        "returns self so it will be compatible with student_registration table"
        
        return self
        
    student_record = property(_student_record)

    def _email_address(self):
        "returns the student email address"

        if not self.email or (len(self.email) == 0):
            return u'No email address'

        return self.email

    email_address = property(_email_address)

    def _get_address(self):
        "returns the address"
        ReturnedAddress = {}

        if self.address1 and (len(self.address1) > 0):
            ReturnedAddress['address1'] = self.address1.strip()
        else:
            ReturnedAddress['address1'] = u''

        if self.address2 and (len(self.address2) > 0):
            ReturnedAddress['address2'] = self.address2.strip()
        else:
            ReturnedAddress['address2'] = u''

        if self.city and (len(self.city) > 0):
            ReturnedAddress['city'] = self.city.strip()
        else:
            ReturnedAddress['city'] = u''

        if self.state and (len(self.state) > 0): # and self.state.upper() != 'MD':
            ReturnedAddress['state'] = self.state.upper().strip()
        else:
            ReturnedAddress['state'] = u''

        if self.postcode and (len(self.postcode) > 0): #showpostcode doesn't seem to be used
            ReturnedAddress['postcode'] = self.postcode.upper().strip()
        else:
            ReturnedAddress['postcode'] = u''

        if self.country and (len(self.country) > 0) and self.country.upper() != 'USA' and self.country.upper() != 'US':
            ReturnedAddress['country'] = self.country.upper().strip()
        elif self.country.upper() != 'USA' and self.country.upper() != 'US':
            ReturnedAddress['country'] = u''

        return ReturnedAddress

    address = property(_get_address)


    def _medical_clearance(self):
        #out of scope
        
        return None
        
    medical_clearance = property(_medical_clearance)






