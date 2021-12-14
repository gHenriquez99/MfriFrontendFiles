import json

from django.db import models

from AppsAdmin.models import Applications, Applinks, UserProfile, LegacyUsers
from AppLegacyBase.models import AppLegacyBase

from MAffiliations.models import Affiliations
from MStaff.models import MfriInstructors
from MOffices.models import MfriOffices, Jurisdictions, LegacyCoursesection, LegacyMfriregions
from MCourses.models import TCode, Coursedescriptions
from MLocations.models import Locations
from MClients.models import MfriClient

#from AppBase.utils_json import UnpackJson #, PackJson, IsDuplicateElement, ReplaceElement, AppendElement, RemoveElementFromList


#duplicated here because would not allow appbase module to load
def UnpackJson(data_to_unpack=None):
    
    if not data_to_unpack:
        return []

     
    if len(data_to_unpack) == 0:
        return []

    return json.loads(data_to_unpack)

def PackJson(data_to_pack=None):
    
    if not data_to_pack:
        return []

    return json.dumps(data_to_pack)

def expanded_day_name(day_abbreviation=None, pluralize=True):
    if not day_abbreviation or len(day_abbreviation) == 0:
        return u''
    
    plural_ending = u''
    if pluralize:
        plural_ending = u's'
        
    if day_abbreviation == u'M':
        return u'Monday%s' % (plural_ending)
    if day_abbreviation == u'Tu':
        return u'Tuesday%s' % (plural_ending)
    if day_abbreviation == u'W':
        return u'Wednesday%s' % (plural_ending)
    if day_abbreviation == u'Th':
        return u'Thursday%s' % (plural_ending)
    if day_abbreviation == u'F':
        return u'Friday%s' % (plural_ending)
    if day_abbreviation == u'Sa':
        return u'Saturday%s' % (plural_ending)
    if day_abbreviation == u'Su':
        return u'Sunday%s' % (plural_ending)
    
class ScheduledCourseStatus(models.Model):
    name = models.CharField(max_length=765, db_column='Name') # Field name made lowercase.

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'ScheduledCourseStatus'
        verbose_name_plural = "ScheduledCourseStatus"
        ordering = ['name']

class LegacyLinkStatus(models.Model):
    name = models.CharField(max_length=765, db_column='Name') # Field name made lowercase.
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'LinkStatus'
        verbose_name_plural = "LegacyLinkStatus"
        ordering = ['name']

class LegacyLinkType(models.Model):
    name = models.CharField(max_length=765, db_column='Name') # Field name made lowercase.

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'LinkTypes'
        verbose_name_plural = "LegacyLinkTypes"
        ordering = ['name']


class Legacy_Link(models.Model):
    name = models.CharField(max_length=765, db_column='Name') # Field name made lowercase.
    url = models.TextField(db_column='URL') # Field name made lowercase.
    
    link_type = models.ForeignKey(LegacyLinkType, db_column='LinkTypeID')
    link_status = models.ForeignKey(LegacyLinkStatus, db_column='LinkStatusID')
    
    #linktypeid = models.IntegerField(null=True, db_column='LinkTypeID', blank=True) # Field name made lowercase.
    #linkstatusid = models.IntegerField(null=True, db_column='LinkStatusID', blank=True) # Field name made lowercase.
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) # Field name made lowercase.
    lastchange = models.DateTimeField(db_column='LastChange') # Field name made lowercase.
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) # Field name made lowercase.
    created = models.DateTimeField(db_column='Created') # Field name made lowercase.

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'Links'
        verbose_name_plural = "Legacy_Links"
        ordering = ['name']


class ScheduleType(models.Model):
    name = models.CharField(max_length=765, db_column='Name') # Field name made lowercase.

    is_available = models.BooleanField(default=True, help_text='Option is available for use.')
    schedule_defaults = models.CharField(max_length=765, help_text='Schedule default values.')

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'ScheduleTypes'
        verbose_name_plural = "ScheduleTypes"
        ordering = ['name']

#    def _get_first_start_time(self):
#        
#        if len(self.schedule_defaults) == 0:
#            return None
#
#        schedule_defaults = UnpackJson(data_to_unpack=self.schedule_defaults)
#
#        if len(schedule_defaults['hours']) == 0:
#            return None
#        
#        start_time = schedule_defaults['hours'][0]['start_time']
#
#        return start_time
#    
#    get_first_start_time = property(_get_first_start_time)
#
#    def _get_start_time(self, session_number):
#        if len(self.schedule_defaults) == 0:
#            return None
#
#        schedule_defaults = UnpackJson(data_to_unpack=self.schedule_defaults)
#
#        if len(schedule_defaults['hours']) == 0:
#            return None
#        
#        if session_number > len(schedule_defaults['hours']):
#            session_number = len(schedule_defaults['hours']) - 1
#            
#        start_time = schedule_defaults['hours'][session_number]['start_time']
#
#        return start_time
#    
#    get_start_time = property(_get_start_time)
#
#    def _get_first_end_time(self):
#        
#        if len(self.schedule_defaults) == 0:
#            return None
#
#        schedule_defaults = UnpackJson(data_to_unpack=self.schedule_defaults)
#
#        if len(schedule_defaults['hours']) == 0:
#            return None
#        
#        end_time = schedule_defaults['hours'][0]['end_time']
#
#        return end_time
#    
#    get_first_end_time = property(_get_first_end_time)
#
#    def _get_end_time(self, session_number):
#        if len(self.schedule_defaults) == 0:
#            return None
#
#        schedule_defaults = UnpackJson(data_to_unpack=self.schedule_defaults)
#
#        if len(schedule_defaults['hours']) == 0:
#            return None
#        
#        if session_number > len(schedule_defaults['hours']):
#            session_number = len(schedule_defaults['hours']) - 1
#            
#        end_time = schedule_defaults['hours'][session_number]['end_time']
#
#        return end_time
#    
#    get_end_time = property(_get_end_time)

#class TCode(models.Model):
#    name = models.CharField(max_length=765, db_column='Name', blank=True) # Field name made lowercase.
#    value = models.CharField(max_length=765, db_column='Value', blank=True) # Field name made lowercase.
#
#    def __unicode__(self):
#        return u'%s %s' %  (self.name, self.value)
#    
#    class Meta:
#        db_table = u'TCodes'
#        verbose_name_plural = "TCodes"
#        ordering = ['name']

class UmdTerm(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) # Field name made lowercase.
    value = models.CharField(max_length=765, db_column='Value', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return u'%s (%s)' %  (self.name, self.value)
    
    class Meta:
        db_table = u'UMDTerms'
        verbose_name_plural = "UmdTerms"
        ordering = ['name']

    def _full_name(self):
        "returns full name"

        return u'%s (%s)' %  (self.name, self.value)

    full_name = property(_full_name)

#class ScheduledcoursesManager(models.Manager):
#    def workflow_count(self, MfriOffices, Status): 
#        return self.filter(mfriofficeid__in=MfriOffices, statusid__in=Status).count()

class ScheduledcoursesManager(models.Manager):
    def courses_for_review(self, MfriOffices=None, legacy_section=None, legacy_region=None): 

        if legacy_section and legacy_region:
            return self.filter(mark_as_deleted__exact=0, legacy_host_section__exact=legacy_section, legacy_host_region__exact=legacy_region, schedule_status__in=[2,11])
        else:
            return self.filter(mark_as_deleted__exact=0, mfri_office__in=MfriOffices, schedule_status__in=[2,11])

    def requested_courses(self, MfriOffices=None, legacy_section=None, legacy_region=None): 
        if legacy_section and legacy_region:
            return self.filter(mark_as_deleted__exact=0, legacy_host_section__exact=legacy_section, legacy_host_region__exact=legacy_region, schedule_status__exact=2) #.query.__str__()
        else:
            return self.filter(mark_as_deleted__exact=0, mfri_office__in=MfriOffices, schedule_status__exact=2)

    def approved_courses(self, MfriOffices=None, legacy_section=None, legacy_region=None): 
        if legacy_section and legacy_region:
            return self.filter(mark_as_deleted__exact=0, legacy_host_section__exact=legacy_section, legacy_host_region__exact=legacy_region, schedule_status__exact=11)
        else:
            return self.filter(mark_as_deleted__exact=0, mfri_office__in=MfriOffices, schedule_status__exact=11)
    
    def confirmed_courses(self, MfriOffices=None, legacy_section=None, legacy_region=None): 
        if legacy_section and legacy_region:
            return self.filter(mark_as_deleted__exact=0, legacy_host_section__exact=legacy_section, legacy_host_region__exact=legacy_region, schedule_status__exact=3)
        else:
            #2020107+
            if MfriOffices:
                return self.filter(mark_as_deleted__exact=0, mfri_office__in=MfriOffices, schedule_status__exact=3)
            return self.filter(mark_as_deleted__exact=0, schedule_status__exact=3)
            #2020107-

    def confirmed_courses_for_public_schedule(self, MfriOffices=None): 
        if MfriOffices:
            return self.filter(mark_as_deleted__exact=0, mfri_office__in=MfriOffices, schedule_status__exact=3)
        return self.filter(mark_as_deleted__exact=0, schedule_status__exact=3)
            #2020107-

    def scheduled_course_from_lognumber(self, category, level, section_number, fiscal_year):
        if len(section_number) == 4:
            section_number = section_number[1:]
            
        return self.filter(course_description__category__contains=category, course_description__level__contains=level, section_number=section_number, fiscal_year=fiscal_year)
 
        
class Scheduledcourses(AppLegacyBase):
    course_description = models.ForeignKey(Coursedescriptions, db_column='CourseID')
    
    location = models.ForeignKey(Locations, db_column='LocationID')
    
    #instructorid = models.IntegerField(null=True, db_column='InstructorID', blank=True) # Field name made lowercase.
    instructor = models.ForeignKey(MfriInstructors, db_column='InstructorID', related_name="scheduled_courses_taught")
    
    #oldinstructorid = models.IntegerField(null=True, db_column='OldInstructorID', blank=True) # Field name made lowercase.
    old_format_log_number_section_and_fiscal_year = models.CharField(max_length=765, db_column='LogNumber', blank=True) # Field name made lowercase.

    miemss_log_number = models.CharField(max_length=765, db_column='MIEMSSLogNumber', blank=True) # Field name made lowercase.
    naemt_course_number = models.CharField(max_length=765, blank=True) 

    funding_source_code = models.CharField(max_length=30, db_column='FundingSourceCode', blank=True) # Field name made lowercase.
    section_number = models.CharField(max_length=9, db_column='SectionNumber', blank=True) # Field name made lowercase.
    fiscal_year = models.CharField(max_length=12, db_column='FiscalYear', blank=True) # Field name made lowercase.
    #lognumber_suffix = models.CharField(max_length=10, default=Null, null=True, blank=True) 

    registration_open_date = models.DateTimeField(null=True, db_column='RegOpenDate', blank=True) # Field name made lowercase.
    registration_close_date = models.DateTimeField(null=True, db_column='RegClosedDate', blank=True) # Field name made lowercase.

    start_date = models.DateTimeField(null=True, db_column='StartDate', blank=True) # Field name made lowercase.
    end_date = models.DateTimeField(null=True, db_column='EndDate', blank=True) # Field name made lowercase.
    recurring_days = models.CharField(max_length=60, db_column='RecurringDays', blank=True) # Field name made lowercase.

    min_students = models.IntegerField(null=True, db_column='MinStudents', blank=True) # Field name made lowercase.
    max_students = models.IntegerField(null=True, db_column='MaxStudents', blank=True) # Field name made lowercase.
    
    use_wait_list = models.BooleanField(default=False, db_column='UseWaitList', help_text='Add students to wait list when registration is count is full.')
    #use_wait_list = models.IntegerField(null=True, db_column='UseWaitList', blank=True) # Field name made lowercase.
    
    use_web_registration = models.BooleanField(default=False, db_column='UseWebRegister', help_text='Allow students to register through the public website.')
    #use_web_registration = models.IntegerField(null=True, db_column='UseWebRegister', blank=True) # Field name made lowercase.
    registered_count = models.IntegerField(null=True, db_column='RegisteredCount', blank=True) # Field name made lowercase.
    dropped_count = models.IntegerField(null=True, db_column='DroppedCount', blank=True) # Field name made lowercase.
    out_of_state_fee = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='OutStateFee', blank=True) # Field name made lowercase.
    in_state_fee = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='InStateFee', blank=True) # Field name made lowercase.
    
    #deprecated
    legacy_host_region = models.ForeignKey(LegacyMfriregions, db_column='RegionID')
    legacy_host_section = models.ForeignKey(LegacyCoursesection, db_column='SectionID')
#    legacy_activity_center = models.IntegerField(null=True, db_column='ActivityCenterID', blank=True) # Field name made lowercase.

    #going forward use mfri_office rather than region, section or activity center
    mfri_office = models.ForeignKey(MfriOffices, db_column='MFRIOfficeID')
    

    legacy_link = models.ForeignKey(Legacy_Link, db_column='LinkID', null=True)

    schedule_type = models.ForeignKey(ScheduleType, db_column='TypeID')

    #linkid = models.IntegerField(null=True, db_column='LinkID', blank=True) # Field name made lowercase.
    #typeid = models.IntegerField(null=True, db_column='TypeID', blank=True) # Field name made lowercase.
    
    show_on_transcript = models.BooleanField(default=True, db_column='ShowOnTranscript', blank=True, help_text='This course will be listed on student transcripts.')
    
    #show_on_transcript = models.IntegerField(null=True, db_column='ShowOnTranscript', blank=True) # Field name made lowercase.
    transcript_note = models.TextField(db_column='TranscriptNote', blank=True) # Field name made lowercase.

    require_program_evaluations = models.BooleanField(default=True, db_column='NeedProgramEvaluations', blank=True, help_text='This course will require program evaluations.')

    #require_program_evaluations = models.IntegerField(null=True, db_column='NeedProgramEvaluations', blank=True) # Field name made lowercase.
    program_evaluation_note = models.TextField(db_column='ProgramEvaluationNote', blank=True) # Field name made lowercase.

    is_seminar = models.BooleanField(default=False, db_column='CourseIsSeminar', blank=True, help_text='This program is a seminar.')

    #is_seminar = models.IntegerField(null=True, db_column='CourseIsSeminar', blank=True) # Field name made lowercase.

    #schedule_status = models.ForeignKey(Scheduledcoursestatus, db_column='StatusID')
    schedule_status = models.ForeignKey(ScheduledCourseStatus, db_column='StatusID')

    #programstatusid = models.IntegerField(null=True, db_column='ProgramStatusID', blank=True) # Field name made lowercase.
    
    #registrationstatusid = models.IntegerField(null=True, db_column='RegistrationStatusID', blank=True) # Field name made lowercase.
    
    #hostagencyid = models.IntegerField(null=True, db_column='HostAgencyID', blank=True) # Field name made lowercase.
    #jurisdictionid = models.IntegerField(null=True, db_column='JurisdictionID', blank=True) # Field name made lowercase.
    host_agency = models.ForeignKey(Affiliations, null=True, db_column='HostAgencyID', blank=True)
    jurisdiction = models.ForeignKey(Jurisdictions, null=True, db_column='JurisdictionID', blank=True)
    hostreservations = models.IntegerField(null=True, db_column='HostReservations', blank=True) # Field name made lowercase.
    hostregistrations = models.IntegerField(null=True, db_column='HostRegistrations', blank=True) # Field name made lowercase.
    use_host_agency_priority = models.BooleanField(default=False, db_column='UseHostAgencyPriority', blank=True)
    use_jurisdiction_priority = models.BooleanField(default=False, db_column='UseJurisdictionPriority', blank=True)
    use_legacy_region_priority = models.BooleanField(default=False, db_column='UseRegionPriority', blank=True)
    use_instate_priority = models.BooleanField(default=True, db_column='UseInStatePriority', blank=True)
    use_emt_certification_expiration_priority = models.BooleanField(default=False, db_column='UseCertExpirationPriority', blank=True)

    #20210927+
    send_alert_email_to_office_before_approval = models.BooleanField(default=False, help_text='Send registration request email alert to region at time of registration before training officer approval.')
    send_alert_email_to_office_after_approval = models.BooleanField(default=True, help_text='Send registration request email alert to region after training officer approval.')
    #20210927-

    #usehostagencypriority = models.IntegerField(null=True, db_column='UseHostAgencyPriority', blank=True) # Field name made lowercase.
    #usejurisdictionpriority = models.IntegerField(null=True, db_column='UseJurisdictionPriority', blank=True) # Field name made lowercase.
    #useregionpriority = models.IntegerField(null=True, db_column='UseRegionPriority', blank=True) # Field name made lowercase.
    #useinstatepriority = models.IntegerField(null=True, db_column='UseInStatePriority', blank=True) # Field name made lowercase.
    #usecertexpirationpriority = models.IntegerField(null=True, db_column='UseCertExpirationPriority', blank=True) # Field name made lowercase.
    sent_to_transcript = models.DateTimeField(null=True, db_column='SentToTranscript', blank=True) # Field name made lowercase.
    saved_in_transcript = models.DateTimeField(null=True, db_column='SavedInTranscript', blank=True) # Field name made lowercase.

    mark_as_deleted = models.BooleanField(default=False, db_column='MarkAsDeleted', blank=True)
    #mark_as_deleted = models.IntegerField(null=True, db_column='MarkAsDeleted', blank=True) # Field name made lowercase.
    #taskid = models.IntegerField(null=True, db_column='TaskID', blank=True) # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True) # Field name made lowercase.
    alert_msg = models.CharField(max_length=765, db_column='AlertMsg', blank=True) # Field name made lowercase.
    special_alert = models.CharField(max_length=765, db_column='SpecialAlert', blank=True) # Field name made lowercase.
    registration_note = models.CharField(max_length=765, db_column='RegistrationNote', blank=True) # Field name made lowercase.

    registration_alert_text                = models.TextField(blank=True, help_text='Highlighted Alert message that will appear prominently on registration form.')
    registration_header_text               = models.TextField(blank=True, help_text='Additional text that will appear on the top of the registration form.')
    registration_special_instructions_text = models.TextField(blank=True, help_text='Additional special instructions that will appear on the registration form.')
    registration_footer_text               = models.TextField(blank=True, help_text='Additional text that will appear on the bottom of the registration form.')

    resource_fee = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='ResourceFee', blank=True) # Field name made lowercase.
    
    t_code = models.ForeignKey(TCode, db_column='TCodeID')
    #tcodeid = models.IntegerField(null=True, db_column='TCodeID', blank=True) # Field name made lowercase.
    
    umd_term = models.ForeignKey(UmdTerm, db_column='TermID')
    
    #termid = models.IntegerField(null=True, db_column='TermID', blank=True) # Field name made lowercase.
    short_log_number = models.CharField(max_length=765, db_column='ShortLogNumber', blank=True) # Field name made lowercase.

    #ownerid = models.IntegerField(null=True, db_column='OwnerID', blank=True) # Field name made lowercase.

    coordinator = models.ForeignKey(MfriInstructors, db_column='OwnerID', related_name="scheduled_courses_coordinated")

    client = models.ForeignKey(MfriClient, db_column='ClientID', related_name="+")
    #clientid = models.IntegerField(null=True, db_column='ClientID', blank=True) # Field name made lowercase.
    require_payment              = models.BooleanField(default=False, help_text='Registrations for this class require payment up front to complete registration process.') #20170823

    require_epins                = models.BooleanField(default=False, help_text='Registrations for this class require EPINS.')
    require_mfri_student_number  = models.BooleanField(default=False,  help_text='Registrations for this class require MFRI Student ID Number.') #20200916
    require_ssn                  = models.BooleanField(default=True,  help_text='Registrations for this class require SSN.')
    require_nfasid               = models.BooleanField(default=True,  help_text='Registrations for this class require NFA SID.')
    require_birth_date           = models.BooleanField(default=True,  help_text='Registrations for this class require Birth Date.')
    require_emt_expiration_date  = models.BooleanField(default=False, help_text='Registrations for this class require EMT Expiration Date.')
    require_address              = models.BooleanField(default=True,  help_text='Registrations for this class require Address.')
    require_affiliation          = models.BooleanField(default=True,  help_text='Registrations for this class require Affiliation.')
    require_email_address        = models.BooleanField(default=True,  help_text='Registrations for this class require Email Address.')
    require_primary_phone        = models.BooleanField(default=True,  help_text='Registrations for this class require Primary Phone.')
    require_cell_phone           = models.BooleanField(default=False, help_text='Registrations for this class require Cell Phone.')
    require_training_officer_approval = models.BooleanField(default=False, help_text='Registrations for this class require Student Affiliation Agency Training Officer Approval.')
    require_mfri_office_approval      = models.BooleanField(default=False, help_text='Registrations for this class require MFRI Office Approval.')

    #20200921a+
    #need to add these to table before use.  Not sure we need this level of rules, left here in case we do.
    #require_book_fee_acknowledgment                 = models.BooleanField(default=False, help_text='Students required to acknowledge obligation for return or payment for books and other resources.')
    #require_rules_and_regulations_acknowledgement   = models.BooleanField(default=False, help_text='Students required to acknowledge they have read rules and regulation.')
    #require_release_statement_acknowledgement       = models.BooleanField(default=False, help_text='Students required to acknowledge records release statement.')
    #show_msfa_acknowledgement                       = models.BooleanField(default=False, help_text='Students can opt-in to sending their contact information to the MSFA.')
    #20200921a-

    allow_late_registration = models.BooleanField(default=False, help_text='Registrations for this class will be accepted after the registration closed date and marked as late.') #20171103

    class_folder_sent_date = models.DateTimeField(null=True, db_column='ClassFolderSentDate', blank=True) # Field name made lowercase.
    class_folder_sent_by = models.ForeignKey(LegacyUsers, db_column='ClassFolderSentID', related_name="class_folder_senders")
    
    class_folder_received_date = models.DateTimeField(null=True, db_column='ClassFolderReceivedDate', blank=True) # Field name made lowercase.
    class_folder_received_by = models.ForeignKey(LegacyUsers, db_column='ClassFolderReceivedID', related_name="class_folder_receivers")

    class_folder_closed_date = models.DateTimeField(null=True, db_column='ClassFolderClosedDate', blank=True) # Field name made lowercase.
    class_folder_closed_by = models.ForeignKey(LegacyUsers, db_column='ClassFolderClosedID', related_name="class_folder_closers")
    #class_folder_sent = models.IntegerField(null=True, db_column='ClassFolderSentID', blank=True) # Field name made lowercase.
    #class_folder_received = models.IntegerField(null=True, db_column='ClassFolderReceivedID', blank=True) # Field name made lowercase.
    #class_folder_closed = models.IntegerField(null=True, db_column='ClassFolderClosedID', blank=True) # Field name made lowercase.

    class_folder_note = models.TextField(db_column='ClassFolderNote', blank=True) # Field name made lowercase.

    registration_message = models.TextField(db_column='RegistrationMessage', blank=True) # Field name made lowercase.
    registration_email_text = models.TextField(db_column='RegistrationEmailText', blank=True) # Field name made lowercase.

    additional_course_prerequisite = models.CharField(max_length=765, blank=True)

    other_registration_release_agency_name = models.CharField(max_length=255, blank=True)

    #20191205+
    umd_canvas_lms_course_identifier = models.CharField(max_length=255, blank=True) 
    umd_canvas_lms_course_name = models.CharField(max_length=255, blank=True) 
    #20191205-
    
    lms_course_identifier = models.CharField(max_length=255, blank=True) 
    lms_course_name = models.CharField(max_length=255, blank=True) 

    #oldcoordinatorid = models.IntegerField(null=True, db_column='OldCoordinatorID', blank=True) # Field name made lowercase.
    #lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) # Field name made lowercase.
    #lastchange = models.DateTimeField(db_column='LastChange') # Field name made lowercase.
    #createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) # Field name made lowercase.
    #created = models.DateTimeField(db_column='Created') # Field name made lowercase.

    objects = ScheduledcoursesManager()
    
    def __unicode__(self):
        return u'%s' % (self.log_number)

#        if not self.courseid:
#            if self.fiscalyear > 2004:
#                return u'No Course-%s%s-%s' % (self.funding_source_code, self.sectionnumber, self.fiscalyear)
#            else:
#                return u'No Course-%s-%s[2:]' % (self.sectionnumber, self.fiscalyear)

#        if self.courseid.category and self.fiscalyear > 2004:
#            return u'%s-%s-%s%s-%s' % (self.courseid.category, self.courseid.level, self.funding_source_code, self.sectionnumber, self.fiscalyear)
#        else:
#            return u'%s-%s-%s[2:]' % (self.courseid.course_code, self.sectionnumber, self.fiscalyear)
#
    def _get_log_number(self):
        "returns the log number for the scheduled course"
 
        if not self.course_description:
            if self.fiscal_year > '2004':
                return u'No Course-%s%s-%s' % (self.funding_source_code, self.section_number, self.fiscal_year)
            else:
                return u'No Course-%s-%s' % (self.section_number, self.fiscal_year[2:])

        if self.course_description.category and self.fiscal_year > '2004':
            return u'%s-%s-%s%s-%s' % (self.course_description.category, self.course_description.level, self.funding_source_code, self.section_number, self.fiscal_year)
        else:
            return u'%s-%s-%s' % (self.course_description.course_code, self.section_number, self.fiscal_year[2:])
        
#        if self.courseid.category and self.fiscalyear >= 2005:
#            return u'%s-%s-%s%s-%s' % (self.courseid.category, self.courseid.level, self.funding_source_code, self.sectionnumber, self.fiscalyear)
#        else:
#            return u'%s-%s-%s[2:]' % (self.courseid.course_code, self.sectionnumber, self.fiscalyear)
            
    log_number = property(_get_log_number)

    def _get_miems_log_number(self):
        "returns the miems log number"

        if self.miemss_log_number and self.miemss_log_number != u'--' and len(self.miemss_log_number) > 0:
#            larry = self.miemss_log_number 
#            assert False
            return self.miemss_log_number

        if not self.course_description:
            return None

#        bob = u'%s-%s-%s' % (self.course_description.course_code, self.section_number, self.fiscal_year[2:])
#        assert False
        return u'%s-%s-%s' % (self.course_description.course_code, self.section_number, self.fiscal_year[2:])
    
    get_miems_log_number = property(_get_miems_log_number)

    def _get_course_name(self):
        "returns the name for the scheduled course"
        
        if not self.course_description:
            return u'No Course'
        
        return self.course_description.name #20161024
            
    course_name = property(_get_course_name)

    def _get_course_prerequisite(self):
        "returns the prerequisite for the scheduled course"
        
        if not self.course_description:
            return u'No Course'
        
        if self.course_description.course_prerequisite:
            if len(self.additional_course_prerequisite) > 0:
                return u'%s Additionally: %s' % (self.course_description.course_prerequisite, self.additional_course_prerequisite)
            else:
                return self.course_description.course_prerequisite
        else:
            if self.additional_course_prerequisite:
                return u'Prerequisite for this class: %s' % (self.additional_course_prerequisite)
            
            return None
            
    course_prerequisite = property(_get_course_prerequisite)

    def _get_category(self):
        "returns the category for the scheduled course"
        
        if not self.course_description:
            return u'No Course Category'
        
        return self.course_description.category
            
    category = property(_get_category)

    def _get_level(self):
        "returns the level for the scheduled course"
        
        if not self.course_description:
            return u'No Course level'
        
        return self.course_description.level
            
    level = property(_get_level)

    def _get_require_medical_clearance(self):
        "returns true if the course requires medical clearance"
        
        if not self.course_description:
            return False
        
        return self.course_description.require_medical_clearance
            
    does_require_medical_clearance = property(_get_require_medical_clearance)

    def _get_require_medical_clearance_note(self):
        "returns the medical clearance note if any"
        
        if not self.course_description:
            return u''
        
        return self.course_description.medical_clearance_note
            
    medical_clearance_note = property(_get_require_medical_clearance_note)

    def _get_has_sim_center_component(self):
        "returns the has_sim_center_component flag"
        
        if not self.course_description:
            return False
        
        return self.course_description.has_sim_center_component
            
    has_sim_center_component = property(_get_has_sim_center_component)
    
    def _get_has_online_component(self):
        "returns the has_online_component flag"
        
        if not self.course_description:
            return False
        
        return self.course_description.has_online_component
            
    has_online_component = property(_get_has_online_component)
    
    #20191125+
    def _get_lms_identifier(self):
        "returns the lms_identifier flag"
        
        if not self.course_description:
            return 'N/A'
        
        return self.course_description.lms_identifier
            
    lms_identifier = property(_get_lms_identifier)
    #20191125-
    
    def _coordinator_name(self):
        "returns the name for the coordinator"

        if not self.coordinator:
            return u'No Coordinator'
        
        return self.coordinator.name
            
    coordinator_name = property(_coordinator_name)

    def _lead_instructor_name(self):
        "returns the name for the lead instructor"
        
        if not self.instructor:
            return u'Instructor TBA'

        if self.instructor.name == 'MFRI Instructor' or self.instructor.name == 'MFRI Staff':
            return u'Instructor TBA'

        return self.instructor.name
            
    lead_instructor_name = property(_lead_instructor_name)

    #20170404+
    def _lead_instructor_uid(self):
        "returns the uid for the lead instructor"
        
        if not self.instructor:
            return u''

        if self.instructor.name == 'MFRI Instructor' or self.instructor.name == 'MFRI Staff':
            return u''

        return self.instructor.uid
            
    lead_instructor_uid = property(_lead_instructor_uid)
    #20170404-
    
    def _lead_instructor_email_address(self):
        "returns the email address for the lead instructor"
        
        if not self.instructor:
            return u''

        if self.instructor.name == 'MFRI Instructor' or self.instructor.name == 'MFRI Staff':
            return u''

        return self.instructor.email_address
            
    lead_instructor_email_address = property(_lead_instructor_email_address)
    
    def _lead_instructor_phone_number(self):
        "returns the phone number for the lead instructor"
        
        if not self.instructor:
            return u''

        if self.instructor.name == 'MFRI Instructor' or self.instructor.name == 'MFRI Staff':
            return u''

        phone_record = self.instructor.private_phone
        
        if phone_record:
            return phone_record.get('Primary', phone_record.get('Secondary', u''))
        
        return u''
            
    lead_instructor_phone_number = property(_lead_instructor_phone_number)

    #20170316+
    def _lead_instructor_lms_user_name(self):
        "returns the lms user name for the lead instructor"
        
        if not self.instructor:
            return None

        if self.instructor.name == 'MFRI Instructor' or self.instructor.name == 'MFRI Staff':
            return None

        return self.instructor.lms_user_name
        
    lead_instructor_lms_user_name = property(_lead_instructor_lms_user_name)

    #20170628+
    def _lead_instructor_lms_user_account_password(self):
        "returns the lms account password for the lead instructor"
        
        if not self.instructor:
            return None

        if self.instructor.name == 'MFRI Instructor' or self.instructor.name == 'MFRI Staff':
            return None

        return self.instructor.lms_user_account_password
        
    lead_instructor_lms_user_account_password = property(_lead_instructor_lms_user_account_password)

    def _lead_instructor_lms_user_name_created_date(self):
        "returns the lms account created date for the lead instructor"
        
        if not self.instructor:
            return None

        if self.instructor.name == 'MFRI Instructor' or self.instructor.name == 'MFRI Staff':
            return None

        return self.instructor.lms_user_name_created_date
        
    lead_instructor_lms_user_name_created_date = property(_lead_instructor_lms_user_name_created_date)
    #20170628-
    
    def _lead_instructor_lms_user_account_identifier(self):
        "returns the lms user name for the lead instructor"
        
        if not self.instructor:
            return None

        if self.instructor.name == 'MFRI Instructor' or self.instructor.name == 'MFRI Staff':
            return None

        return self.instructor.lms_user_account_identifier
        
    lead_instructor_lms_user_account_identifier = property(_lead_instructor_lms_user_account_identifier)
    #20170316-
    
    def _location_name(self):
        "returns the name for the location"
        
        if not self.location:
            return u'Location TBA'

        return self.location.name
            
    location_name = property(_location_name)

    def _start_date_MMDDYYY(self):
        "returns the start date in standard MM-DD-YYYY format."
        
        if not self.start_date:
            return u''

        if self.start_date == u'0000-00-00 00:00:00':
            return u''

        return self.start_date.strftime('%m-%d-%Y')
            
    start_date_MMDDYYY = property(_start_date_MMDDYYY)

    def _start_date_fancy(self):
        "returns the start date in month DD, YYYY format."
        
        if not self.start_date:
            return u''

        if self.start_date == u'0000-00-00 00:00:00':
            return u''

        return self.start_date.strftime("%B %d %Y")
            
    start_date_fancy = property(_start_date_fancy)

    #20170518
    def _registration_open_date_MMDDYYYY(self):
        "returns the registration open date in standard MM-DD-YYYY format."
        
        if not self.registration_open_date:
            return u''

        if self.registration_open_date == u'0000-00-00 00:00:00':
            return u''

        return self.registration_open_date.strftime('%m-%d-%Y')
            
    registration_open_date_MMDDYYYY = property(_registration_open_date_MMDDYYYY)

    #20170518
    def _registration_close_date_MMDDYYYY(self):
        "returns the registration close date in standard MM-DD-YYYY format."
        
        if not self.registration_close_date:
            return u''

        if self.registration_close_date == u'0000-00-00 00:00:00':
            return u''

        return self.registration_close_date.strftime('%m-%d-%Y')
            
    registration_close_date_MMDDYYYY = property(_registration_close_date_MMDDYYYY)

    #20170518
    def _registration_open_date_YYYYMMDD(self):
        "returns the registration open date in standard YYYY-MM-DD format."
        
        if not self.registration_open_date:
            return u''

        if self.registration_open_date == u'0000-00-00 00:00:00':
            return u''

        return self.registration_open_date.strftime('%Y-%m-%d')
            
    registration_open_date_YYYYMMDD = property(_registration_open_date_YYYYMMDD)

    #20170518
    def _registration_close_date_YYYYMMDD(self):
        "returns the registration close date in standard YYYY-MM-DD format."
        
        if not self.registration_close_date:
            return u''

        if self.registration_close_date == u'0000-00-00 00:00:00':
            return u''

        return self.registration_close_date.strftime('%Y-%m-%d')
            
    registration_close_date_YYYYMMDD = property(_registration_close_date_YYYYMMDD)

    def _start_day_name(self):
        "returns the start date day name."
        
        if not self.start_date:
            return u''

        if self.start_date == u'0000-00-00 00:00:00':
            return u''

        return self.start_date.strftime("%A")
            
    start_day_name = property(_start_day_name)

    def _start_month_name(self):
        "returns the start month name."
        
        if not self.start_date:
            return u''

        if self.start_date == u'0000-00-00 00:00:00':
            return u''

        return self.start_date.strftime("%B")
            
    start_month_name = property(_start_month_name)

    def _start_time(self):
        "returns the start time for the first session of the schedule class."
        
        if not self.start_date:
            return u''

        if self.start_date == u'0000-00-00 00:00:00':
            return u''

        return self.start_date.strftime('%H:%M')
            
    start_time = property(_start_time)

    def _end_date_MMDDYYY(self):
        "returns the end date in standard MM-DD-YYYY format."
        
        if not self.end_date:
            return u''

        if self.end_date == u'0000-00-00 00:00:00':
            return u''

        return self.end_date.strftime('%m-%d-%Y')
            
    end_date_MMDDYYY = property(_end_date_MMDDYYY)

    def _end_date_fancy(self):
        "returns the end date in month DD, YYYY format."
        
        if not self.end_date:
            return u''

        if self.end_date == u'0000-00-00 00:00:00':
            return u''

        return self.end_date.strftime("%B %d %Y")
            
    end_date_fancy = property(_end_date_fancy)

    def _end_month_name(self):
        "returns the end month name."
        
        if not self.end_date:
            return u''

        if self.end_date == u'0000-00-00 00:00:00':
            return u''

        return self.end_date.strftime("%B")
            
    end_month_name = property(_end_month_name)

    def _end_time(self):
        "returns the end time for the first session of the scheduled class"
        
        if not self.end_date:
            return u''

        if self.end_date == u'0000-00-00 00:00:00':
            return u''

        return self.end_date.strftime('%H:%M')
            
    end_time = property(_end_time)

    def _has_course_date_error(self):
        "returns True if the start date is after the end date or no start date"
        
        if not self.start_date:
            return True

        if self.start_date == u'0000-00-00 00:00:00':
            return True

        if not self.end_date:
            return False
        

        return (self.start_date.strftime('%Y-%m-%d') > self.end_date.strftime('%Y-%m-%d'))
            
    has_course_date_error = property(_has_course_date_error)

    def _category_and_level(self):
        "returns the category and level for the course"
        
        if not self.course_description:
            return u'No Course'

        if self.course_description.category and self.fiscal_year > '2004':
            return u'%s-%s' % (self.course_description.category, self.course_description.level)
        else:
            return u'%s' % (self.course_description.course_code)

    category_and_level = property(_category_and_level)

    def _get_approximate_course_length(self):
        "returns a the approximate length of the course days months or hours"
        
        if not self.course_description:
            return None
        
        if self.course_description.instructional_hours == 0: #20161025
            return None

        if self.course_description.instructional_hours == 1:  #20161025
            return {'type': 'hour', 'value': str(self.course_description.instructional_hours)}  #20161025

        if self.course_description.instructional_hours <= 8:
            return {'type': 'hours', 'value': str(self.course_description.instructional_hours)}  #20161025

        if (self.end_date and self.end_date != u'0000-00-00 00:00:00') and (self.start_date and self.start_date != u'0000-00-00 00:00:00'):
            delta = self.end_date - self.start_date
            course_length_days = delta.days + 1
            if course_length_days == 1:
                return {'type': 'day', 'value': str(course_length_days)}
            elif course_length_days < 30:
                return {'type': 'days', 'value': str(course_length_days)}
            else:
                months_length = (self.end_date.year - self.start_date.year)*12 + self.end_date.month - self.start_date.month
                if months_length == 1:
                    return {'type': 'month', 'value': str(months_length)}
                else:
                    return {'type': 'months', 'value': str(months_length)}
                    
        return None
            
    approximate_course_length = property(_get_approximate_course_length)

    def _regular_meeting_days(self):
        "returns the regular meeting days of the course"

        
        if self.start_date_MMDDYYY == self.end_date_MMDDYYY:
            return self.start_day_name
    
        if not self.recurring_days:
            return u'First Day: %s' % (self.start_day_name)

        recurring_days_list = self.recurring_days.split(',')
        
        approximate_course_length = self.approximate_course_length

        pluralize_day_names = False
        if approximate_course_length:
            if approximate_course_length.get('type', None) == 'days' and int(approximate_course_length.get('value', 0)) > 7:
                pluralize_day_names = True
            elif approximate_course_length.get('type', None)[:3] == 'mon':
                pluralize_day_names = True
                
        named_days = []
        for day in recurring_days_list:
            if day:
                named_days.append(u'%s,' % (expanded_day_name(day_abbreviation=day, pluralize=pluralize_day_names)))
                
        if len(named_days) > 1:
            named_days[-1] = named_days[-1][:-1]

        if len(named_days) > 1:
            named_days[-2] = named_days[-2][:-1]
            named_days.insert(-1,u'and')
        
        recurring_day_expanded =  " ".join(named_days)

        return recurring_day_expanded
    
    regular_meeting_days = property(_regular_meeting_days)

    def _regular_meeting_days_list(self):
        "returns the regular meeting days of the course"

        
        if self.start_date_MMDDYYY == self.end_date_MMDDYYY:
            return self.start_day_name
    
        if not self.recurring_days:
            return u'First Day: %s' % (self.start_day_name)

        recurring_days_list = self.recurring_days.split(',')
        
        approximate_course_length = self.approximate_course_length

        pluralize_day_names = False
        if approximate_course_length:
            if approximate_course_length.get('type', None) == 'days' and int(approximate_course_length.get('value', 0)) > 7:
                pluralize_day_names = True
            elif approximate_course_length.get('type', None)[:3] == 'mon':
                pluralize_day_names = True
                
        named_days = []
        for day in recurring_days_list:
            if day:
                named_days.append(u'%s' % (expanded_day_name(day_abbreviation=day, pluralize=pluralize_day_names)))

        recurring_day_expanded =  ", ".join(named_days)

        return recurring_day_expanded
    
    regular_meeting_days_list = property(_regular_meeting_days_list)

    #20170619
    def _mfri_office_name(self):
        "returns the mfri office name."
        
        if self.mfri_office:
            return self.mfri_office.facility_name
        else:
            return u''
            
    mfri_office_name = property(_mfri_office_name)

    #20171019
    def _mfri_office_email(self):
        "returns the mfri office email address."

        if self.mfri_office:
            mfri_office_email_address = self.mfri_office.primary_email_address

            if mfri_office_email_address == u'info@mfri.org':
                mfri_office_email_address = u'registrar@mfri.org'
            
            return mfri_office_email_address
        else:
            return u'registrar@mfri.org'
            
    mfri_office_email = property(_mfri_office_email)

    #20170619
    def _mfri_office_abbreviation(self):
        "returns the mfri office abbreviation."
        
        if self.mfri_office:
            return self.mfri_office.abbreviation
        else:
            return u''
            
    mfri_office_abbreviation = property(_mfri_office_abbreviation)

    def _office_specific_text(self):
        "returns any special text for the office running the course"
        
        if not self.course_description:
            return u''

        if self.legacy_host_section:
            if self.legacy_host_section.id == 1: #sps
                return self.course_description.sp_specific_description #20161026
            elif self.legacy_host_section.id == 2: #fops:
                return self.course_description.fp_specific_description #20161026
        
        return u''

    office_specific_text = property(_office_specific_text)

    def _needs_bls_approval(self):
        "returns true if course requires bls approval"
        
        if not self.course_description:
            return False
        
        #20171113+
        if self.course_description.category != u'EMS' and self.course_description.category != u'EMSS':
            return False
        #20171113-

        if self.course_description.is_bls:
            return True
            
        return False

    needs_bls_approval = property(_needs_bls_approval)

    def _needs_als_approval(self):
        "returns true if course requires als approval"
        
        if not self.course_description:
            return False

        #20171113+
        if self.course_description.category != u'EMS' and self.course_description.category != u'EMSS':
            return False
        #20171113-

        if self.course_description.is_als:
            return True
            
        return False

    needs_als_approval = property(_needs_als_approval)

    def _needs_pdi_approval(self):
        "returns true if course requires pdi approval"
        
        if not self.course_description:
            return False

        if self.course_description.is_pdi:
            return True
            
        return False

    needs_pdi_approval = property(_needs_pdi_approval)

    #20170518
    def _needs_other_approval(self):
        "returns true if course does not require bls, als or pdi approval"
        
        is_other = True
        if self.needs_bls_approval:
            is_other = False
        if self.needs_als_approval:
            is_other = False
        if self.needs_pdi_approval:
            is_other = False
            
        return is_other

    needs_other_approval = property(_needs_other_approval)

    #20170518
    def _late_registration_token(self):
        "returns the late registration token."
        
        if self.mfri_office:
            office_abbreviation = self.mfri_office.abbreviation
        else:
            office_abbreviation = u'mfri'
            
        if self.start_date and self.start_date != u'0000-00-00 00:00:00':
            date_string = self.start_date.strftime('%Y%m%d')
        else:
            date_string = datetime.datetime.now().strftime('%Y%m%d')

        return u'%s%s' % (office_abbreviation, date_string)
            
    late_registration_token = property(_late_registration_token)

    def _sessions_per_day(self):
        "returns default number of sessions per day"

        #if not self.course_description:
        #    return 0

        if not self.schedule_type:
            return {'week_day': 1, 'weekend': 2}
            
        schedule_defaults = self.schedule_type.schedule_defaults#UnpackJson(data_to_unpack=self.schedule_type.schedule_defaults)
        
        return {'week_day': schedule_defaults['sessions_per_week_days'], 'weekend': schedule_defaults['sessions_per_weekend']}

    sessions_per_day = property(_sessions_per_day)

    #20180226+
    def _end_email_text_agency(self):
        "returns true if course requires pdi approval"
        
        if not self.course_description:
            return u''

        if self.course_description.final_email_agency_text:
            return self.course_description.final_email_agency_text
            
        return u''

    end_email_text_agency = property(_end_email_text_agency)

    def _end_email_text_student(self):
        "returns true if course requires pdi approval"
        
        if not self.course_description:
                return u''

        if self.course_description.final_email_student_text:
            return self.course_description.final_email_student_text

        return u''

    end_email_text_student = property(_end_email_text_student)
    #20180226-

    #20181023+
    def _is_requested(self):
        "returns true if course status is course requested"
        
        if not self.schedule_status:
                return False

        if self.schedule_status.id == 2:
            return True

        return False

    is_requested = property(_is_requested)

    def _is_approved(self):
        "returns true if course status is approved"
        
        if not self.schedule_status:
                return False

        if self.schedule_status.id == 11:
            return True

        return False

    is_approved = property(_is_approved)

    def _is_confirmed(self):
        "returns true if course status is confirmed"
        
        if not self.schedule_status:
                return False

        if self.schedule_status.id == 3:
            return True

        return False

    is_confirmed = property(_is_confirmed)

    def _is_cancelled(self):
        "returns true if course status is cancelled"
        
        if not self.schedule_status:
                return False

        if self.schedule_status.id == 6:
            return True

        return False

    is_cancelled = property(_is_cancelled)
    #20181023-

    class Meta:
        db_table = u'ScheduledCourses'
        verbose_name_plural = "ScheduledCourses"
        #ordering = ['course_description', 'section_number', 'fiscal_year']
        ordering = ['course_description__category', 'course_description__level', 'section_number', 'fiscal_year']
        permissions = (
                        ('can_global_edit', 'Can edit courses regardless of office.'),
                        ('is_lms_admin', 'is lms administrator.'),
                      )
        

#20200107+
class Publicschedulesstatus(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    value = models.CharField(max_length=765, db_column='Value') 
 
    class Meta:
        db_table = u'PublicSchedulesStatus'

class Publicschedule(AppLegacyBase):
#    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    short_name = models.CharField(max_length=96, db_column='ShortName', blank=True) 

    code_name = models.CharField(max_length=255, db_column='code_name', blank=True) 

    name = models.CharField(max_length=384, db_column='Name', blank=True) 
    description = models.CharField(max_length=765, db_column='Description', blank=True) 
    
    section = models.IntegerField(null=True, db_column='SectionID', blank=True) 
    #approver = models.IntegerField(null=True, db_column='ApproverID', blank=True) 
    #contact = models.IntegerField(null=True, db_column='ContactID', blank=True) 
    #status = models.IntegerField(null=True, db_column='StatusID', blank=True) 
    status = models.ForeignKey(Publicschedulesstatus, db_column='StatusID', default=None, related_name="%(app_label)s_%(class)s_status")
    
    #lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    #lastchange = models.DateTimeField(db_column='LastChange') 
    #createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    #created = models.DateTimeField(db_column='Created') 
    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        db_table = u'PublicSchedules'

class Publicschedulelink(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    #public_schedule = models.IntegerField(null=True, db_column='PublicScheduleID', blank=True) 
    public_schedule = models.ForeignKey(Publicschedule, db_column='PublicScheduleID', default=None)
    #scheduled_course = models.IntegerField(null=True, db_column='ScheduledCourseID', blank=True) 
    scheduled_course = models.ForeignKey(Scheduledcourses, db_column='ScheduledCourseID', default=None)

    class Meta:
        db_table = u'PublicScheduleLink'


#20200107-
