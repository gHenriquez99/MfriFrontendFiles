#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use SEMINAR_MAINT;
use Database;
#use CGI;
use CGI qw(:standard);

my $ScheduledCourseID = CGI::param( 'SCID' );


my $Course_Query_String = qq
{
SELECT
SC.LogNumber,
SC.InstructorID,
SC.LocationID,
SC.StartDate,
SC.EndDate,
CD.CourseCode
FROM ScheduledCourses AS  SC,
CourseDescriptions AS CD
WHERE (SC.ID = $ScheduledCourseID) AND (SC.CourseID = CD.Id)   
};

my $Student_Query_String = qq
{
SELECT
ST.LastName,
ST.FirstName,
ST.IDNumber
FROM StudentRecords AS ST,
StudentRegistration AS SR,
Affiliations AS A
WHERE (SR.StudentID = ST.ID) AND
(SR.AffiliationID = A.ID) AND
(SR.SchedCourseID = $ScheduledCourseID) AND
(SR.StatusID != 4) AND (SR.StatusID != 7)
ORDER BY ST.LastName, ST.FirstName, SR.Created    
};







my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";


my $i = 0;
my $student_counter = 1;


&print_doc_header;


my $page_number = 1;
&print_attendance;

$need_to_query = "YES";
$student_counter = 1;
$i = 0;
$page_number = 2;
&print_attendance;


&print_doc_footer;
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
    my @courseinfo;
    if ($need_to_query eq "YES") 
    { 
	$db->query($Course_Query_String); 
	if ($db->num_rows() < 1) { print "no course ID defined"; return; }
	@courseinfo = $db->get_row();
    }
    
    &print_attendance_header(@courseinfo);
    
    if ($need_to_query eq "YES") 
    {
	$db->query( $Student_Query_String );
	if ($db->num_rows() < 1) { &print_attendance_footer;  print "no students enrolled in class"; return; }
	$need_to_query = "NO";
    }
    
    my @studentinfo;

    while (@studentinfo = $db->get_row())
    {
	
	&print_student_entry(@studentinfo);    
	$student_counter++;
	
    }
    
    &print_attendance_footer;

}










sub print_doc_header
{
    my $Document_Header = qq
    {
	<html>
	    <head>
	    <style type='text/CSS'>
	    
	    table.outline { border: 1px solid black; background-color: "#000"; }
	table.outline tr td { background-color: "#fff"; border: 1px black solid; }
	tr.entry td {font-size: 10px; font-family: 'Verdana, sans-serif'; }
	div.page {page-break-after: always; page-break-before:never; }
	</style>
	    <body>
	};
    print header;
    print $Document_Header;
}

sub print_doc_footer
{
    print "</body></html>";
}








sub print_attendance_header
{
    my $attendance_header = make_attendance_header(@_);
    
    print $attendance_header;
}
   
   sub print_attendance_footer
{
    print "</table></div>";
}


sub print_student_entry
{
    my $student_entry = &make_student_entry(@_);
    
    print $student_entry;    
}


sub make_attendance_header
{
   my ($course_number, $primary_instructor, $location, $date, $exam_date, $CourseCode) = @_;
   my $pagenum = &get_page_num;
   my $Attendance_Header = qq
{
<div class='page'>
<table width=1000>
<tr>
<td width=200><h2>Attendance Record</h2></td>
<td width=400><b>Primary Instructor:</b> $primary_instructor<br>
<b>Date:</b>
</td>
<td width=400><b>Course #:</b> $CourseCode-$course_number<br>
<b>Location:</b> $location<br>
<b>Written Exam Date:</b>
</td>
</tr>
</table>

<table class='outline' width=1000 cellspacing=0 >
<tr>
<td rowspan=3 width=25>#</td>
<td rowspan=3 width=200 align=center><b>Student<br>Name<br>(last, First)</b></td>
<td rowspan=3 width=100 align=center><b>Social<br>Security<br>Number</b></td>
<td width=35>Date</td>
};

    $Attendance_Header .= "<td width=35 align=center>/</td>\n" x 25;
    if ($pagenum == 1) 
    {
           $Attendance_Header .= "<td width=100 rowspan=3>Continued</td></tr>";
    }
    if ($pagenum == 2)
    {
        $Attendance_Header .=    "<td rowspan=3 width=25>I<br>n<br>t<br>e<br>r<br>n</td>
<td rowspan=3 width=25>I<Br>s<br>E</td>
<td rowspan=3 width=25>Stud<br>Verif</td>
<td rowspan=3 width=100>Notes</td>
</tr>";
    } 
    $Attendance_Header .= "<tr>
<td>Note:</td>" . ("<td>&nbsp;</td>" x 25) . "</tr><tr>
<td>Sess:</td>";
if ($pagenum==1)
{
for ($a=1; $a<26; $a++)
{
$Attendance_Header .="<td align=center>$a</td>";
}
}
if ($pagenum==2)
{
for ($a=26; $a<51; $a++)
{
$Attendance_Header .= "<td align=center>$a</td>";
}
}
$Attendance_Header .= "</tr>";

    return $Attendance_Header;
}


sub make_student_entry
{
    my ($last_name, $first_name, $soc_sec) = @_;
    my $pagenum = &get_page_num;
    
    if (!$soc_sec) { $soc_sec = "&nbsp;"; }
    my $student_entry =
"<tr class='entry'><td>$student_counter</td><td>$last_name, $first_name</td><td>$soc_sec</td><td align=center>$student_counter</td>" . 
("<td>&nbsp;</td>" x 25);

        if ($pagenum==1)
        {
                $student_entry = $student_entry . "<td>&nbsp;</td>";
        }
        else
        {
                $student_entry .= "<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>";
        }
$student_entry .= "</tr>";
    return $student_entry;
}

sub get_page_num
{
    return $page_number;
}






