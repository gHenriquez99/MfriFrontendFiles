import re 
import datetime

from django.conf import settings
from django.db import models, connection

from AppsAdmin.dbk import SRecEncryptKeyS, SRecEncryptKeyE, RegEncryptKeyE #20191105

from AppBase.models import AppBase

from AppLegacyBase.models import AppLegacyBase

from MAffiliations.models import Affiliations

from MOffices.models import MfriOffices, Jurisdictions, Phonenumbertypes

from SWebRegistration.models import WebRegHold

from MCourses.models import TCode 

from MExams.models import EvocVehicleType

from MESSA.models import Messrcollegeleveltypes, Messrgendertypes, Messrgradeleveltypes, Messrracetypes, MessrHold, Messrtitletypes, Messrapplicationlevel, Messrapplicationtype #20161102

from SRec.models import Studentrecords

from MSchedule.models import Scheduledcourses, UmdTerm 

from SRegistration.utils_search import FindStudentRecord 

def TitleCaseName(name=None, no_title_case=False): 
    
    if no_title_case:
        return name
        
    if not name:
        return name

    NAME_MC_RE = re.compile(#r'^[mc|mac]*', re.IGNORECASE)
        r'^mc|^mac'  # mc mac
        , re.IGNORECASE)  

    try:
        regex_match = NAME_MC_RE.match(name)
        
        if regex_match: # and regex_match.group(0):
            regex_match_length = regex_match.end()
            fixed_name = name[:regex_match_length].title() + name[regex_match_length:].title() #+ regex_match.group(1).title() 
        else:
            fixed_name = name.title()
    except:
        return name

    return fixed_name

class Registrationpriorityrules(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    userselectable = models.IntegerField(null=True, db_column='UserSelectable', blank=True) 
    useforcourse = models.CharField(max_length=765, db_column='UseForCourse', blank=True) 
    priorityincrement = models.IntegerField(null=True, db_column='PriorityIncrement', blank=True) 
    
    class Meta:
        db_table = u'RegistrationPriorityRules'
        verbose_name_plural = "RegistrationPriorityRules"
        ordering = ['name']


class Preregistrationstatus(models.Model):

    sortorder = models.IntegerField(null=True, db_column='SortOrder', blank=True) 
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    class Meta:
        db_table = u'PreRegistrationStatus'

class Preregistrations(AppLegacyBase):

    student_record = models.ForeignKey(Studentrecords, db_column='StudentID')
    
    scheduled_course = models.ForeignKey(Scheduledcourses, db_column='ScheduledCourseID')
    
    log_number = models.CharField(max_length=765, db_column='LogNumber', blank=True) 

    ssn = models.BinaryField(db_column='SSN', blank=True) 
    state_provider_number = models.BinaryField(db_column='StateProviderNumber', blank=True) 

    mfri_student_number = models.CharField(max_length=255, blank=True) 

    nfa_sid_number = models.BinaryField(blank=True) 
    
    birth_date = models.DateField(null=True, db_column='BirthDate', blank=True) 

    title = models.ForeignKey(Messrtitletypes, db_column='TitleID', blank=True, null=True)
    firstname = models.CharField(max_length=765, db_column='FirstName', blank=True) 
    middlename = models.CharField(max_length=765, db_column='MiddleName', blank=True) 
    lastname = models.CharField(max_length=765, db_column='LastName', blank=True) 
    suffix = models.CharField(max_length=765, db_column='Suffix', blank=True) 
    
    address1 = models.CharField(max_length=765, db_column='Address1', blank=True) 
    address2 = models.CharField(max_length=765, db_column='Address2', blank=True) 
    apt = models.CharField(max_length=765, db_column='Apt', blank=True) 
    city = models.CharField(max_length=765, db_column='City', blank=True) 
    state = models.CharField(max_length=6, db_column='State', blank=True) 
    postcode = models.CharField(max_length=60, db_column='PostCode', blank=True) 
    country = models.CharField(max_length=255, blank=True) 
    
    county = models.ForeignKey(Jurisdictions, db_column='CountyID')

    primary_phone_number = models.CharField(max_length=96, db_column='PrimaryPhoneNumber', blank=True) 
    secondary_phone_number = models.CharField(max_length=96, db_column='SecondaryPhoneNumber', blank=True) 

    email = models.CharField(max_length=255, db_column='Email', blank=True) 
    
    status = models.ForeignKey(Preregistrationstatus, db_column='StatusID')
    
    student_registration = models.ForeignKey('Studentregistration', db_column='StudentRegID', null=True)
    
    is_web_reg = models.BooleanField(default=False, blank=True, help_text='Record submitted through website.')#20170405
    
    is_late_registration = models.BooleanField(default=False, blank=True, help_text='Registration submitted after closed date.')#20171106
    
    owes_course_fee = models.BooleanField(default=False, blank=True, help_text='Student owes course fee.')#20170823
    
    registration_approved_by = models.CharField(max_length=255, blank=True, null=True, help_text='Who has approved the application.') #20170615
    registration_approved_by_username = models.CharField(max_length=80, blank=True, null=True, help_text='Username and system for approver.') #20170615
    registration_approved_on = models.DateTimeField(null=True, help_text='Approval Timestamp.') #20170615
    book_fee_acknowledged = models.BooleanField(default=False, help_text='Student has acknowledged book fee at time of registration.')#20170615
    book_fee_agency_pay = models.BooleanField(default=False, help_text='Affiliation agency has affirmed they will pay all book fees at time of approval.')#20170615
    
    priority = models.IntegerField(null=True, db_column='Priority', blank=True) 

    affiliation = models.ForeignKey(Affiliations, db_column='AffiliationID')

    emt_certification_expiration_date = models.DateField(null=True, db_column='CertificationExpirationDate', blank=True) 
    
    #lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    #lastchange = models.DateTimeField(db_column='LastChange') 
    #createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    #created = models.DateTimeField(db_column='Created') 
    def __unicode__(self):
        return u'%s %s, %s %s' % (self.lastname, self.suffix, self.firstname, self.middlename)


    class Meta:
        db_table = u'PreRegistrations'
        verbose_name_plural = "PreRegistrations"
        ordering = ['priority','created']

    def _HasStudentRecord(self):
        try:
            if not self.student_record:
                return False
        except Studentrecords.DoesNotExist:
            existing_student_record = FindStudentRecord(partial_ssn=self.ssn_clear, last_name=self.lastname, state_provider_number=self.epins_clear, nfa_sid_number=self.nfa_sid) 
            self.student_record = existing_student_record
            self.save(update_fields=['student_record'])
        except:
            return False
        try:
            if not self.student_record:
                return False
        except:
            return False
        
        return True
            
    HasStudentRecord = property(_HasStudentRecord)

    def _get_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(SSN, %s) as ssn FROM PreRegistrations WHERE id=%s", [SRecEncryptKeyS(), self.id])
        if not cursor.fetchone():
            return None
        try:
            return cursor.fetchone()[0]
        except:
            return None
   
    def _set_ssn(self, ssn_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as ssn", [ssn_value, SRecEncryptKeyS()])
        self.ssn = cursor.fetchone()[0]
    
    ssn_clear = property(_get_ssn, _set_ssn)

    def _get_partial_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(SSN, %s) as ssn FROM PreRegistrations WHERE id=%s", [SRecEncryptKeyS(), self.id])
        return cursor.fetchone()[0][-5:]
    
    def _set_partial_ssn(self, ssn_value):
        padded_ssn = ssn_value.rjust(9,'0')
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as ssn", [padded_ssn, SRecEncryptKeyS()])
        self.ssn = cursor.fetchone()[0]

    partial_ssn = property(_get_partial_ssn, _set_partial_ssn)
    
    def _get_epins(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(StateProviderNumber, %s) as epins FROM PreRegistrations WHERE id=%s", [SRecEncryptKeyE(), self.id])
        if not cursor.fetchone():
            return None
        try:
            return cursor.fetchone()[0]
        except:
            return None
   
    def _set_epins(self, epins_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as epins", [epins_value, SRecEncryptKeyE()])
        self.state_provider_number = cursor.fetchone()[0] 
    
    epins_clear = property(_get_epins, _set_epins)

    def _get_nfa_sid(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(nfa_sid_number, %s) as nfa_sid FROM PreRegistrations WHERE id=%s", [RegEncryptKeyE(), self.id])
        return cursor.fetchone()[0]

    def _set_nfa_sid(self, nfa_sid_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as nfa_sid", [nfa_sid_value, RegEncryptKeyE()])
        self.nfa_sid_number = cursor.fetchone()[0]

    nfa_sid = property(_get_nfa_sid, _set_nfa_sid)

    def _get_full_name(self):
        "returns the full name FN MN LN S"
        
        ReturnedName = ''
        if self.firstname and len(self.firstname) > 0:
            ReturnedName += TitleCaseName(self.firstname) 
    
        if self.middlename and len(self.middlename) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(self.middlename) 
    
        if self.lastname and len(self.lastname) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(self.lastname) 
    
        if self.suffix and len(self.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.suffix.title() 

        return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')

    def _get_full_name_reversed(self):
        "returns the full name LN S, FN MN"

        ReturnedName = ''
        if self.lastname and len(self.lastname) > 0:
            ReturnedName += TitleCaseName(name=self.lastname) 

        if self.suffix and len(self.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.suffix.title() 
    
        if len(ReturnedName) > 0:
            ReturnedName += ','
    
        if self.firstname and len(self.firstname) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(name=self.firstname) 
    
        if self.middlename and len(self.middlename) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(name=self.middlename) 
    
        return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')

    full_name_reversed = property(_get_full_name_reversed)

    def _get_full_name_slug(self):
        "returns the full name and object id as slug FNMNLNSID no spaces"
        ReturnedName = ''
        if self.firstname and len(self.firstname) > 0:
            ReturnedName += self.firstname
    
        if self.middlename and len(self.middlename) > 0:
            ReturnedName += self.middlename    
    
        if self.lastname and len(self.lastname) > 0:
            ReturnedName += self.lastname
            
        if self.suffix and len(self.suffix) > 0:
            ReturnedName += self.suffix
    
        slugified_name = slugify(u'%s%d' % (ReturnedName.strip(), self.id))       
        return slugified_name
    
    full_name_slug = property(_get_full_name_slug)
    
    def _set_full_name(self, RawFullName):
        "sets name parts with the given full name"
        NewFullName = RawFullName.strip()
    
        SuffixValues = set(['JR', 'SR', 'I', 'II', 'III', 'IV', 'V'])
    
        if NewFullName.find(',') >= 0: #name contains a comma (,) so is probably reversed
            NameParts = NewFullName.split(',', 1)
    
            NewFullName = NameParts[1].strip() + " " + NameParts[0].strip()
    
        NameTokens = NewFullName.split(' ')
    
        self.firstname = NameTokens[0].strip()
        self.middlename = NameTokens[1].strip()
    
        if NameTokens[-1].upper().replace('.', ' ').strip() in SuffixValues:
            self.suffix = NameTokens[-1].upper().replace('.', ' ').strip() 
            self.lastname = " ".join(NameTokens[2: -1])
        else:
            self.lastname = " ".join(NameTokens[2:])
    
        if not self.lastname:
            self.lastname = ''
        
        if len(self.lastname) == 0:
            if len(self.middlename) > 0:
                self.lastname = self.middlename
                self.middlename = ''
            else:
                self.lastname = self.firstname
                self.firstname = ''
    
    full_name = property(_get_full_name, _set_full_name)
    name = property(_get_full_name)

    def _get_first_name_title_case(self):
        "returns the title cased first name"

        if self.firstname and len(self.firstname.strip()) > 0:
            return TitleCaseName(name=self.firstname.strip()) 
    
        return u''
    
    first_name_tc = property(_get_first_name_title_case)

    def _get_middle_name_title_case(self):
        "returns the title cased middle name"

        if self.middlename and len(self.middlename.strip()) > 0:
            return TitleCaseName(name=self.middlename.strip()) 
    
        return u''
    
    middle_name_tc = property(_get_middle_name_title_case)

    def _get_last_name_title_case(self):
        "returns the title cased last name"
        
        if self.lastname and len(self.lastname.strip()) > 0:
            ReturnedName = TitleCaseName(name=self.lastname.strip()) 
            return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')

        return u''
    
    last_name_tc = property(_get_last_name_title_case)

    def _get_suffix_title_case(self):
        "returns the title cased Suffix"
        
        if self.suffix and len(self.suffix.strip()) > 0:
            return self.suffix.strip().title().replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')
    
        return u''
        
    suffix_tc = property(_get_suffix_title_case)

    def _get_last_name_and_suffix_title_case(self):
        "returns the title cased last name and Suffix"
        
        ReturnedName = ''
        if self.lastname and len(self.lastname) > 0:
            ReturnedName += TitleCaseName(name=self.lastname.strip()) 

        if self.suffix and len(self.suffix.strip()) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.suffix.strip().title() 
    
        return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')
    
    last_name_and_suffix_tc = property(_get_last_name_and_suffix_title_case)

    def _email_address(self):
        "returns the student email address"

        if not self.email:
            return u'No email address'

        return self.email

    email_address = property(_email_address)

    def _phone_number(self):
        "returns the student phone number"

        if not self.primary_phone_number:
            if self.secondary_phone_number:
                return self.secondary_phone_number
            else:
                return u'No Phone Number'
            

        return self.primary_phone_number.strip()

    phone_number = property(_phone_number)
    
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
                
        if self.state and (len(self.state) > 0): 
            ReturnedAddress['state'] = self.state.upper().strip()
        else:
            ReturnedAddress['state'] = u''
        
        if self.postcode and (len(self.postcode) > 0): 
            ReturnedAddress['postcode'] = self.postcode.upper().strip()
        else:
            ReturnedAddress['postcode'] = u''

        if self.country and (len(self.country) > 0) and self.country.upper() != 'USA' and self.country.upper() != 'US':
            ReturnedAddress['country'] = self.country.upper().strip()
        elif self.country.upper() != 'USA' and self.country.upper() != 'US':
            ReturnedAddress['country'] = u''
        
        return ReturnedAddress

    address = property(_get_address)

    def _lms_user_name(self):
        "returns the lms user name"

        if not self.HasStudentRecord:
            return u''

        return self.student_record.lms_user_name

    lms_user_name = property(_lms_user_name)

    def _lms_user_account_password(self):
        "returns the lms user account password that is on file. Should only be the initial temporary password."

        if not self.HasStudentRecord:
            return u''

        return self.student_record.lms_user_account_password

    lms_user_account_password = property(_lms_user_account_password)

    def _lms_user_account_identifier(self):
        "returns the lms user identifier"

        if not self.HasStudentRecord:
            return u''

        return self.student_record.lms_user_account_identifier

    lms_user_account_identifier = property(_lms_user_account_identifier)

    def _lms_user_name_created_date(self):
        "returns the lms user name creation date"

        if not self.HasStudentRecord:
            return u''

        return self.student_record.lms_user_name_created_date

    lms_user_name_created_date = property(_lms_user_name_created_date)

    def _lms_user_name_created_date_MDY(self):
        "returns the lms user name creation date"

        if not self.HasStudentRecord:
            return u''

        if self.student_record.lms_user_name_created_date:
            return self.student_record.lms_user_name_created_date.strftime('%m-%d-%Y')

        return u''

    lms_user_name_created_date_MDY = property(_lms_user_name_created_date_MDY)
    
class Studentfeebatchestypes(models.Model):

    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        
        if self.id == 1:
            return u'Charges'
        elif self.id == 2:
            return u'PIDN'

        return self.name

    class Meta:
        db_table = u'StudentFeeBatchesTypes'

        verbose_name_plural = "Studentfeebatchestypes"
        ordering = ['id', 'name']

    def _batch_type_abbreviation(self):
        "returns short name if id == 2 PIDN or id == 1 Charges depending"

        if self.id == 1:
            return u'Charges'
        elif self.id == 2:
            return u'PIDN'

        return self.name

    batch_type_abbreviation = property(_batch_type_abbreviation)


class Studentfeeerrors(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    value = models.CharField(max_length=765, db_column='Value', blank=True) 
    level = models.IntegerField(null=True, db_column='Level', blank=True) 

    #20210722+
    def __unicode__(self):
        return u'%s %s' % (self.value, self.name)
    #20210722-

    class Meta:
        db_table = u'StudentFeeErrors'
        #20210722+
        verbose_name_plural = "Studentfeeerrors"
        ordering = ['value', 'id', 'name']
        #20210722- 

class Studentfeesstatus(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    #20210722+
    def __unicode__(self):
        return self.name
    #20210722-

    class Meta:
        db_table = u'StudentFeesStatus'
        #20210722+
        verbose_name_plural = "Studentfeesstatuses"
        ordering = ['id', 'name']
        #20210722- 

class Studentfeebatches(AppLegacyBase): #20210722
#    id = models.IntegerField(primary_key=True, db_column='ID') 

    scheduled_course = models.ForeignKey(Scheduledcourses, db_column='ScheduledCourseID') #20210722
    
    #20210722scheduledcourseid = models.IntegerField(null=True, db_column='ScheduledCourseID', blank=True) 
    description = models.CharField(max_length=765, db_column='Description', blank=True) 
    
    status = models.ForeignKey(Studentfeesstatus, db_column='StatusID') #20210722
    
    #20210722statusid = models.IntegerField(null=True, db_column='StatusID', blank=True) 
    
    batch_type = models.ForeignKey(Studentfeebatchestypes, db_column='typeid') #20210722

    #20210722#typeid = models.IntegerField(null=True, db_column='TypeID', blank=True) 

    date_sent_to_accounting = models.DateTimeField(null=True, db_column='DateSentToAccounting', blank=True) #20210722
    
    date_locked_by_accounting = models.DateTimeField(null=True, db_column='DateLockedByAccounting', blank=True)  #20210722
    date_sent_to_bursar = models.DateTimeField(null=True, db_column='DateSentToBursar', blank=True) #20210722
    date_pidn_sent_to_bursar = models.DateTimeField(null=True, db_column='DatePidnSentToBursar', blank=True) #20210722

    recordstatusid = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 

    batch_error = models.ForeignKey(Studentfeeerrors, db_column='ErrorID') #20210722

    #20210722errorid = models.IntegerField(null=True, db_column='ErrorID', blank=True)  
    
    max_amount_due = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='MaxAmountDue', blank=True) #20210722

    tcode = models.ForeignKey(TCode, db_column='TCodeID') #20210722

    umd_term = models.ForeignKey(UmdTerm, db_column='TermID') #20210722
    
    #20210722tcodeid = models.IntegerField(null=True, db_column='TCodeID', blank=True) 
    #20210722termid = models.IntegerField(null=True, db_column='TermID', blank=True) 
    item_reference = models.CharField(max_length=765, db_column='ItemReference', blank=True)  #20210722
    #20210722lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    #20210722lastchange = models.DateTimeField(db_column='LastChange') 
    #20210722createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    #20210722created = models.DateTimeField(db_column='Created') 

    #20210722+
    def __unicode__(self):
        return u'%s-%s-%s%s-%s %s %s' % (self.scheduled_course.course_description.category, self.scheduled_course.course_description.level, self.scheduled_course.funding_source_code, self.scheduled_course.section_number, self.scheduled_course.fiscal_year, self.batch_type, self.status)
    #20210722- 
    
    class Meta:
        db_table = u'StudentFeeBatches'

        #20210722+
        verbose_name_plural = "Studentfeebatches"
        ordering = ['date_sent_to_accounting', 'date_pidn_sent_to_bursar']
        #20210722- 

class Studentfeespreferences(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    userid = models.IntegerField(null=True, db_column='UserID', blank=True) 
    readpermission = models.IntegerField(null=True, db_column='ReadPermission', blank=True) 
    writepermission = models.IntegerField(null=True, db_column='WritePermission', blank=True) 
    accountingreadpermission = models.IntegerField(null=True, db_column='AccountingReadPermission', blank=True) 
    accountingwritepermission = models.IntegerField(null=True, db_column='AccountingWritePermission', blank=True) 
    sendtobursarpermission = models.IntegerField(null=True, db_column='SendToBursarPermission', blank=True) 
    adminreadpermission = models.IntegerField(null=True, db_column='AdminReadPermission', blank=True) 
    adminwritepermission = models.IntegerField(null=True, db_column='AdminWritePermission', blank=True) 
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 
    class Meta:
        db_table = u'StudentFeesPreferences'

class Paymentmethod(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    paymenttypeid = models.IntegerField(null=True, db_column='PaymentTypeID', blank=True) 
    description = models.CharField(max_length=765, db_column='Description', blank=True) 
    notes = models.CharField(max_length=765, db_column='Notes', blank=True) 
    expirydate = models.DateTimeField(null=True, db_column='ExpiryDate', blank=True) 
    statusid = models.IntegerField(null=True, db_column='StatusID', blank=True) 
    class Meta:
        db_table = u'PaymentMethod'

class Paymentmethodstatus(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'PaymentMethodStatus'

class Paymentstatus(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'PaymentStatus'

class Paymenttype(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'PaymentType'


class Registrationstatus(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    sort_order = models.IntegerField(null=True, db_column='SortOrder', blank=True) 

    class Meta:
        db_table = u'RegistrationStatus'
        verbose_name_plural = "Registrationstatuses"
        ordering = ['sort_order']

    def __unicode__(self):
        return '%s' % (self.name)


class Studentgradeoptions(AppLegacyBase):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    live_record = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 
    
    is_passing = models.BooleanField(default=True, blank=True, help_text='Grade option is a passing grade.')
    
#    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
#    lastchange = models.DateTimeField(db_column='LastChange') 
#    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
#    created = models.DateTimeField(db_column='Created') 
    class Meta:
        db_table = u'StudentGradeOptions'

        verbose_name_plural = "Studentgradeoptions"
        ordering = ['name']

    def __unicode__(self):
        return '%s' % (self.name)


class Studentregistration(AppLegacyBase):
    student_record = models.ForeignKey(Studentrecords, db_column='StudentID')
    updatedstudentrecordid = models.IntegerField(null=True, db_column='UpdatedStudentRecordID', blank=True) # consider removing field

    scheduled_course = models.ForeignKey(Scheduledcourses, db_column='SchedCourseID')

    registration_status = models.ForeignKey(Registrationstatus, db_column='RegistrationStatusID', default=None, related_name="%(app_label)s_%(class)s_registration_status")
    registration_status_note = models.CharField(max_length=765, db_column='RegistrationStatusNote', blank=True) 

    payment_due = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='PaymentDue', blank=True) 

    payment_method = models.ForeignKey(Paymentmethod, default=None, db_column='PaymentMethodID')
    
    
    payment_status = models.ForeignKey(Paymentstatus, default=None, db_column='PaymentStatusID')
    
    resource_fee = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='ResourceFee', blank=True) 
    has_book = models.IntegerField(null=True, db_column='HasBook', blank=True) 
    
    pidn_batch = models.ForeignKey(Studentfeebatches, db_column='PidnBatchID', default=None, null=True, blank=True, related_name="pidn_batch")
    
    pidn_sent = models.BooleanField(default=False, blank=True, db_column='PidnSent', help_text='PIDN details sent to UMCP Bursar.')
    
    used_book = models.BooleanField(default=False, blank=True, db_column='UsedBook', help_text='Student given used book.')

    credit_amount = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='CreditAmount', blank=True) 

    invoice_error = models.ForeignKey(Studentfeeerrors, default=None, db_column='InvoiceErrorID')
    invoice_error_list = models.CharField(max_length=765, db_column='InvoiceErrorList', blank=True) 
    invoice_error_level = models.IntegerField(null=True, db_column='InvoiceErrorLevel', blank=True) 

    credit_batch = models.ForeignKey(Studentfeebatches, db_column='CreditBatchID', default=None, null=True, blank=True, related_name="credit_batch")

    invoice_batch = models.ForeignKey(Studentfeebatches, db_column='InvoiceBatchID', default=None,  null=True, blank=True, related_name="invoice_batch")

    affiliation = models.ForeignKey(Affiliations, db_column='AffiliationID')

    grade_note = models.CharField(max_length=240, db_column='GradeNote', blank=True) 
    
    grade = models.ForeignKey(Studentgradeoptions, default=None, db_column='GradeID')
    grade_text = models.CharField(max_length=60, db_column='Grade', blank=True) 
    
    percentage_score = models.CharField(max_length=30, db_column='PercentageScore', blank=True) 

    web_reg_hold = models.ForeignKey(WebRegHold, null=True, blank=True, db_column='WebRegHoldID')

    pre_reg_number = models.IntegerField(null=True, db_column='PreRegNumber', blank=True) 
    pre_reg_priority = models.IntegerField(null=True, db_column='PreRegPriority', blank=True) 
    pre_reg_hold = models.ForeignKey(Preregistrations, default=None, db_column='PreRegID')

    messa_hold = models.ForeignKey(MessrHold, default=None, null=True, blank=True, db_column='MESSRHoldID')
    messa_data_received = models.BooleanField(default=False, blank=True, db_column='MESSRDataReceived', help_text='MESSA Data received by MIEMSS.')

    sent_to_transcript = models.DateTimeField(null=True, db_column='SentToTranscript', blank=True) 
    saved_in_transcript = models.DateTimeField(null=True, db_column='SavedInTranscript', blank=True) 

    status = models.ForeignKey(Registrationstatus, db_column='StatusID', default=None, related_name="%(app_label)s_%(class)s_status")
    status_note = models.CharField(max_length=765, db_column='StatusNote', blank=True) 

    note = models.CharField(max_length=765, db_column='Note', blank=True) 
    
    exam_results = models.TextField(blank=True, default='')  
    last_exam_mastery_report = models.TextField(blank=True, default='')  

    ok_to_email_grades = models.BooleanField(default=True, blank=True, db_column='ok_to_email_grades', help_text='Ok to email grade related records to student.')

    application_type = models.ForeignKey(Messrapplicationtype, default=None, related_name="%(app_label)s_%(class)s_applicationtype")#20161102
    application_level = models.ForeignKey(Messrapplicationlevel, default=None, related_name="%(app_label)s_%(class)s_applicationlevel")#20161102

    evoc_vehicle_type = models.ForeignKey(EvocVehicleType, default=None, related_name="%(app_label)s_%(class)s_evocvehicletype")#20161117

    #20191205+
    umd_canvas_lms_enrollment_identifier = models.CharField(max_length=255, blank=True) 
    umd_canvas_lms_enrollment_date = models.DateField(null=True, blank=True)
    #20191205-

    lms_enrollment_identifier = models.CharField(max_length=255, blank=True) 
    lms_enrollment_date = models.DateField(null=True, blank=True)

    is_web_reg = models.BooleanField(default=False, blank=True, help_text='Record submitted through website.')#20170405

    owes_course_fee = models.BooleanField(default=False, blank=True, help_text='Student owes course fee.')#20170823

    registration_approved_by = models.CharField(max_length=255, blank=True, null=True, help_text='Who has approved the application.') #20170615
    registration_approved_by_username = models.CharField(max_length=80, blank=True, null=True, help_text='Username and system for approver.') #20170615
    registration_approved_on = models.DateTimeField(null=True, help_text='Approval Timestamp.') #20170615
    book_fee_acknowledged = models.BooleanField(default=False, help_text='Student has acknowledged book fee at time of registration.')#20170615
    book_fee_agency_pay = models.BooleanField(default=False, help_text='Affiliation agency has affirmed they will pay all book fees at time of approval.')#20170615

#    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
#    lastchange = models.DateTimeField(db_column='LastChange') 
#    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
#    created = models.DateTimeField(db_column='Created') 
    
    def __unicode__(self):
        return u'%s-%s-%s%s-%s %s %s, %s %s' % (self.scheduled_course.course_description.category, self.scheduled_course.course_description.level, self.scheduled_course.funding_source_code, self.scheduled_course.section_number, self.scheduled_course.fiscal_year, self.student_record.lastname, self.student_record.suffix, self.student_record.firstname, self.student_record.middlename)
    
    class Meta:
        db_table = u'StudentRegistration'
        
        verbose_name_plural = "Studentregistrations"
        ordering = ['created']#['student_record.lastname', 'student_record.suffix', 'student_record.firstname', 'student_record.middlename']
        #['created']

    def _has_passed(self):
        "returns the true if the student has passed the class"

        if self.grade.name == u'Passed':
            return True

        return False

    has_passed = property(_has_passed)

    def _ok_to_bill_student(self):
        "returns the true if the student has passed the class"

        if self.has_passed:
            return True

        if (self.status.name == u'Registered') and (self.grade.name == u'Unknown'):
            return True

        return False

    ok_to_bill_student = property(_ok_to_bill_student)

    def _get_full_name(self):
        "returns the student name"

        if not self.student_record:
            return u'No Name'

        return self.student_record.full_name

    name = property(_get_full_name)


    full_name = property(_get_full_name)

    def _full_name_reversed(self):
        "returns the student name reversed"

        if not self.student_record:
            return u'No Name'

        return self.student_record.full_name_reversed

    full_name_reversed = property(_full_name_reversed)

    def _email_address(self):
        "returns the student email address"

        if not self.student_record:
            return u'No email address'

        return self.student_record.primary_email_address

    email_address = property(_email_address)

    def _phone_number(self):
        "returns the student phone number"

        if not self.student_record:
            return u'No Phone Number'

        return self.student_record.primary_phone_number

    phone_number = property(_phone_number)

    def _evoc_practical_vehicle_type(self):
        "returns the evoc practical vehicle type"

        if not self.evoc_vehicle_type:
            return None

        return self.evoc_vehicle_type

    evoc_practical_vehicle_type = property(_evoc_practical_vehicle_type)

    def _evoc_practical_vehicle_type_name(self):
        "returns the evoc practical vehicle type name"

        if not self.evoc_vehicle_type:
            return u''

        return self.evoc_vehicle_type.name

    evoc_practical_vehicle_type_name = property(_evoc_practical_vehicle_type_name)

    def _lms_user_name(self):
        "returns the lms user name"

        if not self.student_record:
            return u''

        if not self.scheduled_course:
            return u''

        if self.scheduled_course.lms_identifier == u'ABS':
            return self.student_record.lms_user_name
        elif self.scheduled_course.lms_identifier == u'UMDCNV':
            return self.student_record.umd_canvas_lms_user_name
        else:
            return u''

        return self.student_record.lms_user_name

    lms_user_name = property(_lms_user_name)

    def _lms_user_account_password(self):
        "returns the lms user account password that is on file. Should only be the initial temporary password."

        if not self.student_record:
            return u''

        if not self.scheduled_course:
            return u''

        if self.scheduled_course.lms_identifier == u'ABS':
            return self.student_record.lms_user_account_password
        elif self.scheduled_course.lms_identifier == u'UMDCNV':
            return self.student_record.umd_canvas_lms_user_account_password
        else:
            return u''
        
        return self.student_record.lms_user_account_password

    lms_user_account_password = property(_lms_user_account_password)

    def _lms_user_account_identifier(self):
        "returns the lms user identifier"

        if not self.student_record:
            return u''

        if not self.scheduled_course:
            return u''

        if self.scheduled_course.lms_identifier == u'ABS':
            return self.student_record.lms_user_account_identifier
        elif self.scheduled_course.lms_identifier == u'UMDCNV':
            return self.student_record.umd_canvas_lms_user_account_identifier
        else:
            return u''
        
        return self.student_record.lms_user_account_identifier

    lms_user_account_identifier = property(_lms_user_account_identifier)

    def _lms_user_name_created_date(self):
        "returns the lms user name creation date"

        if not self.student_record:
            return u''

        if not self.scheduled_course:
            return u''

        if self.scheduled_course.lms_identifier == u'ABS':
            return self.student_record.lms_user_name_created_date
        elif self.scheduled_course.lms_identifier == u'UMDCNV':
            return self.student_record.umd_canvas_lms_user_name_created_date
        else:
            return u''
        
        return self.student_record.lms_user_name_created_date

    lms_user_name_created_date = property(_lms_user_name_created_date)

    def _lms_user_name_created_date_MDY(self):
        "returns the lms user name creation date"

        if not self.student_record:
            return u''

        if not self.scheduled_course:
            return u''

        if self.scheduled_course.lms_identifier == u'ABS':
            if self.student_record.lms_user_name_created_date:
                return self.student_record.lms_user_name_created_date.strftime('%m-%d-%Y')
        elif self.scheduled_course.lms_identifier == u'UMDCNV':
            if self.student_record.umd_canvas_lms_user_name_created_date:
                return self.student_record.umd_canvas_lms_user_name_created_date.strftime('%m-%d-%Y')
        else:
            return u''
        
        if self.student_record.lms_user_name_created_date:
            return self.student_record.lms_user_name_created_date.strftime('%m-%d-%Y')

        return u''

    lms_user_name_created_date_MDY = property(_lms_user_name_created_date_MDY)

    def _get_address(self):
        "returns the address"
        ReturnedAddress = {}

        if not self.student_record: 
            return {'address1':u'', 'address2': u'', 'city': u'', 'state': u'', 'postcode': u'', 'country': u''}

        return self.student_record.address 

    address = property(_get_address)

