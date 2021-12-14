from django.db import models

from AppLegacyBase.models import AppLegacyBase

from MOffices.models import MfriOffices, Jurisdictions, LegacyCoursesection, LegacyMfriregions

class Locations(AppLegacyBase):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    region = models.ForeignKey(LegacyMfriregions, db_column='RegionID')

    county_name = models.CharField(max_length=765, db_column='County', blank=True) 

    county = models.ForeignKey(Jurisdictions, db_column='CountyID')
    
    address1 = models.CharField(max_length=765, db_column='Address1', blank=True) 
    address2 = models.CharField(max_length=765, db_column='Address2', blank=True) 
    city = models.CharField(max_length=765, db_column='City', blank=True) 
    state = models.CharField(max_length=765, db_column='State', blank=True) 
    postcode = models.CharField(max_length=765, db_column='PostCode', blank=True) 
    country = models.CharField(max_length=765, db_column='Country', blank=True) 

    primary_phone_number = models.CharField(max_length=765, db_column='PrimaryPhoneNumber', blank=True) 
    secondary_phone_number = models.CharField(max_length=765, db_column='SecondaryPhoneNumber', blank=True) 

    fax_number = models.CharField(max_length=765, db_column='FaxNumber', blank=True) 

    email_address = models.CharField(max_length=765, db_column='EmailAddress', blank=True) 


#    lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
#    lastchange = models.DateTimeField(db_column='LastChange') 
#    createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
#    created = models.DateTimeField(db_column='Created') 

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        db_table = u'Locations'
        verbose_name_plural = "Locations"
        ordering = ['name']

    def _get_street_address(self):
        "returns the location street address"
        
        address_to_return = {}
        address_to_return['name'] = self.name
        address_to_return['address1'] = self.address1
        address_to_return['address2'] = self.address2
        address_to_return['city'] = self.city
        address_to_return['state'] = self.state
        address_to_return['postcode'] = self.postcode
        address_to_return['country'] = self.country
        return address_to_return
    
    
    street_address = property(_get_street_address)
