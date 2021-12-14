#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use SEMINAR_MAINT;
#use CGI;
use CGI qw(:standard);
use Database;

use strict;
use PDF_DRAW;
#use PDF::API2;
use PDF::Reuse;

use DBK;

my $ScheduledCourseID = CGI::param('SCID');

if ($ScheduledCourseID <= 0)
{
  MFRI::set_parameter( "error", "Error 1 Invalid Course ID." );
  MFRI::redirect( "error.cgi" );
  exit;
}

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
ST.Suffix,
ST.FirstName,
left(ST.MiddleName, 1) AS MiddleName,
AES_DECRYPT(ST.IDNumber, "} . DBK::Encrypt_Key() . qq{") AS IDNumber,
AES_DECRYPT(ST.StateProviderNumber, "} . DBK::Encrypt_Key() . qq{") AS StateProviderNumber,
CONCAT(CNTY.Name, " " , CNTYT.Name),
ST.AffiliatedCompanyNumber,
MH.LegalQuestion1,
MH.LegalQuestion2,
MH.LegalQuestion3
FROM 
StudentRegistration AS SR,
StudentRecords AS ST,
MESSRHold AS MH,
Jurisdictions AS CNTY,
JurisdictionTypes AS CNTYT
WHERE 
(SR.StudentID = ST.ID) AND
(MH.StudentRegID = SR.ID) AND
(MH.ScheduledCourseID = $ScheduledCourseID) AND
(ST.CountyID = CNTY.ID) AND
(CNTY.TypeID = CNTYT.ID) AND
((MH.LegalQuestion1 = 2) OR (MH.LegalQuestion2 = 2) OR (MH.LegalQuestion3 = 2))
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, MH.Created
};

#,
#Affiliations AS A
#MH.StudentRegID = SR.ID) AND
#(MH.LegalQuestion1 = 2) OR 

if (!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}

my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";


    my $cellHeight = 19;
    my $topY = 789;
    my $cellTopY = 769;
    my $bottomY = $cellTopY - $cellHeight;
    my $leftX = 9; #24
    my $rightX = 990;
    
	my $FirstLine = 753;

	my $LastLine = $FirstLine;
	
	my $currY = $FirstLine;


my $NameX = $leftX;
my $SSNX = 350;
my $StateProviderIDX = 435;
my $CountyNameX = 515;
my $CompanyNameX = 685;
my $Legal1X = 810;
my $Legal2X = 870;
my $Legal3X = 930;

my $student_counter = 1;

my $output_file = "/tmp/REPORT$$";

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
	  
	  if ($db->num_rows() < 1) 
	  { 
	    PDF_DRAW::text(20, 755,  "No course ID defined."); 
	    return; 
	  }
	  @courseinfo = $db->get_row();
    }
    
    my $numrows = $db->num_rows();    
    print_provider_header();
    
    if ($need_to_query eq "YES")
    {
	  $db->query($Student_Query_String);
	  
	  if ($db->num_rows() < 1) 
	  {
	    print_provider_footer(); 
	    PDF_DRAW::text(20, 755, qq{None of the students enrolled in this class indicated "yes" for the Legal Questions.}); 
	    return; 
	  }
	  $need_to_query = "NO";
    }


    my @studentinfo;    

    while (@studentinfo = $db->get_row())
    {
	  print_student_entry(@studentinfo);  
	  $student_counter++;
	  if ($student_counter == 25)
	  {
	    $student_counter = 1;
#        $LastLine = $currY;
	    print_provider_footer();

	    if ($student_counter < $db->num_rows())
	    {
		  print_provider();
	    }
	    else
	    {
		  print_provider_footer();
		  return;
	    }
	  }
    }

 #   $LastLine = $currY;
    
    print_provider_footer();

    #Draw lines
#    my $cellHeight = 19;
#    my $topY = 789;
#    my $cellTopY = 769;
    #$bottomY = $cellTopY - $cellHeight * ($student_counter-1);
#    my $i;
#    my $LineY;
#    for ($i = 0; $i < $student_counter; $i++)
#    {
#	$LineY = $cellTopY - $cellHeight * $i;
#	PDF_DRAW::draw_line($leftX, $LineY, $rightX, $LineY);
#    }
}

sub print_doc_header
{
    print "Content-type: application/pdf\n\n";
    prFile();#$output_file);
    prMbox(0, 0, 1029, 836);
    PDF_DRAW::set_font(PDF_DRAW::get_default_font());
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

sub print_doc_footer
{
    prEnd();
#    my $pdf = PDF::API2->open($output_file);
#    my $content = $pdf->stringify();
#    print $content;
#    unlink($output_file);
}

sub print_provider_header
{

    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 5);
    PDF_DRAW::text($leftX, 801, qq{Providers with Compliance Issues (indicated "yes" for one of the Legal Questions - EMS Only)});
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 2);

	if ($student_counter > 1)
	{
      PDF_DRAW::text($NameX + 2, 774, "Name"); #80
      #PDF_DRAW::text(230, 774, "First Name");
      PDF_DRAW::text($SSNX + 2, 774, "SSN"); #375
      PDF_DRAW::text($StateProviderIDX + 2, 774, "Student ID"); #515 #485
      PDF_DRAW::text($CountyNameX + 2, 774, "County"); #640 #620
      PDF_DRAW::text($CompanyNameX + 2, 774, "Company"); #740
      PDF_DRAW::text($Legal1X + 2, 774, "Question 1");# 840
      PDF_DRAW::text($Legal2X + 2, 774, "Question 2");# 840
      PDF_DRAW::text($Legal3X + 2, 774, "Question 3");# 940
	}
	
	return;
}
   
sub print_provider_footer
{
	$bottomY = $LastLine;
#    my $leftX = 9; #24
#    my $rightX = 990;
    
	if ($student_counter > 1)
	{
    PDF_DRAW::draw_line($NameX, $topY, $NameX, $bottomY); #Left Line
    #PDF_DRAW::draw_line(135, $topY, 135, $bottomY);       #Last Name Line
    PDF_DRAW::draw_line($SSNX, $topY, $SSNX, $bottomY);       #SSN Line
    PDF_DRAW::draw_line($StateProviderIDX, $topY, $StateProviderIDX, $bottomY);       #Student ID Line 595
    PDF_DRAW::draw_line($CountyNameX, $topY, $CountyNameX, $bottomY);       #County Line
    PDF_DRAW::draw_line($CompanyNameX, $topY, $CompanyNameX, $bottomY);       #Company Line #790
    PDF_DRAW::draw_line($Legal1X, $topY, $Legal1X, $bottomY);       #Leg 1 Line
    PDF_DRAW::draw_line($Legal2X, $topY, $Legal2X, $bottomY);       #Leg 2 Line #890
    PDF_DRAW::draw_line($Legal3X, $topY, $Legal3X, $bottomY);       #Leg 3 Line #890
    PDF_DRAW::draw_line($rightX, $topY, $rightX, $bottomY); #Last Line

    #Horizontal lines
    PDF_DRAW::draw_line($leftX, $topY, $rightX, $topY);

    PDF_DRAW::draw_line($leftX, $topY, $rightX, $topY);

    PDF_DRAW::draw_line($leftX, $FirstLine + 14, $rightX, $FirstLine + 14);	
	
	$currY = PDF_DRAW::text($leftX, $currY, qq{Question 1: Have you ever applied for licensure or certification in any state other than Maryland?}); #80
	$currY = PDF_DRAW::text($leftX, $currY, qq{Question 2: Have you ever had any health care certification or license withheld, suspended revoked, or denied, or have you surrendered, or allowed a license or certificate to expire or lapse}); #80
	$currY = PDF_DRAW::text($leftX, $currY, qq{as the result of an investigation or disciplinary action?}); #80
	$currY = PDF_DRAW::text($leftX, $currY, qq{Question 3: Have you ever been convicted of, or pled guilty to, pled nolo contendre to, or received probation before judgement for any crime other than a minor traffic violation, the record}); #80
	$currY = PDF_DRAW::text($leftX, $currY, qq{of which has not been expunged?}); #80
	}
	return;

}


sub print_student_entry
{
    my ($last_name, $suffix, $first_name, $middle_name, $soc_sec, $student_id,$county, $company, $leg1, $leg2, $leg3) = @_;
    
	$soc_sec = STUREG_MAINT::HyphenateSSN($soc_sec);   
	
    if (2 == $leg1) 
	{ 
	  $leg1 = "YES"; 
	}
    else 
	{ 
	  $leg1 = "NO"; 
	}
    
    if (2 == $leg2) 
	{ 
	  $leg2 = "YES"; 
	}
    else 
	{ 
	  $leg2 = "NO"; 
	}
    
    if (2 == $leg3) 
	{ 
	  $leg3 = "YES"; 
	}
    else 
	{ 
	  $leg3 = "NO"; 
	}
    
    #my $currY = 755 - (($student_counter-1) * (PDF_DRAW::get_font_size()+ 6));

    my $nameString = $last_name;
    if (length($suffix) > 0)
	{
	  $nameString .= " " . $suffix;
	}
	
	if (length($nameString) > 0)
	{
	  $nameString .= ", ";
	}
#	else
#	{
#	  $nameString .= ",";
#	}
    
	$nameString .= $first_name;

	if (length($middle_name) > 0)
	{
	  $nameString .= " " . $middle_name;
	}
	#my $nameString2 = "";
    #$nameString2 .= $first_name;

    PDF_DRAW::draw_line($leftX, $currY - 2, $rightX, $currY - 2);	

	$LastLine = $currY;
	
	PDF_DRAW::text($NameX + 2, $currY, $nameString); #25 #10 
	#PDF_DRAW::text(135, $currY, $nameString2);
    #tgs 20050909 PDF_DRAW::center_text(80, $currY, $last_name);
    #tgs 20050909 PDF_DRAW::center_text(230, $currY, $first_name);

    PDF_DRAW::text($SSNX + 2, $currY, $soc_sec);  #375 #355
    PDF_DRAW::text($StateProviderIDX + 2, $currY, $student_id); #515 #485
    PDF_DRAW::text($CountyNameX + 2, $currY, $county); #640 #620
    PDF_DRAW::text($CompanyNameX + 2, $currY, $company); #740
    PDF_DRAW::text($Legal1X + 2, $currY, $leg1);#840
    PDF_DRAW::text($Legal2X + 2, $currY, $leg2);#840
    $currY = PDF_DRAW::text($Legal3X + 2, $currY, $leg3);#940

	$currY -= 3;
	
  return;
}

    
