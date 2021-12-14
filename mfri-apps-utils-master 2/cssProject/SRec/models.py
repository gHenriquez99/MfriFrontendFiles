import re 
import datetime

from django.conf import settings
from django.db import models, connection
from django.template.defaultfilters import slugify

from AppsAdmin.models import LegacyUsers 
from AppsAdmin.dbk import SRecEncryptKeyS, SRecEncryptKeyE
from AppBase.models import AppBase

from MAffiliations.models import Affiliations

from MOffices.models import MfriOffices, Jurisdictions, Phonenumbertypes
from MESSA.models import Messrcollegeleveltypes, Messrgendertypes, Messrgradeleveltypes, Messrracetypes, Messrtitletypes

def TitleCaseName(name=None, no_title_case=False):
    
    if no_title_case:
        return name
        
    if not name:
        return name

    NAME_MC_RE = re.compile(#r'^[mc|mac]*', re.IGNORECASE)
        r'^mc|^mac'  
        , re.IGNORECASE)  

    try:
        regex_match = NAME_MC_RE.match(name)
        
        if regex_match: 
            regex_match_length = regex_match.end()
            fixed_name = name[:regex_match_length].title() + name[regex_match_length:].title() 
        else:
            fixed_name = name.title()
    except:
        return name

    return fixed_name

class Flagpreferences(models.Model):

    user = models.ForeignKey(LegacyUsers, db_column='UserID', related_name="+")
    
    read_permission = models.IntegerField(null=True, db_column='ReadPermission', blank=True) 
    write_permission = models.IntegerField(null=True, db_column='WritePermission', blank=True) 
    admin_read_permission = models.IntegerField(null=True, db_column='AdminReadPermission', blank=True) 
    admin_write_permission = models.IntegerField(null=True, db_column='AdminWritePermission', blank=True) 

    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 

    class Meta:
        db_table = u'FlagPreferences'
        verbose_name_plural = "Flagpreferences"
        ordering = ['user']

class Flagstatus(models.Model):

    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    class Meta:
        db_table = u'FlagStatus'
        verbose_name_plural = "Flagstatus"
        ordering = ['name']

class Flagtypes(models.Model):

    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    class Meta:
        db_table = u'FlagTypes'
        verbose_name_plural = "Flagtypes"
        ordering = ['name']

class Studentrecordflags(models.Model):

    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    note = models.TextField(db_column='Note', blank=True) 
    flag_type = models.IntegerField(null=True, db_column='TypeID', blank=True) 
    status = models.IntegerField(null=True, db_column='StatusID', blank=True) 

    initial_duration_months = models.IntegerField(null=True, db_column='initial_duration_months', default=6, blank=True) 

    record_status = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 

    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 
    class Meta:
        db_table = u'StudentRecordFlags'
        verbose_name_plural = "Studentrecordflags"
        ordering = ['name']

class Studentflagassignments(models.Model):

    student_record = models.ForeignKey('Studentrecords', db_column='UserID', related_name="+")

    flag = models.ForeignKey(Studentrecordflags, db_column='FlagID', related_name="+")

    expiration_date = models.DateField(null=True, db_column='ExpirationDate', blank=True) 
    assignment_date = models.DateField(null=True, db_column='AssignmentDate', blank=True) 
    note = models.TextField(db_column='Note', blank=True) 
    record_status = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 

    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 
    class Meta:
        db_table = u'StudentFlagAssignments'
        verbose_name_plural = "Studentflagassignments"
        ordering = ['student_record', 'flag', 'assignment_date', 'expiration_date']


class Studentflagstatus(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    class Meta:
        db_table = u'StudentFlagStatus'
        verbose_name_plural = "Studentflagstatuses"
        ordering = ['name']

    def __unicode__(self):
        return '%s' % (self.name)
    

class Studentsbilled(models.Model):

    lastname = models.CharField(max_length=765, db_column='LastName', blank=True) 
    firstname = models.CharField(max_length=765, db_column='FirstName', blank=True) 
    middlename = models.CharField(max_length=765, db_column='MiddleName', blank=True) 
    suffix = models.CharField(max_length=765, db_column='Suffix', blank=True) 
    ssn = models.TextField(db_column='SSN', blank=True) 
    address1 = models.CharField(max_length=765, db_column='Address1', blank=True) 
    address2 = models.CharField(max_length=765, db_column='Address2', blank=True) 
    city = models.CharField(max_length=765, db_column='City', blank=True) 
    state = models.CharField(max_length=765, db_column='State', blank=True) 
    postcode = models.CharField(max_length=765, db_column='PostCode', blank=True) 
    country = models.CharField(max_length=765, db_column='Country', blank=True) 
    recordstatusid = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 

    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 

    class Meta:
        db_table = u'StudentsBilled'
        verbose_name_plural = "StudentsBilled"
        ordering = ['lastname', 'suffix', 'firstname', 'middlename']

    def __unicode__(self):
        return '%s' % (self.name)

class MFRIStudentNumberLookup(models.Model):
    mfri_student_number = models.CharField(max_length=255, blank=True, unique=True)

    ssn = models.BinaryField(db_column='SSN', blank=True, unique=True) 

    class Meta:
        db_table = u'MFRIStudentNumberLookup'
        verbose_name_plural = "MFRIStudentNumberLookups"
        ordering = ['mfri_student_number']

    def __unicode__(self):
        return '%s' % (self.mfri_student_number)

    def _get_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(ssn, %s) as ssn FROM MFRIStudentNumberLookup WHERE id=%s", [SRecEncryptKeyS(), self.id])
        return cursor.fetchone()[0]
   
    def _set_ssn(self, ssn_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as ssn", [ssn_value, SRecEncryptKeyS()])
        self.ssn = cursor.fetchone()[0]

    ssn_clear = property(_get_ssn, _set_ssn)

    def lock(self):
        """ Lock table. 

        Locks the object model table so that atomic update is possible.
        Simulatenous database access request pend until the lock is unlock()'ed.

        Note: If you need to lock multiple tables, you need to do lock them
        all in one SQL clause and this function is not enough. To avoid
        dead lock, all tables must be locked in the same order.

        See http://dev.mysql.com/doc/refman/5.0/en/lock-tables.html
        """
        cursor = connection.cursor()
        table = self._meta.db_table

        cursor.execute("LOCK TABLES %s WRITE" % table)
        row = cursor.fetchone()
        return row

    def unlock(self):
        """ Unlock the table. """
        cursor = connection.cursor()
        table = self._meta.db_table
        cursor.execute("UNLOCK TABLES")
        row = cursor.fetchone()
        return row    

class Studentrecords(models.Model):

    title = models.ForeignKey(Messrtitletypes, db_column='TitleID', blank=True, null=True)

    lastname = models.CharField(max_length=765, db_column='LastName', blank=True) 
    firstname = models.CharField(max_length=765, db_column='FirstName', blank=True) 
    middlename = models.CharField(max_length=765, db_column='MiddleName', blank=True) 
    suffix = models.CharField(max_length=765, db_column='Suffix', blank=True) 

    show_name_as_is = models.BooleanField( blank=True, default=False) 

    affiliation = models.ForeignKey(Affiliations, db_column='AffiliationID')
    
    idnumber = models.BinaryField(db_column='IDNumber', blank=True) 

    ssn = models.BinaryField(db_column='SSN', blank=True) 
    
    universityidnumber = models.BinaryField(db_column='UniversityIDNumber', blank=True) 
    stateprovidernumber = models.BinaryField(db_column='StateProviderNumber', blank=True) 

    nfa_sid_number = models.BinaryField(blank=True) 

    mfri_student_number = models.CharField(max_length=255, blank=True, unique=True) 
    old_mfri_student_number = models.CharField(max_length=255, blank=True) 

    affiliatedcompanynumber = models.CharField(max_length=765, db_column='AffiliatedCompanyNumber', blank=True) 
    birthdate = models.DateField(null=True, db_column='BirthDate', blank=True) 

    gender = models.ForeignKey(Messrgendertypes, db_column='GenderID')

    race = models.ForeignKey(Messrracetypes, db_column='RaceID')

    hispanic = models.BooleanField(db_column='Hispanic', blank=True, default=False)     

    gradelevel = models.ForeignKey(Messrgradeleveltypes, db_column='GradeLevelID')

    collegelevel = models.ForeignKey(Messrcollegeleveltypes, db_column='CollegeLevelID')

    county = models.ForeignKey(Jurisdictions, db_column='CountyID')

    address1 = models.CharField(max_length=765, db_column='Address1', blank=True) 
    address2 = models.CharField(max_length=765, db_column='Address2', blank=True) 
    city = models.CharField(max_length=765, db_column='City', blank=True) 
    state = models.CharField(max_length=765, db_column='State', blank=True) 
    postcode = models.CharField(max_length=765, db_column='PostCode', blank=True) 
    country = models.CharField(max_length=765, db_column='Country', blank=True) 

    primaryphonenumber = models.CharField(max_length=765, db_column='PrimaryPhoneNumber', blank=True) 

    primaryphonenumbertypeid = models.ForeignKey(Phonenumbertypes, db_column='PrimaryPhoneNumberTypeID', related_name="+")

    secondaryphonenumber = models.CharField(max_length=765, db_column='SecondaryPhoneNumber', blank=True) 

    secondaryphonenumbertypeid = models.ForeignKey(Phonenumbertypes, db_column='SecondaryPhoneNumberTypeID', related_name="+")

    email = models.CharField(max_length=765, db_column='Email', blank=True) 
    primaryemail = models.CharField(max_length=765, db_column='PrimaryEmail', blank=True) 
    secondaryemail = models.CharField(max_length=765, db_column='SecondaryEmail', blank=True) 

    note = models.TextField(db_column='Note', blank=True) 

    adaflag = models.BooleanField(db_column='ADAFlag', blank=True, default=False) 
    noshowflag = models.BooleanField(db_column='NoShowFlag', blank=True, default=False) 

    no_bulletin_email = models.BooleanField( blank=True, default=False) 

    studentstatusid = models.ForeignKey('Studentflagstatus', db_column='StudentStatusID')

    recordstatusid = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 

    certificationexpirationdate = models.DateField(null=True, db_column='CertificationExpirationDate', blank=True) 

    umd_canvas_lms_user_name = models.CharField(max_length=255, blank=True) 
    umd_canvas_lms_user_account_password = models.CharField(max_length=255, blank=True) 
    umd_canvas_lms_user_account_identifier = models.CharField(max_length=255, blank=True) 
    umd_canvas_lms_user_name_created_date = models.DateField(null=True, blank=True)

    lms_user_name = models.CharField(max_length=255, blank=True) 
    lms_user_account_password = models.CharField(max_length=255, blank=True) 
    lms_user_account_identifier = models.CharField(max_length=255, blank=True) 
    lms_user_name_created_date = models.DateField(null=True, blank=True)

    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 
    
    class Meta:
        db_table = u'StudentRecords'
        
        verbose_name_plural = "StudentRecords"
        ordering = ['lastname', 'suffix', 'firstname', 'middlename']
        
    def __unicode__(self):
        return u'%s %s, %s %s' % (self.lastname, self.suffix, self.firstname, self.middlename)


    def save(self, **kwargs): 
        current_user = kwargs.pop('user', None)

        self.lastchange = datetime.datetime.now()

        if current_user:
            self.lastchangeby = current_user

        if not self.id:
            self.created = datetime.datetime.now()
            self.lastchange = self.created
            if current_user:
                self.createdby = current_user
         
        super(Studentrecords, self).save(**kwargs)
   
    def _get_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(idnumber, %s) as ssn FROM StudentRecords WHERE id=%s", [SRecEncryptKeyS(), self.id])
        return cursor.fetchone()[0]
   
    def _set_ssn(self, ssn_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as ssn", [ssn_value, SRecEncryptKeyS()])
        self.idnumber = cursor.fetchone()[0]
        self.ssn = self.idnumber 
    
    ssn_clear = property(_get_ssn, _set_ssn)

    def _get_partial_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(idnumber, %s) as ssn FROM StudentRecords WHERE id=%s", [SRecEncryptKeyS(), self.id])
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
        
    def _set_partial_ssn(self, ssn_value):
        padded_ssn = ssn_value.rjust(9,'0')
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as ssn", [padded_ssn, SRecEncryptKeyS()])
        self.idnumber = cursor.fetchone()[0]

    partial_ssn = property(_get_partial_ssn, _set_partial_ssn)
    
    def _get_umid(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(universityidnumber, %s) as universityidnumber FROM StudentRecords WHERE id=%s", [SRecEncryptKeyE(), self.id])
        return cursor.fetchone()[0]
   
    def _set_umid(self, umid_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as universityidnumber", [umid_value, SRecEncryptKeyE()])
        self.universityidnumber = cursor.fetchone()[0]
    
    umid_clear = property(_get_umid, _set_umid)
    
    def _get_epins(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(stateprovidernumber, %s) as epins FROM StudentRecords WHERE id=%s", [SRecEncryptKeyE(), self.id])
        return cursor.fetchone()[0]
   
    def _set_epins(self, epins_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as epins", [epins_value, SRecEncryptKeyE()])
        self.stateprovidernumber = cursor.fetchone()[0]
    
    epins_clear = property(_get_epins, _set_epins)

    def _get_nfa_sid(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(nfa_sid_number, %s) as nfa_sid FROM StudentRecords WHERE id=%s", [SRecEncryptKeyE(), self.id]) 
        return cursor.fetchone()[0]

    def _set_nfa_sid(self, nfa_sid_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as nfa_sid", [nfa_sid_value, SRecEncryptKeyE()]) 
        self.nfa_sid_number = cursor.fetchone()[0]

    nfa_sid = property(_get_nfa_sid, _set_nfa_sid)

    def _get_full_name(self):
        "returns the full name FN MN LN S"
        
        ReturnedName = ''
        if self.firstname and len(self.firstname) > 0:
            ReturnedName += TitleCaseName(self.firstname, no_title_case=self.show_name_as_is) 
    
        if self.middlename and len(self.middlename) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(self.middlename, no_title_case=self.show_name_as_is) 
    
        if self.lastname and len(self.lastname) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(self.lastname, no_title_case=self.show_name_as_is) 
    
        if self.suffix and len(self.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            if self.show_name_as_is:
                ReturnedName += self.suffix
            else:
                ReturnedName += self.suffix.title() 
        
        if self.show_name_as_is:
            return ReturnedName
        else:
            return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')

    def _get_full_name_reversed(self):
        "returns the full name LN S, FN MN"

        ReturnedName = ''
        if self.lastname and len(self.lastname) > 0:
            ReturnedName += TitleCaseName(name=self.lastname, no_title_case=self.show_name_as_is) 

        if self.suffix and len(self.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '

            if self.show_name_as_is:
                ReturnedName += self.suffix
            else:
                ReturnedName += self.suffix.title() 
    
        if len(ReturnedName) > 0:
            ReturnedName += ','
    
        if self.firstname and len(self.firstname) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(name=self.firstname, no_title_case=self.show_name_as_is) 
    
        if self.middlename and len(self.middlename) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += TitleCaseName(name=self.middlename, no_title_case=self.show_name_as_is) 

        if self.show_name_as_is:
            return ReturnedName
        else:
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

    def _get_first_name_title_case(self):
        "returns the title cased first name"

        if self.firstname and len(self.firstname.strip()) > 0:
            return TitleCaseName(name=self.firstname.strip(), no_title_case=self.show_name_as_is) 
    
        return u''
    
    first_name_tc = property(_get_first_name_title_case)

    def _get_middle_name_title_case(self):
        "returns the title cased middle name"

        if self.middlename and len(self.middlename.strip()) > 0:
            return TitleCaseName(name=self.middlename.strip(), no_title_case=self.show_name_as_is)
    
        return u''
    
    middle_name_tc = property(_get_middle_name_title_case)

    def _get_last_name_title_case(self):
        "returns the title cased last name"
        
        if self.lastname and len(self.lastname.strip()) > 0:
            ReturnedName = TitleCaseName(name=self.lastname.strip(), no_title_case=self.show_name_as_is) 
            if self.show_name_as_is:
                return ReturnedName
            else:
                return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')

        return u''
    
    last_name_tc = property(_get_last_name_title_case)

    def _get_suffix_title_case(self):
        "returns the title cased Suffix"
        
        if self.suffix and len(self.suffix.strip()) > 0:
            if self.show_name_as_is:
                return self.suffix.strip()
            else:
                return self.suffix.strip().title().replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')
    
        return u''
        
    suffix_tc = property(_get_suffix_title_case)

    def _get_last_name_and_suffix_title_case(self):
        "returns the title cased last name and Suffix"
        
        ReturnedName = ''
        if self.lastname and len(self.lastname.strip()) > 0:
            ReturnedName += TitleCaseName(name=self.lastname.strip(), no_title_case=self.show_name_as_is) 

        if self.suffix and len(self.suffix.strip()) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '

            if self.show_name_as_is:
                ReturnedName += self.suffix.strip()
            else:
                ReturnedName += self.suffix.strip().title() 

        if self.show_name_as_is:
            return ReturnedName
        else:
            return ReturnedName.replace('Abd ', 'abd ').replace('Abdul ', 'abdul ').replace('Le ', 'le ').replace('La ', 'la ').replace('Da ', 'da ').replace('De ', 'de ').replace('Van ', 'van ').replace('Von ', 'von ').replace('Iiii', 'IIII').replace('Iii', 'III').replace('Ii', 'II')
        
    
    last_name_and_suffix_tc = property(_get_last_name_and_suffix_title_case)

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
    
    def _get_email(self):
        "returns the email addresses"
        ReturnedEmail = {}
        
        if self.primaryemail and (len(self.primaryemail) > 0):
            ReturnedEmail['Primary'] = self.primaryemail.strip()

        if self.secondaryemail and (len(self.secondaryemail) > 0):
            ReturnedEmail['Secondary'] = self.secondaryemail.strip()
        
        if self.email and (len(self.email) > 0):
            self.primaryemail = self.email
            self.save()
            ReturnedEmail['Primary'] = self.email.strip()
        
        return ReturnedEmail

    email_address = property(_get_email)

    def _get_primary_email(self):
        "returns the primary email address or secondary if there is no primary"
        ReturnedEmail = u''

        if self.primaryemail and (len(self.primaryemail) > 0):
            ReturnedEmail = self.primaryemail.strip()
        elif self.secondaryemail and (len(self.secondaryemail) > 0):
            ReturnedEmail = self.secondaryemail.strip()
        elif self.email and (len(self.email) > 0):
            self.primaryemail = self.email
            self.save()
            ReturnedEmail = self.email.strip()

        return ReturnedEmail

    primary_email_address = property(_get_primary_email)
    

    def _get_primary_phone_number(self):
        "returns the primary phone number or secondary if there is no primary"
        ReturnedPhoneNumber = None

        if self.primaryphonenumber and (len(self.primaryphonenumber) > 0):
            ReturnedPhoneNumber = self.primaryphonenumber.strip()
        elif self.secondaryphonenumber and (len(self.secondaryphonenumber) > 0):
            ReturnedPhoneNumber = self.secondaryphonenumber.strip()

        if not ReturnedPhoneNumber:
            return u'No Phone Number'
            
        ReturnedPhoneNumber = ReturnedPhoneNumber.replace('+', '')
        ReturnedPhoneNumber = ReturnedPhoneNumber.replace('(', '')
        ReturnedPhoneNumber = ReturnedPhoneNumber.replace(')', '')
        ReturnedPhoneNumber = ReturnedPhoneNumber.replace(' ', '')
        ReturnedPhoneNumber.replace('+', '')
        ReturnedPhoneNumber = ReturnedPhoneNumber.replace('-', '')

        if len(ReturnedPhoneNumber) <= 7:
            exchange = ReturnedPhoneNumber[:3]
            number = ReturnedPhoneNumber[3:]
            ReturnedPhoneNumber = u'%s-%s' % (exchange, number)
        elif len(ReturnedPhoneNumber) == 10:
            area_code = ReturnedPhoneNumber[:3]
            exchange = ReturnedPhoneNumber[3:6]
            number = ReturnedPhoneNumber[6:]
            ReturnedPhoneNumber = u'%s-%s-%s' % (area_code, exchange, number)
        elif len(ReturnedPhoneNumber) == 11 and ReturnedPhoneNumber[:1] == '1':
            country_code = ReturnedPhoneNumber[:1]
            area_code = ReturnedPhoneNumber[1:4]
            exchange = ReturnedPhoneNumber[4:7]
            number = ReturnedPhoneNumber[7:]
            ReturnedPhoneNumber = u'%s-%s-%s' % (area_code, exchange, number)
        
        return ReturnedPhoneNumber

    primary_phone_number = property(_get_primary_phone_number)
    
    def _get_birth_date(self): 
        return self.birthdate
   
    def _set_birth_date(self, birth_date_value):
        self.birthdate = birth_date_value
    
    birth_date = property(_get_birth_date, _set_birth_date)
    
    def _age(self):

        if not self.birthdate:
            return 0
        
        today = datetime.datetime.today()
        
        try:
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        except:
            return 0

        return 0

    age = property(_age)
    
    def lock(self):
        """ Lock table. 

        Locks the object model table so that atomic update is possible.
        Simulatenous database access request pend until the lock is unlock()'ed.

        Note: If you need to lock multiple tables, you need to do lock them
        all in one SQL clause and this function is not enough. To avoid
        dead lock, all tables must be locked in the same order.

        See http://dev.mysql.com/doc/refman/5.0/en/lock-tables.html
        """
        cursor = connection.cursor()
        table = self._meta.db_table

        cursor.execute("LOCK TABLES %s WRITE" % table)
        row = cursor.fetchone()
        return row

    def unlock(self):
        """ Unlock the table. """
        cursor = connection.cursor()
        table = self._meta.db_table
        cursor.execute("UNLOCK TABLES")
        row = cursor.fetchone()
        return row    

   
