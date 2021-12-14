import os
import codecs
import string
import json
import time
import datetime
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import simpleSplit
#from reportlab.platypus.flowables import Image 
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak, Spacer
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, PageTemplate, Table, TableStyle, Paragraph, PageBreak, Spacer, Frame, Image
from reportlab.platypus.doctemplate import NextPageTemplate 
from reportlab.pdfbase.pdfmetrics import stringWidth

from socket import gethostname
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, Permission
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect

from MAffiliations.models import *
from MFRI_Utils.name_string_functions import SplitName

from MSchedule.utils_reports import mfri_report_header_data 

from MSchedule.models import *

def GetResourceListForCourse(course_description=None):
    #outside the scope of project
    return []

def GetBooksAssignmentsForStudent(scheduled_course=None, student_record=None):
    #outside the scope of project
    return []

def GetResourcesForCourse(course_description=None, category=None, level=None, only_billable=True, only_issued_to_students=True, only_issued_to_instructors=False, only_printed_in_house=False, only_is_exam=False):#20170713
    #outside the scope of project
    return None


#################### pdf generation
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            self.saveState()

            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Times-Roman", 10)
        self.drawRightString(10.5*inch, 8*inch,
            "Page %d of %d" % (self._pageNumber, page_count))


def create_resource_assignment_report_pdf(request=None, scheduled_course=None, table_name=u'StudentRegistration'): #20170624

    if not scheduled_course:
        return report_error_pdf(request, error_message=u'No course record provided.', program_error=True)

    if table_name == u'StudentRegistration':#20170624
        registered_student_list = GetRegisteredStudents(scheduled_course=scheduled_course)
    elif table_name == u'PreRegistration':#20170624
        pre_registrations = GetPreRegisteredList(scheduled_course=scheduled_course) #20170624    
        registered_student_list = pre_registrations.get('registered', []) #20170624 
    else:
        registered_student_list = [] #print blank list

    available_book_list = GetResourcesForCourse(course_description=scheduled_course.course_description)

    if not available_book_list or len(available_book_list) == 0:
        return report_error_pdf(request, error_message=u'No resources to issue for course.', user_error=True, scheduled_course=scheduled_course)

    lines_to_print_per_page = 10 / len(available_book_list)  

    letter_portrait_width, letter_portrait_height = letter        
    letter_landscape_height, letter_landscape_width = letter        

    large_font = 14
    medium_font = 12
    small_font = 10
    very_small_font = 8
    very_very_small_font = 6

    filename = u'book_assignments_%s.pdf' % (scheduled_course.log_number)
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
#    response['Content-Disposition'] = u'attachment; filename=%s' % (filename)
    response['Content-Disposition'] = u'filename=%s' % (filename)

    report_form_buffer = StringIO()

    report_form = SimpleDocTemplate(report_form_buffer, pagesize=(letter_landscape_width, letter_landscape_height))
    
    report_form.topMargin = .25 * inch
    report_form.bottomMargin = .25 * inch
    report_form.leftMargin = .25 * inch
    report_form.rightMargin = .25 * inch
    report_form.allowSplitting = True

    elements = []

    current_page = 1
    total_pages = 1
    
    report_form_header = mfri_report_header(scheduled_course=scheduled_course, report_title=u'Textbook Tracking Form') #20170711
    
    report_list_header_width = {
                                            'col1': 3.75 * inch,
                                            'col2': 3 * inch,
                                            'col3': 3.75 * inch,
                                          }


    report_form_header_table = Table(report_form_header, colWidths=[report_list_header_width['col1'], report_list_header_width['col2'], report_list_header_width['col3']])
    report_form_header_table.setStyle(TableStyle([
                                               ('ALIGN',(1,0),(1,3),'CENTER'),
                                               ('ALIGN',(-1,0),(-1,4),'RIGHT'),
                                               ('ALIGN',(0,0),(0,4),'LEFT'),
                                               ('FONTSIZE',(0,0),(-1,-1),12),
                                               #('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                               #('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                               ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.black),
                                               ('BOTTOMPADDING',(0,0),(-1,-2),0),
                                               ('BOTTOMPADDING',(0,-1),(-1,-1),4),
                                               ('TOPPADDING',(0,0),(-1,-1),0),
                                              ]))
                                              


    report_list_header = [
                    ['', '','', '', ''],
                  ]

                                              
                                              
    elements.append(report_form_header_table)
    table_cell_stylesheet = getSampleStyleSheet()

    table_cell_stylesheet['BodyText'].fontSize = very_small_font
    table_cell_stylesheet['BodyText'].leading = table_cell_stylesheet['Normal'].fontSize + 2

    
    report_list = []
    

    report_list_header_line_1 = [u'Student', u'Issued',u'Declined',u'Condition', u'Book Name', u'Returned', u'Rejected', u'Paid', u'Agency', u'Agency' ]
    report_list_header_line_2 = [       u'(Student must initial here.)',       u'',        u'',         u'',          u'',         u'', u'Unusable',     u'',   u' Pay',   u'Name' ]
    
    report_list.append(report_list_header_line_1)
    report_list.append(report_list_header_line_2)

    column_width = {
                    'StudentName': 2 * inch,
                    'StudentAccepted': .5 * inch,
                    'StudentDeclined': .5 * inch,
                    'BookCondition': .6 * inch,
                    'BookName': 2.5 * inch,
                    'BookReturned': .6 * inch,
                    'BookRejected': .6 * inch,
                    'StudentPaid': .6 * inch,
                    'AgencyPaid': .6 * inch,
                    'AgencyName': 1.9 * inch,
                   }
    
    report_list_column_widths = [column_width['StudentName'], column_width['StudentAccepted'], column_width['StudentDeclined'], column_width['BookCondition'], column_width['BookName'], column_width['BookReturned'], column_width['BookRejected'], column_width['StudentPaid'], column_width['AgencyPaid'], column_width['AgencyName']]

    report_list_table_style = [
                                            ('ALIGN',(0,0),(-1,1),"CENTER"),
                                            ('VALIGN',(0,2),(-1,-1),'TOP'),
                                            ('BOTTOMPADDING',(0,0),(-1,-1),0),
                                            ('TOPPADDING',(0,0),(-1,-1),0),
#                                            ('LINEABOVE',(0,2),(-1,2),.25,colors.black),
                                            ('LINEABOVE',(0,2),(-1,2), 0.25,colors.black),
                                            ('LINEBELOW', (0,1), (-1,1), 0.25, colors.black),
#                                            ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black),
                                            #('LINEBELOW', (0,1), (-1,-2), 0.25, colors.lightgrey),
                                            ('INNERGRID', (0,2), (-1,-1), 0.25, colors.black),
                                            ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black),
                                            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                            
                                        ]
    
    line_number = 0
    student_number = 0
    #max_title_length = 6.5 * inch 
    #max_title_length = 3 * inch 
    
    row_left_count = len(registered_student_list)
    printed_first_line_for_student = False

    for student_registration in registered_student_list:
        printed_first_line_for_student = False
        student_number += 1
        
        student_record = student_registration.student_record
        registration_affiliation = student_registration.affiliation

        is_agency_paid_for_unassigned_books = student_registration.book_fee_agency_pay

        student_name = student_record.full_name 

        assigned_book_list = GetBooksAssignmentsForStudent(scheduled_course=scheduled_course, student_record=student_record)

        if assigned_book_list:
            for book_assignment in assigned_book_list:
                book_declined = check_box_option(check_box_value=book_assignment.is_declined)
                
                book_accepted = check_box_option(check_box_value=book_assignment.is_issued)
                
                if book_assignment.is_issued:
                    book_name = Paragraph(u'%s Amount Owed:$%.2f' % (book_assignment.book_description.short_name, book_assignment.price), table_cell_stylesheet['Normal'])
                elif book_assignment.is_declined:
                    book_name = Paragraph(u'%s' % (book_assignment.book_description.short_name), table_cell_stylesheet['Normal'])
                else:
                    book_name = Paragraph(u'%s New:$%.2f Used:$%.2f' % (book_assignment.book_description.short_name, book_assignment.book_description.new_price, book_assignment.book_description.used_price), table_cell_stylesheet['Normal'])

                if book_assignment.affiliation_agency_will_pay:
                    agency_name = Paragraph(book_assignment.affiliation.name, table_cell_stylesheet['Normal'])
                else:
                    agency_name = u''

                if book_assignment.is_issued:
                    book_condition = check_box_option(check_box_value=book_assignment.is_used, return_value_for_none=u'New', return_value_for_true=u'Used', return_value_for_false=u'New')

                    book_returned = check_box_option(check_box_value=book_assignment.is_returned)
                
                    book_rejected = check_box_option(check_box_value=book_assignment.is_rejected_damaged)
                
                    book_paid = check_box_option(check_box_value=book_assignment.is_paid)
                
                    agency_paid = check_box_option(check_box_value=book_assignment.affiliation_agency_will_pay)
                else:
                    book_condition = check_box_option(check_box_value=None, return_value_for_none=u'[]New\n[]Used') 
                    book_returned = check_box_option(check_box_value=None) 
                    book_rejected = check_box_option(check_box_value=None) 
                    book_paid = check_box_option(check_box_value=None) 
                    agency_paid = check_box_option(check_box_value=book_assignment.affiliation_agency_will_pay)
                
                line_number += 1
                student_name_cell_text = Paragraph(u'%d %s' % (student_number, student_name), table_cell_stylesheet['Normal'])
                if printed_first_line_for_student:
                    student_name_cell_text = u''

                report_list.append([
                                         student_name_cell_text,
                                         book_accepted, 
                                         book_declined,
                                         book_condition, 
                                         book_name, 
                                         book_returned,
                                         book_rejected,
                                         book_paid,
                                         agency_paid,
                                         agency_name, 
                                    ])
                printed_first_line_for_student = True
        else:
            for book in available_book_list:
                book_name = Paragraph(u'%s New:$%.2f Used:$%.2f' % (book.short_name, book.new_price, book.used_price), table_cell_stylesheet['Normal'])
                if is_agency_paid_for_unassigned_books:
                    agency_name = Paragraph(registration_affiliation.name, table_cell_stylesheet['Normal'])
                else:
                    agency_name = u''
                
                book_accepted = check_box_option(check_box_value=None)
                
                book_declined = check_box_option(check_box_value=None)
                
                book_condition = check_box_option(check_box_value=None, return_value_for_none=u'[]New\n[]Used') 
                
                book_returned = check_box_option(check_box_value=None) 
                book_rejected = check_box_option(check_box_value=None) 
                book_paid = check_box_option(check_box_value=None) 
                agency_paid = check_box_option(check_box_value=is_agency_paid_for_unassigned_books) 
                        
                line_number += 1
                student_name_cell_text = Paragraph(u'%d %s' % (student_number, student_name), table_cell_stylesheet['Normal'])
                if printed_first_line_for_student:
                    student_name_cell_text = u''
                report_list.append([
                                         student_name_cell_text,
                                         book_accepted, 
                                         book_declined,
                                         book_condition, 
                                         book_name, 
                                         book_returned,
                                         book_rejected,
                                         book_paid,
                                         agency_paid,
                                         agency_name, 
                                        ])
                printed_first_line_for_student = True
        
        if line_number > lines_to_print_per_page and row_left_count > 0:
            report_list_table = Table(report_list, colWidths=report_list_column_widths)
            report_list_table.setStyle(TableStyle(report_list_table_style))
            report_list_table.hAlign='LEFT'
            elements.append(report_list_table)
            elements.append(PageBreak())
            line_number = 0
            elements.append(report_form_header_table)
            report_list = []
            report_list.append(report_list_header_line_1)
            report_list.append(report_list_header_line_2)

    printed_first_line_for_student = False
    while line_number < lines_to_print_per_page:
        printed_first_line_for_student = False
        student_number += 1
        student_name = u''
        student_name_cell_text = Paragraph(u'%d %s' % (student_number, student_name), table_cell_stylesheet['Normal'])
        if printed_first_line_for_student:
            student_name_cell_text = u''

        for book_description in available_book_list:
            book_name = Paragraph(u'%s New:$%.2f Used:$%.2f' % (book_description.short_name, book_description.new_price, book_description.used_price), table_cell_stylesheet['Normal'])
            agency_name = u''

            book_accepted = check_box_option(check_box_value=None)
            
            book_declined = check_box_option(check_box_value=None) 
   
            book_condition = check_box_option(check_box_value=None, return_value_for_none=u'[]New\n[]Used') 

            book_returned = check_box_option(check_box_value=None) 

            book_rejected = check_box_option(check_box_value=None) 
            
            book_paid = check_box_option(check_box_value=None) 
            agency_paid = check_box_option(check_box_value=None) 

            line_number += 1
            student_name_cell_text = Paragraph(u'%d %s' % (student_number, student_name), table_cell_stylesheet['Normal'])
            if printed_first_line_for_student:
                student_name_cell_text = u''
            report_list.append([
                                     student_name_cell_text,
                                     book_accepted, 
                                     book_declined,
                                     book_condition, 
                                     book_name, 
                                     book_returned,
                                     book_rejected,
                                     book_paid,
                                     agency_paid,
                                     agency_name, 
                                    ])
            printed_first_line_for_student = True
    
    if report_list:
        report_list_table = Table(report_list, colWidths=report_list_column_widths)
        report_list_table.setStyle(TableStyle(report_list_table_style))
        report_list_table.hAlign='LEFT'
        elements.append(report_list_table)

    # write the document to disk

    report_form.build(elements, canvasmaker=NumberedCanvas)
    
    response.write(report_form_buffer.getvalue())

    report_form_buffer.close()
    return response

    
def mfri_report_header(scheduled_course=None, log_number=None, report_title=None, one_column=False, report_lines=None):
    column1_report_lines = []
    column3_report_lines = []
    
    if report_title:
        column1_report_lines.append(report_title)

    report_header = mfri_report_header_data(scheduled_course=scheduled_course, log_number=log_number) 

    column1_report_lines.append(u'Log Number: %s' % (report_header['log_number']))
    column1_report_lines.append(u'Course Name: %s' % (report_header['course_name']))
    column1_report_lines.append(u'MFRI Office: %s' % (report_header['mfri_office_name']))
    column1_report_lines.append(u'Instructor: %s UID: %s' % (report_header['lead_instructor_name'], report_header['lead_instructor_uid']))
    column1_report_lines.append(u'Location: %s' % (report_header['location_name']))

    if one_column:
        column1_report_lines.append(report_header['course_dates'])
        column3_report_lines.append(u'')
    else:
        column1_report_lines.append(u'')
        column3_report_lines.append(report_header['course_dates'])

    if not report_title:
        column1_report_lines.append(u'')
    
    if report_lines:
        report_header = [report_lines]
    else:
        report_header = [
                        [column1_report_lines[0], u'', u''],
                        [column1_report_lines[1], u'', column3_report_lines[0]],
                        [column1_report_lines[2], u'', u''],
                        [column1_report_lines[3], u'', u''],
                        [column1_report_lines[4], u'', u''],
                        [column1_report_lines[5], u'', u''],
                    ]
    return report_header

def report_error_pdf(request, return_pdf=True, error_message=None, user_error=False, program_error=False, scheduled_course=None):

    if not return_pdf:
        PDF404Template = get_template('transcript/pdf404.html')

        PDF404Context = RequestContext(request,{'error_message': error_message})
        
        PDF404Html = PDF404Template.render(PDF404Context)
        
        return HttpResponse(PDF404Html)
    else:

        letter_portrait_width, letter_portrait_height = letter        
        #letter_landscape_height, letter_landscape_width = letter        

        large_font = 14
        medium_font = 12
        small_font = 10
        very_small_font = 8
        very_very_small_font = 6

        filename = u'pdf404.pdf'

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
    #    response['Content-Disposition'] = u'attachment; filename=%s' % (filename)
        response['Content-Disposition'] = u'filename=%s' % (filename)

        pdf_not_found_report_buffer = StringIO()

        pdf_not_found_report = SimpleDocTemplate(pdf_not_found_report_buffer, pagesize=letter)

        pdf_not_found_report.topMargin = .5 * inch
        pdf_not_found_report.bottomMargin = .5 * inch
        pdf_not_found_report.leftMargin = .5 * inch
        pdf_not_found_report.rightMargin = .5 * inch

        elements = []

        report_form_header = mfri_report_header(scheduled_course=scheduled_course, report_title=u'Textbook Tracking Form') #20170711

        report_list_header_width = {
                                        'col1': 3 * inch,
                                        'col2': 2 * inch,
                                        'col3': 3 * inch,
                                      }


        report_form_header_table = Table(report_form_header, colWidths=[report_list_header_width['col1'], report_list_header_width['col2'], report_list_header_width['col3']])
        report_form_header_table.setStyle(TableStyle([
                                                ('ALIGN',(1,0),(1,3),'CENTER'),
                                                ('ALIGN',(-1,0),(-1,4),'RIGHT'),
                                                ('ALIGN',(0,0),(0,4),'LEFT'),
                                                ('FONTSIZE',(0,0),(-1,-1),12),
                                                #('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                                #('BOX', (0,0), (-1,-1), 0.5, colors.black),
                                                ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.black),
                                                ('BOTTOMPADDING',(0,0),(-1,-2),0),
                                                ('BOTTOMPADDING',(0,-1),(-1,-1),4),
                                                ('TOPPADDING',(0,0),(-1,-1),0),
                                                  ]))

        elements.append(report_form_header_table)

        elements.append(Spacer(1,.25*inch))

        stylesheet = getSampleStyleSheet()
        table_cell_stylesheet = getSampleStyleSheet()

        stylesheet['Normal'].fontSize = medium_font
        stylesheet['Normal'].leading = stylesheet['Normal'].fontSize + 2

        table_cell_stylesheet['Normal'].fontSize = medium_font
        table_cell_stylesheet['Normal'].leading = table_cell_stylesheet['Normal'].fontSize + 2

        report_main_text = u''
        
        if user_error:
            report_main_text = u'We are unable to print the report because of insufficient information. <br /><br />'

            if error_message:
                report_main_text += u'%s' % (error_message)
        elif program_error:
            report_main_text = u'We are unable to print the report at this time. Please contact support at: <a href="mailto:itdev@mfri.org">itdev@mfri.org</a><br /><br />'

            if error_message:
                report_main_text += u'%s' % (error_message)
        else:
            report_main_text = u'We are unable to print the report at this time. Please contact support at: <a href="mailto:itdev@mfri.org">itdev@mfri.org</a><br /><br />'

            if error_message:
                report_main_text += u'%s' % (error_message)
        
        
        report_main_text_paragraph = Paragraph(report_main_text, stylesheet['Normal'])
        elements.append(report_main_text_paragraph)

        pdf_not_found_report.build(elements)

        response.write(pdf_not_found_report_buffer.getvalue())
        pdf_not_found_report_buffer.close()
        return response
        


def return_resource_assignment_report_pdf(request, scheduled_course=None): 
    """
      return a pdf of the certification_list for the user specified by ssn and last name
    """
        
    resource_assignment_pdf = create_resource_assignment_report_pdf( 
                                  scheduled_course=scheduled_course,
                                 )    
    
    if resource_assignment_pdf:
        return resource_assignment_pdf
    else:
        return report_error_pdf(request, error_message=u'There was an error creating PDF for certification_list.', scheduled_course=scheduled_course)


class BlankReportDocTemplate(BaseDocTemplate):
    """Override the BaseDocTemplate class to print watermark on form."""

    def __init__(self, *args, **kwargs):

        BaseDocTemplate.__init__(self, *args, **kwargs)


