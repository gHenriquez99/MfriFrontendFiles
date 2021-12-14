#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use Database;
use CGI;
use strict;
use PDF_DRAW;
use SCHEDULE_MAINT;
use STUREG_MAINT;
use DATE_UTIL;
use STUREC_PREFS;
use MFRI_UTIL;
use DBK;

#use APPDEBUG;

#Kick the user out if they aren't logged in
if(!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}

#Check the user's permissions...
my $UserID = MFRI::get_current_userid();
my ($IDReadPermission, $IDWritePermission) = STUREC_PREFS::Get_UserPermissionsID($UserID);
#my ($IDReadPermission, $IDWritePermission) = STUREC_PREFS::Get_UserPermissionsID($UserID);

if ($IDReadPermission == 0)
{
    MFRI::set_parameter("error", "You do not have permission to access this feature.");
      MFRI::redirect("error.cgi");
	exit;
}

my $SCID = CGI::param('SCID') || 0;
my $orderBySSN = CGI::param('OBS') || 0;

if ($orderBySSN != 0)
{
  $orderBySSN = 1;
}

if ($SCID <= 0)
{
    MFRI::set_parameter("error", "You must specify which course to print statistics for.");
      MFRI::redirect("error.cgi");
	exit;
}

my $RegisteredCount = STUREG_MAINT::get_registration_count($SCID);

my $SuccessfulCompletionCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 9);
my $FailedCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 19); #Final
   $FailedCount += STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 10); #Midterm

    
my $DroppedCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 7);
my $IncompleteEvaluationCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 11);
my $IncompleteCourseRequirementCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 12);
my $IncompleteAttendanceCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 13);
my $IncompleteWorkConflictCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 14);
my $IncompleteDepartmentConflictCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 15);
my $IncompleteHomeConflictCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 20 );
my $IncompleteIllnessCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 16);
my $IncompleteToStartClassCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 17);
my $IncompleteOtherCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 18);
my $IncompleteCount = STUREG_MAINT::Calculate_RegistrationStatus_Count($SCID, 21) + $DroppedCount + $IncompleteOtherCount + $IncompleteToStartClassCount + $IncompleteIllnessCount + $IncompleteHomeConflictCount + $IncompleteDepartmentConflictCount + $IncompleteAttendanceCount + $IncompleteCourseRequirementCount + $IncompleteEvaluationCount;

my $StudentHours = STUREG_MAINT::Get_Course_Hours($SCID);

my $ScheduledCourseInfo = MFRI_UTIL::GetScheduledCourse($SCID);

my $InstructorName = "";
my $InstructorUIDNumber = "";

if ( defined $ScheduledCourseInfo)	
{

	if ( defined $ScheduledCourseInfo->{InstructorName})	
	{
      $InstructorName = $ScheduledCourseInfo->{InstructorName};
	}

	if ( defined $ScheduledCourseInfo->{InstructorIDNumber})	
	{
      $InstructorUIDNumber = $ScheduledCourseInfo->{InstructorIDNumber};
	}
}

if (($InstructorName eq "MFRI Instructor") || ($InstructorName eq "MFRI Staff"))
{
  $InstructorName = "";
  $InstructorUIDNumber = "";
}


my $topY = 1010;
my $currY = $topY;
my $leftX = 30;
my $pageNum = 1;
my $maxLinesPage = 70;
my $minYPage = $topY - $maxLinesPage * PDF_DRAW::get_line_delta();


print_doc_header();
print_page_header();

print_doc_footer(); #End the pdf document and print it to the screen




sub print_doc_header
{
    PDF_DRAW::doc_header(836, 1029); #Create the document
    PDF_DRAW::set_formatting(1); #Turn on formatting so we can use tags (optional)
    PDF_DRAW::set_font("Times-Roman"); #Set the font (optional)
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+ 4); #Set the font size (optional)
}

sub print_doc_footer
{
    PDF_DRAW::doc_footer(); #Finish and print the document
}


sub print_page_header
{
	
#    Please note!!! Items marked with an * are your responsiblity to complete accurately and promptly.  The other items will be completed by the regional office.  Upon your completion please return to the regional office.

    my $headerText = qq
    {
      <b>INFORMATION FOR THE INSTRUCTOR</b><br>$ScheduledCourseInfo->{LogNumber}<br>
      Upon completion please return to the regional office.
      <br><br>
	  CLASS DATA
    };

    my $RegisteredLabel = qq{Number of Students Registered};
    my $SuccessfullyCompletingLabel = qq{Number of Students Successfully Completing};
    my $FailingExamLabel = qq{Number of Students Failing Exam};
    my $IncompleteLabel = qq{Number of Students Incomplete};
#    my $IncompleteEvaluationLabel = qq{*1. Instructor evaluation};
#    my $IncompleteCourseRequirementLabel = qq{*2. Other course requirement};
#    my $IncompleteAttendanceLabel = qq{*3. Attendance};
#    my $IncompleteWorkConflictLabel = qq{*4. Work schedule conflict};
#    my $IncompleteDepartmentConflictLabel = qq{*5. Department activities conflict};
#    my $IncompleteHomeConflictLabel = qq{*6. Home activities conflict};
#    my $IncompleteIllnessLabel = qq{*7. Illness};
#    my $IncompleteToStartClassLabel = qq{*8. Attended only to get class started};
#    my $IncompleteOtherLabel = qq{*9. Other};
#    my $IncompleteNoteLabel = qq{*Note:};
    my $LongUnderline = qq{________________________};
    my $ShortUnderline = qq{____________};
    my $TotalNumberofStudentHoursLabel = qq{<b>TOTAL NUMBER OF STUDENT HOURS</b>};

    my $SupportInstructorsLabel1 = qq{INSTRUCTOR};
    my $SupportInstructorsLabel2 = qq{NAMES};
    my $SignatureLabel = qq{SIGNATURE};
    my $SSNLabel = qq{HOURS KEY};
    my $SESLabel = qq{SESSION};
    my $DateLabel = qq{DATE};
    my $HrsLabel = qq{HRS};


    my $LeadInstructorVerificationLabel1 = qq{LEAD INSTRUCTOR VERIFICATION};
    my $LeadInstructorVerificationLabel2 = qq{I certify that the information on this form is correct.};

    my $InstructorsNameLabel = qq{Instructor's Name};
    my $InstructorsNameHoursLabel = qq{Hours Taught};
    my $UIDNumberLabel = qq{University ID Number};
    my $InstructorSignatureLabel = qq{Instructor's Signature};
    my $InstructorSignatureDateLabel = qq{Date};

    my $HoursKeyLegend = qq{Check appropriate Hours Key box: H - Hours Only, L - Lead, M - Mentor, P - Proctor, R - Reader, S - Support};


    my $ValueUnderline = qq{________};

	my $LeftXIndented = $leftX + 100;
    
	my $ListTitleY;

    $RegisteredCount = $ValueUnderline if ( 0 == $RegisteredCount );
    $SuccessfulCompletionCount = $ValueUnderline if ( 0 == $SuccessfulCompletionCount );
    $FailedCount = $ValueUnderline if ( 0 == $FailedCount );
   
    $IncompleteCount = $ValueUnderline if ( 0 == $IncompleteCount );
    $IncompleteEvaluationCount = $ValueUnderline if ( 0 == $IncompleteEvaluationCount );
    $IncompleteCourseRequirementCount = $ValueUnderline if ( 0 == $IncompleteCourseRequirementCount );
    $IncompleteAttendanceCount = $ValueUnderline if ( 0 == $IncompleteAttendanceCount );
    $IncompleteWorkConflictCount = $ValueUnderline if ( 0 == $IncompleteWorkConflictCount );
    $IncompleteDepartmentConflictCount = $ValueUnderline if ( 0 == $IncompleteDepartmentConflictCount );
    $IncompleteHomeConflictCount = $ValueUnderline if ( 0 == $IncompleteHomeConflictCount );
    $IncompleteIllnessCount = $ValueUnderline if ( 0 == $IncompleteIllnessCount );
    $IncompleteToStartClassCount = $ValueUnderline if ( 0 == $IncompleteToStartClassCount );
    $IncompleteOtherCount = $ValueUnderline if ( 0 == $IncompleteOtherCount );


    $StudentHours = $ValueUnderline if ( 0 == $StudentHours );

    $currY = PDF_DRAW::wrap_text($leftX, $currY, 730, $headerText);
	
    $ListTitleY = $currY;
    $currY = PDF_DRAW::text($LeftXIndented, $ListTitleY, $RegisteredLabel);
    $currY = PDF_DRAW::text($leftX + 500 , $ListTitleY, $RegisteredCount);

    $ListTitleY = $currY;
    $currY = PDF_DRAW::text($LeftXIndented, $ListTitleY, $SuccessfullyCompletingLabel);
    $currY = PDF_DRAW::text($leftX + 500 , $ListTitleY, $SuccessfulCompletionCount);

    $ListTitleY = $currY;
    $currY = PDF_DRAW::text($LeftXIndented, $ListTitleY, $FailingExamLabel);
    $currY = PDF_DRAW::text($leftX + 500 , $ListTitleY, $FailedCount);

    $ListTitleY = $currY;
    $currY = PDF_DRAW::text($LeftXIndented, $ListTitleY, $IncompleteLabel);
    $currY = PDF_DRAW::text($leftX + 500 , $ListTitleY, $IncompleteCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteEvaluationLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteEvaluationCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteCourseRequirementLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteCourseRequirementCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteAttendanceLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteAttendanceCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteWorkConflictLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteWorkConflictCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteDepartmentConflictLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteDepartmentConflictCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteHomeConflictLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteHomeConflictCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteIllnessLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteIllnessCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteToStartClassLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteToStartClassCount);

#    $ListTitleY = $currY;
#    $currY = PDF_DRAW::text($LeftXIndented + 50, $ListTitleY, $IncompleteOtherLabel);
#    $currY = PDF_DRAW::text($leftX + 400 , $ListTitleY, "*" . $IncompleteOtherCount);

#    $currY = PDF_DRAW::text($LeftXIndented + 70, $currY, $IncompleteNoteLabel);
#    $currY = PDF_DRAW::text($LeftXIndented + 70, $currY, "*" . $LongUnderline);
#    $currY = PDF_DRAW::text($LeftXIndented + 70, $currY, "*" . $LongUnderline);

    my $CheckBoxWidth = PDF_DRAW::get_default_font_size() + 8;	
    my $CheckBoxColumn = 384;
    
    my $HoursWidth = $CheckBoxColumn + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth;
    
    my $LeftXPos = 0;
    my $ColumnSpace = 20;

	$ListTitleY = $currY;
    $currY = PDF_DRAW::text($LeftXIndented, $ListTitleY, $TotalNumberofStudentHoursLabel);
    $currY = PDF_DRAW::text($leftX + 500 , $ListTitleY, $StudentHours);

	$ListTitleY = $currY - 17;
    $currY = PDF_DRAW::center_text($leftX + 90, $ListTitleY, $SupportInstructorsLabel1);

	$ListTitleY = $currY;
    $currY = PDF_DRAW::center_text($leftX + 90, $ListTitleY, $SupportInstructorsLabel2);

    $currY = PDF_DRAW::center_text($leftX + 290, $ListTitleY, $SignatureLabel);
    $currY = PDF_DRAW::center_text($leftX + 441, $ListTitleY, $SSNLabel);
    $currY = PDF_DRAW::center_text($leftX + $HoursWidth + $ColumnSpace + 20, $ListTitleY, $SESLabel);
    $currY = PDF_DRAW::center_text($leftX + 605, $ListTitleY, $DateLabel);
    $currY = PDF_DRAW::center_text($leftX + 677, $ListTitleY, $HrsLabel);

	$ListTitleY = $currY - 17;

#APPDEBUG::WriteDebugMessage("HoursWidth $HoursWidth");
#APPDEBUG::WriteDebugMessage("leftX $leftX");

	my $i = 0;
	for ($i = 0; $i < 25; $i++)
	{
      #$currY = PDF_DRAW::text($leftX, $ListTitleY, $LongUnderline);
#      PDF_DRAW::draw_line($leftX, $ListTitleY - (PDF_DRAW::get_line_delta() / 5), 200, $ListTitleY - (PDF_DRAW::get_line_delta() / 5));
      PDF_DRAW::draw_line($leftX, $ListTitleY , 200, $ListTitleY );
#      $currY = PDF_DRAW::text($leftX + 200, $ListTitleY, $LongUnderline);
#      PDF_DRAW::draw_line($leftX + 200, $ListTitleY - (PDF_DRAW::get_line_delta() / 5), 400, $ListTitleY - (PDF_DRAW::get_line_delta() / 5));
      PDF_DRAW::draw_line($leftX + 200, $ListTitleY, 400, $ListTitleY);


#      $currY = PDF_DRAW::text($leftX + 400, $ListTitleY, $ShortUnderline);
      

      make_letter_box($leftX + $CheckBoxColumn + $CheckBoxWidth, $ListTitleY, "H");
      make_letter_box($leftX + $CheckBoxColumn + $CheckBoxWidth + $CheckBoxWidth, $ListTitleY, "L");
      make_letter_box($leftX + $CheckBoxColumn + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth , $ListTitleY, "M");
      make_letter_box($leftX + $CheckBoxColumn + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth , $ListTitleY, "P");
      make_letter_box($leftX + $CheckBoxColumn + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth, $ListTitleY, "R");
      make_letter_box($leftX + $CheckBoxColumn + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth + $CheckBoxWidth, $ListTitleY, "S");

#      $currY = PDF_DRAW::text($leftX + 500, $ListTitleY, $ValueUnderline);

      $LeftXPos = $leftX + $HoursWidth + $ColumnSpace;
      PDF_DRAW::draw_line($LeftXPos, $ListTitleY, $LeftXPos + 45, $ListTitleY); #500 575 

#      $currY = PDF_DRAW::text($leftX + 575, $ListTitleY, $ValueUnderline);
      $LeftXPos += 45 + $ColumnSpace;
      PDF_DRAW::draw_line($LeftXPos, $ListTitleY, $LeftXPos + 45, $ListTitleY);#$leftX + 575 650

#      $currY = PDF_DRAW::text($leftX + 650, $ListTitleY, $ValueUnderline);
      PDF_DRAW::draw_line($leftX + 650, $ListTitleY, 725, $ListTitleY);
	  
#	  $ListTitleY = $currY;
	  $ListTitleY -= PDF_DRAW::get_line_delta() + 12;
    }
    $currY = $ListTitleY;
	
	$ListTitleY = $currY - 17;
    $currY = PDF_DRAW::text($leftX, $ListTitleY, $HoursKeyLegend);
	
	$ListTitleY = $currY - 17;
    $currY = PDF_DRAW::text($leftX, $ListTitleY, $LeadInstructorVerificationLabel1);
    $currY = PDF_DRAW::text($leftX + 50, $currY, $LeadInstructorVerificationLabel2);

	$ListTitleY = $currY - 17;
    $currY = PDF_DRAW::text($leftX + 50, $ListTitleY, $InstructorsNameLabel);
	$currY = PDF_DRAW::text($leftX + 200, $ListTitleY, $LongUnderline);
	
    $currY = PDF_DRAW::text($leftX + 200, $ListTitleY, $InstructorName);  

    $currY = PDF_DRAW::text($leftX + 400, $ListTitleY, $InstructorsNameHoursLabel);
	$currY = PDF_DRAW::text($leftX + 490, $ListTitleY, $ShortUnderline);

	$ListTitleY = $currY;
    $currY = PDF_DRAW::text($leftX + 50, $ListTitleY, $UIDNumberLabel);
	$currY = PDF_DRAW::text($leftX + 200, $ListTitleY, $LongUnderline);

	$currY = PDF_DRAW::text($leftX + 200, $ListTitleY, $InstructorUIDNumber);

	$ListTitleY = $currY;
    $currY = PDF_DRAW::text($leftX + 50, $ListTitleY, $InstructorSignatureLabel);
	$currY = PDF_DRAW::text($leftX + 200, $ListTitleY, $LongUnderline);
    $currY = PDF_DRAW::text($leftX + 400, $ListTitleY, $InstructorSignatureDateLabel);
	$currY = PDF_DRAW::text($leftX + 440, $ListTitleY, $ShortUnderline);


}

sub make_letter_box
{
    my $x = shift;
    my $y = shift;
    my $char = shift;

    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() - 1);
    PDF_DRAW::center_text($x, $y, $char);
    PDF_DRAW::draw_rectangle_coords($x-7, $y+12, $x+7, $y-3);

    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

