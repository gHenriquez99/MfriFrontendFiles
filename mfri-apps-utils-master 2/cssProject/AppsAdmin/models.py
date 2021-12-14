from django.db import models
from django.contrib.auth.models import User

from MStaff.models import MfriInstructors
from MOffices.models import MfriOffices, LegacyCoursesection, LegacyMfriregions #20180830Jurisdictions, 



class Applications(models.Model):
    name = models.CharField(unique=True, max_length=96, db_column='Name') 
    description = models.CharField(max_length=384, db_column='Description', blank=True) 
    contactid = models.IntegerField(null=True, db_column='ContactId', blank=True) 
    cginame = models.CharField(max_length=387, db_column='CGIName', blank=True) 

    content_type_app_label = models.CharField(max_length=100, blank=True) 
     
    class Meta:
        verbose_name_plural = "Applications"
        db_table = u'Applications'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def _app_home(self):
        "returns url for app home"

        if self.cginame:
            return u'/%s' % (self.cginame)
        else:
            return "/"

    app_home = property(_app_home)

    def _is_cgi(self):
        "returns True for CGI Fals for not CGI"

        if '.cgi' in self.cginame:
            return True
        else:
            return False

    is_cgi = property(_is_cgi)


class Applinks(models.Model):
    application = models.ForeignKey(Applications, db_column='Application')    
#    application = models.IntegerField(null=True, db_column='Application', blank=True) 
    link = models.CharField(max_length=765, db_column='Link', blank=True) 
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    arguments = models.CharField(max_length=765, db_column='Arguments', blank=True) 
    menulink = models.IntegerField(null=True, db_column='MenuLink', blank=True) 
    apphomepage = models.IntegerField(null=True, db_column='AppHomePage', blank=True) 
    description = models.CharField(max_length=765, db_column='Description', blank=True) 
    requirescreate = models.IntegerField(null=True, db_column='RequiresCreate', blank=True) 
    requiresmodify = models.IntegerField(null=True, db_column='RequiresModify', blank=True) 
    requiresdelete = models.IntegerField(null=True, db_column='RequiresDelete', blank=True) 
    requiresapprove = models.IntegerField(null=True, db_column='RequiresApprove', blank=True) 
    requiresoverride = models.IntegerField(null=True, db_column='RequiresOverride', blank=True) 

    class Meta:
        verbose_name_plural = "Applinks"
        db_table = u'AppLinks'
        ordering = ['application', 'link']
        
    def __unicode__(self):
        return u'%s >> %s %s : %d' % (self.application.name, self.name, self.link, self.apphomepage)




class LegacyUsers(models.Model):
    username = models.CharField(unique=True, max_length=96, db_column='UserName') 
    fullname = models.CharField(max_length=384, db_column='FullName', blank=True) 
    password = models.CharField(max_length=96, db_column='Password') 
    email = models.CharField(max_length=765, db_column='Email') 
    permissions = models.CharField(max_length=96, db_column='Permissions') 
    applications = models.CharField(max_length=96, db_column='Applications') 
    groupid = models.IntegerField(db_column='GroupId') 
    sectionid = models.IntegerField(null=True, db_column='SectionID', blank=True) 
    regionid = models.IntegerField(null=True, db_column='RegionID', blank=True) 
    contactid = models.IntegerField(null=True, db_column='ContactID', blank=True) 
    #IsActive = models.IntegerField(null=True, db_column='IsActive', blank=True) 
    
    IsActive = models.BooleanField(default=False, db_column='IsActive', blank=True, help_text='User is active staff and allowed access to system.')
    
    instructorid = models.ForeignKey(MfriInstructors, db_column='InstructorID')
    #instructorid = models.IntegerField(null=True, db_column='InstructorID', blank=True) #20180830
    lssrmanagerid = models.IntegerField(null=True, db_column='LSSRManagerID', blank=True) 
    lssrlevelid = models.IntegerField(null=True, db_column='LSSRLevelID', blank=True) 
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 
#    ApplicationsAvailable = models.ManyToManyField(Applications, through='LegacyPermissions')

    def __unicode__(self):
        return u'%s : %s' % (self.username, self.email)

    class Meta:
        verbose_name_plural = "LegacyUsers"
        db_table = u'Users'
        ordering = ['instructorid']

    def _get_legacy_region(self):
        "returns legacy region"

        if not self.regionid:
            return None
        #return None 
        try:
            legacy_mfri_region = LegacyMfriregions.objects.get(pk = self.regionid)
        except:
            return None
        
        return legacy_mfri_region

    def _set_legacy_region(self, legacy_mfri_region=None):
        "returns sets lagacy id"

        if not legacy_mfri_region:
            return
        
        self.regionid = legacy_mfri_region.id

    legacy_region = property(_get_legacy_region, _set_legacy_region)

    def _get_legacy_section(self):
        "returns legacy section"

        if not self.sectionid:
            return None
        #return None 
        try:
            legacy_mfri_section = LegacyCoursesection.objects.get(pk = self.sectionid)
        except:
            return None
        
        return legacy_mfri_section

    def _set_legacy_section(self, legacy_mfri_section=None):
        "returns sets lagacy id"

        if not legacy_mfri_section:
            return
        
        self.sectionid = legacy_mfri_section.id

    legacy_section = property(_get_legacy_section, _set_legacy_section)

    def _get_staff_record(self):
        "returns sets lagacy id"

        if not self.instructorid:
            return None

        return self.instructorid

    staff_record = property(_get_staff_record)


class Schedpreferences(models.Model):
    userid = models.ForeignKey(LegacyUsers, db_column='UserId')
    adminreadpermission = models.IntegerField(null=True, db_column='AdminReadPermission', blank=True) 
    adminwritepermission = models.IntegerField(null=True, db_column='AdminWritePermission', blank=True) 
    globalreadpermission = models.IntegerField(null=True, db_column='GlobalReadPermission', blank=True) 
    globalwritepermission = models.IntegerField(null=True, db_column='GlobalWritePermission', blank=True) 
    activitycenterreadpermission = models.IntegerField(null=True, db_column='ActivityCenterReadPermission', blank=True) 
    activitycenterwritepermission = models.IntegerField(null=True, db_column='ActivityCenterWritePermission', blank=True) 
    sectionreadpermission = models.IntegerField(null=True, db_column='SectionReadPermission', blank=True) 
    sectionwritepermission = models.IntegerField(null=True, db_column='SectionWritePermission', blank=True) 
    primaryapprover = models.IntegerField(null=True, db_column='PrimaryApprover', blank=True) 
    fundingapprover = models.IntegerField(null=True, db_column='FundingApprover', blank=True) 
    scheduleapprover = models.IntegerField(null=True, db_column='ScheduleApprover', blank=True) 
    equivalencyclasscreator = models.IntegerField(null=True, db_column='EquivalencyClassCreator', blank=True) 
    classfoldersendpermission = models.IntegerField(null=True, db_column='ClassFolderSendPermission', blank=True) 
    classfolderreceivepermission = models.IntegerField(null=True, db_column='ClassFolderReceivePermission', blank=True) 
    classfolderclosepermission = models.IntegerField(null=True, db_column='ClassFolderClosePermission', blank=True) 
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 

#    objects = SchedpreferencesManager()
    
    def __unicode__(self):
        return u'Schedule Permissions User: %s' % (self.userid.username)

    class Meta:
        verbose_name_plural = "Schedpreferences"
        db_table = u'SchedPreferences'

class Studentregistrationpreferences(models.Model):
    userid = models.ForeignKey(LegacyUsers, db_column='UserId')
    adminreadpermission = models.IntegerField(null=True, db_column='AdminReadPermission', blank=True) 
    adminwritepermission = models.IntegerField(null=True, db_column='AdminWritePermission', blank=True) 
    gradesreadpermission = models.IntegerField(null=True, db_column='GradesReadPermission', blank=True) 
    gradeswritepermission = models.IntegerField(null=True, db_column='GradesWritePermission', blank=True) 
    affiliationreadpermission = models.IntegerField(null=True, db_column='AffiliationReadPermission', blank=True) 
    affiliationwritepermission = models.IntegerField(null=True, db_column='AffiliationWritePermission', blank=True) 
    registrationreadpermission = models.IntegerField(null=True, db_column='RegistrationReadPermission', blank=True) 
    registrationwritepermission = models.IntegerField(null=True, db_column='RegistrationWritePermission', blank=True) 
    reportspermission = models.IntegerField(null=True, db_column='ReportsPermission', blank=True) 
    importpermission = models.IntegerField(null=True, db_column='ImportPermission', blank=True) 
    exportpermission = models.IntegerField(null=True, db_column='ExportPermission', blank=True) 
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 

    def __unicode__(self):
        return u'Registration Permissions User: %s' % (self.userid.username)
    
    class Meta:
        verbose_name_plural = "Studentregistrationpreferences"
        db_table = u'StudentRegistrationPreferences'

#20210808+
class Studentrecordspreferences(models.Model):
    #id = models.IntegerField(primary_key=True, db_column='ID') 
    userid = models.ForeignKey(LegacyUsers, db_column='UserId')
    admin_read_permission = models.IntegerField(null=True, db_column='AdminReadPermission', blank=True) 
    admin_write_permission = models.IntegerField(null=True, db_column='AdminWritePermission', blank=True) 
    id_read_permission = models.IntegerField(null=True, db_column='IDReadPermission', blank=True) 
    id_write_permission = models.IntegerField(null=True, db_column='IDWritePermission', blank=True) 
    private_read_permission = models.IntegerField(null=True, db_column='PrivateReadPermission', blank=True) 
    private_write_permission = models.IntegerField(null=True, db_column='PrivateWritePermission', blank=True) 
    contact_read_permission = models.IntegerField(null=True, db_column='ContactReadPermission', blank=True) 
    contact_write_permission = models.IntegerField(null=True, db_column='ContactWritePermission', blank=True) 
    affiliation_read_permission = models.IntegerField(null=True, db_column='AffiliationReadPermission', blank=True) 
    affiliation_write_permission = models.IntegerField(null=True, db_column='AffiliationWritePermission', blank=True) 
    flags_read_permission = models.IntegerField(null=True, db_column='FlagsReadPermission', blank=True) 
    flags_write_permission = models.IntegerField(null=True, db_column='FlagsWritePermission', blank=True) 
    import_permission = models.IntegerField(null=True, db_column='ImportPermission', blank=True) 
    export_permission = models.IntegerField(null=True, db_column='ExportPermission', blank=True) 
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 

    def __unicode__(self):
        return u'Student Records Permissions User: %s' % (self.userid.username)
    
    class Meta:
        verbose_name_plural = "StudentRecordsPreferences"
        db_table = u'StudentRecordsPreferences'

#20210808-

#20190816+
class Instpreferences(models.Model):
    userid = models.ForeignKey(LegacyUsers, db_column='UserId')
    globaleditpermissions = models.IntegerField(null=True, db_column='GlobalEditPermissions', blank=True) 
    officeeditpermissions = models.CharField(max_length=66, db_column='OfficeEditPermissions', blank=True) 
    sendemail = models.IntegerField(null=True, db_column='SendEmail', blank=True) 
    reademail = models.IntegerField(null=True, db_column='ReadEmail', blank=True) 
    adminreadpermission = models.IntegerField(null=True, db_column='AdminReadPermission', blank=True) 
    adminwritepermission = models.IntegerField(null=True, db_column='AdminWritePermission', blank=True) 
    reportspermission = models.IntegerField(null=True, db_column='ReportsPermission', blank=True) 
    idreadpermission = models.IntegerField(null=True, db_column='IDReadPermission', blank=True) 
    idwritepermission = models.IntegerField(null=True, db_column='IDWritePermission', blank=True) 
    privatereadpermission = models.IntegerField(null=True, db_column='PrivateReadPermission', blank=True) 
    privatewritepermission = models.IntegerField(null=True, db_column='PrivateWritePermission', blank=True) 
    contactreadpermission = models.IntegerField(null=True, db_column='ContactReadPermission', blank=True) 
    contactwritepermission = models.IntegerField(null=True, db_column='ContactWritePermission', blank=True) 
    mailingaddressreadpermission = models.IntegerField(null=True, db_column='MailingAddressReadPermission', blank=True) 
    mailingaddresswritepermission = models.IntegerField(null=True, db_column='MailingAddressWritePermission', blank=True) 
    employmentreadpermission = models.IntegerField(null=True, db_column='EmploymentReadPermission', blank=True) 
    employmentwritepermission = models.IntegerField(null=True, db_column='EmploymentWritePermission', blank=True) 
    homeofficewritepermissions = models.IntegerField(null=True, db_column='HomeOfficeWritePermissions', blank=True) 
    payratereadpermission = models.IntegerField(null=True, db_column='PayRateReadPermission', blank=True) 
    payratewritepermission = models.IntegerField(null=True, db_column='PayRateWritePermission', blank=True) 
    driverslicenseprivatereadpermission = models.IntegerField(null=True, db_column='DriversLicensePrivateReadPermission', blank=True) 
    driverslicensereadpermission = models.IntegerField(null=True, db_column='DriversLicenseReadPermission', blank=True) 
    instructordetailsreadpermission = models.IntegerField(null=True, db_column='InstructorDetailsReadPermission', blank=True) 
    driverslicenseprivatewritepermission = models.IntegerField(null=True, db_column='DriversLicensePrivateWritePermission', blank=True) 
    securityreadpermission = models.IntegerField(null=True, db_column='SecurityReadPermission', blank=True) 
    securitywritepermission = models.IntegerField(null=True, db_column='SecurityWritePermission', blank=True) 
    driverslicensewritepermission = models.IntegerField(null=True, db_column='DriversLicenseWritePermission', blank=True) 
    instructordetailswritepermission = models.IntegerField(null=True, db_column='InstructorDetailsWritePermission', blank=True) 
    instructorteachinghoursreadpermission = models.IntegerField(null=True, db_column='InstructorTeachingHoursReadPermission', blank=True) 
    instructorteachinghourswritepermission = models.IntegerField(null=True, db_column='InstructorTeachingHoursWritePermission', blank=True) 
    skillsreadpermission = models.IntegerField(null=True, db_column='SkillsReadPermission', blank=True) 
    skillswritepermission = models.IntegerField(null=True, db_column='SkillsWritePermission', blank=True) 
    facultywritepermissions = models.IntegerField(null=True, db_column='FacultyWritePermissions', blank=True) 
    facultyreadpermissions = models.IntegerField(null=True, db_column='FacultyReadPermissions', blank=True) 
    teachingspecialtyreadpermission = models.IntegerField(null=True, db_column='TeachingSpecialtyReadPermission', blank=True) 
    teachingspecialtywritepermission = models.IntegerField(null=True, db_column='TeachingSpecialtyWritePermission', blank=True) 
    medicalexamreadpermission = models.IntegerField(null=True, db_column='MedicalExamReadPermission', blank=True) 
    medicalexamwritepermission = models.IntegerField(null=True, db_column='MedicalExamWritePermission', blank=True) 
    medicalexamprivatereadpermission = models.IntegerField(null=True, db_column='MedicalExamPrivateReadPermission', blank=True) 
    medicalexamprivatewritepermission = models.IntegerField(null=True, db_column='MedicalExamPrivateWritePermission', blank=True) 
    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(db_column='LastChange') 
    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 

    def __unicode__(self):
        return u'Staff List Permissions User: %s' % (self.userid.username)
    
    class Meta:
        verbose_name_plural = "Instpreferences"
        db_table = u'InstPreferences'
#20190816-

class LegacyPermissionsManager(models.Manager):
    
    def Permission_Student_Registration(self, user_id): 
        return self.get(appid__exact=33, userid__exact=user_id)

    def Permission_Instructor_List(self, user_id): 
        return self.get(appid__exact=26, userid__exact=user_id)

    def Permission_Transcript(self, user_id): 
        return self.get(appid__exact=27, userid__exact=user_id)

    def Permission_Course_Registration(self, user_id): 
        return self.get(appid__exact=15, userid__exact=user_id)

    def Permission_Scheduled_Course(self, user_id): 
        return self.get(appid__exact=6, userid__exact=user_id)

class LegacyPermissions(models.Model):
    userid = models.ForeignKey(LegacyUsers, db_column='UserId')
    appid = models.ForeignKey(Applications, db_column='AppID')
#    userid = models.IntegerField(null=True, db_column='UserId', blank=True) 
#    appid = models.IntegerField(null=True, db_column='AppID', blank=True) 
    readpermission = models.IntegerField(null=True, db_column='ReadPermission', blank=True) 
    createpermission = models.IntegerField(null=True, db_column='CreatePermission', blank=True) 
    modifypermission = models.IntegerField(null=True, db_column='ModifyPermission', blank=True) 
    deletepermission = models.IntegerField(null=True, db_column='DeletePermission', blank=True) 
    approvepermission = models.IntegerField(null=True, db_column='ApprovePermission', blank=True) 
    overridepermission = models.IntegerField(null=True, db_column='OverridePermission', blank=True) 

    objects = LegacyPermissionsManager()

    def __unicode__(self):
        username = self.userid.username
        appid_name = self.appid.name
        appid_cginame = self.appid.cginame
        
        user_name = u'Unknown User'
        app_name = u'Unknown App'
        app_cgi = u'Unknown App CGI'
        
        if self.userid:
            user_name = self.userid.username

        if self.appid:
            app_name = self.appid.name
            app_cgi = self.appid.cginame
        
        return u'{"user": "%s", "name":"%s", "link":"%s"}' % (user_name, app_name, app_cgi)
#        return u'%s : %s Permission: %d' % (self.userid.username, self.appid.name, self.readpermission)
    
    class Meta:
        verbose_name_plural = "LegacyPermissions"
        db_table = u'Permissions'


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='+')#20180904
#    total_points = models.IntegerField()
    WorkingOffice = models.ForeignKey(MfriOffices)
    #WorkingOffice = models.IntegerField(null=True, db_column='WorkingOffice_id', blank=True) #20180830
    LegacyUserData = models.ForeignKey(LegacyUsers)
#    StaffDBEntry = models.ForeignKey(MfriInstructors)
    
#    ApplicationsAvailable = models.ManyToManyField(Applications, through='LegacyPermissions')
#    ApplicationsAvailable = models.ForeignKey(Applications)
    
    def __unicode__(self):
        return u'New User: %s - Legacy User: %s' % (self.user.username, self.LegacyUserData.username)

    class Meta:
#        app_label = 'AppsAdmin'
        permissions = (
                        ('can_change_pw', 'Can change password'),
                        ('can_edit_profile', 'Can edit User Profile'),
                      )
        ordering = ['user']


    def _get_full_name(self):
        "returns the full name FN MN LN S"
        
        if not self.LegacyUserData:
            return None

        staff_record = getattr(self.LegacyUserData, 'staff_record', None)
        
        if staff_record:
#            bob = getattr(staff_record, 'name', self.LegacyUserData.fullname)
#            assert False
            return getattr(staff_record, 'name', self.LegacyUserData.fullname)
        else:
            return self.LegacyUserData.fullname
#        ReturnedName = ''
#        if len(self.LegacyUserData.first_name) > 0:
#            ReturnedName += self.LegacyUserData.first_name
#    
#        if len(self.LegacyUserData.middle_name) > 0:
#            if len(ReturnedName) > 0:
#                ReturnedName += ' '
#                
#            ReturnedName += self.LegacyUserData.middle_name
#            
#        if len(self.LegacyUserData.last_name) > 0:
#            if len(ReturnedName) > 0:
#                ReturnedName += ' '
#    
#            ReturnedName += self.LegacyUserData.last_name
#    
#        if len(self.LegacyUserData.suffix) > 0:
#            if len(ReturnedName) > 0:
#                ReturnedName += ' '
#    
#            ReturnedName += self.LegacyUserData.suffix
#        
#        return ReturnedName
    
    def _set_full_name(self, RawFullName):
        "sets name parts with the given full name"
        NewFullName = RawFullName.strip()
    
        SuffixValues = set(['JR', 'SR', 'I', 'II', 'III', 'IV'])
    
        if NewFullName.find(',') >= 0: #name contains a comma (,) so is probably reversed
            NameParts = NewFullName.split(',', 1)
    
            NewFullName = NameParts[1].strip() + " " + NameParts[0].strip()
    
        NameTokens = NewFullName.split(' ')
    
        suffix_name = None
        first_name = NameTokens[0].strip()
        middle_name = NameTokens[1].strip()
    
        if NameTokens[-1].upper().replace('.', ' ').strip() in SuffixValues:
            suffix_name = NameTokens[-1].upper().replace('.', ' ').strip()
            last_name = " ".join(NameTokens[2: -1])
        else:
            last_name = " ".join(NameTokens[2:])
    
        if len(last_name) == 0:
            if len(middle_name) > 0:
                last_name = middle_name
                middle_name = ''
            else:
                last_name = first_name
                first_name = ''
    
        if len(middle_name) > 0:
            self.LegacyUserData.fullname = u'%s %s %s' % (first_name, middle_name, last_name)
        else:
            self.LegacyUserData.fullname = u'%s %s' % (first_name, last_name)
            
            
        if suffix_name:
            self.LegacyUserData.fullname = u'%s %s' % (self.LegacyUserData.fullname, suffix_name)
            
    full_name = property(_get_full_name, _set_full_name)

    def _get_full_name_reversed(self):
        "returns the full name LN S, FN MN"
        ReturnedName = ''
        if self.LegacyUserData and self.LegacyUserData.last_name and len(self.LegacyUserData.last_name) > 0:
            ReturnedName += self.LegacyUserData.last_name
    
        if self.suffix and len(self.LegacyUserData.suffix) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.LegacyUserData.suffix
    
        if len(ReturnedName) > 0:
            ReturnedName += ','
    
        if self.LegacyUserData and self.LegacyUserData.first_name and len(self.LegacyUserData.first_name) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.LegacyUserData.first_name
    
        if self.LegacyUserData and self.LegacyUserData.middle_name and len(self.LegacyUserData.middle_name) > 0:
            if len(ReturnedName) > 0:
                ReturnedName += ' '
    
            ReturnedName += self.LegacyUserData.middle_name
    
    
        return ReturnedName
    
    full_name_reversed = property(_get_full_name_reversed)
    
    def _get_email(self):
        "returns the email address"
        
        #return u'%'
        staff_record = getattr(self.LegacyUserData, 'staff_record', None)

        if staff_record:
            user_staff_record_official_email = user_staff_record.official_email
            if not user_staff_record_official_email:
                return user.email
            return user_staff_record_official_email.get('Primary', user_staff_record_official_email.get('Secondary', self.user.email))
        
        return self.LegacyUserData.email
    
    email = property(_get_email)
    
    def _get_staff_record(self):
        "returns sets lagacy id"

        if not self.LegacyUserData:
            return None

        return self.LegacyUserData.staff_record

    staff_record = property(_get_staff_record)
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

