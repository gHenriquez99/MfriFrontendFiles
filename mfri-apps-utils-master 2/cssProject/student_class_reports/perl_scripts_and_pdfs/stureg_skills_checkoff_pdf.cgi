#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use SEMINAR_MAINT;
use Database;
#use CGI;
use CGI qw(:standard);
use SCHEDULE_MAINT;
use MFRI_STRINGS; #20190418

use strict;
use PDF_DRAW;
#use PDF::API2;
use PDF::Reuse;

use DBK;

#use APPDEBUG;

my $ScheduledCourseID = CGI::param( 'SCID' );

$ScheduledCourseID = 0 if (!defined $ScheduledCourseID);


if (!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "you must be logged in to access the attendance record." );
	MFRI::redirect( "error.cgi" );
	exit;
}
#my $Course_Query_String = qq
#{
#SELECT
#SC.LogNumber,
#SC.InstructorID,
#SC.LocationID,
#SC.StartDate,
#SC.EndDate,
#CD.CourseCode
#FROM ScheduledCourses AS  SC,
#CourseDescriptions AS CD
#WHERE (SC.ID = $ScheduledCourseID) AND (SC.CourseID = CD.Id)   
#};

my $RecordsPerPage = 25; #was 46; tgs
my $SkillsPerPage = 40; #tgs
my $TotalSkills = 160; #tgs


my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($ScheduledCourseID);

my $Student_Query_String = qq
{
SELECT
ST.LastName,
ST.Suffix,
ST.FirstName,
LEFT(ST.MiddleName, 1)
#ST.IDNumber
FROM StudentRecords AS ST,
StudentRegistration AS SR,
Affiliations AS A
WHERE (SR.StudentID = ST.ID) AND
(SR.AffiliationID = A.ID) AND
(SR.SchedCourseID = $ScheduledCourseID) AND
(SR.StatusID != 4) AND (SR.StatusID != 22)
ORDER BY ST.LastName, ST.FirstName, SR.Created    
};

# AND (SR.StatusID != 7)


my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );

my $need_to_query = "YES";

my $i = 0;
my $student_counter = 1;
my $maxEntries = $RecordsPerPage; #45;

my $NameX = 22;
my $NameWidth = 224;
    my $cellHeight = 24;#15;#tgs #18 #23
    my $topY = 766;
    my $cellTopY = 735;
    my $leftX = 1; #7
    my $rightX = 1024; #992; #1028

my $NumberOfPages = $TotalSkills / $SkillsPerPage;

#APPDEBUG::WriteDebugMessage("TotalSkills $TotalSkills");	
#APPDEBUG::WriteDebugMessage("SkillsPerPage $SkillsPerPage");	
#APPDEBUG::WriteDebugMessage("NumberOfPages $NumberOfPages");	


my $page_number = 1;
my $output_file = "/tmp/REPORT$$";

  print_doc_header();

for ($page_number = 1; $page_number <= $NumberOfPages; $page_number++) #tgs 40
{

  print_attendance();

  $need_to_query = "YES";
  $student_counter = 1;
  #$i = 0;
  #tgs 20051017 $page_number = 2;
  #prPage();
  #tgs 20051017 print_attendance();
  PDF_DRAW::new_page();
}


print_doc_footer();
$db->finish(); #03-11-2005 WPL Added DB Finish



#useless... used before for placeholders
sub get_course_info
{
    return ($db->get_row());
}

sub get_student_info
{
    return ($db->get_row());
}




sub print_attendance
{
    print_attendance_header();
	
    if ($need_to_query eq "YES") 
    {
	$db->query( $Student_Query_String );	
	$need_to_query = "NO";
    }
    

    if ($db->num_rows() > 0)
    {
	  my @studentinfo;
	
	  while (@studentinfo = $db->get_row())
	  {
	    
	    if ($student_counter >= $maxEntries)
	    {
		  print_attendance_footer(); #Print a page footer
		  PDF_DRAW::new_page();  #Start a new page
		  #$page_number++;        #Increment the page counter
		  print_attendance_header(); #Print a page header
		  $student_counter = 1;
	    }

		
	    print_student_entry(@studentinfo);    
	    $student_counter++;
	    
	  }

	
	
    }

#Pad out the rest of the form with blank entries
    while ($student_counter <= $maxEntries)
    {
	  print_student_entry("", "", "", "", "");
	  $student_counter++;
    }

    print_attendance_footer();
    #Draw lines
    
}



sub print_doc_header
{
    #print "Content-type: application/pdf\n\n";
    #prFile(undef);
    #prMbox(0, 0, 1029, 836);
	PDF_DRAW::doc_header(1029, 836);
    PDF_DRAW::set_font(PDF_DRAW::get_default_font());
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

sub print_doc_footer
{
    #prEnd();
	PDF_DRAW::doc_footer();
}

sub print_attendance_header
{
#    my ($logNum, $instructor) = @_;
    my $logNum = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 1);
    my $instructor = $ScheduleInfo->{InstructorName};
    my $pagenum = get_page_num();
    my $i;
    my $currX;
    my $currY;
    
	if (($instructor eq "MFRI Instructor") || ($instructor eq "MFRI Staff"))
	{
	  $instructor = "";
	}
	
#APPDEBUG::WriteDebugMessage("print_attendance_header");	
#APPDEBUG::WriteDebugMessage("pagenum $pagenum");	
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 4);

    if ($pagenum == 1)
    {
	  PDF_DRAW::text(7, 806, "MARYLAND FIRE & RESCUE INSTITUTE"); #792
	  PDF_DRAW::text(7, 792, "UNIVERSITY OF MARYLAND"); #778
    }
    
    PDF_DRAW::text(7, 778, "Skills Completion");
	
    PDF_DRAW::text(350, 778, "LOG: $logNum");
    PDF_DRAW::text(760, 778, "INSTRUCTOR: $instructor");
    
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+4); #1
    PDF_DRAW::center_text(64, 743, "Student Name"); #70
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());

    
    $currX = $NameWidth + 8;   #200     

#    if ($pagenum == 1)
#    {
	  my $ColumnNumberStart = (($SkillsPerPage * $pagenum) - $SkillsPerPage) + 1; 
	  my $ColumnNumberStop = $SkillsPerPage * $pagenum;
#APPDEBUG::WriteDebugMessage("SkillsPerPage $SkillsPerPage");	
#APPDEBUG::WriteDebugMessage("ColumnNumberStart $ColumnNumberStart");	
#APPDEBUG::WriteDebugMessage("ColumnNumberStop $ColumnNumberStop");		   
	
#	  for ($i = 1; $i <= 40; $i++)
	  for ($i = $ColumnNumberStart; $i <= $ColumnNumberStop; $i++)
	  {	
	    PDF_DRAW::center_text($currX+2, 743, "$i");
	      $currX += 20;
	  }    
#    }
#    else
#    {
#	  for ($i = 41; $i <= 80; $i++)
#	  {	
#	    PDF_DRAW::center_text($currX+2, 743, "$i");
#	      $currX += 20;
#	  }  

#    }
	


    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}
   
sub print_attendance_footer
{

    my $pageNum = get_page_num();

    if ($pageNum == 1)
    {
	  PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 4);
	  PDF_DRAW::text(7, 40, "I verify that these students have performed the objectives listed at the indicated level of proficiency.");
	  PDF_DRAW::text(7, 18, "Instructor's Signature ______________________________________________________");
	  PDF_DRAW::text(700, 18, "Date _______________________________");
	  PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() - 2);
	  PDF_DRAW::text(7, 5, "(     - Satisfactory         - Unsatisfactory)");

	  #Draw Check
	  PDF_DRAW::draw_line(15, 3, 20, 12);
	  PDF_DRAW::draw_line(12, 7, 15, 3);

	  #Draw X
	  PDF_DRAW::draw_line(85, 3, 93, 12);
	  PDF_DRAW::draw_line(85, 12, 93, 3);
      }

	Print_Page_Lines();


}


sub print_student_entry
{
    my ($last_name, $suffix, $first_name, $middle_name) = @_;
    my $pagenum = get_page_num();
 
    #my $currY = 725 - (($student_counter-1) * (PDF_DRAW::get_default_font_size() + 12)); #was 4 before that #5 #tgs #7
	
	my $currY = 725 - (($student_counter-1) * $cellHeight + 4); #was 4 before that #5 #tgs #7
    

    #PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() - 1); #tgs
	PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 2); #1
    PDF_DRAW::text(5, $currY, $student_counter); #11
    
    #20190418+
    my $MaxNameLength = 23;
    my $nameString = MFRI_STRINGS::Build_Name($first_name, $middle_name, $last_name, $suffix, 1, ($MaxNameLength > 0), $MaxNameLength, 1); 
    #20190418-

    #tgs 20050909 my $nameString = "$last_name, $first_name";
	#20190418my $nameString = "$last_name";
    #20190418if (length($suffix) > 0)
	#20190418{
	#20190418  $nameString .= " $suffix,";
	#20190418}
	#20190418else
	#20190418{
	#20190418  $nameString .= ",";
	#20190418}
	#20190418
	#20190418my $MaxNameLength = 23;
	#20190418my $NameLength = length($nameString) + length($first_name) + length($middle_name);
	#20190418
	#20190418if ($NameLength > $MaxNameLength)
	#20190418{
    #20190418  #$nameString .= " " . substr($first_name, 0, ($MaxNameLength - $NameLength)) . ".";
	#20190418  $nameString .= " " . substr($first_name, 0, 1);
    #20190418  $nameString .= " " . $middle_name;
	#20190418}
	#20190418else
	#20190418{
    #20190418  $nameString .= " $first_name $middle_name";
	#20190418}
	#20190418
    #20190418$nameString = "" if (($last_name eq "") && ($first_name eq ""));  
	 	
    PDF_DRAW::text($NameX, $currY, $nameString); #32
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

sub get_page_num
{
    return $page_number;
}

sub Print_Page_Lines
{

    my $bottomY = $cellTopY - $cellHeight * ($student_counter-1);
    
    PDF_DRAW::draw_line($leftX, $topY, $leftX, $bottomY); #Left Line
    #PDF_DRAW::draw_line(28, $topY, 28, $bottomY);         #Name Line
    #PDF_DRAW::draw_line(143, $topY, 143, $bottomY);       #Soc Line
    #PDF_DRAW::draw_line(213, $topY, 213, $bottomY);       #Date Line
    
    my $i;
    my $currX;
    for ($i = 0; $i < $SkillsPerPage; $i++) #tgs 40
    {
	  $currX = $NameWidth + ($i * 20); #192
	  PDF_DRAW::draw_line($currX, $topY, $currX, $bottomY);
    }

    
    
    PDF_DRAW::draw_line($rightX, $topY, $rightX, $bottomY); #Last Line

    #Horizontal lines
    PDF_DRAW::draw_line($leftX, $topY, $rightX, $topY);

    my $currY;
    for ($i = 0; $i < $student_counter; $i++)
    {
	  $currY = $cellTopY - $cellHeight * $i;
	  PDF_DRAW::draw_line($leftX, $currY, $rightX, $currY);
    }

}





