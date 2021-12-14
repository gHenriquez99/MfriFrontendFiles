#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use SEMINAR_MAINT;
use Database;
use CGI;
use strict;
#use PDF::Reuse;
use PDF_DRAW;
use POSIX;
use SCHEDULE_MAINT;
use DATE_UTIL;
use MFRI_STRINGS; #20190418

use DBK;

my $ScheduledCourseID = CGI::param( 'SCID' );
$ScheduledCourseID = 0 if (not defined $ScheduledCourseID);


if(!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}

my ($CurrentYear, $CurrentMonth, $CurrentDay) = DATE_UTIL::CurrentDate();
my ($CurrentHour, $CurrentMinute, $CurrentSecond) = DATE_UTIL::CurrentTime();

my $ReportDate =  qq{Report Date: } . $CurrentMonth . "-" . $CurrentDay . "-" . $CurrentYear . " " . $CurrentHour . ":" . $CurrentMinute;

#my $Course_Query_String = qq
#{
#SELECT
#SC.LogNumber,
#SC.InstructorID,
#SC.LocationID,
#CD.CourseCode
#FROM ScheduledCourses AS SC,
#CourseDescriptions AS CD
#WHERE (SC.ID = $ScheduledCourseID) AND (SC.CourseID = CD.Id)   
#};

#tgs 20050909 SSN blow was IDNumber
 
my $Student_Query_String = qq
{
SELECT
ST.LastName,
ST.Suffix,
ST.FirstName,
LEFT(ST.MiddleName, 1),
SR.StatusID,
SR.Grade,
SR.GradeID,
SR.PercentageScore,
SR.GradeNote,
SR.StatusNote
FROM StudentRecords AS ST,
StudentRegistration AS SR
WHERE 
(SR.SchedCourseID = $ScheduledCourseID) AND
(SR.StudentID = ST.ID) AND
(SR.StatusID != 4) AND (SR.StatusID != 22)
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, ST.Suffix, SR.Created    
};

#(SR.StatusID in (8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 ))

my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($ScheduledCourseID);



my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";

my $i = 0;
my $student_counter = 1;

my $EntryCount = 0;
my $EntriesPerPage = 3;

my $PageWidth = 836;
my $PageHeight = 1029;#1029;

my $FormWidth = $PageWidth - 20;
my $FormHeight = $PageHeight / $EntriesPerPage;

my $StartTextY = $PageHeight - PDF_DRAW::get_line_delta();#- 12;#268; #270 #340; #480

my $leftXOffset = 10;#60;

my $currY = $StartTextY;

my $leftX = 1;# 7

my $course_code = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 1);
my $course_name = $ScheduleInfo->{Title};
my $location = $ScheduleInfo->{LocationName};
my $StartDate = DATE_UTIL::ReorderDate($ScheduleInfo->{StartDate}, "MDY");
my $EndDate = DATE_UTIL::ReorderDate($ScheduleInfo->{EndDate}, "MDY");


print_doc_header();
my $page_number = 1;
my $page_count = 0;
print_report();
print_doc_footer();
$db->finish(); #03-14-2005 WPL Added DB Finish

sub print_report
{
    if ($need_to_query eq "YES")
    {
	$db->query($Student_Query_String);	
	$need_to_query = "NO";
    }
    
    
    #my $tmp = $db->num_rows();
#    warn "numrows: $tmp";

    if ($db->num_rows() == 0)
    {
      print_report_header();
      PDF_DRAW::center_text(40, $currY, "No Records."); # 227 #50
  	  print_report_footer();
	  return;
	}
	
	my @studentinfo;
    my $MarginAdjust = 0;
	
	while (@studentinfo = $db->get_row())
	{
#warn "1 currY: $currY";
       if (0 == $EntryCount) 
	   {
	     $MarginAdjust = 0;
       }
	   elsif (1 == $EntryCount)
	   {
	     $MarginAdjust = PDF_DRAW::get_line_delta() * 2;
       }		
	   else
	   {
	     $MarginAdjust = PDF_DRAW::get_line_delta() * 5;
       }		

        $currY = $StartTextY - ($EntryCount * $FormHeight) - $MarginAdjust;
#my $t1 = $EntryCount * $FormHeight;
#my $t2 = $StartTextY - $t1;

#warn "2 currY: $currY";
#warn "StartTextY: $StartTextY";
#warn "EntryCount: $EntryCount";
##warn "FormHeight: $FormHeight";
#warn "EntryCount * FormHeight: $t1";
#warn "StartTextY - EntryCount * FormHeight: $t2";

		print_report_header();
	    print_student_entry(@studentinfo);  
		$page_number++;
		
		$EntryCount++;

		if ($EntriesPerPage == $EntryCount) 
		{
	      $EntryCount = 0;
          $currY = $StartTextY;
		  print_report_footer();
		  PDF_DRAW::new_page();
		}

	}

	
}

sub print_doc_header
{   
    #PDF_DRAW::doc_header(1029, 836);
#    PDF_DRAW::doc_header(950, 411);

    PDF_DRAW::doc_header($PageWidth, $PageHeight);

	PDF_DRAW::set_formatting(1);

    PDF_DRAW::set_font(PDF_DRAW::get_default_font());
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

sub print_doc_footer
{
    PDF_DRAW::doc_footer();
}

sub print_report_header
{

  return;
}

   

sub print_report_footer
{
  return;    
}

sub print_boiler_plate
{
  my $GradeID = shift;

  my $BPcurrY = $currY;

  my $HeaderStart = $BPcurrY;
  my $HeaderSize = 0;

  my $FontSize = PDF_DRAW::get_default_font_size() + 2;

    PDF_DRAW::set_font_size($FontSize); 
	$BPcurrY = PDF_DRAW::center_text($PageWidth/2, $BPcurrY, "<b>UNIVERSITY OF MARYLAND</b>");  
	$BPcurrY -= 2;
	$BPcurrY = PDF_DRAW::center_text($PageWidth/2, $BPcurrY, "<b>MARYLAND FIRE AND RESCUE INSTITUTE</b>");  
	$BPcurrY -= 2;
	$BPcurrY = PDF_DRAW::center_text($PageWidth/2, $BPcurrY, "<b>COLLEGE PARK, MARYLAND 20742</b>");  
	$BPcurrY -= 2;
	$BPcurrY = PDF_DRAW::center_text($PageWidth/2, $BPcurrY, "<b>FINAL GRADE REPORT</b>");  
    
	$HeaderSize = $HeaderStart - $BPcurrY + 16;

	$BPcurrY += 5;#2;

    my $TopLineY = $BPcurrY;
    my $BottomLineY = 0;


	$BPcurrY -= 5;#2;

	$BPcurrY -= 10;#2;

	$currY = $BPcurrY;

    #PDF_DRAW::draw_line($leftXOffset + 45, $BPcurrY, 400, $BPcurrY);
    $BPcurrY = PDF_DRAW::text($leftXOffset + 10, $BPcurrY, "Name:"); 
	$BPcurrY -= 2;
    #PDF_DRAW::draw_line($leftXOffset + 157, $BPcurrY, 400, $BPcurrY);
    $BPcurrY = PDF_DRAW::text($leftXOffset + 10, $BPcurrY, "Course or Training Seminar:"); 
	$BPcurrY -= 2;
    #PDF_DRAW::draw_line($leftXOffset + 127, $BPcurrY, 400, $BPcurrY);
    $BPcurrY = PDF_DRAW::text($leftXOffset + 10, $BPcurrY, "Class Location:"); 

	$BPcurrY -= 2;
    #PDF_DRAW::draw_line($leftXOffset + 147, $BPcurrY, 400, $BPcurrY);
    $BPcurrY = PDF_DRAW::text($leftXOffset + 10, $BPcurrY, "Final Grade:"); 
	 
    #$currY -= 17;

	if ((2 == $GradeID) || (7 == $GradeID)) 
    {
      $BPcurrY -= 2;
    
	  $BPcurrY = PDF_DRAW::text($leftXOffset + 40, $BPcurrY, "You have successfully completed the course."); 
      $BPcurrY -= 10;
      $BPcurrY = PDF_DRAW::text($leftXOffset + 120, $BPcurrY, " "); 
      $BPcurrY = PDF_DRAW::text($leftXOffset + 120, $BPcurrY, " "); 
      $BPcurrY = PDF_DRAW::text($leftXOffset + 120, $BPcurrY, " "); 
      $BPcurrY = PDF_DRAW::text($leftXOffset + 120, $BPcurrY, " "); 
      $BPcurrY = PDF_DRAW::text($leftXOffset + 120, $BPcurrY, " "); 

    } 
	else
    {
      $BPcurrY -= 2;
      $BPcurrY = PDF_DRAW::text($leftXOffset + 40, $BPcurrY, "You did not successfully complete the course for the following reason:"); 

	  $BPcurrY -= 2;
      $BPcurrY = PDF_DRAW::text($leftXOffset + 60, $BPcurrY, "( ) Exam grade was less than 70%"); 

	  $BPcurrY -= 2;
      $BPcurrY = PDF_DRAW::text($leftXOffset + 60, $BPcurrY, "( ) Instructor evaluation was unsatisfactory"); 

      $BPcurrY -= 2;
      $BPcurrY = PDF_DRAW::text($leftXOffset + 60, $BPcurrY, "( ) Attendance requirement was unsatisfactory"); 
	 
      $BPcurrY -= 2;
      $BPcurrY = PDF_DRAW::text($leftXOffset + 60, $BPcurrY, "( ) Failed to complete required class session(s)"); 

	  $BPcurrY -= 2;
      $BPcurrY = PDF_DRAW::text($leftXOffset + 60, $BPcurrY, "( ) Skills card unsatisfactory"); 
	}
	
    $BottomLineY = $BPcurrY + 5;

	$BPcurrY -= 10;

	#$BPcurrY = PDF_DRAW::text($leftXOffset + 10, $BPcurrY, "STATION CERTIFICATES: Where applicable, at the close of training season, station certificates will be"); 
	#$BPcurrY -= 2;
	#$BPcurrY = PDF_DRAW::text($leftXOffset + 10, $BPcurrY, "prepared and distributed to the companies of the successful graduates."); 
	

	#PDF_DRAW::draw_line($leftXOffset, $TopLineY, $leftXOffset, $PageHeight - $FormHeight + $HeaderSize);  
    PDF_DRAW::draw_line($FormWidth, $TopLineY, $FormWidth, $BottomLineY);  
    PDF_DRAW::draw_line($FormWidth-1, $TopLineY, $FormWidth-1, $BottomLineY);  
	PDF_DRAW::draw_line($leftXOffset, $TopLineY, $leftXOffset, $BottomLineY);  
	PDF_DRAW::draw_line($leftXOffset+1, $TopLineY, $leftXOffset+1, $BottomLineY);  

	#PDF_DRAW::draw_line($leftXOffset, $PageHeight - $FormHeight + $HeaderSize, $FormWidth, $PageHeight - $FormHeight + $HeaderSize);
    PDF_DRAW::draw_line($leftXOffset, $TopLineY, $FormWidth, $TopLineY);
    PDF_DRAW::draw_line($leftXOffset, $TopLineY-1, $FormWidth, $TopLineY-1);
	PDF_DRAW::draw_line($leftXOffset, $BottomLineY, $FormWidth, $BottomLineY);
	PDF_DRAW::draw_line($leftXOffset, $BottomLineY+1, $FormWidth, $BottomLineY+1);

	PDF_DRAW::text($FormWidth - (20 * $FontSize), $BottomLineY+4, $ReportDate);  

	PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
    
}

sub print_student_entry
{
    #warn "printing entry";
    my ($last_name, $suffix, $first_name, $middle_name, $StatusID, $Grade, $GradeID, $PercentageScore, $GradeNote, $StatusNote) = @_;

    my $student_name;
 
    print_boiler_plate($GradeID);
    #my $currY = 220 - (($currEntries) * (PDF_DRAW::get_default_font_size() + 14));
  
    #tgs 20050909 $student_name = $last_name;
    #tgs 20050909 $student_name .= ", $first_name" if ($first_name ne "");

    #20190418+
    my $maxNameLength = 100; #max length for student name  might need to try 20
    my $nameString = MFRI_STRINGS::Build_Name($first_name, $middle_name, $last_name, $suffix, 1, ($maxNameLength > 0), $maxNameLength, 1); 
    #20190418-

    #20190418my $nameString = "$last_name";
    #20190418if (length($suffix) > 0)
	#20190418{
	#20190418  $nameString .= " $suffix,";
	#20190418}
	#20190418else
	#20190418{
	#20190418  $nameString .= ",";
	#20190418}

	#20190418if ((length($first_name) > 0) || (length($middle_name) > 0))
	#20190418{
    #20190418  $nameString .= " $first_name $middle_name";
	#20190418}
	#20190418else
	#20190418{
    #20190418  $nameString = "";
	#20190418}	

	if (length($PercentageScore) == 0) 
	{
	  $PercentageScore = 0;
	}

    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 2); 
	$currY = PDF_DRAW::text($leftXOffset + 50, $currY, "<b>" . $nameString . "</b>");  
    
	$currY -= 2;
    $currY = PDF_DRAW::text($leftXOffset + 166, $currY, "<b>" . $course_name . " " . $course_code . "</b>"); 
	$currY -= 2;

    if ($StartDate eq $EndDate)
    {
      $currY = PDF_DRAW::text($leftXOffset + 98, $currY, "<b>" . $location . "</b>" . " Course Date: <b>" . $StartDate . "</b>"); 
    }
    else
    {
        $currY = PDF_DRAW::text($leftXOffset + 98, $currY, "<b>" . $location . "</b>" . " Course Dates: <b>" . $StartDate . " - " . $EndDate . "</b>"); 
    }

	$currY -= 2;
    $currY = PDF_DRAW::text($leftXOffset + 82, $currY, "<b>" . $PercentageScore  . "</b>" . " %" ); 
	 
    #$currY -= 17;

	#if (9 == $StatusID)
##	if ((2 == $GradeID) || (7 == $GradeID))
##	{
##	  $currY -= 2;
##	  $currY = PDF_DRAW::text($leftXOffset + 115, $currY, "<b>" . "X" . "</b>"); 
	  #$currY -= 2;
	  #$currY = PDF_DRAW::text($leftXOffset + 115, $currY, "(   )"); 
##	}
##	else
##	{
##	  $currY -= 2;
##	  $currY = PDF_DRAW::text($leftXOffset + 115, $currY, " "); 
##	  $currY -= 2;
##	  $currY = PDF_DRAW::text($leftXOffset + 115, $currY, "<b>" . "X" . "</b>"); 
##	}
	 
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
    #warn "done.";
    #die;
    
}




