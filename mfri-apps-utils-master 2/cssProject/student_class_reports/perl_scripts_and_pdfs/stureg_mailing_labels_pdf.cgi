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

my $PageWidth = 836;#836;   
my $PageHeight = 1029;#1029;   
my $currY = 1010;


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

sub Print_Label
{
  my $RowCounter = shift;
  my $ColumnCounter = shift;
  my $LinesToPrint = shift;
  
  my $NumberOfLines = @$LinesToPrint;
  
  my $FontMagnifier = 4;
  
  if ($NumberOfLines > 4)
  {
    $FontMagnifier = 2;
  }

  my $i;
  
  for ( $i = 0; $i < $NumberOfLines; $i++ )
  {
    if (length($LinesToPrint->[$i]) > 25)
	{
	  $FontMagnifier = 2;
	  next;
	}   
  }
  
  PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + $FontMagnifier); 

	my $RowY = 100;
	my $ColumnX = 18;

	if (1 == $ColumnCounter)
	{
	  $ColumnX = 296;
	}
	elsif (2 == $ColumnCounter)
	{ 
	  $ColumnX = 582; #578 #574;
	}
	
	my $LabelOffset = 102;
	
    $RowY = $PageHeight - 25;

	my $tlo = ($LabelOffset * $RowCounter) + 40;
	
	if ($RowCounter > 0)
	{
	  $RowY = $PageHeight - (($LabelOffset * $RowCounter) + 25);
	}

#APPDEBUG::WriteDebugMessage("RowCounter $RowCounter");		
#APPDEBUG::WriteDebugMessage("ColumnCounter $ColumnCounter");		
#APPDEBUG::WriteDebugMessage("LabelOffset $LabelOffset");		
#APPDEBUG::WriteDebugMessage("tlo $tlo");		
#APPDEBUG::WriteDebugMessage("RowY $RowY");		
#APPDEBUG::WriteDebugMessage("ColumnX $ColumnX");		
#$RowY = 200;
#$ColumnX = 100;
	
	$currY = $RowY;

    
	
	for ( $i = 0; $i < $NumberOfLines; $i++ )
	{
	  $currY = PDF_DRAW::text($ColumnX, $currY, $LinesToPrint->[$i]);  
	  $currY -= 2;
	}

    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());		

  return;  
}


my $ScheduledCourseID = CGI::param( 'SCID' );

if (not defined $ScheduledCourseID)
{
  $ScheduledCourseID = 0;
}

my $PrintStudentAddress = CGI::param( 'SADDR' );
#my $UserNumber10EnvelopeSize = 1;
#print address for each student or one for each agency
if (not defined $PrintStudentAddress)
{
  $PrintStudentAddress = 0;
}

#if (0 == $PrintStudentAddress)
#{
#  $UserNumber10EnvelopeSize = 0;
#}

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
  LEFT(ST.MiddleName, 1) AS MiddleName,
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
  AF.ID AS AffiliationID,
  AF.Name AS AffiliationName,
  AF.MailingAddress1 AS AffiliationAddress1,
  AF.MailingAddress2 AS AffiliationAddress2,
  AF.MailingCity AS AffiliationCity,
  AF.MailingState AS AffiliationState,
  AF.MailingPostCode AS AffiliationPostCode,
  AF.MailingCountry AS AffiliationCountry,
  RAF.ID AS RegionID,
  RAF.Name AS RegionName,
  RAF.Address1 AS RegionAddress1,
  RAF.Address2 AS RegionAddress2,
  RAF.City AS RegionCity,
  RAF.State AS RegionState,
  RAF.PostCode AS RegionPostCode,
  RAF.Country AS RegionCountry
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

#APPDEBUG::WriteDebugMessage("Student_Query_String $Student_Query_String");

my ($ReturnAddressName, $ReturnAddressAddress1, $ReturnAddressAddress2, $ReturnAddressCity, $ReturnAddressState, $ReturnAddressPostCode) = Get_Region_Return_Address($ScheduledCourseID);

my $ReturnAddressCityStateZip = "";
	
$ReturnAddressCityStateZip = $ReturnAddressCity . " " . $ReturnAddressState . " " . $ReturnAddressPostCode;


my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";

my $i = 0;
my $student_counter = 1;

#this is number 10 envelope size

#if  (0 == $UserNumber10EnvelopeSize)
#{
#  $PageWidth = 1029;
#  $PageHeight = 836;  
#}

#my $StartTextY = ($PageHeight / 2) - 25;#225; #270 #340; #480
#my $StartTextYReturnAddress = $PageHeight  - 36;#375; #270 #340; #480

#my $leftXOffsetReturnAddress = 30;
#my $leftXOffset = ($PageWidth / 2) + 50;


#my $leftX = 1;# 7

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
	
	my $AddressInfo;
	my $MaxRows = 9;
	my $MaxColumns = 2;
	
	my $RowCounter = 0;
	my $ColumnCounter = 0;
	
	my $PrintedRecord = 1;

	print_report_header();
#APPDEBUG::WriteDebugMessage("*****Start");	
	
	while ($AddressInfo = $db->get_rowh())
	{

        if (1 == $PrintStudentAddress)
        {
	      $PrintedRecord = print_student_entry($AddressInfo, $RowCounter, $ColumnCounter++);  
		}
		else
        {
	      $PrintedRecord = print_agency_entry($AddressInfo, $RowCounter, $ColumnCounter++);  
		  
		  if (0 == $PrintedRecord)
		  {
		    $ColumnCounter--;
		  }
		}
		
		if ($ColumnCounter > $MaxColumns)
		{
		  $ColumnCounter = 0;
		  $RowCounter++;
		}

		if ($RowCounter > $MaxRows)
		{
		  $RowCounter = 0;
	      $page_number++;
  	      print_report_footer();
	      #$currY = $StartTextY;
 	      PDF_DRAW::new_page();
		}

	}

#APPDEBUG::WriteDebugMessage("*****End");	
	
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
#    my ($last_name, $suffix, $first_name, $middle_name, $Address1, $Address2, $City, $State, $PostCode, $Country) = @_;
	my $Columnsh = shift;
	my $RowCounter = shift;
	my $ColumnCounter = shift;

	my $Address1 = uc($Columnsh->{Address1}); 
	my $Address2 = uc($Columnsh->{Address2});
	my $City = uc($Columnsh->{City});
	my $State = uc($Columnsh->{State});
	my $PostCode = uc($Columnsh->{PostCode});
	my $Country = uc($Columnsh->{Country});


	if (length($Address2) > 0) 
	{
	  if ((length($Address2) < 3 ) || ($Address2 =~ /^-?\d+$/))
	  {
	    $Address2 = "APT " . $Address2;
	  }
	}
	 
    my $nameString = $Columnsh->{FirstName};
	
	if (length($Columnsh->{MiddleName}) > 0)
	{
	  if (length($nameString) > 0)
	  {
	    $nameString .= " ";
	  }
	  $nameString .= $Columnsh->{MiddleName};
	}
	
    if (length($nameString) > 0)
	{
	  $nameString .= " ";
	}

    if (length($Columnsh->{LastName}) > 0)
	{
	  $nameString .= $Columnsh->{LastName};
	}
	
    if (length($nameString) > 0)
	{
	  $nameString .= " ";
	}

    if (length($Columnsh->{Suffix}) > 0)
	{
	  $nameString .= $Columnsh->{Suffix};
	}

	$nameString = uc($nameString);
	

	
	my $RowY = 100;
	my $ColumnX = 18;

	if (1 == $ColumnCounter)
	{
	  $ColumnX = 296;
	}
	elsif (2 == $ColumnCounter)
	{
	  $ColumnX = 574;
	}
	
	my $LabelOffset = 100;
	
    $RowY = $PageHeight - 26;

	my $tlo = ($LabelOffset * $RowCounter) + 40;
	
	if ($RowCounter > 0)
	{
	  $RowY = $PageHeight - (($LabelOffset * $RowCounter) + 26);
	}

#APPDEBUG::WriteDebugMessage("name $nameString");	
#APPDEBUG::WriteDebugMessage("RowCounter $RowCounter");		
#APPDEBUG::WriteDebugMessage("ColumnCounter $ColumnCounter");		
#APPDEBUG::WriteDebugMessage("LabelOffset $LabelOffset");		
#APPDEBUG::WriteDebugMessage("tlo $tlo");		
#APPDEBUG::WriteDebugMessage("RowY $RowY");		
#APPDEBUG::WriteDebugMessage("ColumnX $ColumnX");		
#$RowY = 200;
#$ColumnX = 100;
	
	$currY = $RowY;
    my @LinesToPrint;
	
	my $i = 0;
	@LinesToPrint[$i++] = $nameString;
	@LinesToPrint[$i++] = $Address1;
	
	if (length($Address2) > 0)
	{
	  @LinesToPrint[$i++] = $Address2;
	}
	
	if (length($City) > 0)
	{
	  @LinesToPrint[$i] = $City;

	  if (length($State) > 0)
	  {
	    @LinesToPrint[$i] .= " " . $State;
	  }

	  if (length($PostCode) > 0)
	  {
	    @LinesToPrint[$i] .= " " . $PostCode;
	  }
	  $i++;
	}
	

	if ((length($Country) > 0) && (uc($Country) ne "US") && (uc($Country) ne "USA"))
	{
	  @LinesToPrint[$i++] = $Country;
	}

	Print_Label( $RowCounter, $ColumnCounter, \@LinesToPrint );

  return 1;    
}

sub print_agency_entry
{
    #warn "printing entry";
    #my ($AFID, $AFName, $AFAddress1, $AFAddress2, $AFCity, $AFState, $AFPostCode, $AFCountry, $RAFID, $RAFName, $RAFAddress1, $RAFAddress2, $RAFCity, $RAFState, $RAFPostCode, $RAFCountry) = @_;
#APPDEBUG::WriteDebugMessage("print_agency_entry");	

	my $Columnsh = shift;
	my $RowCounter = shift;
	my $ColumnCounter = shift;

	my $AFName = uc($Columnsh->{AffiliationName}); 
	my $AFAddress1 = uc($Columnsh->{AffiliationAddress1}); 
	my $AFAddress2 = uc($Columnsh->{AffiliationAddress2});
	my $AFCity = uc($Columnsh->{AffiliationCity});
	my $AFState = uc($Columnsh->{AffiliationState});
	my $AFPostCode = uc($Columnsh->{AffiliationPostCode});
	my $AFCountry = uc($Columnsh->{AffiliationCountry});

	my $RFName = uc($Columnsh->{RegionName}); 
	my $RFAddress1 = uc($Columnsh->{RegionAddress1}); 
	my $RFAddress2 = uc($Columnsh->{RegionAddress2});
	my $RFCity = uc($Columnsh->{RegionCity});
	my $RFState = uc($Columnsh->{RegionState});
	my $RFPostCode = uc($Columnsh->{RegionPostCode});
	my $RFCountry = uc($Columnsh->{RegionCountry});

    my $AFID = $Columnsh->{AffiliationID};
    my $RFID = $Columnsh->{RegionID};
	my $Name = "";

	
	my $ID;
	my $Name;
	my $Address1;
	my $Address2;
	my $City;
	my $State;
	my $PostCode;
	my $Country;
	
	#558 None Given
	# 633 No Initial Affiliation
	#534 534
    if ((558 == $AFID) || (633 == $AFID) || (534 == $AFID) || (257 == $AFID))
	{
	  if ((558 == $RFID) || (633 == $RFID) || (534 == $RFID) || (257 == $RFID))
	  {
	    return 0;
	  }
	  
	  $ID = $RFID;
	  $Name = uc($RFName);
	  $Address1 = uc($RFAddress1);
	  $Address2 = uc($RFAddress2);
	  $City = uc($RFCity);
	  $State = uc($RFState);
	  $PostCode = uc($RFPostCode);
	  $Country = uc($RFCountry);
  
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
#APPDEBUG::WriteDebugMessage("Name $Name");		

    if ($LastNamePrinted eq $Name)
	{
	  return 0;
	}
#APPDEBUG::WriteDebugMessage("Address1 $Address1");		
#APPDEBUG::WriteDebugMessage("Address2 $Address2");		
#APPDEBUG::WriteDebugMessage("City $City");		
#APPDEBUG::WriteDebugMessage("State $State");		
#APPDEBUG::WriteDebugMessage("PostCode $PostCode");		

	$LastNamePrinted = $Name;

	
	my $RowY = 100;
	my $ColumnX = 18;

	if (1 == $ColumnCounter)
	{
	  $ColumnX = 296;
	}
	elsif (2 == $ColumnCounter)
	{
	  $ColumnX = 574;
	}
	
	my $LabelOffset = 100;
	
    $RowY = $PageHeight - 26;

	my $tlo = ($LabelOffset * $RowCounter) + 40;
	
	if ($RowCounter > 0)
	{
	  $RowY = $PageHeight - (($LabelOffset * $RowCounter) + 26);
	}
#APPDEBUG::WriteDebugMessage("RowCounter $RowCounter");		
#APPDEBUG::WriteDebugMessage("ColumnCounter $ColumnCounter");		
#APPDEBUG::WriteDebugMessage("LabelOffset $LabelOffset");		
#APPDEBUG::WriteDebugMessage("tlo $tlo");		
#APPDEBUG::WriteDebugMessage("RowY $RowY");		
#APPDEBUG::WriteDebugMessage("ColumnX $ColumnX");		
	
	$currY = $RowY;
    my @LinesToPrint;
	
	my $i = 0;
		
	my ($Name1, $Name2) = MFRI_STRINGS::Split_String_At_Word($Name, 31);

	if (length($Name2) < 5)
	{
      @LinesToPrint[$i++] = $LastNamePrinted;
	}
	elsif (length($Name2) > 0)
	{
	  $currY -= 2;
      @LinesToPrint[$i++] = $Name1;
	  
	  my ($Name21, $Name22) = MFRI_STRINGS::Split_String_At_Word($Name2, 31);
	  
      if (length($Name22) > 0)
	  {
        @LinesToPrint[$i++] = $Name21;
        @LinesToPrint[$i++] = $Name22;
	  }
	  else
	  {
	    @LinesToPrint[$i++] = $Name21;
	  }
	}
    
	@LinesToPrint[$i++] = $Address1;
	
	if (length($Address2) > 0)
	{
	  @LinesToPrint[$i++] = $Address2;
	}
	
	if (length($City) > 0)
	{
	  @LinesToPrint[$i] = $City;

	  if (length($State) > 0)
	  {
	    @LinesToPrint[$i] .= " " . $State;
	  }

	  if (length($PostCode) > 0)
	  {
	    @LinesToPrint[$i] .= " " . $PostCode;
	  }
	  $i++;
	}
	

	if ((length($Country) > 0) && (uc($Country) ne "US") && (uc($Country) ne "USA"))
	{
	  @LinesToPrint[$i++] = $Country;
	}

	Print_Label( $RowCounter, $ColumnCounter, \@LinesToPrint );
    
	return 1;
}



