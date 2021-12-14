
from django.core.urlresolvers import reverse

from django.template.defaultfilters import slugify
from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings

from AppBase.models import unique_slugify

from MCourses.models import Coursedescriptions

STATUS_CHOICES = (
                    ('Dflt', 'Default'),
                    ('Ok', 'Available'),
                    ('N/A', 'No Longer Available'),
                    )

class ExamModuleName(models.Model):
    slug = models.SlugField(unique=True, help_text='Must be unique, no spaces, only letters, numbers.') 

    name = models.CharField(max_length=255, blank=False, help_text='This is the name of the module exam.')

    is_midterm = models.BooleanField(default=False, help_text='This module exam is the midterm exam.')

    is_final = models.BooleanField(default=False, help_text='This module exam is the final exam.')

    sort_order = models.IntegerField(null=True, blank=True) 

    status = models.CharField(max_length=4, choices=STATUS_CHOICES, blank=False, default='Ok')

    class Meta:
        verbose_name_plural = "ExamModuleNames"
        ordering = ['sort_order', 'name', 'is_midterm', 'is_final']

    def __unicode__(self):
        
        return self.name

    def save(self, **kwargs): 
        if not self.name:
            raise ValueError(u'Exam Module name is required.')
            
        
        if not self.slug:
            slug_name = self.name
            
            unique_slugify(self, u'%s' % (slug_name.replace('\\', '').replace('/', '').replace("'", '').replace('"', '').replace(',', '').replace('.', '').strip()))
        else:
            unique_slugify(self, u'%s' % (self.slug.replace('\\', '').replace('/', '').replace("'", '').replace('"', '').replace(',', '').replace('.', '').strip()))
#
        super(ExamModuleName, self).save(**kwargs)


class EvocVehicleType(models.Model):
    name = models.CharField(max_length=255, blank=True) 
    code = models.CharField(max_length=2, blank=True) 
    vehicle_class = models.CharField(max_length=5, blank=True) 
    number_of_axles = models.IntegerField(null=True, blank=True) 
    gross_vehicle_weight = models.CharField(max_length=20, blank=True) 
    sort_order = models.IntegerField(null=True, blank=True)
    
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, blank=False, default='Ok')
        
    class Meta:
        db_table = u'EvocVehicleType'
        verbose_name_plural = "EvocVehicleTypes"
        ordering = ['sort_order', 'name']
