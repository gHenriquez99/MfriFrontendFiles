from django.db import models

from AppLegacyBase.models import AppLegacyBase

from MOffices.models import Jurisdictions

class Affiliations(AppLegacyBase):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    abbreviation = models.CharField(max_length=20, db_column='abbreviation', blank=True) 

    mfri_code = models.CharField(max_length=96, db_column='MFRICode', blank=True) 
    miemss_number = models.CharField(max_length=20, db_column='miemss_number', blank=True) 

    mfirs_number = models.CharField(max_length=5, db_column='mfirs_number', blank=True) 
    
    county = models.ForeignKey(Jurisdictions, db_column='CountyID')

    mailing_address1 = models.CharField(max_length=765, db_column='MailingAddress1', blank=True) 
    mailing_address2 = models.CharField(max_length=765, db_column='MailingAddress2', blank=True) 
    mailing_city = models.CharField(max_length=765, db_column='MailingCity', blank=True) 
    mailing_state = models.CharField(max_length=765, db_column='MailingState', blank=True) 
    mailing_postcode = models.CharField(max_length=765, db_column='MailingPostCode', blank=True) 
    mailing_country = models.CharField(max_length=765, db_column='MailingCountry', blank=True) 

    street_address1 = models.CharField(max_length=765, db_column='StreetAddress1', blank=True) 
    street_address2 = models.CharField(max_length=765, db_column='StreetAddress2', blank=True) 
    street_city = models.CharField(max_length=765, db_column='StreetCity', blank=True) 
    street_state = models.CharField(max_length=765, db_column='StreetState', blank=True) 
    street_postcode = models.CharField(max_length=765, db_column='StreetPostCode', blank=True) 
    street_country = models.CharField(max_length=765, db_column='StreetCountry', blank=True) 

    primary_phone_number = models.CharField(max_length=765, db_column='PrimaryPhoneNumber', blank=True) 
    secondary_phone_number = models.CharField(max_length=765, db_column='SecondaryPhoneNumber', blank=True) 
    fax_number = models.CharField(max_length=765, db_column='FaxNumber', blank=True) 

    email_address = models.CharField(max_length=765, db_column='EmailAddress', blank=True) 
    
    is_atra = models.BooleanField(default=False, help_text='This agency is an ATRA.', blank=True)
    has_delegation_of_authority = models.BooleanField(default=False, help_text='This agency is an ATRA with Delegation of Authority.', blank=True)
    atra_number = models.CharField(max_length=2, default='', help_text='If the agency is an ATRA, this is their ATRA Number', null=True, blank=True) 

    show_as_registration_option = models.BooleanField(default=False, help_text='Show this agency as affiliation option on registration form.')
    is_md_emergency_service = models.BooleanField(default=True, help_text='This agency is an emergency services agency that responds into Maryland.')
    has_training_officer = models.BooleanField(default=True, help_text='This agency has a training officer and will appear in the Training Officer Admin app.')
    has_no_address = models.BooleanField(default=False, help_text='This agency listing is a place holder and so does not have an address.')
    has_error = models.BooleanField(default=False, help_text='This agency listing has an error that must be fixed by the system administrator.')
    is_duplicate = models.BooleanField(default=False, help_text='This agency listing appears to be a duplicate listing and must be fixed by the system administrator.')

    internal_note = models.TextField(blank=True, help_text='Optional note used internally to describe any required changes or problems with this entry.')

    has_bls_approver   = models.BooleanField(default=False, blank=True, help_text='Has Training Officer that approves BLS registration applications.')
    has_als_approver   = models.BooleanField(default=False, blank=True, help_text='Has Training Officer that approves ALS registration applications.')
    has_pdi_approver   = models.BooleanField(default=False, blank=True, help_text='Has Training Officer that approves MICRB Instructor PDI registration applications.')
    has_other_approver = models.BooleanField(default=False, blank=True, help_text='Has Training Officer that approves Other registration applications.')

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        db_table = u'Affiliations'
        verbose_name_plural = "Affiliations"
        ordering = ['name']

    def _complete_mailing_address(self):
        "returns true if mailing address is complete."

        if not self.mailing_address1:
            return False

        if not self.mailing_city:
            return False

        if not self.mailing_state:
            return False

        if not self.mailing_postcode:
            return False
        
        if len(self.mailing_address1.strip()) == 0:
            return False

        if len(self.mailing_city.strip()) == 0:
            return False

        if len(self.mailing_state.strip()) == 0:
            return False

        if len(self.mailing_postcode.strip()) == 0:
            return False

        return True

    complete_mailing_address = property(_complete_mailing_address)
    
    def _complete_street_address(self):
        "returns true if street address is complete."

        if not self.street_address1:
            return False

        if not self.street_city:
            return False

        if not self.street_state:
            return False

        if not self.street_postcode:
            return False
        
        if len(self.street_address1.strip()) == 0:
            return False

        if len(self.street_city.strip()) == 0:
            return False

        if len(self.street_state.strip()) == 0:
            return False

        if len(self.street_postcode.strip()) == 0:
            return False

        return True

    complete_street_address = property(_complete_street_address)
    
    def _mailing_and_street_address_match(self):
        "if there is a mailing address, returns true if the mailing address and stree address match"
        ReturnedAddress = {}

        if not self.complete_mailing_address:
            return False

        if not self.complete_street_address:
            return False

        if self.mailing_address1.strip().upper() != self.street_address1.strip().upper():
            return False

#        if self.mailing_address2 and self.street_address2:
#            if self.mailing_address2.strip().upper() != self.street_address2.strip().upper():
#                return False


        if self.mailing_city.strip().upper() != self.street_city.strip().upper():
            return False
                
        if self.mailing_state.strip().upper() != self.street_state.strip().upper():
            return False

        if self.mailing_postcode.strip().upper() != self.street_postcode.strip().upper():
            return False
        
        return True

    mailing_and_street_address_match = property(_mailing_and_street_address_match)

    def _get_street_address(self):
        "returns the street address"
        ReturnedAddress = {}

        if self.street_address1 and (len(self.street_address1) > 0):
            ReturnedAddress['address1'] = self.street_address1
        
        if self.street_address2 and (len(self.street_address2) > 0):
            ReturnedAddress['address2'] = self.street_address2
        
        if self.street_city and (len(self.street_city) > 0):
            ReturnedAddress['city'] = self.street_city
                
        if self.street_state and (len(self.street_state) > 0): # and self.street_state.upper() != 'MD':
           ReturnedAddress['state'] = self.street_state.upper()
        
        if self.street_postcode and (len(self.street_postcode) > 0):  
            ReturnedAddress['postcode'] = self.street_postcode.upper()
        
        if self.street_country and (len(self.street_country) > 0) and self.street_country.upper() != 'USA' and self.street_country.upper() != 'US':
            ReturnedAddress['country'] = self.street_country.upper()
            
        return ReturnedAddress

    street_address = property(_get_street_address)

    def _get_mailing_address(self):
        "returns the mailing address, if none, then the street address"
        ReturnedAddress = {}

        if self.complete_mailing_address:
            if self.mailing_address1 and (len(self.mailing_address1) > 0):
                ReturnedAddress['address1'] = self.mailing_address1
            
            if self.mailing_address2 and (len(self.mailing_address2) > 0):
                ReturnedAddress['address2'] = self.mailing_address2
            
            if self.mailing_city and (len(self.mailing_city) > 0):
                ReturnedAddress['city'] = self.mailing_city
                    
            if self.mailing_state and (len(self.mailing_state) > 0): # and self.mailing_state.upper() != 'MD':
               ReturnedAddress['state'] = self.mailing_state.upper()
            
            if self.mailing_postcode and (len(self.mailing_postcode) > 0):  
                ReturnedAddress['postcode'] = self.mailing_postcode.upper()
            
            if self.mailing_country and (len(self.mailing_country) > 0) and self.mailing_country.upper() != 'USA' and self.mailing_country.upper() != 'US':
                ReturnedAddress['country'] = self.mailing_country.upper()
        else:
            return self.street_address
            
        return ReturnedAddress

    mailing_address = property(_get_mailing_address)

    def _maryland_agency(self):
        "returns true if street or mailing address is MD, false otherwise"
        
        if self.street_state.strip().upper() == u'MD':
            return True
        elif self.mailing_state.strip().upper() == u'MD':
            return True
        
        return False
        
    is_maryland_agency = property(_maryland_agency)

    def _known_county(self):
        "returns true if county is not Unknown County, false otherwise"
        
        if self.county.name != u'Unknown':
#            bob = self.county.name
#            assert False
            return True
        
        return False
        
    is_known_county = property(_known_county)

    def _has_address_error(self):
        "returns true if has_error or is_duplicate is true and if it fails several tests"


        if self.has_error:
            return True
        
        if self.is_duplicate:
            return True
        
        if self.has_no_address:
            return False
        
        if self.mailing_and_street_address_match:
            return True
        
        if not self.complete_street_address and not self.complete_mailing_address:
            return True
            
        return False

    has_address_error = property(_has_address_error)

    def _served_by_mfri_office(self):
        "returns mfri office that serves this affiliation"

        if not self.county:
            return None 

        if not self.county.mfri_office:
            return None 

        return self.county.mfri_office
            
    served_by_mfri_office = property(_served_by_mfri_office)

    def _get_training_officer_types(self):
        "returns a dict with the training officer types"

        return { 
                  "has_bls_approver"  : self.has_bls_approver  ,
                  "has_als_approver"  : self.has_als_approver  ,
                  "has_pdi_approver"  : self.has_pdi_approver  ,
                  "has_other_approver": self.has_other_approver,
               }

    def _set_training_officer_types(self, available_training_officer_types):
        "sets training_officer_types"


        if not available_training_officer_types:
            return
            
        self.has_bls_approver   = available_training_officer_types.get('has_bls_approver', False)
        self.has_als_approver   = available_training_officer_types.get('has_als_approver', False)
        self.has_pdi_approver   = available_training_officer_types.get('has_pdi_approver', False)
        self.has_other_approver = available_training_officer_types.get('has_other_approver', False)
        self.save(update_fields=['has_bls_approver', 'has_als_approver', 'has_pdi_approver', 'has_other_approver'])
        
    training_officer_types = property(_get_training_officer_types, _set_training_officer_types)

