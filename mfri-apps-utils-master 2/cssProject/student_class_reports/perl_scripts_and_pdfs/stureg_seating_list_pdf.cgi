#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use SEMINAR_MAINT;
use Database;
use CGI;
use strict;
use PDF_DRAW;
use POSIX;
use SCHEDULE_MAINT;
use MFRI_STRINGS;

use DBK;

#use APPDEBUG;

#Kick the user out if they aren't logged in
if(!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}

#Get the scheduled course ID.
my $ScheduledCourseID = CGI::param( 'SCID' ) || 0;

#Build the query string.
#SSN
#tgs 20050909 changed to MIEMSSNumber #tgs 20050909 changed to StateProviderNumber - was: ID Num.  We dont appear to be using this so I'll retrieve it then blank it out.
my $Student_Query_String = qq
{
SELECT
PR.LastName,
PR.Suffix,
LEFT(PR.MiddleName, 1),
PR.FirstName,
AES_DECRYPT(PR.IDNumber, "} . DBK::Encrypt_Key() . qq{") AS IDNumber, 
AES_DECRYPT(PR.StateProviderNumber, "} . DBK::Encrypt_Key() . qq{") AS StateProviderNumber,
PR.BirthDate,
PR.Address1,
PR.Apt,
PR.City,
PR.State,
PR.PostCode,
PR.PrimaryPhoneNumber,
PR.SecondaryPhoneNumber,
PR.Email,
PR.AffiliatedCompanyNumber,
PR.AffiliationID,
A.Name,
PR.StatusID,
PRS.Name as Status
FROM
RegistrationStatus AS PRS,
PreRegistrations as PR,
Affiliations as A
WHERE
( PR.AffiliationID = A.ID) AND
( PR.StatusID = PRS.Id) AND
( PR.ScheduledCourseID = $ScheduledCourseID ) AND 
( PR.StatusID not in ( 3, 4, 7) )
ORDER BY PRS.SortOrder, PR.Priority, PR.Created
};


#APPDEBUG::WriteDebugMessage("Student_Query_String $Student_Query_String");

#my $Student_Query_String = qq
#{
#SELECT
#ST.LastName,
#ST.Suffix,
#ST.FirstName,
#LEFT(ST.MiddleName, 1),
#AES_DECRYPT(ST.IDNumber, "} . DBK::Encrypt_Key() . qq{") AS IDNumber, 
#ST.MIEMSSNumber, 
#DATE_FORMAT(ST.BirthDate, \"%m-%d-%Y\"),
#ST.Address1,
#ST.Address2,
#ST.City,
#ST.State,
#ST.PostCode,
#ST.PrimaryPhoneNumber,
#ST.SecondaryPhoneNumber,
#ST.Email,
#ST.AffiliatedCompanyNumber
#FROM StudentRecords AS ST,
#StudentRegistration AS SR,
#Affiliations AS A
#WHERE (SR.StudentID = ST.ID) AND
#(SR.AffiliationID = A.ID) AND
#(SR.SchedCourseID = $ScheduledCourseID) AND
#(SR.StatusID != 4) AND (SR.StatusID != 7)
#ORDER BY SR.Created    
#};
#SR.Priority, 
#Get info about this course
my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($ScheduledCourseID);

#Connect to the database
my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";

my $MaxStudents = 0;

my $i = 0;
my $student_counter = 1;   #The total number of student entries
my $waitlist_counter = 1;   #The wait list counter
my $maxEntries = 25;#25;       #The max number of entries to be printed on the current page
my $currEntries = 0;       #The number of entries printed on the current page

my $cellHeight = 0;#25;                                  #The height of each cell
#my $ReportY = 953; #760;                                       #The topmost part of the grid
my $ReportY = 980;#926#953#1010;

my $DetailY = 909;#953;#926#733;                                   #The topmost cell
#my $TextStartY = 0;
#my $DetailRowY = 909;#716;
my $FirstRowY = 895;
my $DetailRowY = $FirstRowY; #909; #$ReportY;
my $leftX = 7;                                        #The left margin of the report
my $rightX = 800;  #1020                                  #The right margin of the report

my $bottomY = 0;#$DetailY - $cellHeight * ($maxEntries + 1);

my $CounterX = 10;
my $NameX = 92;
my $AffiliationX = 215;
my $AddressX = 400;
my $ContactX = 600;

my $TextColumnOffset = 3;

#Print the document
print_doc_header();
my $page_number = 1;
my $page_count = 0;
print_roster();
print_doc_footer();
$db->finish(); #03-11-2005 WPL Added DB Finish


sub print_roster
{
    if ($need_to_query eq "YES") 
    {
#APPDEBUG::WriteDebugMessage("Student_Query_String $Student_Query_String");		
	$db->query( $Student_Query_String );	
	$need_to_query = "NO";
    }

    #Calculate the number of pages that we will use
    $page_count = POSIX::ceil($db->num_rows() / $maxEntries);
    $page_count = 1 if ($page_count == 0);

    #print the page header
    print_roster_header();

    #Print any student entries found
    if ($db->num_rows() > 0)
    {
	my @studentroster;
	
	while (@studentroster = $db->get_row())
	{
	    #Is it time to start a new page?
	    if ($currEntries >= $maxEntries)
	    {
		
		  print_roster_footer(); #Print a page footer
		  PDF_DRAW::new_page();  #Start a new page
		  $page_number++;        #Increment the page counter
		  print_roster_header(); #Print a page header
		  $currEntries = 0;
		  $DetailRowY = $FirstRowY;
	    }
	    
	    print_student_entry(@studentroster);    
	    $student_counter++;
	    $currEntries++;	    	    
	}

    }

    #Fill out the rest of the page with empty entries
    while (($currEntries > 0) && ($currEntries < $maxEntries))
    {
	  print_student_entry();
	  $student_counter++;
	  $currEntries++;
    }

    print_roster_footer();
    
}

#Used to setup our page for printing PDF documents
sub print_doc_header
{
#    PDF_DRAW::doc_header(1029, 836);
#    PDF_DRAW::doc_header(836, 1029);
    PDF_DRAW::doc_header(836, 1029); #Create the document
    PDF_DRAW::set_formatting(1); #Turn on formatting so we can use tags (optional)
    PDF_DRAW::set_font("Times-Roman"); #Set the font (optional)
	
}

#Ends the pdf document and prints it to the screen
sub print_doc_footer
{
    PDF_DRAW::doc_footer();
}

#A header printed at the start of EACH PAGE
sub print_roster_header
{
    my $CourseCode = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 1);
    my $instName = $ScheduleInfo->{InstructorName};
    my $location = $ScheduleInfo->{LocationName};
    my $course_title = $ScheduleInfo->{Title};
    $MaxStudents = $ScheduleInfo->{MaxStudents};
    my $pagenum = get_page_num();
    my $i;
    my $currX;
    #my $DetailRowY;
    
    $instName = "" if (($instName eq "MFRI Instructor") || ($instName eq "MFRI Staff"));

	$location = "" if ($location eq "TBD - To be determined");
	
	my $RowCounter = $ReportY - 12;# - 44;
	my $TitleX = 11;
	my $DetailsX = 411;
	my $PageNumberX = 775;#975
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 10);

    $RowCounter = PDF_DRAW::text($TitleX, $RowCounter, $course_title); #792
    $RowCounter = PDF_DRAW::text($TitleX, $RowCounter, "Course Roster"); #774

	$RowCounter = $ReportY - 12; # - 22;
    
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 2);
    $RowCounter = PDF_DRAW::text($DetailsX, $RowCounter, "Course \#: $CourseCode"); #814
    $RowCounter = PDF_DRAW::text($DetailsX, $RowCounter, "Primary Instructor: $instName"); #794
    $RowCounter = PDF_DRAW::text($DetailsX, $RowCounter, "Location: $location"); #773

	$RowCounter = $DetailY + 4; #$ReportY - 94;
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+1);
    PDF_DRAW::text($CounterX, $RowCounter, "Max: $MaxStudents");#742

    PDF_DRAW::text($NameX + $TextColumnOffset, $RowCounter, "Name"); #742

    PDF_DRAW::text($AffiliationX + $TextColumnOffset, $RowCounter, "Affiliation");#742
    PDF_DRAW::text($AddressX + $TextColumnOffset, $RowCounter, "Address");#742
    PDF_DRAW::text($ContactX + $TextColumnOffset, $RowCounter, "Contact");#742

	$RowCounter = $ReportY;
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() - 2);
    PDF_DRAW::text($PageNumberX, $RowCounter, "Page $page_number of $page_count"); #820

	$RowCounter = $DetailY + 4;#$ReportY - 98;
	
	PDF_DRAW::draw_line($leftX, $DetailY, $rightX, $DetailY);	 #738 #$RowCounter
    
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

#A footer printed at the bottom of EACH PAGE   
sub print_roster_footer
{

    #It's easier to draw all the lines of the form at the end of each page.
    #This way, we already know how many entries to account for.

	$bottomY = $DetailY - $cellHeight * $maxEntries; # + 1
    #Draw lines
    #my $bottomY = $DetailY - $cellHeight * $maxEntries;  #The bottom of the cells/report
    
    #Vertical Lines
    PDF_DRAW::draw_line($leftX, $DetailY, $leftX, $bottomY); #Left Line
    PDF_DRAW::draw_line($NameX, $DetailY, $NameX, $bottomY);         #Name

    PDF_DRAW::draw_line($AffiliationX, $DetailY, $AffiliationX, $bottomY);       #Affiliation
    #PDF_DRAW::draw_line(755, $ReportY, 755, $bottomY);       #Apt Line
    #PDF_DRAW::draw_line(875, $ReportY, 875, $bottomY);       #City Line
    #PDF_DRAW::draw_line(905, $ReportY, 905, $bottomY);       #St Line
    PDF_DRAW::draw_line($AddressX, $DetailY, $AddressX, $bottomY);       #Address

    PDF_DRAW::draw_line($ContactX, $DetailY, $ContactX, $bottomY); #Contact

	PDF_DRAW::draw_line($rightX, $DetailY, $rightX, $bottomY);  #Right Line # 

	
    #Horizontal lines
	PDF_DRAW::draw_line($leftX, $bottomY, $rightX, $bottomY);
   # PDF_DRAW::draw_line($leftX, $DetailY, $rightX, $DetailY);

	
    #Draw Lines between each entry
#    my $DetailRowY;
#    my $midY;
#    for ($i = 0; $i < $maxEntries+1; $i++)
#    {
#	$DetailRowY = $DetailY - $cellHeight * $i;
#	$midY = $DetailRowY - $cellHeight / 2;
#	PDF_DRAW::draw_line($leftX, $DetailRowY, $rightX, $DetailRowY);	

#    }

}


#Print a single student entry
sub print_student_entry
{


    my ($last_name, $suffix, $MI, $first_name, $SSN, $ID, $DOB, $Address1, $Address2, $city, $state, $zip, $PrimaryPhoneNumber, $SecondaryPhoneNumber, $Email, $COMP, $AffiliationID, $AffiliationName, $StatusID, $StatusName) = @_;

    if (length($last_name) == 0)
	{
	  $last_name = "";
	}
	
    if (length($suffix) == 0)
	{
	  $suffix = "";
	}
	
    if (length($MI) == 0)
	{
	  $MI = "";
	}
	
    if (length($first_name) == 0)
	{
	  $first_name = "";
	}
	
    if (length($SSN) == 0)
	{
	  $SSN = "";
	}
	
    if (length($DOB) == 0)
	{
	  $DOB = "";
	}
	
    if (length($Address1) == 0)
	{
	  $Address1 = "";
	}
	
    if (length($Address2) == 0)
	{
	  $Address2 = "";
	}
	
    if (length($city) == 0)
	{
	  $city = "";
	}
	
    if (length($state) == 0)
	{
	  $state = "";
	}
	
    if (length($zip) == 0)
	{
	  $zip = "";
	}
	
#APPDEBUG::WriteDebugMessage("1 PrimaryPhoneNumber >$PrimaryPhoneNumber<");	
    if (length($PrimaryPhoneNumber) == 0)
	{
	  $PrimaryPhoneNumber = "";
	}
    else
	{	
	  $PrimaryPhoneNumber =~ s/\\//gm;
	  $PrimaryPhoneNumber =~ s/\'//gm;
  	  $PrimaryPhoneNumber =~ s/\"//gm;
    }
#APPDEBUG::WriteDebugMessage("2 PrimaryPhoneNumber >$PrimaryPhoneNumber<");	

	if ($PrimaryPhoneNumber eq "NULL")
	{
	  $PrimaryPhoneNumber = "";
	}
	
    if (length($SecondaryPhoneNumber) == 0)
	{
	  $SecondaryPhoneNumber = "";
	}
	
    if (length($Email) == 0)
	{
	  $Email = "";
	}
	
    if (length($COMP) == 0)
	{
	  $COMP = "";
	}
	
    if (length($AffiliationName) == 0)
	{
	  $AffiliationName = "";
	}
	
    $MI = substr($MI, 0, 1);
    my $pagenum = &get_page_num;
	
	$SSN = STUREG_MAINT::HyphenateSSN($SSN);  
 
 #   my $DetailRowY = 716 - (($currEntries) * (PDF_DRAW::get_default_font_size() + 14));
  	my $NameString1 = "";
  	my $NameString2 = "";
  	my $NameString3 = "";


#APPDEBUG::WriteDebugMessage("first_name $first_name");	
	
	my $nameString = $first_name;
	
	if (length($nameString) > 0)
	{
	  $nameString .= " ";
	}

	$nameString .= $MI;
	
	if (length($MI) > 0)
	{
	  $nameString .= ".";
	}

	if (length($nameString) > 0)
	{
	  $nameString .= " ";
	}

	$nameString .= $last_name;
	
    if (length($suffix) > 0)
	{
	  $nameString .= " $suffix";
	}

	($NameString1, $NameString2) = MFRI_STRINGS::Split_String_At_Word( $nameString, 20);
	($NameString2, $NameString3) = MFRI_STRINGS::Split_String_At_Word( $NameString2, 20);	
	
    my $CityStateZip = $city;
    
	if (length($CityStateZip) > 0)
	{
	  $CityStateZip .= " ";
	}

	$CityStateZip .= $state;
	
	if (length($state) > 0)
	{
	  $CityStateZip .= ",";
	}

	if (length($CityStateZip) > 0)
	{
	  $CityStateZip .= " ";
	}

	$CityStateZip .= $zip;

	my $LineY = $DetailRowY;
	my $NextY = $DetailRowY;
	my $Line2Y = 0;
	my $Line3Y = 0;
	
    my $OldFontSize = PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 4);

    PDF_DRAW::text($CounterX + $TextColumnOffset, $LineY - $TextColumnOffset, $student_counter);
	
    PDF_DRAW::text($CounterX + $TextColumnOffset, $LineY - $TextColumnOffset, $student_counter);

	if (($MaxStudents > 0) && ($student_counter > $MaxStudents))
	{
      PDF_DRAW::text($NameX - 30, $LineY - $TextColumnOffset, qq{($waitlist_counter)});
	  $waitlist_counter++;
	}
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()- 1 ); # - 1
	
    #PDF_DRAW::text($NameX + $TextColumnOffset, $LineY, $nameString);

	if (length($NameString3) > 0)
	{
	  $Line2Y = PDF_DRAW::text($NameX + $TextColumnOffset, $LineY, $NameString1);
	  $Line3Y = PDF_DRAW::text($NameX + $TextColumnOffset, $Line2Y, $NameString2);
	  $NextY  = PDF_DRAW::text($NameX + $TextColumnOffset, $Line3Y, $NameString3);
	}
	elsif (length($NameString2) > 0)
	{
	  $Line2Y = PDF_DRAW::text($NameX + $TextColumnOffset, $LineY, $NameString1);
	  $Line3Y = PDF_DRAW::text($NameX + $TextColumnOffset, $Line2Y, $NameString2);
	}
	else
	{
	  $Line2Y = PDF_DRAW::text($NameX + $TextColumnOffset, $LineY, $NameString1);
	}

    #tgs 20050909 PDF_DRAW::text(55, $DetailRowY, $last_name);

	my $AffiliationName1 = "";
	my $AffiliationName2 = "";
	($AffiliationName1, $AffiliationName2) = MFRI_STRINGS::Split_String_At_Word( $AffiliationName, 39);

    
	if (length($AffiliationName2) > 0)
	{
	  $Line2Y = PDF_DRAW::text($AffiliationX + $TextColumnOffset, $LineY, $AffiliationName1);
	  $Line3Y = PDF_DRAW::text($AffiliationX + $TextColumnOffset, $Line2Y, $AffiliationName2);
	  $NextY  = PDF_DRAW::text($AffiliationX + $TextColumnOffset, $Line3Y, $COMP);
	}
	else
	{
	  $Line2Y = PDF_DRAW::text($AffiliationX + $TextColumnOffset, $LineY, $AffiliationName);
      $Line3Y = PDF_DRAW::text($AffiliationX + $TextColumnOffset, $Line2Y, $COMP);
	}
#APPDEBUG::WriteDebugMessage("currY $DetailRowY");		
#APPDEBUG::WriteDebugMessage("LineY $LineY");		
    $Line2Y = PDF_DRAW::text($AddressX + $TextColumnOffset, $LineY, $Address1);
#APPDEBUG::WriteDebugMessage("Line2Y $Line2Y");		

    $Line3Y = PDF_DRAW::text($AddressX + $TextColumnOffset, $Line2Y, $Address2);
#APPDEBUG::WriteDebugMessage("Line3Y $Line3Y");		
    $NextY = PDF_DRAW::text($AddressX + $TextColumnOffset, $Line3Y, $CityStateZip);
#APPDEBUG::WriteDebugMessage("NextY $NextY");		

    PDF_DRAW::text($ContactX + $TextColumnOffset, $LineY, $PrimaryPhoneNumber);
    PDF_DRAW::text($ContactX + $TextColumnOffset, $Line2Y, $SecondaryPhoneNumber);
    PDF_DRAW::text($ContactX + $TextColumnOffset, $Line3Y, $Email);
    
	if ($currEntries < ($maxEntries - 1))
	{
	  PDF_DRAW::draw_line($leftX, $Line3Y - 2, $rightX, $Line3Y - 2);	
	  
	  if (($MaxStudents > 0) && ($student_counter == $MaxStudents))
	  {
	    PDF_DRAW::draw_line($leftX, $Line3Y + 1, $rightX, $Line3Y + 1);	
	  }
	  
	}
	
    if (0 == $cellHeight)
	{
#APPDEBUG::WriteDebugMessage("DetailRowY $DetailRowY");		
#APPDEBUG::WriteDebugMessage("NextY $NextY");		
	  $cellHeight = $DetailRowY - $NextY;
#APPDEBUG::WriteDebugMessage("cellHeight $cellHeight");		
	}
    
	$DetailRowY = $NextY;
	
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
}

#Get the current page number
sub get_page_num
{
    return $page_number;
}
