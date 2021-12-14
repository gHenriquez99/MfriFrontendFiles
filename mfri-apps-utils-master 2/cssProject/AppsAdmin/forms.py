from django import forms
from django.forms import widgets
from django.forms import ValidationError
from AppsAdmin.models import *
from django.contrib.auth.models import Permission 
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt 
from django.forms import ModelForm
from django.db import models


class UserHomeForm(forms.Form):
        InputSearchField = forms.CharField(required=False, max_length=80, label= u'Search Field')

