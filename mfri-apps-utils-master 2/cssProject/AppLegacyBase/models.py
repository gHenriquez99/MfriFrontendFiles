import datetime
#import re

#from django.conf import settings
from django.db import models
#from django.contrib.auth.models import User

#from django.template.defaultfilters import slugify

class AppLegacyBase(models.Model):
    lastchange = models.DateTimeField(db_column='LastChange') 
    lastchangeby = models.CharField(max_length=20, db_column='LastChangeBy', blank=True) 
    created = models.DateTimeField(db_column='Created') 
    createdby = models.CharField(max_length=20, db_column='CreatedBy', blank=True) 
 
 
    
    class Meta:
        abstract = True
