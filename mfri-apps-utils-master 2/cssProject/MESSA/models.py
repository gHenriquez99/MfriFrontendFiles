from django.db import models

import datetime

from django.conf import settings
from django.db import models, connection

from AppsAdmin.dbk import MESSAEncryptKeyS, MESSAEncryptKeyE

from AppBase.models import AppBase

from MSchedule.models import Scheduledcourses


MARYLAND_BULK_UPLOAD_FORM_PACKAGE_ID = u'6869C0BF-EE43-E211-9D83-CB5C586EC439'


MFRI_CRT_INITIAL_LICENSE_ID = u'52789EA7-84AF-E311-B3F8-AE437D699481'
MFRI_CRT_RENEWAL_LICENSE_ID = u'C92228C2-84AF-E311-B3F8-AE437D699481'
MFRI_EMR_INITIAL_LICENSE_ID = u'CC11C0D1-84AF-E311-B3F8-AE437D699481'
MFRI_EMR_RENEWAL_LICENSE_ID = u'A9FAF5E4-84AF-E311-B3F8-AE437D699481'
MFRI_EMT_INITIAL_LICENSE_ID = u'DDC27EF1-84AF-E311-B3F8-AE437D699481'
MFRI_EMT_RENEWAL_LICENSE_ID = u'14E5BC05-85AF-E311-B3F8-AE437D699481'
MFRI_PARAMEDIC_INITIAL_LICENSE_ID = u'5740A418-85AF-E311-B3F8-AE437D699481'
MFRI_PARAMEDIC_RENEWAL_LICENSE_ID = u'84D3492E-85AF-E311-B3F8-AE437D699481'


class Messrapplicationlevel(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRApplicationLevel'
        verbose_name_plural = "Messrapplicationlevels"
        ordering = ['name']    

    def __unicode__(self):
        return '%s' % (self.name)

class Messrapplicationtype(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRApplicationTypes'
        verbose_name_plural = "Messrapplicationtypes"
        ordering = ['name']    

    def __unicode__(self):
        return '%s' % (self.name)


class Messrcollegeleveltypes(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRCollegeLevelTypes'
        verbose_name_plural = "MESSRCollegeLevelTypes"
        ordering = ['name']    

    def __unicode__(self):
        return '%s' % (self.name)

class Messrgendertypes(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRGenderTypes'
        verbose_name_plural = "MESSRGenderTypes"
        ordering = ['name']    

    def __unicode__(self):
        return '%s' % (self.name)


class Messrgradeleveltypes(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRGradeLevelTypes'
        verbose_name_plural = "MESSRGradeLevelTypes"
        ordering = ['name']    
        
    def __unicode__(self):
        return '%s' % (self.name)
    
class Messrracetypes(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRRaceTypes'
        verbose_name_plural = "MESSRRaceTypes"
        ordering = ['name']    

    def __unicode__(self):
        return '%s' % (self.name)

class Messrholdstatus(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRHoldStatus'

class Messroutcomenumbertypes(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSROutcomeNumberTypes'

class Messroutcometypes(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 

    class Meta:
        db_table = u'MESSROutcomeTypes'

    def __unicode__(self):
        return self.name

#class Messrracetypes(models.Model):
##    id = models.IntegerField(primary_key=True, db_column='ID') 
#    name = models.CharField(max_length=765, db_column='Name') 
#    class Meta:
#        db_table = u'MESSRRaceTypes'

class Messrsponsortypes(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRSponsorTypes'

class Messrsuffixtypes(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRSuffixTypes'

class Messrtitletypes(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    name = models.CharField(max_length=765, db_column='Name') 
    class Meta:
        db_table = u'MESSRTitleTypes'

    def __unicode__(self):
        return '%s' % (self.name)


class MessrHold(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') 
    formversion = models.IntegerField(null=True, db_column='FormVersion', blank=True) 
    formnumberback = models.CharField(max_length=60, db_column='FormNumberBack', blank=True) 
    formnumberfront = models.CharField(max_length=60, db_column='FormNumberFront', blank=True) 
    #scheduledcourseid = models.IntegerField(null=True, db_column='ScheduledCourseID', blank=True) 
    scheduled_course = models.ForeignKey(Scheduledcourses, db_column='ScheduledCourseID')

    #applicationtypeid = models.IntegerField(null=True, db_column='ApplicationTypeID', blank=True) 
    #applicationlevelid = models.IntegerField(null=True, db_column='ApplicationLevelID', blank=True) 
    application_type = models.ForeignKey(Messrapplicationtype, db_column='ApplicationTypeID')
    application_level = models.ForeignKey(Messrapplicationlevel, db_column='ApplicationLevelID')
    
    county_number = models.CharField(max_length=9, db_column='CountyNumber', blank=True) 
    log_number = models.CharField(max_length=765, db_column='LogNumber', blank=True) 
    log_number_category = models.CharField(max_length=765, db_column='LogNumberCategory', blank=True) 
    log_number_level = models.CharField(max_length=765, db_column='LogNumberLevel', blank=True) 
    log_number_funding_source = models.CharField(max_length=765, db_column='LogNumberFundingSource', blank=True) 
    log_number_section = models.CharField(max_length=765, db_column='LogNumberSection', blank=True) 
    log_number_prefix = models.CharField(max_length=384, db_column='LogNumberPrefix', blank=True) 
    log_number_ordinal = models.CharField(max_length=384, db_column='LogNumberOrdinal', blank=True) 
    log_number_fiscal_year = models.CharField(max_length=384, db_column='LogNumberFiscalYear', blank=True) 

    #sponsorid = models.IntegerField(null=True, db_column='SponsorID', blank=True) 
    sponsor = models.ForeignKey(Messrsponsortypes, db_column='SponsorID')

    client_number = models.CharField(max_length=48, db_column='ClientNumber', blank=True) 

    ssn = models.BinaryField(db_column='IDNumber', blank=True) #20180925 #20180904

    back_page_id_number = models.BinaryField(db_column='BIDNumber', blank=True) #20180925 #20180904

    state_provider_number = models.BinaryField(db_column='StateProviderNumber', blank=True) #20180925 #20180904
    back_page_state_provider_number = models.BinaryField(db_column='BStateProviderNumber', blank=True) #20180925 #20180904

    company_number = models.CharField(max_length=765, db_column='CompanyNumber', blank=True) 

    birth_date = models.DateField(null=True, db_column='BirthDate', blank=True) 

#    legal_question_1 = models.IntegerField(null=True, db_column='LegalQuestion1', blank=True) 
#    legal_question_2 = models.IntegerField(null=True, db_column='LegalQuestion2', blank=True) 
#    legal_question_3 = models.IntegerField(null=True, db_column='LegalQuestion3', blank=True) 
    legal_question_1 = models.BooleanField(db_column='LegalQuestion1', blank=True, default=False) 
    legal_question_2 = models.BooleanField(db_column='LegalQuestion2', blank=True, default=False) 
    legal_question_3 = models.BooleanField(db_column='LegalQuestion3', blank=True, default=False)     
    
    #titleid = models.IntegerField(null=True, db_column='TitleID', blank=True) 
    title = models.ForeignKey(Messrtitletypes, db_column='TitleID', related_name="+")

    firstname = models.CharField(max_length=765, db_column='FirstName', blank=True) 
    middlename = models.CharField(max_length=765, db_column='MiddleName', blank=True) 
    lastname = models.CharField(max_length=765, db_column='LastName', blank=True) 
    suffix = models.CharField(max_length=765, db_column='Suffix', blank=True) 

    #po_box = models.IntegerField(null=True, db_column='POBox', blank=True) 
    #rural_route = models.IntegerField(null=True, db_column='RuralRoute', blank=True) 
    po_box = models.BooleanField(db_column='POBox', blank=True, default=False)     
    rural_route = models.BooleanField(db_column='RuralRoute', blank=True, default=False)     

    street_address_number = models.CharField(max_length=96, db_column='StreetAddressNumber', blank=True) 
    street_address = models.CharField(max_length=765, db_column='StreetAddress', blank=True) 
    apartment_number = models.CharField(max_length=765, db_column='Apt', blank=True) 
    city = models.CharField(max_length=765, db_column='City', blank=True) 
    state = models.CharField(max_length=6, db_column='State', blank=True) 
    postcode = models.CharField(max_length=60, db_column='PostCode', blank=True) 

    home_phone = models.CharField(max_length=96, db_column='HomePhone', blank=True) 
    work_phone = models.CharField(max_length=96, db_column='WorkPhone', blank=True) 

    #genderid = models.IntegerField(null=True, db_column='GenderID', blank=True) 
    gender = models.ForeignKey(Messrgendertypes, db_column='GenderID')

    #hispanic = models.IntegerField(null=True, db_column='Hispanic', blank=True) 
    hispanic = models.BooleanField(db_column='Hispanic', blank=True, default=False)     

    #raceid = models.IntegerField(null=True, db_column='RaceID', blank=True) 
    race = models.ForeignKey(Messrracetypes, db_column='RaceID')

    #gradelevelid = models.IntegerField(null=True, db_column='GradeLevelID', blank=True) 
    grade_level = models.ForeignKey(Messrgradeleveltypes, db_column='GradeLevelID')

    #collegelevelid = models.IntegerField(null=True, db_column='CollegeLevelID', blank=True) 
    college_level = models.ForeignKey(Messrcollegeleveltypes, db_column='CollegeLevelID')

    #outcome = models.IntegerField(null=True, db_column='Outcome', blank=True) 
    outcome = models.ForeignKey(Messroutcometypes, db_column='Outcome')

    #outcometypeid = models.IntegerField(null=True, db_column='OutcomeTypeID', blank=True) 
    outcome_type = models.ForeignKey(Messroutcomenumbertypes, db_column='OutcomeTypeID')

    outcome_number = models.IntegerField(null=True, db_column='OutcomeNum', blank=True) 

    practical_exam_resuscitation = models.CharField(max_length=3, db_column='PracticalExamResuscitation', blank=True) 
    practical_exam_resuscitation_retest = models.CharField(max_length=3, db_column='PracticalExamResuscitationRetest', blank=True) 
    practical_exam_medical = models.CharField(max_length=3, db_column='PracticalExamMedical', blank=True) 
    practical_exam_medical_retest = models.CharField(max_length=3, db_column='PracticalExamMedicalRetest', blank=True) 
    practical_exam_trauma = models.CharField(max_length=3, db_column='PracticalExamTrauma', blank=True) 
    practical_exam_trauma_retest = models.CharField(max_length=3, db_column='PracticalExamTraumaRetest', blank=True) 

    written_exam_number = models.CharField(max_length=9, db_column='WrittenExamNumber', blank=True) 

    overall_score = models.CharField(max_length=9, db_column='OverAllScore', blank=True) 

    front_page = models.DateTimeField(null=True, db_column='FrontPage', blank=True) 
    back_page = models.DateTimeField(null=True, db_column='BackPage', blank=True) 

    synched_front = models.DateTimeField(null=True, db_column='SynchedFront', blank=True) 
    synched_back = models.DateTimeField(null=True, db_column='SynchedBack', blank=True) 

    #mergeid = models.IntegerField(null=True, db_column='MergeID', blank=True) 

    #statusid = models.IntegerField(null=True, db_column='StatusID', blank=True) 
    status = models.ForeignKey(Messrholdstatus, db_column='StatusID')


    evaluation_results = models.TextField(db_column='EvaluationResults', blank=True) 
    modular_grades = models.TextField(db_column='ModularGrades', blank=True) 

    pre_reg_id = models.IntegerField(null=True, db_column='PreRegID', blank=True) 
    student_reg_id = models.IntegerField(null=True, db_column='StudentRegID', blank=True) 

    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 
    priority = models.IntegerField(null=True, db_column='Priority', blank=True) 

    class Meta:
        db_table = u'MESSRHold'
        
        verbose_name_plural = "MessrHolds"
        ordering = ['lastname', 'suffix', 'firstname', 'middlename']
        
    def __unicode__(self):
        return u'%s %s, %s %s' % (self.lastname, self.suffix, self.firstname, self.middlename)

    def _get_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(idnumber, %s) as ssn FROM MESSRHold WHERE id=%s", [MESSAEncryptKeyS(), self.id])
        return cursor.fetchone()[0]
   
    def _set_ssn(self, ssn_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as ssn", [ssn_value, MESSAEncryptKeyS()])
        self.idnumber = cursor.fetchone()[0]
    
    ssn_clear = property(_get_ssn, _set_ssn)

    def _get_epins(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(StateProviderNumber, %s) as epins FROM MESSRHold WHERE id=%s", [MESSAEncryptKeyE(), self.id])
        return cursor.fetchone()[0]
   
    def _set_epins(self, epins_value):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as epins", [epins_value, MESSAEncryptKeyE()])
        self.state_provider_number = cursor.fetchone()[0]
    
    epins_clear = property(_get_epins, _set_epins)

    def _get_partial_ssn(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(idnumber, %s) as ssn FROM MESSRHold WHERE id=%s", [MESSAEncryptKeyS(), self.id])
        return cursor.fetchone()[0][-5:]
    
    def _set_partial_ssn(self, ssn_value):
        padded_ssn = ssn_value.rjust(9,'0')
        cursor = connection.cursor()
        cursor.execute("SELECT AES_ENCRYPT(%s, %s) as ssn", [padded_ssn, MESSAEncryptKeyS()])
        self.idnumber = cursor.fetchone()[0]

    partial_ssn = property(_get_partial_ssn, _set_partial_ssn)
    
    def _get_full_name(self):
        "returns the full name FN MN LN S"
        ReturnedName = ''
        if self.firstname and len(self.firstname) > 0:
            ReturnedName += self.firstname
    
        if self.middlename and len(self.middlename) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.middlename
    
        if self.lastname and len(self.lastname) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.lastname
    
        if self.suffix and len(self.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.suffix
    
        return ReturnedName
    
    def _get_full_name_reversed(self):
        "returns the full name LN S, FN MN"
        ReturnedName = ''
        if self.lastname and len(self.lastname) > 0:
            ReturnedName += self.lastname
    
        if self.suffix and len(self.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.suffix
    
        if len(ReturnedName) > 0:
            ReturnedName += ','
    
        if self.firstname and len(self.firstname) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.firstname
    
        if self.middlename and len(self.middlename) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.middlename
    
    
        return ReturnedName

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

    def _get_highest_education_level(self):
        "returns the highest education level"

#        if self.college_level and len(self.college_level.name) > 0 and self.college_level.name != u'None':
#            return self.college_level.name
    
        if self.grade_level and len(self.grade_level.name) > 0 and self.grade_level.name != u'None':
            return self.grade_level.name
        else:
            return ''
    
    highest_education_level = property(_get_highest_education_level)


    def _get_miemss_license_id(self):
        "returns the MIEMSS License ID"

        
        if not self.application_level:
            return u''
            
        if self.application_level.name == u'None':
            return u''
            
        if not self.application_type:
            return u''

        if self.application_type.name == u'None':
            return u''
    
        if self.application_level.id == 1:
            return u''
        elif self.application_level.id == 2: #  was FR now EMR
            if self.application_type == 2: #Initial
                return MFRI_EMR_INITIAL_LICENSE_ID
            elif self.application_type == 5: #Recertifciation
                return MFRI_EMR_RENEWAL_LICENSE_ID
            else:
                return MFRI_EMR_RENEWAL_LICENSE_ID
                
        elif self.application_level.id == 3: # was EMT-B now EMT
            if self.application_type == 2: #Initial
                return MFRI_EMT_INITIAL_LICENSE_ID
            elif self.application_type == 5: #Recertifciation
                return MFRI_EMT_RENEWAL_LICENSE_ID
            else: #everything else
                return MFRI_EMT_RENEWAL_LICENSE_ID

        elif self.application_level.id == 4: # CRT/EMT-I 
            if self.application_type == 2: #Initial
                return MFRI_CRT_INITIAL_LICENSE_ID
            elif self.application_type == 5: #Recertifciation
                return MFRI_CRT_RENEWAL_LICENSE_ID
            else: #everything else
                return MFRI_CRT_RENEWAL_LICENSE_ID
        elif self.application_level.id == 5: # EMT-P
            if self.application_type == 2: #Initial
                return MFRI_PARAMEDIC_INITIAL_LICENSE_ID
            elif self.application_type == 5: #Recertifciation
                return MFRI_PARAMEDIC_RENEWAL_LICENSE_ID
            else: #everything else
                return MFRI_PARAMEDIC_RENEWAL_LICENSE_ID
        elif self.application_level.id == 6: # EMD
            if self.application_type == 2: #Initial
                return u''
            elif self.application_type == 5: #Recertifciation
                return u''
            else: #everything else
                return u''
        else:
            return u''
            
    
    miemss_license_id = property(_get_miemss_license_id)
    

#    LICENSE_LEVEL_RENEWING
    def _get_miemss_license_level(self):
        "returns the MIEMSS License Level in PROVIDER_LICENSE_HISTORY"
        
        if not self.application_level:
            return u''
            
        if self.application_level.name == u'None':
            return u''
            
        if self.application_level.id == 1:
            return u''
        elif self.application_level.id == 2: #  was FR now EMR
            return u'EMR - Emergency Medical Responder'
        elif self.application_level.id == 3: # was EMT-B now EMT
            return u'EMT - Emergency Medical Technician'
        elif self.application_level.id == 4: # CRT/EMT-I 
            return u'CRT - Cardiac Rescue Technician'
        elif self.application_level.id == 5: # EMT-P
            return u'Paramedic'
        elif self.application_level.id == 6: # EMD
            return u'EMD - Emergency Medical Dispatcher'
        else:
            return u''
    
    miemss_license_level = property(_get_miemss_license_level)

    def _get_miemss_date_of_birth(self):
        "returns the birth date for MIEMSS PERSONNEL record"
        
        if not self.birth_date:
            return u''
            
        if self.birth_date.strftime('%m-%d-%Y') == "00-00-0000":
            return u''

        return self.birth_date.strftime('%m-%d-%Y')
            
    
    miemss_date_of_birth = property(_get_miemss_date_of_birth)

    def _get_miemss_outcome(self):
        "returns the MIEMSS outcome"
        
        try:
            if not self.outcome:
                return u''
        except Messroutcometypes.DoesNotExist:            
            return u''
            
        #if self.outcome.name == u'None':
        #    return u''
            
        if self.outcome.id == 1:
            return u''
        elif self.outcome.id == 2: #  Successfully Completed
            return u'Pass'
        elif self.outcome.id == 3: # Withdrew
            return u'Withdrew'
        elif self.outcome.id == 4: # Dropped
            return u'Withdrew'
        elif self.outcome.id == 5: # Failed
            return u'Fail'
        elif self.outcome.id == 6: # Incomplete
            return u'Incomplete'
        elif self.outcome.id == 7: # Successfully Completed Retraining
            return u'Pass'
        elif self.outcome.id == 8: # Transferred
            return u'Transferred To:'
        elif self.outcome.id == 9: # Failed Practical Exam
            return u'Fail'
        elif self.outcome.id == 10: # Failed Midterm Exam
            return u'Fail'
        else:
            return u''
    
    miemss_outcome = property(_get_miemss_outcome)


#20161102
class StudentMessaDataDescription(models.Model):
    file_name = models.CharField(max_length=765, db_column='FileName', blank=True) 
    front_page_05_format = models.IntegerField(null=True, db_column='FrontPage05Format', blank=True) 

    #scheduled_course = models.IntegerField(null=True, db_column='ScheduledCourseID', blank=True) 
    scheduled_course = models.ForeignKey(Scheduledcourses, db_column='ScheduledCourseID')
    
    page_sides_scanned = models.IntegerField(null=True, db_column='PageSidesScanned', blank=True) 
    #data_sent_to_miemss = models.IntegerField(null=True, db_column='DataSentToMIEMSS', blank=True) 
    is_data_sent_to_miemss = models.BooleanField(db_column='DataSentToMIEMSS', blank=True, default=False) 

    #is_data_retrieved_by_miemss = models.IntegerField(null=True, db_column='DataRetrievedByMIEMSS', blank=True) 
    is_data_retrieved_by_miemss = models.BooleanField(db_column='DataRetrievedByMIEMSS', blank=True, default=False) 
    retrieved_date = models.DateTimeField(null=True, db_column='RetrievedDate', blank=True) 

    #notificationsenttomiemss = models.IntegerField(null=True, db_column='NotificationSentToMIEMSS', blank=True) 
    is_notification_sent_to_miemss = models.BooleanField(db_column='NotificationSentToMIEMSS', blank=True, default=False) 
    notification_date = models.DateTimeField(null=True, db_column='NotificationDate', blank=True) 

    miemss_user = models.CharField(max_length=96, db_column='MIEMSSUser', blank=True) 
    send_date = models.DateTimeField(null=True, db_column='SendDate', blank=True) 
    record_count = models.IntegerField(null=True, db_column='RecordCount', blank=True) 
    prereg_count = models.IntegerField(null=True, db_column='PreRegCount', blank=True) 

    status = models.IntegerField(null=True, db_column='StatusID', blank=True) 
    
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 
    
    class Meta:
        db_table = u'StudentMESSRData'
        verbose_name_plural = "StudentMessaDataDescriptions"
        #ordering = ['lastname', 'suffix', 'firstname', 'middlename']

    def __unicode__(self):
        if self.scheduled_course:
            log_number = self.scheduled_course.log_number
        else:
            log_number = u'Unknown'
        
        if self.is_data_sent_to_miemss:
            data_sent_text = u'Data was sent to MIEMSS.'
        else:
            data_sent_text = u'Data was not sent to MIEMSS.'
        
        if self.is_data_retrieved_by_miemss:
            data_retrieved_text = u'Data was retrieved by MIEMSS on %s.' % (self.retrieved_date.strftime('%m-%d-%Y %H:%M'))
        else:
            data_retrieved_text = u'Data was not retrieved by MIEMSS.'

        if self.is_notification_sent_to_miemss:
            data_notification_text = u'MIEMSS notified on %s.' % (self.notification_date.strftime('%m-%d-%Y %H:%M'))
        else:
            data_notification_text = u'MIEMSS not yet notified.'

        status_text = u''
        if self.status == 1:
            status_text = u'New record.'
        elif self.status == 2:
            status_text = u'Data ready for MIEMSS'
            
        return u'%s %s %s %s %s' % (log_number, status_text, data_notification_text, data_sent_text, data_retrieved_text )


    def _lock_messa_data(self):
        "sets the status = 2 to lock the data and make available to miemss"
        
        self.status = 2
        self.save(update_fields=['status'])
        
        return True
        
    lock_messa_data = property(_lock_messa_data)

    def _unlock_messa_data(self):
        "sets the status = 1 to unlock the data and hide from miemss"
        
        self.status = 1
        self.save(update_fields=['status'])
        
        return False
        
    unlock_messa_data = property(_unlock_messa_data)

    def _is_locked(self):
        "returns True if status == 2 otherwise returns False"
        
        if self.status == 2:
            return True
        
        return False
        
    is_locked = property(_is_locked)

