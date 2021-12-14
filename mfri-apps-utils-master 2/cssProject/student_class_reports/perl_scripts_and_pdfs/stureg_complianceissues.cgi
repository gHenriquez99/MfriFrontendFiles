#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use SEMINAR_MAINT;
#use CGI;
use CGI qw(:standard);
use Database;

my $ScheduledCourseID = CGI::param('SCID');



my $Course_Query_String = qq
{
select
SC.LogNumber
FROM ScheduledCourses AS  SC
WHERE (SC.ID = $ScheduledCourseID)    
};


my $Student_Query_String = qq
{
select
ST.LastName,
ST.FirstName,
ST.IDNumber,
ST.LocalProviderNumber,
ST.CountyID,
ST.AffiliatedCompanyNumber,
MH.LegalQuestion2,
MH.LegalQuestion3
FROM StudentRecords AS ST,
MESSRHold AS MH,
Affiliations AS A
WHERE (MH.StudentRegID = ST.ID) AND
(MH.CompanyNumber = A.FireMarshalNumber) AND
(MH.ScheduledCourseID = $ScheduledCourseID) AND
((MH.LegalQuestion1 = 1) OR (MH.LegalQuestion2 = 1))
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, MH.Created
};

#warn("\n*******START QUERY\n$Student_Query_String\n**********END QUERY\n");

my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";


my $student_counter = 0;

&print_doc_header;

&print_provider;

&print_doc_footer;


$db->finish(); #03-11-2005 WPL Added DB Finish
#pointless...used before as placeholders
sub get_course_info
{
    return;
}

sub get_student_info
{
    return ($db->get_row());
}





sub print_provider
{


    my @courseinfo;

    if ($need_to_query eq "YES")
    {
	$db->query($Course_Query_String);
	if ($db->num_rows() < 1) { print "no course ID defined"; return; }
	@courseinfo = $db->get_row();
    }
    
    my $numrows = $db->num_rows();    
    &print_provider_header;
    
    if ($need_to_query eq "YES")
    {
	$db->query($Student_Query_String);
	if ($db->num_rows() < 1) 
	{
	    &print_provider_footer; 
	    print "no students with compliance issues enrolled in class"; 
	    return; 
	}
	$need_to_query = "NO";
    }

    my $numrows = $db->num_rows();

    my @studentinfo;    

    while (@studentinfo = $db->get_row())
    {
	&print_student_entry(@studentinfo);  
	$student_counter++;
	if ($student_counter == 25)
	{
	    &print_provider_footer;

	    if ($student_counter < $db->num_rows())
	    {
		&print_provider;
	    }

	    else
	    {
		&print_provider_footer;
		return;
	    }


	}
    }
    
    &print_provider_footer;
}

sub print_doc_header
{
    my $Document_Header = qq
    {
	<html>
	    <head>
	    <style type='text/CSS'>
	    
	    table.outline tr td {padding: 0px; margin: 0px; border-style: solid; border-width: 1px; border-color: black;}
	tr.entry td {font-size: 10px; font-family: 'Verdana, sans-serif'; }
	div.page {page-break-after: always; page-break-before:never; }
	</style>
	    <body>
	};
    
    print header;
    print  $Document_Header;
}

sub print_doc_footer
{
    print  "</body></html>";
}

sub print_provider_header
{
    my $provider_header = &make_provider_header;
    
    print  $provider_header;
}
   
sub print_provider_footer
{
    print  "</table></div>";
}


sub print_student_entry
{
    my $student_entry = make_student_entry(@_);
    
    print  $student_entry;    
}

    
sub make_provider_header
{
    
   my $Provider_Header = qq
   {
       <div class='page'>
	   <table width=1000><tr><td><h2>New Providers With Compliance Issues</h2></td></tr></table>
	   <table width=1000 border=0>
	   <tr>
	   <td width=150><b>last Name</b></td>
	   <td width=150><b>First Name</b></td>
	   <td width=100><b>SSN</b></td>
	   <td width=150><b>Student ID</b></td>
	   <td width=100><b>County</b></td>
	   <td width=100><b>Company</b></td>
	   <td width=50><b>Leg 2</b></td>
	   <td width=50><b>Leg 3</b></td>
	   </tr>
       };
   return $Provider_Header;
}


sub make_student_entry
{
    my ($last_name, $first_name, $soc_sec, $student_id,$county, $company, $leg2, $leg3) = @_;

    if ($leg2) { $leg2 = "YES"; }
    else { $leg2 = "NO"; }
    
    if ($leg3) { $leg3 = "YES"; }
    else { $leg3 = "NO"; }

    my $student_entry = qq
    {
	<tr class='entry'>
	    <td>$last_name</td>
	    <td>$first_name</td>
	    <td>$soc_sec</td>
	    <td>$student_id</td>
	    <td>$county</td>
	    <td>$company</td>
	    <td>$leg2</td>
	    <td>$leg3</td>
	    </tr>
	};

    return $student_entry;
}



