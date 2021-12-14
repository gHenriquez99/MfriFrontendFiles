#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use MFRI_UTIL;
use MFRI_STRINGS;
use STUREG_MAINT;
use SEMINAR_MAINT;
use Database;
#use CGI;
use CGI qw(:standard);
use SCHEDULE_MAINT;
use DATE_UTIL;

use strict;
use PDF_DRAW;
#use PDF::API2;
use PDF::Reuse;

use DBK;

my $ScheduledCourseID = CGI::param( 'SCID' );

$ScheduledCourseID = 0 if (!defined $ScheduledCourseID);


if (!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "you must be logged in to access the attendance record." );
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
#DATE_FORMAT(SC.StartDate, "%m-%d-%Y"),
#DATE_FORMAT(SC.EndDate, "%m-%d-%Y"),
#CD.CourseCode
#FROM ScheduledCourses AS  SC,
#CourseDescriptions AS CD
#WHERE (SC.ID = $ScheduledCourseID) AND (SC.CourseID = CD.Id)   
#};

#AES_DECRYPT(ST.IDNumber, "} . DBK::Encrypt_Key() . qq{") AS IDNumber

my $Student_Query_String = qq
{
SELECT
ST.LastName,
ST.Suffix,
ST.FirstName,
LEFT(ST.MiddleName, 1)
FROM 
StudentRecords AS ST,
StudentRegistration AS SR,
Affiliations AS A
WHERE (SR.StudentID = ST.ID) AND
(SR.AffiliationID = A.ID) AND
(SR.SchedCourseID = $ScheduledCourseID) AND
(SR.StatusID != 4) AND (SR.StatusID != 22)
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, ST.Suffix, SR.Created    
};
#AND (SR.StatusID != 7)
my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($ScheduledCourseID);




my $i = 0;
my $student_counter = 1;
my $RecordsPerPage = 35;#25; #31 was 46; tgs

my $MaxSessions = 40; 

if ($ScheduleInfo->{InstructionalHours} > 0)
{
    $MaxSessions = $ScheduleInfo->{InstructionalHours} / 3;
}

my $SessionsPerPage = 20; #tgs
my $session_count_page_start = 1; #2013-07-26

my $currEntries = 0;

my $PriorPageEntriesCount = 0;

my $cellHeight = 18;#15;#tgs
my $topY = 766;
my $cellTopY = 690;
#my $bottomY = $cellTopY - $cellHeight * ($student_counter-1);
my $bottomY = $cellTopY - $cellHeight * $RecordsPerPage;
my $leftX = 7;
my $rightX = 1020;

my $ColumnX1 = $leftX;
my $ColumnX2 = 28;
my $ColumnX3 = 278;
my $ColumnX4 = 325; #395

my $ColumnX1Width = $ColumnX2 - $ColumnX1;
my $ColumnX2Width = $ColumnX3 - $ColumnX2;
my $ColumnX3Width = $ColumnX4 - $ColumnX3;
my $ColumnX4Width = 27;



my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";




print_doc_header();

#warn "-------";

my $page_number = 1;
my $output_file = "/tmp/REPORT$$";
print_attendance();

$need_to_query = "YES";
$student_counter = 1;
$i = 0;
#$page_number = 2;
prPage();
#print_attendance();


print_doc_footer();
$db->finish(); #03-11-2005 WPL Added DB Finish

my @StudentNames;
#my @StudentSSN;

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

	    if ($student_counter > $RecordsPerPage)
	    {
		  print_page_footer();
          $PriorPageEntriesCount += $RecordsPerPage;
		  PDF_DRAW::new_page();
		  $page_number++;
		  print_attendance_header();
		  $student_counter = 1;
		  $session_count_page_start = 1; #2013-07-26
	    }
	    
	    print_student_entry(@studentinfo);    
	    $student_counter++;
	    
	  }

	  #Fill the rest of the form with blank lines
	  while ($student_counter <= $RecordsPerPage) #46 #tgs
	  {
	    print_student_entry("", "", "", "");
	    $student_counter++;
	  }
    }
    else
    {
	#If the class is empty, just create a blank form
	
	  my $i;
	  for ($i = 0; $i <= $RecordsPerPage; $i++)
	  {
	    print_student_entry("","","","");
	    $student_counter++;
	  }

    }

    print_page_footer();
    

}



sub print_doc_header
{
    print "Content-type: application/pdf\n\n";
    prFile();
    prMbox(0, 0, 1029, 836);
    PDF_DRAW::set_font(PDF_DRAW::get_default_font());
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

sub print_doc_footer
{
    prEnd();
}

sub print_attendance_header
{
    my $course_number = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 1);
    my $primary_instructor = $ScheduleInfo->{InstructorName};
    my $location = $ScheduleInfo->{LocationName};
    my $StartDate = $ScheduleInfo->{StartDate}; #tgs 20050909 chaged StartDate to End Date
    my $EndDate = $ScheduleInfo->{EndDate}; #tgs 20050909 chaged StartDate to End Date
    my $exam_date = "";#TODO:  What's the written exam date?
    my $pagenum = get_page_num();
    my $i;
    my $currX;
    my $currY;

    my $InstructorData;
    my $InstructorUID = "";

    if ($ScheduleInfo->{InstructorID} > 0)
    {
      $InstructorData = MFRI_UTIL::GetStaff($ScheduleInfo->{InstructorID}, "", 0);

	  if ( defined $InstructorData)
	  {
 	    $InstructorUID = $InstructorData->{UniversityIDNumber};
	  }
    }

    if (($primary_instructor eq "MFRI Instructor") || ($primary_instructor eq "MFRI Staff"))
    {
      $primary_instructor = "";
      $InstructorUID = "";
    }

    if ($location eq "TBD - To be determined")
    {
	  $location = "";
	}
	 
    $StartDate =~ /(\d+)-(\d+)-(\d+)/;
    $StartDate = "$2-$3-$1" if ($StartDate ne "");

    $EndDate =~ /(\d+)-(\d+)-(\d+)/;
    $EndDate = "$2-$3-$1" if ($EndDate ne "");
	
	
    $exam_date =~ /(\d+)-(\d+)-(\d+)/;
    $exam_date = "$2-$3-$1" if ($exam_date ne "");
    
    
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 8);
    PDF_DRAW::text(11, 792, "Attendance Record");
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 2);

    if (length($primary_instructor) > 0)
    {
	  PDF_DRAW::text(214, 814, "Primary Instructor: $primary_instructor UID: $InstructorUID");
    }
    else
    {
      PDF_DRAW::text(214, 814, "Primary Instructor: ");
    }
    
    PDF_DRAW::text(214, 794, "Start Date: $StartDate");
    PDF_DRAW::text(214, 773, "End Date: $EndDate");
    PDF_DRAW::text(611, 814, "Course \#: $course_number");
    PDF_DRAW::text(611, 794, "Location: $location");
    PDF_DRAW::text(611, 773, "Written Exam Date: $exam_date");      
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+1);





    PDF_DRAW::center_text(($ColumnX1Width/2) + $ColumnX1, 742, "#");              #18
    PDF_DRAW::center_text(($ColumnX2Width/2) + $ColumnX2, 743, "Student");        #87
    PDF_DRAW::center_text(($ColumnX2Width/2) + $ColumnX2, 724, "Name");           #87
    PDF_DRAW::center_text(($ColumnX2Width/2) + $ColumnX2, 701, "(Last, First)");  #87
#    PDF_DRAW::center_text(313, 743, "Social"); #tgs 178
#    PDF_DRAW::center_text(313, 724, "Security"); #tgs 178
#    PDF_DRAW::center_text(313, 701, "Number"); #tgs 178
    PDF_DRAW::center_text(($ColumnX3Width/2) + $ColumnX3, 748, "Date"); #tgs 238 #373
    PDF_DRAW::center_text(($ColumnX3Width/2) + $ColumnX3, 724, "Note:");#tgs 238 #373
    PDF_DRAW::center_text(($ColumnX3Width/2) + $ColumnX3, 700, "Sess:");#tgs 238 #373

    	

#    if ($pagenum == 1)
#    {
	
#    }
    
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}
   

sub print_student_entry
{
    my ($last_name, $suffix, $first_name, $middle_name) = @_;
    my $pagenum = get_page_num();
 
    my $currY = 679 - (($student_counter-1) * (PDF_DRAW::get_default_font_size() + 7)); #was 4 before that #5 #tgs
 
   #20190418+
   my $maxNameLength = 26; #max length for student name  
   my $StudentName = MFRI_STRINGS::Build_Name($first_name, $middle_name, $last_name, $suffix, 1, ($maxNameLength > 0), $maxNameLength, 1); 
   #20190418-
   
   # if (!$soc_sec) { $soc_sec = " ";}

#    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() - 2); #tgs
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
    PDF_DRAW::text(($ColumnX1Width/2) + $ColumnX1 - 4, $currY, $student_counter + $PriorPageEntriesCount);
    
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
    #20190418#$nameString .= " $first_name $middle_name";
	#20190418$nameString .= " $first_name";
	#20190418$nameString .= " $middle_name";
	#20190418
	#20190418if (($last_name eq "") && ($first_name eq ""))
	#20190418{ 
    #20190418  $nameString = "";   	
	#20190418}
	
	@StudentNames[$student_counter] = $StudentName; #20190418 $nameString;
#	@StudentSSN[$student_counter] =  $soc_sec;
	
    PDF_DRAW::text($ColumnX2 + 5, $currY, $StudentName); #20190418 $nameString);
#    PDF_DRAW::center_text(312, $currY, $soc_sec); #tgs 177
    PDF_DRAW::center_text(($ColumnX3Width/2) + $ColumnX3, $currY, $student_counter); #tgs 235 #370
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

sub Print_Page_2
{
    my $page_number = shift;

  PDF_DRAW::new_page();

  print_attendance_header();

  if (length($page_number) == 0)
  {
      $page_number = 0;
  }

  $session_count_page_start = ($SessionsPerPage * $page_number) + 1; #2013-07-26 declare globally so print_page_footer can use it for determining whether to print continued or grade heading.
  my $session_count_page_end = $SessionsPerPage + ($SessionsPerPage * $page_number);
  
  my $RecordCounter = 1;
  
  my $StudentRecordCount = scalar(@StudentNames);
  
  my $currY = 679 - (($RecordCounter-1) * (PDF_DRAW::get_default_font_size() + 7)); #was 4 before that #5 #tgs

  
  for ($RecordCounter = 1; $RecordCounter <= $RecordsPerPage; $RecordCounter++)  
  {
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
    PDF_DRAW::text(($ColumnX1Width/2) + $ColumnX1 - 4, $currY, $RecordCounter  + $PriorPageEntriesCount);
	
	if ($RecordCounter < $StudentRecordCount)
	{
	  PDF_DRAW::text($ColumnX2 + 5, $currY, $StudentNames[$RecordCounter]);
#      PDF_DRAW::center_text(312, $currY, $StudentSSN[$RecordCounter]); #tgs 177
	}
	
    PDF_DRAW::center_text(($ColumnX3Width/2) + $ColumnX3, $currY, $RecordCounter); #tgs 235
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());

    $currY -= (PDF_DRAW::get_default_font_size() + 7); #was 4 before that #5 #tgs

  }

  my $currX = $ColumnX4;#407;#272; #tgs
  
	  for ($i = $session_count_page_start; $i <= $session_count_page_end; $i++)
	  {
	    PDF_DRAW::center_text($currX + ($ColumnX4Width / 2), 748, "/");
	    PDF_DRAW::center_text($currX + ($ColumnX4Width / 2), 700, "$i");
	    $currX += $ColumnX4Width;
	  }

	PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()-2);
#	$currY = 752;
#	PDF_DRAW::center_text(940, $currY, "I");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);
#	PDF_DRAW::center_text(940, $currY, "n");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);
#	PDF_DRAW::center_text(940, $currY, "t");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);
#	PDF_DRAW::center_text(940, $currY, "e");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);
#	PDF_DRAW::center_text(940, $currY, "r");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);
#	PDF_DRAW::center_text(940, $currY, "n");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);

#	$currY = 752;
#	PDF_DRAW::center_text(953, $currY, "I");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);
#	PDF_DRAW::center_text(953, $currY, "s");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);
#	PDF_DRAW::center_text(953, $currY, "E");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);

#	$currY = 752;
#	PDF_DRAW::center_text(973, $currY, "Stud");
#	$currY -= (PDF_DRAW::get_default_font_size() + 1);
#	PDF_DRAW::center_text(973, $currY, "Verif");

	$currY = 752;

	$currY -= (PDF_DRAW::get_default_font_size() + 1);


    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+2);

    #my $temp = $MaxSessions - $session_count_page_start;
    #warn "Print_Page_2 MaxSessions $MaxSessions - session_count_page_start $session_count_page_start = $temp > SessionsPerPage $SessionsPerPage";
    if (($MaxSessions - $session_count_page_start) > $SessionsPerPage)
    {
     #warn "printing: Continued";
	  PDF_DRAW::text(950, 724, "Continued"); #1005
    }
    else
    {
     #warn "printing: Grade";
  	  PDF_DRAW::text(950, 724, "Grade"); #1005
    }
    
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());

#	PDF_DRAW::text($currX + 5, $currY, "Grade"); #1005


#    PDF_DRAW::draw_line($currX, $topY, $currX, $bottomY); #947
#	PDF_DRAW::draw_line(958, $topY, 958, $bottomY);
#	PDF_DRAW::draw_line(990, $topY, 990, $bottomY);
	
	Print_Page_Lines();
	
#  for ($RecordCounter = 0; $RecordCounter < $StudentRecordCount; $RecordCounter++)  
#  {
#	@StudentNames[$RecordCounter] = "";
#  } 
  
}

sub get_page_num
{
    return $page_number;
}

sub Print_Page_Lines
{
    PDF_DRAW::draw_line($ColumnX1, $topY, $ColumnX1, $bottomY); #Left Line
    PDF_DRAW::draw_line($ColumnX2, $topY, $ColumnX2, $bottomY);         #Name Line
#    PDF_DRAW::draw_line(278, $topY, 278, $bottomY);       #Soc Line #tgs 143
    PDF_DRAW::draw_line($ColumnX3, $topY, $ColumnX3, $bottomY);       #Date Line #tgs 213 #348

    my $i;
    my $currX;
    for ($i = 0; $i <= $SessionsPerPage; $i++) #26 #tgs
    {
	  $currX = $ColumnX4 + ($i * $ColumnX4Width); #260 #tgs
	  PDF_DRAW::draw_line($currX, $topY, $currX, $bottomY);
    }

    PDF_DRAW::draw_line($rightX, $topY, $rightX, $bottomY); #Last Line
	
    PDF_DRAW::draw_line($leftX, $topY, $rightX, $topY);
	
	
    my $currY;
    for ($i = 0; $i < ($RecordsPerPage + 1); $i++)
    {
	  $currY = $cellTopY - $cellHeight * $i;
	  PDF_DRAW::draw_line($leftX, $currY, $rightX, $currY);
    }

}

sub print_page_footer
{
    #Draw lines
    
    my $currX = $ColumnX4;#407;#272; #tgs

	  for ($i = 1; $i <= $SessionsPerPage; $i++) #25 #tgs
	  {
	    PDF_DRAW::center_text($currX + ($ColumnX4Width / 2), 748, "/");
	    PDF_DRAW::center_text($currX+($ColumnX4Width/2), 700, "$i");
	    $currX += $ColumnX4Width;
	  }

	PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+2);

    #my $temp = $MaxSessions - $session_count_page_start;
    #warn "print_page_footer MaxSessions $MaxSessions - session_count_page_start $session_count_page_start = $temp > SessionsPerPage $SessionsPerPage";

    if (($MaxSessions - $session_count_page_start) > $SessionsPerPage)#2013-07-26
    {
    #warn "printing: Continued";        
	  PDF_DRAW::text(950, 724, "Continued"); #1005
    }
    else
    {
     #warn "printing: Grade";        
  	  PDF_DRAW::text(950, 724, "Grade"); #1005
    }

#    PDF_DRAW::text(950, 724, "Continued");

   	PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());

	Print_Page_Lines();
	
	my $FooterY = $cellTopY - ($cellHeight * ($RecordsPerPage + 1));

	PDF_DRAW::text($leftX, $FooterY, $ReportDate);  
	

	if ($MaxSessions > 20)
	{
#
	  Print_Page_2(1);

	  PDF_DRAW::text($leftX, $FooterY, $ReportDate);  
    }
    
	if ($MaxSessions > 40)
	{
 
	    Print_Page_2(2);

	    PDF_DRAW::text($leftX, $FooterY, $ReportDate);  
    }
    
    my $RecordCounter = 0;
   for ($RecordCounter = 0; $RecordCounter < scalar(@StudentNames); $RecordCounter++)  
   {
     @StudentNames[$RecordCounter] = "";
   } 
	
	
}




