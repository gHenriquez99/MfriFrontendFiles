import decimal

from django.db import models
from MOffices.models import MfriOffices, LegacyCoursesection 

from AppLegacyBase.models import AppLegacyBase

STANDARD_SESSION_HOURS = 3

class TCode(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    value = models.CharField(max_length=765, db_column='Value', blank=True) 

    def __unicode__(self):
        return u'%s %s' %  (self.name, self.value)
    
    class Meta:
        db_table = u'TCodes'
        verbose_name_plural = "TCodes"
        ordering = ['name']

    def _full_name(self):
        "returns full name"

        return u'%s %s' %  (self.name, self.value)

    full_name = property(_full_name)

class Coursecategorytypes(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'CourseCategoryTypes'
        verbose_name_plural = "Coursecategorytypes"
        ordering = ['name']

class Coursetypes(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'CourseTypes'
        verbose_name_plural = "Coursetypes"
        ordering = ['name']

class Coursecategories(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    description = models.CharField(max_length=765, db_column='Description', blank=True) 
    typeid = models.ForeignKey(Coursecategorytypes, db_column='TypeID')

    def __unicode__(self):
        return self.name
        #return u'%s %s' % (self.name, self.typeid.name)

    class Meta:
        db_table = u'CourseCategories'
        verbose_name_plural = "Coursecategories"
        ordering = ['name']

class Coursefundingsources(models.Model):
    name = models.CharField(max_length=25, db_column='Name', blank=True) 
    code = models.CharField(max_length=1, db_column='Code', blank=True) 

    def __unicode__(self):
        return u'%s : %s' % (self.code, self.name)

    class Meta:
        db_table = u'CourseFundingSources'
        verbose_name_plural = "Coursefundingsources"
        ordering = ['code']


class Coursestatus(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    is_current_edition = models.BooleanField(default=False, blank=True, help_text='This type shows the current edition.')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'CourseStatus'
        verbose_name_plural = "Coursestatus"
        ordering = ['name']


class Coursesponsors(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'CourseSponsors'
        verbose_name_plural = "Coursesponsors"
        ordering = ['name']

LMS_OPTION_CHOICES = (
                    ('ABS', 'Absorb LMS'),
                    ('UMDCNV', 'UMD Canvas'),
                    ('MYBL', 'My Brady Lab'),
                    ('N/A', 'Not Applicable'),
                    )

class Coursedescriptions(AppLegacyBase):
    abbreviation = models.CharField(max_length=96, db_column='Abbr', blank=True) 
    course_code = models.CharField(max_length=96, db_column='CourseCode', blank=True) 

    category_lookup = models.ForeignKey(Coursecategories, db_column='CategoryID')
    
    category = models.CharField(max_length=96, db_column='Category', blank=True) 
    level = models.CharField(max_length=15, db_column='Level', blank=True) 
    
    name = models.CharField(max_length=765, db_column='Title', blank=True) 
    ace_code = models.CharField(max_length=765, db_column='ACECode', blank=True) 
    nfa_code = models.CharField(max_length=765, db_column='NFACode', blank=True) 
    
    total_hours = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='TotalHours', blank=True) 

    instructional_hours = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='InstructionalHours', blank=True) 

    track_count = models.IntegerField(default=1, null=True, blank=True, help_text='Usual number of simultaneous tracks for course, usually 1.') 

    module_count = models.IntegerField(default=1, null=True, db_column='ModuleCount', blank=True, help_text='Number of modules for course, usually 1.') 

    has_session_zero = models.BooleanField(default=False, blank=True, help_text='This course usually is scheduled with a session zero.')

    session_length_hours = models.IntegerField(default=3, null=True, blank=True, help_text='Standard length of a session in hours, usually 3.') 

    session_count = models.IntegerField(default=0, null=True, blank=True, help_text='Number of sessions for course.') 

    session_in_modules = models.CharField(max_length=765, blank=True, help_text='List of sessions in each module, format: 1,2,3|4,5,6') 

    use_session_registration = models.BooleanField(default=False, blank=True, help_text='Allow students to register for individual sessions.')

    in_state_fee = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='InStateFee', blank=True) 
    out_state_fee = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='OutStateFee', blank=True) 
    min_students = models.IntegerField(null=True, db_column='MinStudents', blank=True) 
    max_students = models.IntegerField(null=True, db_column='MaxStudents', blank=True) 

    course_section = models.ForeignKey(LegacyCoursesection, db_column='coursesectionid', null=True, blank=True)
        
    description = models.TextField(db_column='Description', blank=True) 
    ace_description = models.TextField(db_column='ACEDescription', blank=True) 

    prerequisites = models.TextField(db_column='Prerequisites', blank=True) 

    fp_specific_description = models.TextField(db_column='FPProcedures', blank=True) 
    sp_specific_description = models.TextField(db_column='SPProcedures', blank=True) 

    registration_message = models.TextField(db_column='RegistrationMessage', blank=True) 
    registration_email_text = models.TextField(db_column='RegistrationEmailText', blank=True) 

    final_email_agency_text  = models.TextField(blank=True, help_text='Text to add to email sent to affiliation agency sponsoring student at end of course.')#20180226
    final_email_student_text = models.TextField(blank=True, help_text='Text to add to email sent to student at end of course.')#20180226

    course_type = models.ForeignKey(Coursetypes, db_column='TypeID')

    course_sponsor = models.ForeignKey(Coursesponsors, db_column='SponsorID')
    
    status = models.ForeignKey('Coursestatus', db_column='StatusID')

    developer_name = models.CharField(max_length=765, db_column='developer_name', blank=True) #20210624
    developer_email = models.CharField(max_length=765, db_column='developer_email', blank=True) #20210624
    
    show_in_catalog = models.BooleanField(default=True, blank=True, help_text='Show this course description in course catalog.')

    has_sim_center_component = models.BooleanField(default=False, blank=True, help_text='Has Sim Center component.')
    has_online_component = models.BooleanField(default=False, blank=True, help_text='Has online component.')

    pay_override = models.DecimalField(decimal_places=2, max_digits=4, default=decimal.Decimal('0.00'), help_text='Override Pay for Lead Instructor.', blank=True, null=True)  #20210624

    lms_identifier = models.CharField(max_length=6, choices=LMS_OPTION_CHOICES, blank=False, default='N/A')

    is_sps_only = models.BooleanField(default=False, blank=True, help_text='Only used by SPS.')

    is_bls = models.BooleanField(default=False, blank=True, help_text='If EMS course, it is open to students with BLS credentials.')
    is_als = models.BooleanField(default=False, blank=True, help_text='If EMS course, it is open to students with ALS credentials.')

    is_pdi = models.BooleanField(default=False, blank=True, help_text='If Instructor course, it is open only to MICRB instructors.')

    acknowledge_physical_requirements = models.BooleanField(default=False, blank=True, help_text='Require student to acknowledge physical requirements of course.')

    physical_requirements = models.TextField(blank=True)

    show_on_transcript = models.BooleanField(default=False, blank=True, db_column='ShowOnTranscript', help_text='This course will appear on student transcripts.')

    require_program_evaluations = models.BooleanField(default=False, blank=True, db_column='NeedProgramEvaluations', help_text='This program reuires Program Evaluation Forms from students.')

    resource_fee = models.DecimalField(decimal_places=2, null=True, max_digits=10, db_column='ResourceFee', blank=True) 

    t_code = models.ForeignKey(TCode, db_column='TCodeID')
    
    internal_note = models.TextField(db_column='Notes', blank=True) 

    edition_date = models.DateField(null=True, db_column='EditionDate', blank=True) 
    edition_name = models.CharField(max_length=765, db_column='EditionName', blank=True) 

    require_medical_clearance = models.BooleanField(default=False, blank=True, db_column='RequireMedicalClearance', help_text='This course requires medical clearance for students.')
    medical_clearance_note = models.CharField(max_length=255, db_column='MedicalClearanceNote', blank=True) 
    
    
    #lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    #lastchange = models.DateTimeField(db_column='LastChange') 
    #createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    #created = models.DateTimeField(db_column='Created') 

    def __unicode__(self):
        
        if not self.category:
            return u'%s %s' % (self.course_code, self.name)
        else:
            if self.edition_date:#20170512
                if self.edition_name:
                    return u'%s-%s %s %s %s' % (self.category, self.level, self.name, self.edition_date.strftime('%m-%d-%Y'), self.edition_name)

                return u'%s-%s %s %s' % (self.category, self.level, self.name, self.edition_date.strftime('%m-%d-%Y'))
                    
            return u'%s-%s %s' % (self.category, self.level, self.name)

    def save(self, **kwargs): 
        if not self.in_state_fee:
            self.in_state_fee = 0.00

        if not self.out_state_fee:
            self.out_state_fee = 0.00
            
        super(Coursedescriptions, self).save(**kwargs)

    class Meta:
        db_table = u'CourseDescriptions'
        verbose_name_plural = "Coursedescriptions"
        ordering = ['category', 'level', 'edition_date']


    def _category_level(self):
        "returns category and level of course"

        if not self.category:
            if self.category_lookup:
                category = self.category_lookup.name
                
                if category and self.level:
                    return u'%s-%s' % (category, self.level)
                else:
                    return u''
            else:
                if self.level:
                    return u'%s' % (self.level)
                else:
                    return u''
        else:
            if self.level:
                return u'%s-%s' % (self.category, self.level)
            else:
                return u'%s' % (self.category)

    category_level = property(_category_level)

    def _full_name(self):
        "returns full name of course"

        if not self.category:
            if self.edition_date:
                return u'%s %s %s' % (self.course_code, self.name, self.edition_date.strftime('%m-%d-%Y'))
            else:
                return u'%s %s' % (self.course_code, self.name)
        else:
            if self.edition_date:
                return u'%s-%s %s %s' % (self.category, self.level, self.name, self.edition_date.strftime('%m-%d-%Y'))
            else:
                return u'%s-%s %s' % (self.category, self.level, self.name)

    full_name = property(_full_name)

    def _edition(self):
        "returns category and level of course"

        if self.edition_date:
            if self.edition_name:
                return u'%s %s' % (self.edition_date.strftime('%m-%d-%Y'), self.edition_name)
            else:
                return self.edition_date.strftime('%m-%d-%Y')

    edition = property(_edition)

    def _course_sessions_count(self):
        "returns number of sessions in course"

        if self.session_count and self.session_count > 0:
            return self.session_count
        else:
            if self.instructional_hours and self.instructional_hours > 0:
                return self.instructional_hours / STANDARD_SESSION_HOURS
            
            return 0

    course_sessions_count = property(_course_sessions_count)

    def _sessions_in_module(self, module_number=None):
        "returns list of sessions numbers in module"

        if self.module_number and self.module_number > 0:
            module_list = self.session_in_modules.split('|')

            if not module_list:
                return None
            
            for sessions in module_list:
                module_number -= 1
                if module_number == 0:
                    return sessions
                
        return None

    sessions_in_module = property(_sessions_in_module)

    def _course_prerequisite(self, module_number=None):
        "returns course_prerequisites"

        if self.prerequisites:
            return u'Prerequisite for this class: %s' % (self.prerequisites)

        return None

    course_prerequisite = property(_course_prerequisite)

    def _get_require_medical_clearance_label(self):
        "returns the the medical clearance label"
        
        medical_clearance_label = u''
        
        if self.require_medical_clearance:
            medical_clearance_label = u'(Requires Medical Clearance)'

        return medical_clearance_label

    medical_clearance_label = property(_get_require_medical_clearance_label)

    def _get_lms_type_label(self):
        "returns the lms identifier label"
        
        if self.lms_identifier:
            return self.get_lms_identifier_display()

        return u'' #20200115

    lms_type_label = property(_get_lms_type_label)

    def _get_has_online_component_label(self):
        "returns the has online component label"
        
        if self.has_online_component:
            return u'Has online component.'

        return u''

    has_online_component_label = property(_get_has_online_component_label)




