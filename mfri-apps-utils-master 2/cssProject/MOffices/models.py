import datetime

from django.db import models

class Phonenumbertypes(models.Model):
    name = models.CharField(max_length=11, db_column='Name', blank=True) 

    class Meta:
        db_table = u'PhoneNumberTypes'
        verbose_name_plural = "PhoneNumberTypes"
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)

    def _get_spaceless_name(self):
        "returns the name with whitespace removed"
        
        if not self.name:
            return u''
        
        return "".join(self.name.split())

    name_spaceless = property(_get_spaceless_name)

class LegacyMfriregions(models.Model):
    regionnumber = models.IntegerField(null=True, db_column='RegionNumber', blank=True) 
    name = models.CharField(max_length=240, db_column='Name', blank=True) 
    abbreviation = models.CharField(max_length=30, db_column='Abbreviation', blank=True) 
    county = models.CharField(max_length=765, db_column='County', blank=True) 
    streetaddress1 = models.CharField(max_length=765, db_column='StreetAddress1', blank=True) 
    streetaddress2 = models.CharField(max_length=765, db_column='StreetAddress2', blank=True) 
    postaladdress1 = models.CharField(max_length=765, db_column='PostalAddress1', blank=True) 
    postalstreetaddress2 = models.CharField(max_length=765, db_column='PostalStreetAddress2', blank=True) 
    city = models.CharField(max_length=765, db_column='City', blank=True) 
    state = models.CharField(max_length=765, db_column='State', blank=True) 
    postcode = models.CharField(max_length=765, db_column='PostCode', blank=True) 
    primaryphonenumber = models.CharField(max_length=765, db_column='PrimaryPhoneNumber', blank=True) 
    secondaryphonenumber = models.CharField(max_length=765, db_column='SecondaryPhoneNumber', blank=True) 
    metrophonenumber = models.CharField(max_length=765, db_column='MetroPhoneNumber', blank=True) 
    tollfreephonenumber = models.CharField(max_length=765, db_column='TollFreePhoneNumber', blank=True) 
    faxnumber = models.CharField(max_length=765, db_column='FaxNumber', blank=True) 
    email = models.CharField(max_length=765, db_column='Email', blank=True) 
    url = models.CharField(max_length=765, db_column='URL', blank=True) 
    contactid = models.IntegerField(null=True, db_column='ContactID', blank=True) 
    
    class Meta:
        db_table = u'MFRIRegions'
        verbose_name_plural = "LegacyMfriregions"
        ordering = ['name']
        
    def __unicode__(self):
        return u'%s %s' % (self.name, self.abbreviation)

class LegacyCoursesection(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    abbreviation = models.CharField(max_length=30, db_column='Abbreviation', blank=True) 
    
    class Meta:
        db_table = u'CourseSection'
        verbose_name_plural = "LegacyCoursesections"
        ordering = ['name']

    def __unicode__(self):
        return u'%s %s' % (self.name, self.abbreviation)


class Jurisdictiontypes(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    
    class Meta:
        db_table = u'JurisdictionTypes'
        verbose_name_plural = "Jurisdictiontypes"
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)
    
class Jurisdictions(models.Model):
    name = models.CharField(max_length=765, db_column='Name') 
    number = models.CharField(max_length=30, db_column='Number', blank=True) 
    #typeid = models.IntegerField(null=True, db_column='TypeID', blank=True) 
    jurisdiction_type = models.ForeignKey('Jurisdictiontypes', db_column='TypeID')
    mfri_region_number = models.IntegerField(null=True, db_column='MfriRegionID', blank=True) 

    mfri_office = models.ForeignKey('MfriOffices', null=True, blank=True, help_text='The MFRI office serving this jurisdiction.')

    sort_order = models.IntegerField(null=True, db_column='SortOrder', blank=True) 
    special_type = models.BooleanField(default=False, help_text='This listing is a special type and so hide the type name.')
    
    class Meta:
        db_table = u'Jurisdictions'
        verbose_name_plural = "Jurisdictions"
        ordering = ['sort_order', 'name', 'jurisdiction_type__name']

    def __unicode__(self):
        if self.special_type:
            return u'%s' % (self.name)
        else:
            return u'%s %s' % (self.name, self.jurisdiction_type.name)

    def _get_full_name(self):
        "returns the complete name for the jurisdiction"
        
        if self.special_type:
            return u'%s' % (self.name)
        else:
            return u'%s %s' % (self.name, self.jurisdiction_type.name)

    full_name = property(_get_full_name)

    
class MfriOffices(models.Model):
    regionnumber = models.IntegerField(null=True, db_column='RegionNumber', help_text='Number of Region, must be a number.', blank=True) 
    name = models.CharField(max_length=240, db_column='Name', help_text='Name of region, limit 240 characters.', blank=False) 
    abbreviation = models.CharField(max_length=30, db_column='Abbreviation', help_text='Abbreviation or short name for region, limit 30 characters (should be less than 6).', blank=False) 
    
    frsnumber = models.CharField(max_length=10, db_column='FRSNumber', help_text='FRS Number, limit 10 characters.', blank=True) 

    is_payroll_processor = models.BooleanField(default=False, help_text='Office processes payroll through MITTS')
    
    is_department = models.BooleanField(default=True, help_text='Office is an organizational department.')

    is_registration_processor = models.BooleanField(default=True, help_text='Office processes student registrations.')

    is_statewide = models.BooleanField(default=True, help_text='Office operates statewide not just in a region.')#20161121

    sort_order = models.IntegerField(default=0, help_text='Sort Order in Directory')

    internal_note = models.TextField(blank=True, help_text='Optional notes for internal use.')

    public_note = models.TextField(blank=True, help_text='Optional notes for the public office directory.')

    public_alert_text = models.TextField(blank=True, help_text='Optional alert note for the public office directory, which will be highlighted.') #20200821

    public_schedule_note = models.TextField(blank=True, help_text='Optional notes for the public schedule for this office.') #20200821

    public_schedule_alert_text = models.TextField(blank=True, help_text='Optional alert note for the public schedule for this office, which will be highlighted.') #20200821

    default_send_alert_email_to_office_before_approval = models.BooleanField(default=False, help_text='Send registration request email alert to region at time of registration before training officer approval.')
    default_send_alert_email_to_office_after_approval = models.BooleanField(default=True, help_text='Send registration request email alert to region after training officer approval.')

    street_address1 = models.CharField(max_length=765, db_column='StreetAddress1', help_text='Street Address.', blank=True) 
    street_address2 = models.CharField(max_length=765, db_column='StreetAddress2', blank=True) 
    street_city = models.CharField(max_length=765, db_column='StreetCity', blank=True) 
    street_state = models.CharField(max_length=765, db_column='StreetState', blank=True) 
    street_postcode = models.CharField(max_length=60, db_column='StreetPostCode', blank=True) 

    postal_address1 = models.CharField(max_length=765, db_column='PostalAddress1', help_text='Mailing Address.', blank=True) 
    postal_address2 = models.CharField(max_length=765, db_column='PostalAddress2', blank=True) 
    postal_city = models.CharField(max_length=765, db_column='PostalCity', blank=True) 
    postal_state = models.CharField(max_length=765, db_column='PostalState', blank=True) 
    postal_postcode = models.CharField(max_length=60, db_column='PostalPostCode', blank=True) 
    
    phone_number1_type = models.ForeignKey('Phonenumbertypes', db_column='PhoneNumber1TypeID', related_name="+")
    
    phone_number1 = models.CharField(max_length=96, db_column='PhoneNumber1', blank=True) 
    
    phone_number2_type = models.ForeignKey('Phonenumbertypes', db_column='PhoneNumber2TypeID', related_name="+")
    phone_number2 = models.CharField(max_length=96, db_column='PhoneNumber2', blank=True) 
    
    phone_number3_type = models.ForeignKey('Phonenumbertypes', db_column='PhoneNumber3TypeID', related_name="+")
    phone_number3 = models.CharField(max_length=96, db_column='PhoneNumber3', blank=True) 
    
    phone_number4_type = models.ForeignKey('Phonenumbertypes', db_column='PhoneNumber4TypeID', related_name="+")
    phone_number4 = models.CharField(max_length=96, db_column='PhoneNumber4', blank=True) 
    
    phone_number5_type = models.ForeignKey('Phonenumbertypes', db_column='PhoneNumber5TypeID', related_name="+")
    phone_number5 = models.CharField(max_length=96, db_column='PhoneNumber5', blank=True) 

    primary_email = models.CharField(max_length=765, db_column='PrimaryEmail', blank=True) 
    secondary_email = models.CharField(max_length=765, db_column='SecondaryEmail', blank=True) 

    parent_location = models.ForeignKey('self', db_column='LocationOfficeID', null=True, blank=True, related_name="hosted_offices")
    parent_department = models.ForeignKey('self', db_column='parentofficeid', null=True, blank=True, related_name="reporting_offices")

    recordstatusid = models.IntegerField(null=True, default=1, db_column='RecordStatusID', blank=True) 
    lastchangeby = models.CharField(null=True, max_length=96, db_column='LastChangeBy', blank=True) 
    lastchange = models.DateTimeField(blank=True, db_column='LastChange') 
    createdby = models.CharField(null=True, max_length=96, db_column='CreatedBy', blank=True) 
    created = models.DateTimeField(blank=True, db_column='Created') 

    def __unicode__(self):
        return self.long_facility_name

    class Meta:
        verbose_name_plural = "MfriOffices"
        db_table = u'MFRIOffices'
        ordering = ['regionnumber', 'name']
        

    def _get_main_numbers(self):
        "returns the contact numbers for office"
        ReturnedNumber = {}
        
        if self.phone_number1_type and self.phone_number1_type != 'None' and self.phone_number1:
            ReturnedNumber[self.phone_number1_type.name_spaceless] = self.phone_number1
    
        if self.phone_number2_type and self.phone_number2_type != 'None' and self.phone_number2:
            ReturnedNumber[self.phone_number2_type.name_spaceless] = self.phone_number2
        
        if self.phone_number3_type and self.phone_number3_type != 'None' and self.phone_number3:
            ReturnedNumber[self.phone_number3_type.name_spaceless] = self.phone_number3
        
        if self.phone_number4_type and self.phone_number4_type != 'None' and self.phone_number4:
            ReturnedNumber[self.phone_number4_type.name_spaceless] = self.phone_number4
        
        if self.phone_number5_type and self.phone_number5_type != 'None' and self.phone_number5:
            ReturnedNumber[self.phone_number5_type.name_spaceless] = self.phone_number5

        return ReturnedNumber

    office_phone_numbers = property(_get_main_numbers)

    def _get_fax_number(self):
        "returns the fax number for office"
        ReturnedNumber = u''

        if self.phone_number1_type and self.phone_number1_type.name == 'Fax':
            ReturnedNumber = self.phone_number1
    
        if self.phone_number2_type and self.phone_number2_type.name == 'Fax':
            ReturnedNumber = self.phone_number2
        
        if self.phone_number3_type and self.phone_number3_type.name == 'Fax':
            ReturnedNumber = self.phone_number3
        
        if self.phone_number4_type and self.phone_number4_type.name == 'Fax':
            ReturnedNumber = self.phone_number4
        
        if self.phone_number5_type and self.phone_number5_type.name == 'Fax':
            ReturnedNumber = self.phone_number5

        return ReturnedNumber

    fax_number = property(_get_fax_number)

    def _get_toll_free_number(self):
        "returns a toll number for office"
        ReturnedNumber = u''

        if self.phone_number1_type and self.phone_number1_type.name == 'Toll Free':
            if self.phone_number1 and len(self.phone_number1) > 0:
                return self.phone_number1
            else:
                return u''#20180522u'1-800-ASK-MFRI'
        if self.phone_number2_type and self.phone_number2_type.name == 'Toll Free':
            if self.phone_number2 and len(self.phone_number2) > 0:
                return self.phone_number2
            else:
                return u''#20180522u'1-800-ASK-MFRI'
        if self.phone_number3_type and self.phone_number3_type.name == 'Toll Free':
            if self.phone_number2 and len(self.phone_number2) > 0:
                return self.phone_number2
            else:
                return u''#20180522u'1-800-ASK-MFRI'
        if self.phone_number4_type and self.phone_number4_type.name == 'Toll Free':
            if self.phone_number4 and len(self.phone_number4) > 0:
                return self.phone_number4
            else:
                return u''#20180522u'1-800-ASK-MFRI'
        if self.phone_number5_type and self.phone_number5_type.name == 'Toll Free':
            if self.phone_number5 and len(self.phone_number5) > 0:
                return self.phone_number5
            else:
                return u''

        return u''

    toll_free_number = property(_get_toll_free_number)
    
    def _get_main_number(self):
        "returns the main number for office"
        ReturnedNumber = u''

        if self.phone_number1_type and self.phone_number1_type.name == 'Primary':
            if self.phone_number1 and len(self.phone_number1) > 0:
                return self.phone_number1
        if self.phone_number2_type and self.phone_number2_type.name == 'Primary':
            if self.phone_number2 and len(self.phone_number2) > 0:
                return self.phone_number2
        if self.phone_number3_type and self.phone_number3_type.name == 'Primary':
            if self.phone_number2 and len(self.phone_number2) > 0:
                return self.phone_number2
        if self.phone_number4_type and self.phone_number4_type.name == 'Primary':
            if self.phone_number4 and len(self.phone_number4) > 0:
                return self.phone_number4
        if self.phone_number5_type and self.phone_number5_type.name == 'Primary':
            if self.phone_number5 and len(self.phone_number5) > 0:
                return self.phone_number5

        return u''

    main_number = property(_get_main_number)
    
    def _get_metro_dc_number(self):
        "returns the Metro DC Local number for office"
        ReturnedNumber = u''

        if self.phone_number1_type and self.phone_number1_type.name == 'Metro DC Local':
            if self.phone_number1 and len(self.phone_number1) > 0:
                return self.phone_number1
        if self.phone_number2_type and self.phone_number2_type.name == 'Metro DC Local':
            if self.phone_number2 and len(self.phone_number2) > 0:
                return self.phone_number2
        if self.phone_number3_type and self.phone_number3_type.name == 'Metro DC Local':
            if self.phone_number2 and len(self.phone_number2) > 0:
                return self.phone_number2
        if self.phone_number4_type and self.phone_number4_type.name == 'Metro DC Local':
            if self.phone_number4 and len(self.phone_number4) > 0:
                return self.phone_number4
        if self.phone_number5_type and self.phone_number5_type.name == 'Metro DC Local':
            if self.phone_number5 and len(self.phone_number5) > 0:
                return self.phone_number5

        return u''

    metro_dc_number = property(_get_metro_dc_number)
    
    def _get_office_location(self):
        "returns the office location"

        if self.parent_location:
            if self.parent_location == self:
                return self
            elif self.parent_location.abbreviation != 'NA':
                return self.parent_location
            else:
                return None
        else:
            return None

    office_location = property(_get_office_location)
    
    def _get_parent_office(self):
        "returns the office location"

        if self.parent_department and self.parent_department.abbreviation != 'NA':
            return self.parent_department

        return None

    parent_office = property(_get_parent_office)
    
    def _get_street_address(self):
        "returns the office street address"
        
        address_to_return = {}
        if self.street_address1 and len(self.street_address1) > 0:
            address_to_return['facility_name'] = self.facility_name
            address_to_return['address1'] = self.street_address1
            address_to_return['address2'] = self.street_address2
            address_to_return['city'] = self.street_city
            address_to_return['state'] = self.street_state
            address_to_return['postcode'] = self.street_postcode
            return address_to_return
        elif self.postal_address1 and len(self.postal_address1) > 0:
            address_to_return['facility_name'] = self.facility_name
            address_to_return['address1'] = self.postal_address1
            address_to_return['address2'] = self.postal_address2
            address_to_return['city'] = self.postal_city
            address_to_return['state'] = self.postal_state
            address_to_return['postcode'] = self.postal_postcode
            return address_to_return
        else:
            if self.parent_location and self.parent_location != self:
                return self.parent_location.street_address

        return {}

    street_address = property(_get_street_address)
    
    def _get_mailing_address(self):
        "returns the office mailing address"
        
        address_to_return = {}
        if self.postal_address1 and len(self.postal_address1) > 0:
            address_to_return['facility_name'] = self.facility_name
            address_to_return['address1'] = self.postal_address1
            address_to_return['address2'] = self.postal_address2
            address_to_return['city'] = self.postal_city
            address_to_return['state'] = self.postal_state
            address_to_return['postcode'] = self.postal_postcode
            return address_to_return
        elif self.street_address1 and len(self.street_address1) > 0:
            address_to_return['facility_name'] = self.facility_name
            address_to_return['address1'] = self.street_address1
            address_to_return['address2'] = self.street_address2
            address_to_return['city'] = self.street_city
            address_to_return['state'] = self.street_state
            address_to_return['postcode'] = self.street_postcode
            return address_to_return
        else:
            if self.parent_location and self.parent_location != self:
                return self.parent_location.mailing_address

        return {}

    mailing_address = property(_get_mailing_address)
    
    def _get_email_addresses(self):
        "returns the office email addresses"
        
        addresses_to_return = {}
        if self.primary_email and len(self.primary_email) > 0:
            addresses_to_return['primary'] = self.primary_email
            if self.secondary_email and len(self.secondary_email) > 0:
                addresses_to_return['secondary'] = self.secondary_email
            return addresses_to_return
        elif self.secondary_email and len(self.secondary_email) > 0:
            addresses_to_return['primary'] = self.secondary_email
            return addresses_to_return
        else:
            if self.parent_department and self.parent_department != self:
                return self.parent_department.email_addresses

        return {}

    email_addresses = property(_get_email_addresses)

    def _primary_email_address(self):
        "returns the primary office email addresses"
        
        return self.email_addresses.get('primary', u'info@mfri.org')

    primary_email_address = property(_primary_email_address)

    def _get_facility_name(self):
        "returns the complete name for the facility"
        
        if u'RTC' in self.abbreviation:
            return u'%s Regional Training Center' % (self.name)
        elif u'RO' in self.abbreviation:
            return u'%s Regional Office' % (self.name)
        elif u'HQ' in self.abbreviation:
            return u'Maryland Fire and Rescue Institute %s' % (self.name)
        else:
            return self.name
        
        return {}

    facility_name = property(_get_facility_name)

    def _get_long_facility_name(self):
        "returns the complete name for the facility"
        
        if self.regionnumber > 0:
            return u'%s (%s) Region: %d' % (self.facility_name, self.abbreviation, self.regionnumber)
        else:
            return u'%s (%s)' % (self.facility_name, self.abbreviation)
        
        return {}

    long_facility_name = property(_get_long_facility_name)
    

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

        #the created field should have a value but doesn't so get it from the table, if not there, set to current date.
        if not self.created:
            try:
                self.created = MfriOffices.objects.get(pk=self.id).created
                if not self.created:
                    self.created = datetime.datetime.now()
            except:
                self.created = datetime.datetime.now()

        #the createdby field should have a value but doesn't so get it from the table, if not there, set to current user.
        if not self.createdby:
            try:
                self.createdby = MfriOffices.objects.get(pk=self.id).createdby
                if not self.createdby:
                    self.createdby = current_user
            except:
                self.createdby = current_user

        super(MfriOffices, self).save(**kwargs)

        
        
        
        
        
        








