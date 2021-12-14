from django.db import models

from AppLegacyBase.models import AppLegacyBase
from MStaff.models import MfriInstructors
#from MOffices.models import MfriOffices, LegacyCoursesection #, LegacyMfriregions



class ClientStatus(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'ClientStatus'
        verbose_name_plural = "ClientStatus"
        ordering = ['name']

class ClientType(models.Model):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 

    def __unicode__(self):
        return self.name
        verbose_name_plural = "ClientTypes"
        ordering = ['name']
    
    class Meta:
        db_table = u'ClientTypes'

class MfriClient(AppLegacyBase):
    name = models.CharField(max_length=765, db_column='Name', blank=True) 
    number = models.CharField(max_length=765, db_column='Number', blank=True) 

    description = models.CharField(max_length=765, db_column='Description', blank=True) 

    street_address1 = models.CharField(max_length=765, db_column='StreetAddress1', blank=True) 
    street_address2 = models.CharField(max_length=765, db_column='StreetAddress2', blank=True) 
    street_city = models.CharField(max_length=765, db_column='StreetCity', blank=True) 
    street_state = models.CharField(max_length=765, db_column='StreetState', blank=True) 
    street_postcode = models.CharField(max_length=765, db_column='StreetPostCode', blank=True) 
    street_country = models.CharField(max_length=765, db_column='StreetCountry', blank=True) 

    mailing_address1 = models.CharField(max_length=765, db_column='MailingAddress1', blank=True) 
    mailing_address2 = models.CharField(max_length=765, db_column='MailingAddress2', blank=True) 
    mailing_city = models.CharField(max_length=765, db_column='MailingCity', blank=True) 
    mailing_state = models.CharField(max_length=765, db_column='MailingState', blank=True) 
    mailing_postcode = models.CharField(max_length=765, db_column='MailingPostCode', blank=True) 
    mailing_country = models.CharField(max_length=765, db_column='MailingCountry', blank=True) 

    contact_name = models.CharField(max_length=765, db_column='ContactName', blank=True) 

    primary_phone_number = models.CharField(max_length=765, db_column='PrimaryPhoneNumber', blank=True) 
    secondary_phone_number = models.CharField(max_length=765, db_column='SecondaryPhoneNumber', blank=True) 
    fax_number = models.CharField(max_length=765, db_column='FaxNumber', blank=True) 

    email_address = models.CharField(max_length=765, db_column='EmailAddress', blank=True) 

    client_type = models.ForeignKey(ClientType, db_column='TypeID', related_name="+")
    client_status = models.ForeignKey(ClientStatus, db_column='StatusID', related_name="+")


    #typeid = models.IntegerField(null=True, db_column='TypeID', blank=True) 
    #statusid = models.IntegerField(null=True, db_column='StatusID', blank=True) 

#    mfricoordinatorid = models.IntegerField(null=True, db_column='MFRICoordinatorID', blank=True) 
    coordinator = models.ForeignKey(MfriInstructors, db_column='MFRICoordinatorID', related_name="+")

    record_status = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 

    #recordstatusid = models.IntegerField(null=True, db_column='RecordStatusID', blank=True) 
    #lastchangeby = models.CharField(max_length=96, db_column='LastChangeBy', blank=True) 
    #lastchange = models.DateTimeField(db_column='LastChange') 
    #createdby = models.CharField(max_length=96, db_column='CreatedBy', blank=True) 
    #created = models.DateTimeField(db_column='Created') 

    def __unicode__(self):
        return u'%s %s' % (self.name, self.number)

    class Meta:
        db_table = u'MFRIClients'
        verbose_name_plural = "MfriClients"
        ordering = ['name']

