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
use MFRI_STRINGS; #20190418

use DBK;

use APPDEBUG;

my $ScheduledCourseID = CGI::param( 'SCID' );
$ScheduledCourseID = 0 if (not defined $ScheduledCourseID);


if(!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}


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
AES_DECRYPT(ST.IDNumber, "} . DBK::Encrypt_Key() . qq{") AS IDNumber 
FROM StudentRecords AS ST,
StudentRegistration AS SR,
Affiliations AS A
WHERE (SR.StudentID = ST.ID) AND
(SR.AffiliationID = A.ID) AND
(SR.SchedCourseID = $ScheduledCourseID) AND
(SR.StatusID != 4) AND (SR.StatusID != 22) 
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, SR.Created    
};
# AND (SR.StatusID != 7)
my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($ScheduledCourseID);


my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";

my $i = 0;
my $student_counter = 1;
my $maxEntries = 25;
my $currEntries = 0;

my $cellHeight = 25;
my $topY = 745; #745
my $cellTopY = 703;
my $bottomY = $cellTopY - $cellHeight * ($maxEntries + 1);
my $leftX = 1;# 7
my $rightX = 1028; #1020

my $Column1 = $leftX; 
my $Column2 = $leftX + 25;   

#my $Column3 = $leftX +  368; #169
#my $Column4 = $leftX +  412; #269 #274 #286
#my $Column5 = $leftX +  455; #316 #320 #328
#my $Column6 = $leftX +  530; #369
#my $Column7 = $leftX +  605; #422
#my $Column8 = $leftX +  643; # 475
#my $Column9 = $leftX +  682; # 533 
#my $Column10 = $leftX + 720; #591
#my $Column11 = $leftX + 760;  #649
#my $Column12 = $leftX + 798; #707
#my $Column13 = $leftX + 834; #767
#my $Column14 = $leftX + 863; #821
#my $Column15 = $leftX + 892; 
#my $Column16 = $rightX; 


my $Column3 = $leftX +  284; #284;#169
my $Column4 = $leftX +  328; #368;#269 #274 #286
my $Column5 = $leftX +  371; #412;#316 #320 #328
my $Column6 = $leftX +  446; #455;#369
my $Column7 = $leftX +  521; #530;#422
my $Column8 = $leftX +  559; #605;# 475
my $Column9 = $leftX +  598; #643;# 533 
my $Column10 = $leftX + 636; #682;#591
my $Column11 = $leftX + 676; #720; #649
my $Column12 = $leftX + 714; #760;#707
my $Column13 = $leftX + 750; #798;#767
my $Column14 = $leftX + 779; #834;#821
my $Column15 = $leftX + $rightX; #863; #863;
my $Column16 = $rightX; 

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

    $page_count = POSIX::ceil($db->num_rows() / $maxEntries);
    $page_count = 1 if ($page_count == 0);
    
    
    print_report_header();
    my $tmp = $db->num_rows();
#    warn "numrows: $tmp";

    if ($db->num_rows() > 0)
    {
	my @studentinfo;
	
	while (@studentinfo = $db->get_row())
	{
	    if ($currEntries >= $maxEntries)
	    {
		print_report_footer();
		PDF_DRAW::new_page();
		$page_number++;
		print_report_header();
		$currEntries = 0;
	    }

	    #warn "printing entry for @studentinfo";
	    print_student_entry(@studentinfo);  
	    $student_counter++; 
	    $currEntries++;
	    
	}
    }

    #die "doing filler";
    while (($currEntries > 0) && ($currEntries < $maxEntries))
    {
	  print_student_entry();
	  $student_counter++;
	  $currEntries++;
    }
    
    print_report_footer();

}

sub print_doc_header
{
    PDF_DRAW::doc_header(1029, 836);
    PDF_DRAW::set_font(PDF_DRAW::get_default_font());
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

sub print_doc_footer
{
    PDF_DRAW::doc_footer();
}

sub print_report_header
{
    my $MFRILogNumber = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 1);
    my $course_code = STUREG_MAINT::get_miemss_log_number_by_id($ScheduledCourseID);
	
    my $location = $ScheduleInfo->{LocationName};
    my $instructor_name = $ScheduleInfo->{InstructorName};
    my $written_exam_date = ""; #TODO:  fill this info out
    my $practical_date = ""; #TODO: fill this info out
    my $retest = ""; #TODO:  fill this info out
    my $page_num = get_page_num();
    my $i;
    my $currX;
    my $currY;

	my $HeaderTop = 810; #814
	my $HeaderLeft = 380; #520 #611
	
	if (($instructor_name eq "MFRI Instructor") || ($instructor_name eq "MFRI Staff"))
	{
      $instructor_name = "";
    }
	
	$location = "" if ($location eq "TBD - To be determined");
    #TODO:  Insert date-prettifying code here when we know what exactly will be dates

    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 10);
    my $MFRILogNumberYOffset = PDF_DRAW::text(11, 792, "Examination Sheet");
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 4);
	
	PDF_DRAW::text(11, $MFRILogNumberYOffset, "MFRI Log Number: " . $MFRILogNumber);
	

    PDF_DRAW::text($HeaderLeft, $HeaderTop, "Course \#: $course_code"); #611 #814
    PDF_DRAW::text($HeaderLeft + 230, $HeaderTop, "Location: $location"); #780 #814
    PDF_DRAW::text($HeaderLeft, $HeaderTop - 20, "Primary Instructor: $instructor_name"); #611 #794
    PDF_DRAW::text($HeaderLeft, $HeaderTop - 40, "Written Exam Date: $written_exam_date"); #611 #774
    PDF_DRAW::text($HeaderLeft, $HeaderTop - 60, "Practical Date: $practical_date"); #611 #754
    PDF_DRAW::text($HeaderLeft + 200, $HeaderTop - 60, "Retest: $retest"); #780 #754
    
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+4); #+1
    PDF_DRAW::center_text($Column1 + 12, 727, "#"); #20  # 13
    PDF_DRAW::center_text($Column2 + 70, 727, "Student Name");  # 105
#    PDF_DRAW::center_text($Column3 + 42, 727, "SSN"); # 227 #52
    PDF_DRAW::center_text($Column3 + 22, 727, "W."); # 300  #28
    PDF_DRAW::center_text($Column3 + 22, 712, "Score"); # 300 #28
    PDF_DRAW::center_text($Column4 + 20, 727, "Written"); # 350  # 34
    PDF_DRAW::center_text($Column4 + 20, 712, "Exam"); # 350 
    PDF_DRAW::center_text($Column5 + 74, 727, "Written Exam"); # 430  #61
    PDF_DRAW::center_text($Column5 + 74, 712, "Retest"); # 430
    PDF_DRAW::center_text($Column7 + 38, 727, "Medical"); # 541
    PDF_DRAW::center_text($Column9 + 38, 727, "Trauma"); # 657 #  63
    PDF_DRAW::center_text($Column11 + 20, 727, "Intern."); # 745 #33
    PDF_DRAW::center_text($Column12 + 18, 727, "Affil."); # 802
    PDF_DRAW::center_text($Column13 + 14, 727, "Pass"); # 850 #24
    PDF_DRAW::center_text($Column14 + 80, 727, "Remarks"); # 946

    PDF_DRAW::center_text($Column5 + 30, 687, "#1"); # 402
    PDF_DRAW::center_text($Column6 + 30, 687, "#2"); # 455
    PDF_DRAW::center_text($Column7 + 20, 687, "#1"); # 508
    PDF_DRAW::center_text($Column8 + 20, 687, "#2"); # 566
    PDF_DRAW::center_text($Column9 + 20, 687, "#1"); # 624 # 30
    PDF_DRAW::center_text($Column10 + 20, 687, "#2"); # 682 # 30
    PDF_DRAW::center_text($Column11 + 18, 687, "Y"); # 745 # 32
    PDF_DRAW::center_text($Column12 + 18, 687, "Y"); # 802

    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() - 1);
    PDF_DRAW::text(975, 820, "Page $page_number of $page_count");

    
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

   

sub print_report_footer
{
    #Draw lines
    
    PDF_DRAW::draw_line($Column1, $topY, $Column1, $bottomY);    #Left Line
    PDF_DRAW::draw_line($Column2, $topY, $Column2, $bottomY);            ## Line #33
#    PDF_DRAW::draw_line($Column3, $topY, $Column3, $bottomY);          #Name Line # 177
    PDF_DRAW::draw_line($Column3, $topY, $Column3, $bottomY);          #SSN Line # 277
    PDF_DRAW::draw_line($Column4, $topY, $Column4, $bottomY);          #W. Score Line # 323
    PDF_DRAW::draw_line($Column5, $topY, $Column5, $bottomY);          #Written Exam Line # 377
    PDF_DRAW::draw_line($Column6, 703, $Column6, $bottomY);             # 430
    PDF_DRAW::draw_line($Column7, $topY, $Column7, $bottomY);          #Written Exam Retest Line  # 483
    PDF_DRAW::draw_line($Column8, 703, $Column8, $bottomY);             # 541
    PDF_DRAW::draw_line($Column9, $topY, $Column9, $bottomY);          #Medical Line  # 599
    PDF_DRAW::draw_line($Column10, 703, $Column10, $bottomY);            #   657
    PDF_DRAW::draw_line($Column11, $topY, $Column11, $bottomY);          #Trauma Line # 715
    PDF_DRAW::draw_line($Column12, $topY, $Column12, $bottomY);          #Internship Line # 775
    PDF_DRAW::draw_line($Column13, $topY, $Column13, $bottomY);          #Affiliation Line # 829
    PDF_DRAW::draw_line($Column14, $topY, $Column14, $bottomY);          #Pass Line # 871
    PDF_DRAW::draw_line($Column15, $topY, $Column15, $bottomY);  #Right Line # 

    #Horizontal lines
    PDF_DRAW::draw_line($leftX, $topY, $rightX, $topY);

    my $currY;
    my $midY;
    for ($i = 0; $i < $maxEntries+2; $i++)
    {
	$currY = $cellTopY - $cellHeight * $i;
	$midY = $currY - $cellHeight / 2;
	PDF_DRAW::draw_line($leftX, $currY, $rightX, $currY);	

    }
    
}

sub print_student_entry
{
    #warn "printing entry";
    my ($last_name, $suffix, $first_name, $middle_name, $SSN) = @_;
    my $student_name;
    my $written_score = "";
    my $pagenum = &get_page_num;
 
    $SSN = STUREG_MAINT::HyphenateSSN($SSN);
	       
    my $currY = 660 - (($currEntries) * (PDF_DRAW::get_default_font_size() + 14));
  
    #tgs 20050909 $student_name = $last_name;
    #tgs 20050909 $student_name .= ", $first_name" if ($first_name ne "");

    #20190418+
    my $MaxNameLength = 25;
    my $nameString = MFRI_STRINGS::Build_Name($first_name, $middle_name, $last_name, $suffix, 1, ($MaxNameLength > 0), $MaxNameLength, 1); 
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

	#20190418my $MaxNameLength = 25;
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
	#20190418  if ((length($first_name) > 0) || (length($middle_name) > 0))
	#20190418  {
    #20190418    $nameString .= " $first_name $middle_name";
	#20190418  }
	#20190418  else
	#20190418  {
    #20190418    $nameString = "";
	#20190418  }	
	#20190418}
	
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 4); #tgs 20051014 - 1
    PDF_DRAW::center_text($Column1 + 12, $currY, $student_counter); #20 # 13 #12
	PDF_DRAW::text($Column2 + 4, $currY, $nameString); # 37
    #tgs 20050909 PDF_DRAW::text(37, $currY, $student_name);
#    PDF_DRAW::center_text($Column3 + 40, $currY, $SSN); # 227 #50
    make_pass_fail_box($Column4 + 20, $currY); #written exam # 350
    make_pass_fail_box($Column5 + 20, $currY); #written exam retest 1 #405 # 395
    make_pass_fail_box($Column6 + 20, $currY); #written exam retest 2 #458 # 448
    make_pass_fail_box($Column7 + 20, $currY); #medical 1 # 511
    make_pass_fail_box($Column8 + 20, $currY); #medical 2 # 569
    make_pass_fail_box($Column9 + 20, $currY); #trauma 1 # 627 # 30
    make_pass_fail_box($Column10 + 20, $currY); #trauma 2 # 685 # 30
    make_letter_box($Column11 + 18, $currY, "Y"); # 745 #internship
    make_letter_box($Column12 + 18, $currY, "Y"); # 802 #affiliation # 18
    make_letter_box($Column13 + 16, $currY, "P"); # 850 #22

    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
    #warn "done.";
    #die;
    
}


sub make_pass_fail_box
{
    my $x = shift;
    my $y = shift;
    
    make_letter_box($x-7, $y, "P");
    make_letter_box($x+7, $y, "F");
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
    

sub get_page_num
{
    return $page_number;
}


