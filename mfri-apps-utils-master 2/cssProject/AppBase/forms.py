import datetime

from django import forms
from django.forms import widgets
from django.forms import ValidationError



from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 
from django.utils.html import escape
from django.utils.safestring import mark_safe

from django.forms import ModelForm

from AppBase.models import AppBase


class baseForm(ModelForm):
    class Meta:
        model = AppBase
        exclude = ('modified_by','modified_date', 'created_by','created_date',)

    def save(self, *args, **kwargs):
        kwargs['commit']=False
        user = kwargs.pop('user', None)

        obj = super(baseForm, self).save(*args, **kwargs)        
        obj.modified_date = datetime.datetime.now()

        self_instance = getattr(self, 'instance', None)
        self_instance_user = None
        
        if self_instance:
            self_instance_user = getattr(self_instance, 'user', None)

        if self_instance and self_instance_user:
            obj.modified_by = self.instance.user
            if not obj.id:
                obj.modified_date = datetime.datetime.now()

        if not obj.id:
            obj.created_date = datetime.datetime.now()
            obj.created_by = self.instance.user

        if user:
            obj.save(user=user)
        else:
            obj.save()
        return obj

#left here for reference
#    def clean(self, *args, **kwargs):
#        cleaned_data = self.cleaned_data
#        
#        slug = cleaned_data.get("slug")
##        raw_slug = ''
#        if not slug:
##            raw_slug = ''.join([slug_part for slug_part in kwargs['slug_fields']])
#                
#            name = cleaned_data.get("name")
#
##            slug = u'%03d%s' % (template_obj.application.id, name)
#
#
#            self.data['slug'] = slugify(name)
#        
#        bob = dir(self)
#        assert False
#        
#        return super(baseForm, self).clean()
 
class AppBaseExceptionForm(forms.Form):
    def __init__(self, *args, **kwargs): #request=None,
        
        super(AppBaseExceptionForm, self).__init__(*args, **kwargs)

         
