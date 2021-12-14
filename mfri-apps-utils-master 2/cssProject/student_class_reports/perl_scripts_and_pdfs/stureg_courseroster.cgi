#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use SEMINAR_MAINT;
use Database;
use CGI;  
#use CGI qw(:standard); #added by wlowe, removed by tgs, not necessary

my $ScheduledCourseID = CGI::param( 'SCID' );

$ScheduledCourseID = 0 if (not defined $ScheduledCourseID);

if ($ScheduledCourseID <= 0)
{
  MFRI::set_cookie( "error", "Error 1 Invalid Course ID." );
  MFRI::redirect( "error.cgi" );
  exit;
}

my $Student_Query_String = qq
{
SELECT
ST.LastName,
ST.FirstName,
ST.MiddleName,
DATE_FORMAT(ST.BirthDate, \"%m-%d-%Y\"),
ST.IDNumber,
ST.Address1,
ST.Address2,
ST.City,
ST.State,
ST.PostCode,
ST.AffiliatedCompanyNumber
FROM StudentRecords AS ST,
StudentRegistration AS SR,
Affiliations AS A
WHERE (SR.StudentID = ST.ID) AND
(SR.AffiliationID = A.ID) AND
(SR.SchedCourseID = $ScheduledCourseID) AND
(SR.StatusID != 4) AND (SR.StatusID != 7)
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, SR.Created    
};

if( MFRI::is_authenticated() )
{

  print_doc_header();

  print_roster();

  print_doc_footer();
}
else
{
	MFRI::set_cookie( "error", "you must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
}





sub print_roster
{
  my $student_counter = 0;

  my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );

  print_roster_header();
    
  $db->query($Student_Query_String);
  if ($db->num_rows() < 1) 
  {  
    print_roster_footer();
	print "no students enrolled in class"; 
	$db->finish();
	return; 
  }
    
  my @studentinfo;

    while (@studentinfo = $db->get_row())
    {
	  print_student_entry(@studentinfo);  
	  $student_counter++; 
	  
	  if ($student_counter >= 25) 
	  {
	    print_roster_footer();
	    	    
	    if ($student_counter < $db->num_rows())
	    {
		  #&print_roster;
		  print_roster_header();
		  $student_counter = 0;
	    }
	    #else
	    #{
		#  print_roster_footer();
		#  $db->finish();
		#  return;
	    #}
	    
	  }#if ($student_counter == 25) 
    }#while (@studentinfo = $db->get_row())
	 
    print_roster_footer();
    $db->finish();

}


sub print_doc_header
{
    my $Document_Header = qq
    {
	
	
	<html>
	    <head>
	    <style type='text/CSS'>
	    
	    table.outline { background: black; border: solid black 1px; }
	table.outline tr td { border: solid black 1px; background: white;}
	tr.entry td {font-size: 10px; font-family: 'Verdana, sans-serif'; height: 25;}
	div.page {page-break-after: always; page-break-before:never; }
	</style>
	    <body>
	};
    
	print "Content-type: text/html\n\n"; #02-21-2005 tgs added for browser compatability

    #print header; #removed by TGS added by wlowe, not necessary
    print $Document_Header;
}

sub print_doc_footer
{
    print "</body></html>";
}

sub print_roster_header
{

  my $Course_Query_String = qq
  {
  SELECT
  SC.LogNumber,
  SC.InstructorID,
  C.LastName,
  C.FirstName,
  SC.LocationID,
  L.Name,
  CD.CourseCode
  FROM ScheduledCourses AS SC,
  Locations AS L,
  Users AS U,
  Contacts AS C,
  CourseDescriptions AS CD
  WHERE (SC.ID = $ScheduledCourseID) AND (SC.CourseID = CD.Id) AND (SC.LocationID = L.ID) AND (SC.InstructorID = U.ID) AND (U.ContactID = C.ID)
  };

	my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
	
    $db->query($Course_Query_String);
  
    if ($db->num_rows() < 1) 
	{ 
	  $db->finish();
	  return "no course ID defined";  
    }
	
  my ($course_number, $primary_instructorID, $Primary_InstructorLName, $Primary_InstructorFName, $locationID, $location, $CourseCode) = $db->get_row();

  $db->finish();
    
  if ((3 == $primary_instructorID) || (4 == $primary_instructorID))
  {
    $Primary_InstructorFName = "TBA";
	$Primary_InstructorLName = "";	
  }
  	
  my $Roster_Header = qq
{
<div class='page'>
<table width=1000>
<tr>
<td width=500 align=center><h1>Course Roster</h1></td>
<td>
<b>Course #:</b> $CourseCode-$course_number
<Br>
<b>Primary Instructor:</b> $Primary_InstructorFName $Primary_InstructorLName
<br>
<b>Location:</b> $location
</td>
</tr></table>

<table width=1000 cellspacing=0 class='outline'>
<tr>
<td rowspan=2 width=10>in<br>it</td>
<td colspan=3 align=center width=150><b>Student Name</b></td>
<td align=center width=85><b>Soc.Sec #</b></td>
<td align=center width=50><b>ID #</b></td>
<td align=center width=75><b>DOB</b></td>
<td colspan=5 align=center width=250><b>Address</b></td>
<td align=center width=100><b>Company</b></td>
</tr>
<tr>
<td width=70 align=center>last</td>
<td width=70 align=center>First</td>
<td width=10 align=center>MI</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align=center width=125>STREET</td>
<td align=center width=25>APT</td>
<td align=center width=75>CITY</td>
<td align=center width=25>ST.</td>
<td align=center width=50>ZIP</td>
<td>&nbsp;</td>
</tr>
};

    print $Roster_Header;
}
   
   sub print_roster_footer
{
    print "</table></div>";
}

sub print_student_entry
{
    my $student_entry = &make_student_entry(@_);
 
    print $student_entry;    
}



    
sub make_roster_header
{
}

sub make_student_entry
{
#warn "make_student_entry\n";

    my ($last_name, $first_name, $middle_init, $DOB, 
	$soc_sec, $street, $apt, $city, $state, $zip, $company) = @_;
	
#warn "last_name $last_name\n";
#warn "first_name $first_name\n";
#warn "middle_init $middle_init\n";
#warn "DOB $DOB\n";
#warn "street $street\n";
#warn "apt $apt\n";
#warn "city $city\n";
#warn "state $state\n";
#warn "zip $zip\n";
#warn "company $company\n";
   
    $middle_init = substr($middle_init, 1, 1);
	
    if (!$middle_init) { $middle_init = "&nbsp;"; }
    if (!$soc_sec) { $soc_sec = "&nbsp;"; }
    if (!$ID_num) { $ID_num =  "&nbsp;"; }
    if (!$DOB) { $DOB = "&nbsp;"; }
    if (!$street) { $street = "&nbsp;"; }
    if (!$apt ) { $apt = "&nbsp;" }
    if (!$city ) { $city = "&nbsp;"; }
    if (!state ) {$state = "&nbsp;"; }
    if (!$zip ) {$zip = "$nbsp;"; }
    if (!$company) { $company = "&nbsp;"; }
    
#if ($middle_init) { $middle_init = &substr($middle_init, 0, 1); }
    
    my $student_entry = qq
    {
	<tr class='entry'>
	    <td>&nbsp;</td>
	    <td>$last_name</td>
	    <td>$first_name</td>
	    <td>$middle_init</td>
	    <td>$soc_sec</td>
	    <td>$ID_num</td>
	    <td>$DOB</td>
	    <td>$street</td>
	    <td>$apt</td>
	    <td>$city</td>
	    <td>$state</td>
	    <td>$zip</td>
	    <td>$company</td>
	</tr>
    };
    
    return $student_entry;
}


