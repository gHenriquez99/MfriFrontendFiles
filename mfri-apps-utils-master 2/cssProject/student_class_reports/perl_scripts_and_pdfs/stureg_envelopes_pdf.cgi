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

use DBK;

use APPDEBUG;


sub Get_Region_Return_Address
{
	my $SchedID = shift;
	
	my $Name = "";
	my $Address1 = "";
	my $Address2 = "";
	my $City = "";
	my $State = "";
	my $PostCode = "";
	
	if( not defined $SchedID )
	{
		return ($Name, $Address1, $Address2, $City, $State, $PostCode);
	}

	my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
	
	my $QueryString = qq{select 
Reg.Name,
Reg.PostalAddress1,
Reg.PostalStreetAddress2,
Reg.City,
Reg.State,
Reg.PostCode,
Sched.RegionID,
Sched.SectionID
FROM ScheduledCourses AS Sched, 
MFRIRegions AS Reg, 
CourseSection AS CSec 
WHERE (Sched.RegionID = Reg.ID) AND (Sched.SectionID = CSec.Id) AND (Sched.ID = $SchedID)
};

	$db->query( $QueryString );

    if( $db->num_rows() < 1 )
    {
	  #return "";
	    $db->finish();  
		return ($Name, $Address1, $Address2, $City, $State, $PostCode);

	}
        
	my $SchedInfo = $db->get_rowh();
  

	$Name = $SchedInfo->{Name};

	if (2 == $SchedInfo->{RegionID})
	{
	  $Name .= " Regional Office";
	}
	elsif (7 == $SchedInfo->{RegionID})
	{
	  $Name = "Maryland Fire and Rescue Institute";
	}
	else
	{
	  $Name .= " Regional Training Center";
	}

	$Address1 = $SchedInfo->{PostalAddress1};
	$Address2 = $SchedInfo->{PostalStreetAddress2};
	$City = $SchedInfo->{City};
	$State = $SchedInfo->{State};
	$PostCode = $SchedInfo->{PostCode};

	$db->finish();  
	
	return ($Name, $Address1, $Address2, $City, $State, $PostCode);
}


my $ScheduledCourseID = CGI::param( 'SCID' );

if (not defined $ScheduledCourseID)
{
  $ScheduledCourseID = 0;
}

my $PrintStudentAddress = CGI::param( 'SADDR' );
my $UserNumber10EnvelopeSize = 1;
#print address for each student or one for each agency
if (not defined $PrintStudentAddress)
{
  $PrintStudentAddress = 0;
}

if (0 == $PrintStudentAddress)
{
  $UserNumber10EnvelopeSize = 0;
}

if(!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}

 
my $Student_Query_String = "";

if (1 == $PrintStudentAddress)
{
  $Student_Query_String = qq
  {
  SELECT
  ST.LastName,
  ST.Suffix,
  ST.FirstName,
  LEFT(ST.MiddleName, 1),
  ST.Address1,
  ST.Address2,
  ST.City,
  ST.State,
  ST.PostCode,
  ST.Country
  FROM StudentRecords AS ST,
  StudentRegistration AS SR
  WHERE 
  (SR.SchedCourseID = $ScheduledCourseID) AND
  (SR.StudentID = ST.ID) AND
  (SR.StatusID != 4)
  ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, ST.Suffix, SR.Created    
  };
  
  #  (SR.StatusID != 4)
  #envelopes should only be printed for people who have passed, StatusID = 7
}
else
{
  $Student_Query_String = qq  
  {
  SELECT
  AF.ID,
  AF.Name,
  AF.MailingAddress1 AS Address1,
  AF.MailingAddress2 AS Address2,
  AF.MailingCity AS City,
  AF.MailingState AS State, 
  AF.MailingPostCode AS PostCode,
  AF.MailingCountry AS Country,
  RAF.ID,
  RAF.Name,
  RAF.MailingAddress1 AS ReturnAddress1,
  RAF.MailingAddress2 AS ReturnAddress2,
  RAF.MailingCity AS ReturnCity,
  RAF.MailingState AS ReturnState, 
  RAF.MailingPostCode AS ReturnPostCode,
  RAF.MailingCountry AS ReturnCountry
  FROM StudentRecords AS ST,
  StudentRegistration AS SR,
  Affiliations AS AF,
  Affiliations AS RAF
  WHERE 
  (SR.SchedCourseID = $ScheduledCourseID) AND
  (SR.StudentID = ST.ID) AND
  (SR.StatusID != 4) AND (SR.StatusID != 22) AND 
  (SR.AffiliationID = AF.ID) AND
  (ST.AffiliationID = RAF.ID)
  ORDER BY AF.Name, RAF.Name    
  };

  #  (SR.StatusID != 4)
  #envelopes should only be printed for people who have passed, StatusID = 7

}

#(SR.StatusID in (8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 ))

my ($ReturnAddressName, $ReturnAddressAddress1, $ReturnAddressAddress2, $ReturnAddressCity, $ReturnAddressState, $ReturnAddressPostCode) = Get_Region_Return_Address($ScheduledCourseID);

my $ReturnAddressCityStateZip = "";
	
$ReturnAddressCityStateZip = $ReturnAddressCity . " " . $ReturnAddressState . " " . $ReturnAddressPostCode;


my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";

my $i = 0;
my $student_counter = 1;

#this is number 10 envelope size
my $PageWidth = 950;   
my $PageHeight = 411;   

if  (0 == $UserNumber10EnvelopeSize)
{
  $PageWidth = 1029;
  $PageHeight = 836;  
}

my $StartTextY = ($PageHeight / 2) - 25;#225; #270 #340; #480
my $StartTextYReturnAddress = $PageHeight  - 36;#375; #270 #340; #480

my $leftXOffsetReturnAddress = 30;
my $leftXOffset = ($PageWidth / 2) + 50;

my $currY = $StartTextY;

my $leftX = 1;# 7

my $LastNamePrinted = "";

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
	
	my @AddressInfo;
	
	while (@AddressInfo = $db->get_row())
	{
		print_report_header();

        if (1 == $PrintStudentAddress)
        {
	      print_student_entry(@AddressInfo);  
		}
		else
        {
	      print_agency_entry(@AddressInfo);  
		}
		
		$page_number++;
		print_report_footer();
		$currY = $StartTextY;
		PDF_DRAW::new_page();
	}

	
}

sub print_doc_header
{   
    #PDF_DRAW::doc_header(1029, 836);
#    PDF_DRAW::doc_header(950, 411);
    PDF_DRAW::doc_header($PageWidth, $PageHeight);
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

sub print_student_entry
{
    #warn "printing entry";
    my ($last_name, $suffix, $first_name, $middle_name, $Address1, $Address2, $City, $State, $PostCode, $Country) = @_;

#	my $ReturnAddressY = $StartTextYReturnAddress;
 
#	$ReturnAddressY = PDF_DRAW::text($leftXOffsetReturnAddress, $ReturnAddressY, $ReturnAddressName);  

#    	$ReturnAddressY -= 2;
 #   $ReturnAddressY = PDF_DRAW::text($leftXOffsetReturnAddress, $ReturnAddressY, $ReturnAddressAddress1); 
	
#	$ReturnAddressY -= 2;
    
#	if (length($ReturnAddressAddress2) > 0)
#	{
#      $ReturnAddressY = PDF_DRAW::text($leftXOffsetReturnAddress, $ReturnAddressY, $ReturnAddressAddress2); 
#	}
	
#	$ReturnAddressY -= 2;
#    $ReturnAddressY = PDF_DRAW::text($leftXOffsetReturnAddress, $ReturnAddressY, $ReturnAddressCityStateZip); 
	 
	$Address1 = uc($Address1); 
	$Address2 = uc($Address2);
	$City = uc($City);
	$State = uc($State);
	$PostCode = uc($PostCode);
	$Country = uc($Country);
	
	
	if (length($Address2) > 0) 
	{
	  if ((length($Address2) < 3 ) || ($Address2 =~ /^-?\d+$/))
	  {
	    $Address2 = "APT " . $Address2;
	  }
	}
	 
    my $nameString = $first_name;
	
	if (length($middle_name) > 0)
	{
	  if (length($nameString) > 0)
	  {
	    $nameString .= " ";
	  }
	  $nameString .= $middle_name;
	}
	
    if (length($nameString) > 0)
	{
	  $nameString .= " ";
	}

    if (length($last_name) > 0)
	{
	  $nameString .= $last_name;
	}
	
    if (length($nameString) > 0)
	{
	  $nameString .= " ";
	}

    if (length($suffix) > 0)
	{
	  $nameString .= $suffix;
	}

	$nameString = uc($nameString);
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 8); 
	$currY = PDF_DRAW::text($leftXOffset, $currY, $nameString);  
    
	$currY -= 2;
    $currY = PDF_DRAW::text($leftXOffset, $currY, $Address1); 
	
	if (length($Address2) > 0)
	{
	  $currY -= 2;
    
      $currY = PDF_DRAW::text($leftXOffset, $currY, $Address2); 
	}
	
	my $CityStateZip = "";
	
	if (length($City) > 0)
	{
	  $CityStateZip = $City . " " . $State . "  " . $PostCode;
    }
	
	$currY -= 2;
    $currY = PDF_DRAW::text($leftXOffset, $currY, $CityStateZip); 
	 
    #$currY -= 17;

	if ((length($Country) > 0) && (uc($Country) ne "US") && (uc($Country) ne "USA"))
	{
	  $currY -= 2;
	  $currY = PDF_DRAW::text($leftXOffset, $currY, uc($Country)); 
	}
	 
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
    #warn "done.";
    #die;
    
}

sub print_agency_entry
{
    #warn "printing entry";
    my ($AFID, $AFName, $AFAddress1, $AFAddress2, $AFCity, $AFState, $AFPostCode, $AFCountry, $RAFID, $RAFName, $RAFAddress1, $RAFAddress2, $RAFCity, $RAFState, $RAFPostCode, $RAFCountry) = @_;


    my $ID;
	my $Name = "";
	my $Address1 = "";
	my $Address2 = "";
	my $City = "";
	my $State = "";
	my $PostCode = "";
	my $Country = "";

	#558 None Given
	# 633 No Initial Affiliation
	#534 534
    if ((558 == $AFID) || (633 == $AFID) || (534 == $AFID))
	{
	  if ((558 == $RAFID) || (633 == $AFID) || (534 == $AFID))
	  {
	    return;
	  }
	  
	  $ID = $RAFID;
	  $Name = uc($RAFName);
	  $Address1 = uc($RAFAddress1);
	  $Address2 = uc($RAFAddress2);
	  $City = uc($RAFCity);
	  $State = uc($RAFState);
	  $PostCode = uc($RAFPostCode);
	  $Country = uc($RAFCountry);
  
	}
	else
	{
	  $ID = $AFID;
	  $Name = uc($AFName);
	  $Address1 = uc($AFAddress1);
	  $Address2 = uc($AFAddress2);
	  $City = uc($AFCity);
	  $State = uc($AFState);
	  $PostCode = uc($AFPostCode);
	  $Country = uc($AFCountry);
	}

    if ($LastNamePrinted eq $Name)
	{
	  return;
	}

	$LastNamePrinted = $Name;
	
	my $ReturnAddressY = $StartTextYReturnAddress;
 
	$ReturnAddressY = PDF_DRAW::text($leftXOffsetReturnAddress, $ReturnAddressY, $ReturnAddressName);  
    
	$ReturnAddressY -= 2;
    $ReturnAddressY = PDF_DRAW::text($leftXOffsetReturnAddress, $ReturnAddressY, $ReturnAddressAddress1); 
	
	$ReturnAddressY -= 2;
    
	if (length($ReturnAddressAddress2) > 0)
	{
      $ReturnAddressY = PDF_DRAW::text($leftXOffsetReturnAddress, $ReturnAddressY, $ReturnAddressAddress2); 
	}
	
	$ReturnAddressY -= 2;
    $ReturnAddressY = PDF_DRAW::text($leftXOffsetReturnAddress, $ReturnAddressY, $ReturnAddressCityStateZip); 
	
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 8); 
	
	my ($Name1, $Name2) = MFRI_STRINGS::Split_String_At_Word($Name, 45);

	if (length($Name2) < 5)
	{
	  $Name1 = $LastNamePrinted;
	  $Name2 = "";
	}
	
	$currY = PDF_DRAW::text($leftXOffset, $currY, $Name1);  
	
	if (length($Name2) > 0)
	{
	  $currY -= 2;
	  $currY = PDF_DRAW::text($leftXOffset, $currY, $Name2);  
	}
    
	$currY -= 2;
    $currY = PDF_DRAW::text($leftXOffset, $currY, $Address1); 

	if (length($Address2) > 0)
	{
	  $currY -= 2;
      $currY = PDF_DRAW::text($leftXOffset, $currY, $Address2); 
	}
	
	my $CityStateZip = "";
	
	if (length($City) > 0)
	{
	  $CityStateZip = $City . " " . $State . "  " . $PostCode;
    }
	
	$currY -= 2;
    $currY = PDF_DRAW::text($leftXOffset, $currY, $CityStateZip); 
	 
    #$currY -= 17;

	if ((length($Country) > 0) && (uc($Country) ne "US") && (uc($Country) ne "USA"))
	{
	  $currY -= 2;
	  $currY = PDF_DRAW::text($leftXOffset, $currY, uc($Country)); 
	}
	 
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
    #warn "done.";
    #die;
    
}



