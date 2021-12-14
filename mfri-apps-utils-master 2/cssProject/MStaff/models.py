import datetime

from django.contrib.auth.models import User 
from django.db import models, connection

from AppsAdmin.dbk import StaffEncryptKeyU, StaffEncryptKeyS

from AppBase.models import AppBase, unique_slugify

from AppLegacyBase.models import AppLegacyBase 

from MOffices.models import MfriOffices, Jurisdictions, LegacyCoursesection, LegacyMfriregions, Phonenumbertypes

from MFRI_Utils.data_validate import valid_suffix_values

class Instructorpayratefactors(models.Model):
    value = models.DecimalField(null=True, max_digits=3, decimal_places=2, db_column='Value', blank=True)  #max_digits=10

    def __unicode__(self):
        return u'%.2f' % (self.value)

    class Meta:
        db_table = u'InstructorPayRateFactors'
        verbose_name_plural = "Instructorpayratefactors"
        ordering = ['value']

class Instructorpayrates(models.Model):
    value = models.DecimalField(null=True, max_digits=5, decimal_places=2, db_column='Value', blank=True)  #max_digits=10
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        return u'%.2f' % (self.value)

    class Meta:
        db_table = u'InstructorPayRates'
        verbose_name_plural = "InstructorPayRates"
        ordering = ['value']



class Employmentstatus(models.Model):

    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Employmentstatus"
        db_table = u'EmploymentStatus'
        ordering = ['id']

class Positioncategories(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "PositionCategories"
        db_table = u'PositionCategories'
        ordering = ['id']

class MfriInstructorsManager(models.Manager):
    def by_uid_lastname(self, uid, lastname):
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM MfriInstructors WHERE (AES_DECRYPT(UniversityIDNumber, %s) like %s) AND (LastName like %s)", [StaffEncryptKeyU(), uid, lastname])
        
        row = cursor.fetchone()
        
        record_found = self.model(id=row[0])

        return record_found

    def CurrentEmployees(self, homeoffice=None): 

        if not homeoffice:
            return self.filter().exclude(employmentstatus__in=(1, 6, 7))

        return self.filter(homeoffice__exact=homeoffice).exclude(employmentstatus__in=(1, 6, 7))

class MfriInstructors(models.Model):
    titleid = models.IntegerField(null=True, db_column='TitleID', blank=True) 
    firstname = models.CharField(max_length=765, db_column='FirstName', blank=True) 
    middlename = models.CharField(max_length=765, db_column='MiddleName', blank=True) 
    lastname = models.CharField(max_length=765, db_column='LastName', blank=True) 
    suffix = models.CharField(max_length=765, db_column='Suffix', blank=True) 
    nickname = models.CharField(max_length=765, db_column='NickName', blank=True) 
    shownickname = models.IntegerField(null=True, db_column='ShowNickName', blank=True) 
    showname = models.IntegerField(null=True, db_column='ShowName', blank=True) 

    internal_name_note = models.CharField(max_length=765, help_text='Internal note for name changes.', blank=True, null=True) 
    show_name_as_is = models.BooleanField( blank=True, default=True) 
    no_bulletin_email = models.BooleanField( blank=True, default=False) 
    no_marketing_email = models.BooleanField( blank=True, default=False) 

    public_first_name = models.CharField(max_length=765, db_column='public_first_name', blank=True) 
    public_middle_name = models.CharField(max_length=765, db_column='public_middle_name', blank=True) 
    public_last_name = models.CharField(max_length=765, db_column='public_last_name', blank=True) 
    public_suffix = models.CharField(max_length=765, db_column='public_suffix', blank=True) 
    use_public_name = models.BooleanField(default=False, help_text='Use Public Name when displaying record')

    ssn = models.CharField(max_length=765, db_column='SSN', blank=True) 
    
    universityidnumber = models.BinaryField(db_column='UniversityIDNumber', blank=True) 
    
    birthdate = models.DateField(null=True, db_column='BirthDate', blank=True) 
    medicalexamrequired = models.IntegerField(null=True, db_column='MedicalExamRequired', blank=True) 

    no_medical_exam_suspended = models.IntegerField(default=False, null=True, db_column='no_medical_exam_suspended', blank=True) 

    stateprovidernumber = models.BinaryField(db_column='StateProviderNumber', blank=True) 
    driverslicensenumber = models.BinaryField(db_column='DriversLicenseNumber', blank=True) 
    driverslicensestate = models.CharField(max_length=765, db_column='DriversLicenseState', blank=True) 
    driverslicensecommercial = models.IntegerField(null=True, db_column='DriversLicenseCommercial', blank=True) 
    driverslicenseclass = models.CharField(max_length=765, db_column='DriversLicenseClass', blank=True) 
    driverslicenseendorsement = models.CharField(max_length=765, db_column='DriversLicenseEndorsement', blank=True) 
    driverslicenserestriction = models.CharField(max_length=765, db_column='DriversLicenseRestriction', blank=True) 
    driverslicensepoints = models.BinaryField(db_column='DriversLicensePoints', blank=True) 
    driverslicensetypeid = models.CharField(max_length=765, db_column='DriversLicenseTypeID', blank=True) 
    driverslicenseexpirationdate = models.DateField(null=True, db_column='DriversLicenseExpirationDate', blank=True) 
    passportnumber = models.CharField(max_length=765, db_column='PassportNumber', blank=True) 
    passportexpirationdate = models.DateField(null=True, db_column='PassportExpirationDate', blank=True) 
    
    county = models.ForeignKey(Jurisdictions, db_column='CountyID')
        
    showcounty = models.IntegerField(null=True, db_column='ShowCountyID', blank=True) 
    address1 = models.CharField(max_length=765, db_column='Address1', blank=True) 
    address2 = models.CharField(max_length=765, db_column='Address2', blank=True) 
    showaddress = models.IntegerField(null=True, db_column='ShowAddress', blank=True) 
    city = models.CharField(max_length=765, db_column='City', blank=True) 
    showcity = models.IntegerField(null=True, db_column='ShowCity', blank=True) 
    state = models.CharField(max_length=765, db_column='State', blank=True) 
    showstate = models.IntegerField(null=True, db_column='ShowState', blank=True) 
    postcode = models.CharField(max_length=96, db_column='PostCode', blank=True) 
    showpostcode = models.IntegerField(null=True, db_column='ShowPostCode', blank=True) 
    country = models.CharField(max_length=765, db_column='Country', blank=True) 
    showcountry = models.IntegerField(null=True, db_column='ShowCountry', blank=True) 

    primaryphonenumbertypeid = models.ForeignKey(Phonenumbertypes, db_column='PrimaryPhoneNumberTypeID', related_name="+")

    primaryphonenumber = models.CharField(max_length=96, db_column='PrimaryPhoneNumber', blank=True) 
    showprimaryphonenumber = models.IntegerField(null=True, db_column='ShowPrimaryPhoneNumber', blank=True) 
    
    secondaryphonenumbertypeid = models.ForeignKey(Phonenumbertypes, db_column='SecondaryPhoneNumberTypeID', related_name="+")
        
    secondaryphonenumber = models.CharField(max_length=96, db_column='SecondaryPhoneNumber', blank=True) 
    showsecondaryphonenumber = models.IntegerField(null=True, db_column='ShowSecondaryPhoneNumber', blank=True) 
    
    alternate1phonenumbertypeid = models.ForeignKey(Phonenumbertypes, db_column='Alternate1PhoneNumberTypeID', related_name="+")

    alternate1phonenumber = models.CharField(max_length=96, db_column='Alternate1PhoneNumber', blank=True) 
    showalternate1phonenumber = models.IntegerField(null=True, db_column='ShowAlternate1PhoneNumber', blank=True) 

    alternate2phonenumbertypeid = models.ForeignKey(Phonenumbertypes, db_column='Alternate2PhoneNumberTypeID', related_name="+")

    alternate2phonenumber = models.CharField(max_length=96, db_column='Alternate2PhoneNumber', blank=True) 

    alternate3phonenumbertypeid = models.ForeignKey(Phonenumbertypes, db_column='Alternate3PhoneNumberTypeID', related_name="+")

    alternate3phonenumber = models.CharField(max_length=96, db_column='Alternate3PhoneNumber', blank=True) 

    alternate4phonenumbertypeid = models.ForeignKey(Phonenumbertypes, db_column='Alternate4PhoneNumberTypeID', related_name="+")

    alternate4phonenumber = models.CharField(max_length=96, db_column='Alternate4PhoneNumber', blank=True) 
    showalternate4phonenumber = models.IntegerField(null=True, db_column='ShowAlternate4PhoneNumber', blank=True) 
    showalternate3phonenumber = models.IntegerField(null=True, db_column='ShowAlternate3PhoneNumber', blank=True) 
    showalternate2phonenumber = models.IntegerField(null=True, db_column='ShowAlternate2PhoneNumber', blank=True) 

    mfri_primary_phone_number = models.CharField(max_length=96, db_column='mfri_primary_phone_number', blank=True) 
    mfri_secondary_phone_number = models.CharField(max_length=96, db_column='mfri_secondary_phone_number', blank=True) 

    show_mfri_primary_phone_number = models.BooleanField(default=True, help_text='(Show on public directory)')
    show_mfri_secondary_phone_number = models.BooleanField(default=True, help_text='(Show on public directory)')

    mfri_email = models.CharField(max_length=765, db_column='mfri_email', null=True, blank=True, help_text='MFRI assigned email address') 
    umd_directory = models.CharField(max_length=765, db_column='umd_directory', null=True, blank=True, help_text='UMD Directory ID')  
    umd_email = models.CharField(max_length=765, db_column='umd_email', null=True, blank=True, help_text='UMD assigned email address')  

    primaryemail = models.CharField(max_length=765, db_column='PrimaryEmail', blank=True) 
    showprimaryemail = models.IntegerField(null=True, db_column='ShowPrimaryEmail', blank=True) 
    secondaryemail = models.CharField(max_length=765, db_column='SecondaryEmail', blank=True) 

    alternateaddress1 = models.CharField(max_length=765, db_column='AlternateAddress1', blank=True) 
    alternateaddress2 = models.CharField(max_length=765, db_column='AlternateAddress2', blank=True) 
    showalternateaddress = models.IntegerField(null=True, db_column='ShowAlternateAddress', blank=True) 
    alternatecity = models.CharField(max_length=765, db_column='AlternateCity', blank=True) 
    showalternatecity = models.IntegerField(null=True, db_column='ShowAlternateCity', blank=True) 
    alternatestate = models.CharField(max_length=765, db_column='AlternateState', blank=True) 
    showalternatestate = models.IntegerField(null=True, db_column='ShowAlternateState', blank=True) 
    alternatepostcode = models.CharField(max_length=96, db_column='AlternatePostCode', blank=True) 
    alternatecountry = models.CharField(max_length=765, db_column='AlternateCountry', blank=True) 

    showsecondaryemail = models.IntegerField(null=True, db_column='ShowSecondaryEmail', blank=True) 
    
    homeoffice = models.ForeignKey(MfriOffices, db_column='HomeOfficeID')
    
    directsupervisorid = models.IntegerField(null=True, db_column='DirectSupervisorID', blank=True) 
    
    showhomeoffice = models.IntegerField(null=True, db_column='ShowHomeOfficeID', blank=True) 

    employmentstatus = models.ForeignKey(Employmentstatus, db_column='EmploymentStatusID')

    positioncategory = models.ForeignKey(Positioncategories, db_column='PositionCategoryID')
    
    
    is_instructor = models.BooleanField(default=False, db_column='IsInstructor', help_text='This staffer is an instructor.')
        
    hiredate = models.DateField(null=True, db_column='HireDate', blank=True) 
    adjustedservicedate = models.DateField(null=True, db_column='AdjustedServiceDate', blank=True) 
    separationdate = models.DateField(null=True, db_column='SeparationDate', blank=True) 
    lastphysicalexamid = models.IntegerField(null=True, db_column='LastPhysicalExamID', blank=True) 
    lastphysicalexamdate = models.DateField(null=True, db_column='LastPhysicalExamDate', blank=True) 

    hourlyrate = models.ForeignKey(Instructorpayrates, db_column='hourlyrateid')

    hourlyratefactor = models.ForeignKey(Instructorpayratefactors, db_column='hourlyratefactorid')

    leave_balance = models.DecimalField(blank=True, decimal_places=2, max_digits=6, default=0.00, help_text='Sick and Safe Leave Balance.') #20190516

    facultyannualleave = models.FloatField(null=True, db_column='FacultyAnnualLeave', blank=True) 
    facultysickleave = models.FloatField(null=True, db_column='FacultySickLeave', blank=True) 
    facultypersonalleave = models.FloatField(null=True, db_column='FacultyPersonalLeave', blank=True) 
    facultymilitaryleave = models.FloatField(null=True, db_column='FacultyMilitaryLeave', blank=True) 
    facultynonpaidleave = models.FloatField(null=True, db_column='FacultyNonPaidLeave', blank=True) 
    facultyimmediatefamilysickleave = models.FloatField(null=True, db_column='FacultyImmediateFamilySickLeave', blank=True) 
    facultyofficialholidayleave = models.IntegerField(null=True, db_column='FacultyOfficialHolidayLeave', blank=True) 
    employmentacknowledgementdate = models.DateField(null=True, db_column='EmploymentAcknowledgementDate', blank=True) 
    totalinstructionalhours = models.IntegerField(null=True, db_column='TotalInstructionalHours', blank=True) 
    pdihours = models.IntegerField(null=True, db_column='PDIHours', blank=True) 
    practiceteaching1evaluationdate = models.DateField(null=True, db_column='PracticeTeaching1EvaluationDate', blank=True) 
    practiceteaching2evaluationdate = models.DateField(null=True, db_column='PracticeTeaching2EvaluationDate', blank=True) 
    interimevaluation1date = models.DateField(null=True, db_column='InterimEvaluation1Date', blank=True) 
    interimevaluation2date = models.DateField(null=True, db_column='InterimEvaluation2Date', blank=True) 
    routineevaluationdate = models.DateField(null=True, db_column='RoutineEvaluationDate', blank=True) 
    instructortrainerdate = models.DateField(null=True, db_column='InstructorTrainerDate', blank=True) 
    micrbevaluatordate = models.DateField(null=True, db_column='MICRBEvaluatorDate', blank=True) 
    micrbcertificationdate = models.DateField(null=True, db_column='MICRBCertificationDate', blank=True) 
    micrbid = models.IntegerField(null=True, db_column='MicrbID', blank=True) 
    totalotherhours = models.IntegerField(null=True, db_column='TotalOtherHours', blank=True) 
    recordstatusid = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 

    umd_canvas_lms_user_name = models.CharField(max_length=255, blank=True) 
    umd_canvas_lms_user_account_password = models.CharField(max_length=255, blank=True) 
    umd_canvas_lms_user_account_identifier = models.CharField(max_length=255, blank=True) 
    umd_canvas_lms_user_name_created_date = models.DateField(null=True, blank=True)

    lms_user_name = models.CharField(max_length=255, blank=True) 
    lms_user_account_password = models.CharField(max_length=255, blank=True) 
    lms_user_account_identifier = models.CharField(max_length=255, blank=True) 
    lms_user_name_created_date = models.DateField(null=True, blank=True)

    objects = MfriInstructorsManager()
    
    def __unicode__(self):
        return self.name_reversed 

    def _get_university_id(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(universityidnumber, %s) as uid FROM MfriInstructors WHERE id=%s", [StaffEncryptKeyU(), self.id])
        return cursor.fetchone()[0]
    
    def _set_university_id(self, uid_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as uid", [uid_value, StaffEncryptKeyU()])
        self.universityidnumber = cursor.fetchone()[0]
    
    uid = property(_get_university_id, _set_university_id)

    def _get_full_name(self):
        "returns the full name FN MN LN S"

        ReturnedName = u''
        if self.firstname and (len(self.firstname) > 0):
            ReturnedName += u'%s' % (self.firstname)

        if self.middlename and (len(self.middlename) > 0):
            if len(ReturnedName) > 0:
                ReturnedName += u' '
                
            ReturnedName += u'%s' % (self.middlename)
            
        if self.lastname and (len(self.lastname) > 0):
            if len(ReturnedName) > 0:
                ReturnedName += u' '

            ReturnedName += u'%s' % (self.lastname)

        if self.suffix and (len(self.suffix) > 0):
            if len(ReturnedName) > 0:
                ReturnedName += u' '

            ReturnedName += u'%s' % (self.suffix)
        
        return ReturnedName

    def _get_full_name_reversed(self):
        "returns the full name LN S, FN MN"
        ReturnedName = u''
        if self.lastname and (len(self.lastname) > 0):
            ReturnedName += u'%s' % (self.lastname)
            
        if self.suffix and (len(self.suffix) > 0):
            if len(ReturnedName) > 0:
                ReturnedName += u' '
            
            ReturnedName += u'%s' % (self.suffix)

        if len(ReturnedName) > 0:
            ReturnedName += u','
        
        if self.firstname and (len(self.firstname) > 0):
            if len(ReturnedName) > 0:
                ReturnedName += u' '

            ReturnedName += u'%s' % (self.firstname)

        if len(self.middlename) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += u' '
            
            if self.middlename:
                ReturnedName += u'%s' % (self.middlename)
            
        
        return ReturnedName
    
    full_name_reversed = property(_get_full_name_reversed)
    
    def _set_full_name(self, RawFullName):
        "sets name parts with the given full name"
        NewFullName = RawFullName.strip()

        SuffixValues = valid_suffix_values() 

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

        if len(self.lastname) == 0:
            if len(self.middlename) > 0:
                self.lastname = self.middlename
                self.middlename = u''
            else:
                self.lastname = self.firstname
                self.firstname = u''


    full_name = property(_get_full_name, _set_full_name)

    def _get_name(self):
        "returns the full name or the public name"
        ReturnedName = u''

        if self.use_public_name:
            if not (self.public_first_name or self.public_middle_name or self.public_last_name):
                return u'%s' % (self.full_name)
            
            if self.public_first_name and (len(self.public_first_name) > 0):
                ReturnedName += u'%s' % (self.public_first_name)

            if self.shownickname and self.nickname and (len(self.nickname) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '

                ReturnedName += u'"%s"' % (self.nickname)
            else:    
                if self.public_middle_name and (len(self.public_middle_name) > 0):
                    if len(ReturnedName) > 0:
                        ReturnedName += u' '

                    ReturnedName += u'"%s"' % (self.nickname)

            if self.public_last_name and (len(self.public_last_name) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '

                ReturnedName += u'%s' % (self.public_last_name)

            if self.public_suffix and (len(self.public_suffix) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '

                ReturnedName += u'%s' % (self.public_suffix)
        else:    
            if self.firstname and (len(self.firstname) > 0):
                ReturnedName += u'%s' % (self.firstname)

            if self.shownickname and self.nickname and (len(self.nickname) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '

                ReturnedName += u'"%s"' % (self.nickname)
            else:
                if self.middlename and (len(self.middlename) > 0):
                    if len(ReturnedName) > 0:
                        ReturnedName += u' '
                    
                    ReturnedName += u'%s' % (self.middlename)
                
            if self.lastname and (len(self.lastname) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
            
                ReturnedName += u'%s' % (self.lastname)
            
            if self.suffix and (len(self.suffix) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
            
                ReturnedName += u'%s' % (self.suffix)
        
        return ReturnedName

    name = property(_get_name)

    def _short_name(self):
        "returns the full name or the public name with the nickname instead of first name"
        ReturnedName = u''

        if self.use_public_name:
            if not (self.public_first_name or self.public_middle_name or self.public_last_name):
                return u'%s' % (self.full_name)
            
            if self.shownickname and self.nickname and (len(self.nickname) > 0):
                ReturnedName += u'%s' % (self.nickname)
            else:
                if self.public_first_name and (len(self.public_first_name) > 0):
                    ReturnedName += u'%s' % (self.public_first_name)

            if self.public_last_name and (len(self.public_last_name) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '

                ReturnedName += u'%s' % (self.public_last_name)

            if self.public_suffix and (len(self.public_suffix) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '

                ReturnedName += u'%s' % (self.public_suffix)
        else:    

            if self.shownickname and self.nickname and (len(self.nickname) > 0):
                ReturnedName += u'%s' % (self.nickname)
            else:
                if self.firstname and (len(self.firstname) > 0):
                    ReturnedName += u'%s' % (self.firstname)

            if self.lastname and (len(self.lastname) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
            
                ReturnedName += u'%s' % (self.lastname)
            
            if self.suffix and (len(self.suffix) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
            
                ReturnedName += u'%s' % (self.suffix)
        
        return ReturnedName

    short_name = property(_short_name)
    
    def _get_name_parts(self):
        "returns the full name or the public name"
        first_name = None
        middle_name = None
        nick_name = None
        last_name = None
        suffix = None

        if self.use_public_name and (self.public_first_name or self.public_middle_name or self.public_last_name):

            if self.public_first_name and (len(self.public_first_name) > 0):
                first_name = self.public_first_name

            if self.shownickname and self.nickname and (len(self.nickname) > 0):
                nick_name = self.nickname
            
            if self.public_middle_name and (len(self.public_middle_name) > 0):
                middle_name = self.public_middle_name

            if self.public_last_name and (len(self.public_last_name) > 0):
                last_name = self.public_last_name
                
            if self.public_suffix and (len(self.public_suffix) > 0):
                suffix = self.public_suffix
        else:    
            if self.firstname and (len(self.firstname) > 0):
                first_name = self.firstname

            if self.shownickname and self.nickname and (len(self.nickname) > 0):
                nick_name = self.nickname

            if self.middlename and (len(self.middlename) > 0):
                middle_name = self.middlename
                
            if self.lastname and (len(self.lastname) > 0):
                last_name = self.lastname
            
            if self.suffix and (len(self.suffix) > 0):
                suffix = self.suffix
        
        return {'first_name': first_name, 'nick_name': nick_name, 'middle_name': middle_name, 'last_name': last_name, 'suffix': suffix}

    name_parts = property(_get_name_parts)

    def _get_name_reversed(self):
        "returns the full name or public name"

        ReturnedName = u''
        
        if self.use_public_name:        
            if not (self.public_first_name or self.public_middle_name or self.public_last_name):
                return full_name_reversed
            
            if self.public_last_name and (len(self.public_last_name) > 0):
                ReturnedName += u'%s' % (self.public_last_name)
        
            if self.public_suffix and (len(self.public_suffix) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
        
                ReturnedName += u'%s' % (self.public_suffix)
        
            if len(ReturnedName) > 0:
                ReturnedName += u','
        
            if self.public_first_name and (len(self.public_first_name) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
        
                ReturnedName += u'%s' % (self.public_first_name)
        
            if self.shownickname and self.nickname and (len(self.nickname) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
        
                ReturnedName += u'"%s"' % (self.nickname)
            else:    
                if self.public_middle_name and (len(self.public_middle_name) > 0):
                    if len(ReturnedName) > 0:
                        ReturnedName += u' '
        
                    ReturnedName += u'%s' % (self.public_middle_name)
        else:
            if self.lastname and (len(self.lastname) > 0):
                ReturnedName += u'%s' % (self.lastname)
                
            if self.suffix and (len(self.suffix) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
                
                ReturnedName += self.suffix
            
            if len(ReturnedName) > 0:
                ReturnedName += u','
            
            if self.firstname and (len(self.firstname) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
            
                ReturnedName += u'%s' % (self.firstname)
        
            if self.shownickname and self.nickname and (len(self.nickname) > 0):
                if len(ReturnedName) > 0:
                    ReturnedName += u' '
        
                ReturnedName += u'"%s"' % (self.nickname)
            else:
                if self.middlename and (len(self.middlename) > 0):
                    if len(ReturnedName) > 0:
                        ReturnedName += u' '
                    
                    ReturnedName += u'%s' % (self.middlename)
        
        return u'%s' % (ReturnedName)
    
    name_reversed = property(_get_name_reversed)

    def _get_private_address_line(self):
        "returns the address"
        ReturnedAddress = u''

        if self.showaddress:
            if self.address1 and (len(self.address1) > 0):
                ReturnedAddress += u'%s' % (self.address1)

            if self.address2 and (len(self.address2) > 0):
                if len(ReturnedAddress) > 0:
                    ReturnedAddress += u' '

                ReturnedAddress += u'%s' % (self.address2)

        if self.showcity:
            if self.city and (len(self.city) > 0):
                if len(ReturnedAddress) > 0:
                    ReturnedAddress += u' '
                    
                ReturnedAddress += u'%s' % (self.city)
                
        if self.showstate and (len(self.state) > 0): # and self.state.upper() != 'MD':
                if len(ReturnedAddress) > 0:
                    ReturnedAddress += u' '
            
                ReturnedAddress += u'%s' % (self.state.upper())
        
        if self.showpostcode and (len(self.postcode) > 0): #showpostcode doesn't seem to be used
                if len(ReturnedAddress) > 0:
                    ReturnedAddress += u' '
            
                ReturnedAddress += u'%s' % (self.postcode.upper())

        if self.showcountry and (len(self.country) > 0) and self.country.upper() != 'USA' and self.country.upper() != 'US':
                if len(ReturnedAddress) > 0:
                    ReturnedAddress += u' '
            
                ReturnedAddress += u'%s' % (self.country.upper())
        
        return ReturnedAddress

    private_address_line = property(_get_private_address_line)

    def _get_private_address(self):
        "returns the address"
        ReturnedAddress = {}

        if self.showaddress:
            if self.address1 and (len(self.address1) > 0):
                ReturnedAddress['address1'] = u'%s' % (self.address1)

            if self.address2 and (len(self.address2) > 0):
                ReturnedAddress['address2'] = u'%s' % (self.address2)

        if self.showcity:
            if self.city and (len(self.city) > 0):
                ReturnedAddress['city'] = u'%s' % (self.city)
                
        if self.showstate and (len(self.state) > 0): # and self.state.upper() != 'MD':
                ReturnedAddress['state'] = u'%s' % (self.state.upper())
        
        if self.showpostcode and (len(self.postcode) > 0): #showpostcode doesn't seem to be used
                ReturnedAddress['postcode'] = u'%s' % (self.postcode.upper())

        if self.showcountry and (len(self.country) > 0) and self.country.upper() != 'USA' and self.country.upper() != 'US':
                ReturnedAddress['country'] = u'%s' % (self.country.upper())
        
        return ReturnedAddress

    private_address = property(_get_private_address)
    
    def _get_private_phone_line(self):
        "returns the phone numbers"
        ReturnedPhone = u''

        if self.showprimaryphonenumber:
            if self.primaryphonenumber and (len(self.primaryphonenumber) > 0):
                ReturnedPhone += u'%s: %s' % (self.primaryphonenumbertypeid.name, self.primaryphonenumber)

        if self.showsecondaryphonenumber:
            if self.secondaryphonenumber and (len(self.secondaryphonenumber) > 0):
                if len(ReturnedPhone) > 0:
                    ReturnedPhone += u' '
                    
                ReturnedPhone += u'%s: %s' % (self.secondaryphonenumbertypeid.name, self.secondaryphonenumber)
                
        if self.showalternate1phonenumber:
            if self.alternate1phonenumber and (len(self.alternate1phonenumber) > 0):
                if len(ReturnedPhone) > 0:
                    ReturnedPhone += u' '
            
                ReturnedPhone += u'%s: %s' % (self.alternate1phonenumbertypeid.name, self.alternate1phonenumber)
        
        if self.showalternate2phonenumber:
            if self.alternate2phonenumber and (len(self.alternate2phonenumber) > 0):
                if len(ReturnedPhone) > 0:
                    ReturnedPhone += u' '
            
                ReturnedPhone += u'%s: %s' % (self.alternate2phonenumbertypeid.name, self.alternate2phonenumber)

        if self.showalternate3phonenumber:
            if self.alternate3phonenumber and (len(self.alternate3phonenumber) > 0):
                if len(ReturnedPhone) > 0:
                    ReturnedPhone += u' '
            
                ReturnedPhone += u'%s: %s' % (self.alternate3phonenumbertypeid.name, self.alternate3phonenumber)

        if self.showalternate4phonenumber:
            if self.alternate4phonenumber and (len(self.alternate4phonenumber) > 0):
                if len(ReturnedPhone) > 0:
                    ReturnedPhone += u' '
            
                ReturnedPhone += u'%s: %s' % (self.alternate4phonenumbertypeid.name, self.alternate4phonenumber)
        
        
        return ReturnedPhone

    private_phone_line = property(_get_private_phone_line)

    def _get_private_phone(self):
        "returns the phone numbers"
        ReturnedPhone = {}
        
        key_name = u''
        if self.showprimaryphonenumber:
            if self.primaryphonenumber and (len(self.primaryphonenumber) > 0):
                if len(self.primaryphonenumbertypeid.name.strip()) > 0:
                    key_name = self.primaryphonenumbertypeid.name.strip()
                else:
                    key_name = u'Primary'
            
                ReturnedPhone[key_name] = u'%s' % (self.primaryphonenumber)

        if self.showsecondaryphonenumber:
            if self.secondaryphonenumber and (len(self.secondaryphonenumber) > 0):
                if len(self.secondaryphonenumbertypeid.name.strip()) > 0:
                    key_name = self.secondaryphonenumbertypeid.name.strip()
                else:
                    key_name = u'Secondary'
            
                ReturnedPhone[key_name] = u'%s' % (self.secondaryphonenumber)
                
        if self.showalternate1phonenumber:
            if self.alternate1phonenumber and (len(self.alternate1phonenumber) > 0):
                if len(self.alternate1phonenumbertypeid.name.strip()) > 0:
                    key_name = self.alternate1phonenumbertypeid.name.strip()
                else:
                    key_name = u'Alternate 1'
            
                ReturnedPhone[key_name] = u'%s' % (self.alternate1phonenumber)
        
        if self.showalternate2phonenumber:
            if self.alternate2phonenumber and (len(self.alternate2phonenumber) > 0):
                if len(self.alternate2phonenumbertypeid.name.strip()) > 0:
                    key_name = self.alternate2phonenumbertypeid.name.strip()
                else:
                    key_name = u'Alternate 2'
            
                ReturnedPhone[key_name] = u'%s' % (self.alternate2phonenumber)

        if self.showalternate3phonenumber:
            if self.alternate3phonenumber and (len(self.alternate3phonenumber) > 0):
                if len(self.alternate3phonenumbertypeid.name.strip()) > 0:
                    key_name = self.alternate3phonenumbertypeid.name.strip()
                else:
                    key_name = u'Alternate 3'
            
                ReturnedPhone[key_name] = u'%s' % (self.alternate3phonenumber)

        if self.showalternate4phonenumber:
            if self.alternate4phonenumber and (len(self.alternate4phonenumber) > 0):
                if len(self.alternate4phonenumbertypeid.name.strip()) > 0:
                    key_name = self.alternate4phonenumbertypeid.name.strip()
                else:
                    key_name = u'Alternate 4'
            
                ReturnedPhone[key_name] =  u'%s' % (self.alternate4phonenumber)
        
        
        return ReturnedPhone

    private_phone = property(_get_private_phone)

    def _get_official_street_address(self):
        "returns the official MFRI street addresses"

        if not self.is_employment_current:
            return {}

        if not self.homeoffice:
            return {}

        return self.homeoffice.street_address

    official_street_address = property(_get_official_street_address)

    def _get_official_mailing_address(self):
        "returns the official MFRI street addresses"

        if not self.is_employment_current:
            return {}

        if not self.homeoffice:
            return {}

        return self.homeoffice.mailing_address

    official_mailing_address = property(_get_official_mailing_address)
    
    def _get_official_phone(self):
        "returns the official phone numbers"
        
        if not self.is_employment_current:
            return {}
        
        ReturnedPhone = {}


        if self.show_mfri_primary_phone_number:
            if self.mfri_primary_phone_number and (len(self.mfri_primary_phone_number) > 0):
                ReturnedPhone['Primary'] = u'%s' % (self.mfri_primary_phone_number)

        if self.show_mfri_secondary_phone_number:
            if self.mfri_secondary_phone_number and (len(self.mfri_secondary_phone_number) > 0):
                ReturnedPhone['Secondary'] = u'%s' % (self.mfri_secondary_phone_number)


        return ReturnedPhone

    official_phone = property(_get_official_phone)

    def _get_private_email_line(self):
        "returns the email addresses"
        ReturnedEmail = u''

        if self.showprimaryemail:
            if self.primaryemail and (len(self.primaryemail) > 0):
                ReturnedEmail += u'%s' % (self.primaryemail)
                

        if self.showsecondaryemail:
            if self.secondaryemail and (len(self.secondaryemail) > 0):
                if len(ReturnedEmail) > 0:
                    ReturnedEmail += u' '
                    
                ReturnedEmail += u'%s' % (self.secondaryemail)
                
        
        return ReturnedEmail

    private_email_line = property(_get_private_email_line)
    
    def _get_private_email(self):
        "returns the email addresses"
        ReturnedEmail = {}

        if self.showprimaryemail:
            if self.primaryemail and (len(self.primaryemail) > 0):
                ReturnedEmail['Primary'] = u'%s' % (self.primaryemail.strip())

        if self.showsecondaryemail:
            if self.secondaryemail and (len(self.secondaryemail) > 0):
                ReturnedEmail['Secondary'] = u'%s' % (self.secondaryemail.strip())
                
        
        return ReturnedEmail

    private_email = property(_get_private_email)

    def _email_address(self):
        "returns the email address, primary then secondary"
        ReturnedEmail = None

        if self.primaryemail and (len(self.primaryemail.strip()) > 0):
            ReturnedEmail = u'%s' % (self.primaryemail.strip())
        elif self.secondaryemail and (len(self.secondaryemail.strip()) > 0):
            ReturnedEmail = u'%s' % (self.secondaryemail.strip())
                
        
        return ReturnedEmail

    email_address = property(_email_address)

    def _get_official_email(self):
        "returns the official email addresses"

            
        ReturnedEmail = {}

        if self.mfri_email or len(self.mfri_email) > 0:
            ReturnedEmail['Primary'] = u'%s' % (self.mfri_email.strip())
            return ReturnedEmail

        if self.showprimaryemail:
            if self.primaryemail and (len(self.primaryemail) > 0):
                if u'@mfri.org' in self.primaryemail:
                    ReturnedEmail['Primary'] = u'%s' % (self.primaryemail.strip())

        if self.showsecondaryemail:
            if self.secondaryemail and (len(self.secondaryemail) > 0):
                if u'@mfri.org' in self.secondaryemail:
                    ReturnedEmail['Secondary'] = u'%s' % (self.secondaryemail.strip())
        
        return ReturnedEmail

    official_email = property(_get_official_email)

    def _is_employment_current(self):
        "returns True if the record is a current record, false if the record is marked as Not Specified, Separated or Suspended"

        if self.employmentstatus.id in (1, 6, 7):
            return False
        else:
            return True
    
    is_employment_current = property(_is_employment_current)

    def _primary_phone_number(self):
        
        phone_number_options = self.official_phone
        
        if phone_number_options:
            return u'%s' % (phone_number_options['Primary'])
            
        return u''
    
    primary_phone_number = property(_primary_phone_number)

    def _birth_date(self):
        "returns True if the birth date with a different moniker for compitbility reasons"

        return self.birthdate
    
    birth_date = property(_birth_date)
    
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
        #logger.debug("Locking table %s" % table)
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

    class Meta:
        verbose_name_plural = 'MfriInstructors'
        db_table = u'MfriInstructors'
        ordering = ['lastname', 'firstname', 'middlename', 'suffix']

