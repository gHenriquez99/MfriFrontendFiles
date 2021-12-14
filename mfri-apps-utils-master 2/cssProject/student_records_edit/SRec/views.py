import os
import codecs
import string
import json
import time
import datetime

from socket import gethostname
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse 
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 


from AppsAdmin.models import *

from AppBase.views import JSDatePicker

from AppBase.utils_exception import ExceptionRedirect 

from MEmailMan.utils_context import encode_context, decode_context 

from SMEDReview.utils import GetMedicalClearanceForStudent, FormatMedicalClearanceMessage  

from SRegistration.utils_reports import ListRegistrationRecordsForStudent 

from SRegistration.utils_fee_batches import FormatFeeBatchesForStudent 

from SRec.utils_permissions import get_student_record_read_permission, get_student_record_write_permission, get_student_record_id_read_permission, get_student_record_id_write_permission, get_student_record_private_read_permission, get_student_record_private_write_permission, get_student_record_contact_read_permission, get_student_record_contact_write_permission, get_student_record_affiliation_read_permission, get_student_record_affiliation_write_permission, get_student_record_flags_read_permission, get_student_record_flags_write_permission, get_student_record_import_permission, get_student_record_export_permission 

from SRec.utils_student_flags import GetStudentFlagsList 
from SRec.models import *
from SRec.forms import StudentRecordEditForm, StudentRecordNewForm, StudentNameEditForm, StudentNumberEditForm, StudentNumberInitConfirmForm 

from SRec.utils import FormatListRegistrationRecordsForDisplay, GetDefaultStudentFlagStatus 
from SRec.utils_msn import ValidateEAN8CheckSum, AssignNewMFRIStudentNumber, GetMFRIStudentNumberForSSN, SetMFRIStudentNumberForSSN 

from SRec.utils_form import ValidateStudentRecord 

def StudentRecordCGIURL(srec_id=None):

    if not srec_id:
        return None

    return u'/cgi-bin/strc_edit.cgi?MID=%s' % (srec_id)

@login_required
def StudentDataEdit(request, pk=None, context_encoded=None, template_name=None):
    
    context_decoded = {}

    if pk:
        context_decoded['student_record_id'] = pk
    else:
        if context_encoded:
            context_decoded = decode_context(context_encoded)

    parent_url = None
    parent_url_label = None

    if context_decoded and parent_url in context_decoded:
        parent_url = context_decoded.get('parent_url', parent_url)
        parent_url_label = context_decoded.get('parent_url_label', parent_url_label)

    user_write_permission = False
    student_record = None
    student_record_id = None

    student_record_read_permission = get_student_record_read_permission(user=request.user)
    student_record_write_permission = get_student_record_write_permission(user=request.user)

    student_record_flags_read_permission = get_student_record_flags_read_permission(user=request.user) 
    student_record_flags_write_permission = get_student_record_flags_write_permission(user=request.user) 

    user_write_permission = student_record_write_permission

    if pk:
        if not student_record_write_permission:
            return ExceptionRedirect(log_number=None, office_code=None,
                        exception_label=u'Student Data Edit Error',
                        exception_message=u'E102 You do not have the appropriate permissions to view this data. Please contact IT support.')

        try:
            student_record = Studentrecords.objects.get(pk=pk)
        except Studentrecords.DoesNotExist:
            return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Data Edit Error',
                    exception_message=u'E104 No student record not found.')

        student_record_id = student_record.id
    else:

        if not student_record_write_permission:
            return ExceptionRedirect(log_number=None, office_code=None,
                        exception_label=u'Student Data Edit Error',
                        exception_message=u'E103 You do not have the appropriate permissions to view this data. Please contact IT support.')

    if student_record:
        form_handler = StudentRecordEditForm
    else:
        form_handler = StudentRecordNewForm

    if request.method == u'POST':
        if request.POST['FormButton'] == 'Cancel':
            return HttpResponseRedirect(parent_url)

        if student_record:
            form = form_handler(request.POST, request.FILES, instance=student_record)
        else:
            form = form_handler(request.POST, request.FILES)

        if form.is_valid():
            print u'it is valid\n'
            form.instance.user = request.user

            set_flag_status = False

            if not student_record:
                set_flag_status = True
            else:
                try:
                    if not student_record.studentstatusid:
                        set_flag_status = True
                except:
                    set_flag_status = True

            saved_student_record = form.save(user=request.user.username) 

            clean_data = form.cleaned_data

            ssn_to_save = clean_data.get('id_number', u'')
            epins_to_save = clean_data.get('stateprovidernumber', u'')
            umid_to_save = clean_data.get('umid', u'')
            nfa_sid_to_save = clean_data.get('nfa_sid', u'')

            try:
                if set_flag_status:
                    saved_student_record.studentstatusid = GetDefaultStudentFlagStatus()

                if len(ssn_to_save) > 0:
                    saved_student_record.ssn_clear = ssn_to_save
                if len(epins_to_save) > 0:
                    saved_student_record.epins_clear = epins_to_save

                if len(nfa_sid_to_save) > 0:
                    saved_student_record.nfa_sid = nfa_sid_to_save
                print u'user username %s\n' % (request.user.username)
                saved_student_record.save(user=request.user.username) 
            except Exception as e:
                print u'error saving saved_student_record ssn %s\n' % (e)
                pass

            print u'new saved_student_record ssn %s\n' % (saved_student_record.ssn_clear)
            print u'go AssignNewMFRIStudentNumber\n'
            mfri_student_number = AssignNewMFRIStudentNumber(student_record=saved_student_record)
            print u'ssn %s\n' % (ssn_to_save)
            print u'mfri_student_number %s\n' % (mfri_student_number)
            if saved_student_record and not student_record:
                student_record = saved_student_record

            print u'parent_url %s\n' % (parent_url)
            print u'new student record id %d\n' % (student_record.id)
            if parent_url:
                return HttpResponseRedirect(parent_url)
            else:
                print u'no parent_url\n'
                if student_record:
                    print u'redirect to edit form\n'
                    return HttpResponseRedirect(reverse('srec_edit_student_data_pk', kwargs={'pk':student_record.id}))
        #else:
        #    print u'oops, errors! %s\n' % (form.errors)

    else:
        if student_record:
            print u'student record id %d\n' % (student_record.id)
            form = form_handler(instance=student_record)
        else:
            print u'no student record (yet)\n'
            form = form_handler()


    student_flag_list = []
    registration_lists = {}
    invoice_batch_list = []

    student_record_validate_results = {}

    medical_clearance_display = None

    if student_record:
        student_flag_list = GetStudentFlagsList(student_record=student_record)

        registration_record_lists = ListRegistrationRecordsForStudent(student_record=student_record, mfri_student_number=student_record.mfri_student_number) 
        registration_lists = FormatListRegistrationRecordsForDisplay(registration_record_list=registration_record_lists.get('registration_record_list', None), preregistration_records=registration_record_lists.get('preregistration_records', None), online_registration_record_list=registration_record_lists.get('online_registration_record_list', None)) 

        student_record_validate_results = ValidateStudentRecord(student_record=student_record)

        medical_clearance = GetMedicalClearanceForStudent(student_record=student_record)
        medical_clearance_display = FormatMedicalClearanceMessage(medical_clearance_record=medical_clearance)

        invoice_batch_list = FormatFeeBatchesForStudent(student_record=student_record)

    birthdate_end_year = int(datetime.datetime.now().strftime('%Y'))
    birthdate_end_date = datetime.date( birthdate_end_year,12,31)

    emt_certification_end_year = int(datetime.datetime.now().strftime('%Y')) + 6
    emt_certification_end_date = datetime.date( birthdate_end_year,12,31)

    form_js = u''
    form_js += JSDatePicker(field_id_name='id_birthdate',
                                     Default_Value=datetime.datetime.now(),
                                     StartDate=datetime.date(1900,01,01),
                                     EndYear=birthdate_end_year,
                                     EndDate=birthdate_end_date)

    form_js += JSDatePicker(field_id_name='id_certificationexpirationdate',
                                     Default_Value=datetime.datetime.now(),
                                     StartDate=datetime.date(1980,01,01),
                                     EndYear=emt_certification_end_year,
                                     EndDate=emt_certification_end_date)


    if student_record:
        read_only = {
                    'name': student_record.full_name,
                    'mfri_student_number': student_record.mfri_student_number,
                    'show_name_as_is': student_record.show_name_as_is,
                }
    else:
        read_only = {
                    'name': None,
                    'mfri_student_number': None,
                    'show_name_as_is': False,
                }

    return render(request=request, template_name=template_name, context={'form': form,
                                         'read_only': read_only,
                                         'parent_url': parent_url,
                                         'parent_url_label': parent_url_label,
                                         'student_record_id': student_record_id,
                                         'student_flag_list': student_flag_list,
                                         'registration_list': registration_lists.get('registration_list', None),
                                         'preregistration_list': registration_lists.get('preregistration_list', None),
                                         'onlineregistration_list': registration_lists.get('onlineregistration_list', None),
                                         'duplicate_ssn_list': student_record_validate_results.get('duplicate_ssn_list', None),
                                         'duplicate_state_provider_number_list': student_record_validate_results.get('duplicate_state_provider_number_list', None),
                                         'duplicate_nfa_sid_number_list': student_record_validate_results.get('duplicate_nfa_sid_number_list', None),
                                         'medical_clearance': medical_clearance_display,
                                         'merge_ssn_record_id_string': student_record_validate_results.get('merge_ssn_record_id_string', None),
                                         'merge_state_provider_number_record_id_string': student_record_validate_results.get('merge_state_provider_number_record_id_string', None),
                                         'merge_nfa_sid_number_record_id_string': student_record_validate_results.get('merge_nfa_sid_number_record_id_string', None),
                                         'invoice_batch_list': invoice_batch_list,
                                         'user_write_permission': user_write_permission,
                                         'user_flags_read_permission': student_record_flags_read_permission,
                                         'user_flags_write_permission': student_record_flags_write_permission, 
                                         'form_js': form_js,
                                        })


@login_required
def StudentNameEdit(request, pk=None, context_encoded=None, template_name=None):

    context_decoded = {}

    if pk:
        context_decoded['student_record_id'] = pk
    else:
        if context_encoded:
            context_decoded = decode_context(context_encoded)

    if not context_decoded:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Name Edit Error',
                    exception_message=u'E101 No edit context.')
    else:
        pk = context_decoded.get('student_record_id', None)

    parent_url = reverse('srec_edit_student_data_pk', kwargs={'pk':pk})

    if parent_url in context_decoded:
        parent_url = context_decoded.get('parent_url', parent_url)

    student_record_id_read_permission = get_student_record_id_read_permission(user=request.user)
    student_record_id_write_permission = get_student_record_id_write_permission(user=request.user)

    if pk:
        if not student_record_id_write_permission:
            return ExceptionRedirect(log_number=None, office_code=None,
                        exception_label=u'Student Name Edit Error',
                        exception_message=u'E102 You do not have the appropriate permissions to view this data. Please contact IT support.')
        try:
            student_record = Studentrecords.objects.get(pk=pk)
        except Studentrecords.DoesNotExist:
            return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Name Edit Error',
                    exception_message=u'E104 No student record not found.')
        
    else:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Name Edit Error',
                    exception_message=u'E102 No student record to edit.')


    if request.method == u'POST':
        if request.POST['FormButton'] == 'Cancel':
            return HttpResponseRedirect(parent_url)

        if student_record:
            form = StudentNameEditForm(request.POST, request.FILES, instance=student_record)

        if form.is_valid():
            form.instance.user = request.user

            clean_data = form.cleaned_data

            student_record1 = form.save()

            return HttpResponseRedirect(parent_url)

    if student_record:
        form = StudentNameEditForm(instance=student_record)
    else:
        form = StudentNameEditForm()

    student_record_id = None

    if student_record:
        student_record_id = student_record.id

    read_only = {
                    'mfri_student_number': student_record.mfri_student_number,
                }


    return render(request=request, template_name=template_name, context={'form': form,
                                         'read_only': read_only,
                                         'parent_url': parent_url,
                                         'student_record_id': student_record_id,
                                        })

@login_required
def StudentNumberEdit(request, pk=None, context_encoded=None, template_name=None):

    context_decoded = {}

    if pk:
        context_decoded['student_record_id'] = pk
    else:
        if context_encoded:
            context_decoded = decode_context(context_encoded)

    if not context_decoded:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Number Edit Error',
                    exception_message=u'E101 No edit context.')
    else:
        pk = context_decoded.get('student_record_id', None)

    parent_url = reverse('srec_edit_student_data_pk', kwargs={'pk':pk})

    if parent_url in context_decoded:
        parent_url = context_decoded.get('parent_url', parent_url)

    student_record_id_read_permission = get_student_record_id_read_permission(user=request.user)
    student_record_id_write_permission = get_student_record_id_write_permission(user=request.user)

    if pk:
        if not student_record_id_write_permission:
            return ExceptionRedirect(log_number=None, office_code=None,
                        exception_label=u'Student Number Edit Error',
                        exception_message=u'E104 You do not have the appropriate permissions to view this data. Please contact IT support.')
        student_record = get_object_or_404(Studentrecords, pk=pk)
    else:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Number Form Error',
                    exception_message=u'E103 No student record.')

    if request.method == u'POST':
        if request.POST['FormButton'] == 'Cancel':
            return HttpResponseRedirect(parent_url)

        if student_record:
            form = StudentNumberEditForm(request.POST, request.FILES, instance=student_record)

        if form.is_valid():
            form.instance.user = request.user
            form.save()

            return HttpResponseRedirect(parent_url)
    else:
        if student_record:
            form = StudentNumberEditForm(instance=student_record)
            student_record_id = student_record.id
        else:
            return ExceptionRedirect(log_number=None, office_code=None,
                   exception_label=u'Student Number Form Error',
                   exception_message=u'E104 No student record.')


    student_flag_list = GetStudentFlagsList(student_record=student_record)

    read_only = {
                    'name': student_record.full_name,
                }


    return render(request=request, template_name=template_name, context={'form': form,
                                         'read_only': read_only,
                                         'parent_url': parent_url,
                                         'student_record_id': student_record.id,
                                        })

@login_required
def StudentNumberInitConfirm(request=None, pk=None, context_encoded=None, template_name=None):

    context_decoded = {}

    if not request.user.is_superuser:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Permssion Error',
                    exception_message=u'E100 You do not have permssion to edit MFRI Student Number.')

    if pk:
        context_decoded['student_record_id'] = pk
    else:
        if context_encoded:
            context_decoded = decode_context(context_encoded)

    if not context_decoded:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Number Edit Error',
                    exception_message=u'E101 No edit context.')
    else:
        pk = context_decoded.get('student_record_id', None)

    parent_url = reverse('srec_edit_student_data_pk', kwargs={'pk':pk})

    if parent_url in context_decoded:
        parent_url = context_decoded.get('parent_url', parent_url)

    student_record_id_read_permission = get_student_record_id_read_permission(user=request.user)
    student_record_id_write_permission = get_student_record_id_write_permission(user=request.user)

    if pk:
        if not student_record_id_write_permission:
            return ExceptionRedirect(log_number=None, office_code=None,
                        exception_label=u'Student Number Edit Error',
                        exception_message=u'E102 You do not have the appropriate permissions to view this data. Please contact IT support.')
        try:
            student_record = Studentrecords.objects.get(pk=pk)
        except Studentrecords.DoesNotExist:
            return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Number Edit Error',
                    exception_message=u'E104 No student record not found.')
    else:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Number Form Error',
                    exception_message=u'E103 No student record.')

    student_record_id = student_record.id

    if request.method == u'POST':
        if request.POST['FormButton'] == 'Cancel':
            return HttpResponseRedirect(parent_url)

        form = StudentNumberInitConfirmForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            form_pk = cleaned_data.get('pk', None)

            if not form_pk:
                return ExceptionRedirect(log_number=None, office_code=None,
                            exception_label=u'MFRI Student Number Intialization Error',
                            exception_message=u'E104 No intialization context.')

            if form_pk != student_record_id:
                return ExceptionRedirect(log_number=None, office_code=None,
                            exception_label=u'MFRI Student Number Intialization Error',
                            exception_message=u'E104 Intialization context mismatch.')


            pre_register_result_dict = {}
            if request.POST['FormButton'] == u'Confirm MFRI Student Number Initialization':

                new_mfri_student_number = AssignNewMFRIStudentNumber(student_record=student_record) 


                if new_mfri_student_number:
                    return HttpResponseRedirect(reverse('srec_init_confirm_done_student_number_pk', kwargs={'pk': student_record.id}))

    form = StudentNumberInitConfirmForm(initial={
                                         'pk':   student_record_id,
                                         })

    return render(request=request, template_name=template_name, context={'form': form,
                                          'student_record': student_record,
                                        })

@login_required
def StudentNumberInitConfirmDone(request=None, pk=None, confirm_context=None, template_name=None): 

    context_decoded = {}

    if not request.user.is_superuser:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Permssion Error',
                    exception_message=u'E100 You do not have permssion to edit MFRI Student Number.')

    if pk:
        context_decoded['student_record_id'] = pk
    else:
        if context_encoded:
            context_decoded = decode_context(context_encoded)

    if not context_decoded:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Number Edit Error',
                    exception_message=u'E101 No edit context.')
    else:
        pk = context_decoded.get('student_record_id', None)
        mfri_student_number_init_result = context_decoded.get('mfri_student_number_init_result', u'MFRI Student Number Successfully Initialized')

    parent_url = reverse('srec_edit_student_data_pk', kwargs={'pk':pk})

    if parent_url in context_decoded:
        parent_url = context_decoded.get('parent_url', parent_url)

    student_record_id_read_permission = get_student_record_id_read_permission(user=request.user)
    student_record_id_write_permission = get_student_record_id_write_permission(user=request.user)

    if pk:
        if not student_record_id_write_permission:
            return ExceptionRedirect(log_number=None, office_code=None,
                        exception_label=u'Student Number Edit Error',
                        exception_message=u'E102 You do not have the appropriate permissions to view this data. Please contact IT support.')
        student_record = get_object_or_404(Studentrecords, pk=pk)
    else:
        return ExceptionRedirect(log_number=None, office_code=None,
                    exception_label=u'Student Number Form Error',
                    exception_message=u'E103 No student record.')

    student_record_id = student_record.id

    return render(request=request, template_name=template_name, context={
                                 'student_record_id': student_record_id,
                                 'student_record': student_record,
                                 'mfri_student_number_init_result': mfri_student_number_init_result,
                                 })
