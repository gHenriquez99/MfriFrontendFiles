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
use MFRI_UTIL;
use DATE_UTIL;
use MFRI_MED;
use MFRI_STRINGS;

use DBK;

use APPDEBUG;

if(!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}

my $ScheduledCourseID = CGI::param( 'SCID' );

if (not defined $ScheduledCourseID)
{
  $ScheduledCourseID = 0;
}

if ($ScheduledCourseID < 1)
{
  MFRI::set_parameter("error", "No course specified ($ScheduledCourseID).");
  MFRI::redirect("error.cgi");
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
#CD.CourseCode
#FROM ScheduledCourses AS SC,
#CourseDescriptions AS CD
#WHERE (SC.ID = $ScheduledCourseID) AND (SC.CourseID = CD.Id)   
#};

#tgs 20050909 SSN blow was IDNumber

my $EncryptKey = qq{"} . DBK::Encrypt_Key() . qq{"};

my $Student_Query_String = qq
{
SELECT
ST.ID,
ST.LastName,
ST.Suffix,
ST.FirstName,
ST.MiddleName,
AES_DECRYPT(ST.IDNumber, $EncryptKey) AS SSN,
DATE_FORMAT(ST.BirthDate,"%m-%d-%Y") AS BirthDate,
ST.Address1,                   
ST.Address2,                   
ST.City,                       
ST.State,                      
ST.PostCode,                   
ST.Country,                    
ST.PrimaryPhoneNumber,         
ST.SecondaryPhoneNumber,       
ST.Email,
A.Name AS AffiliationName,
A.miemss_number AS CompanyNumber
FROM StudentRecords AS ST,
StudentRegistration AS SR,
Affiliations AS A
WHERE 
(SR.SchedCourseID = $ScheduledCourseID) AND
(SR.StudentID = ST.ID) AND
(SR.AffiliationID = A.ID)
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, ST.Suffix, SR.Created    
};

#(SR.StatusID in (8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 ))

#my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($ScheduledCourseID);

my $ScheduledCourseInfo = MFRI_UTIL::GetScheduledCourse($ScheduledCourseID);

my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";

my $i = 0;
my $student_counter = 1;

my $EntryCount = 0;
my $EntriesPerPage = 3;

my $PageWidth = 836;
my $PageHeight = 1000;#1029;#1029;

my $FormWidth = $PageWidth - 20;

my $MarginCount = ($EntriesPerPage - 1);

my $FormMargin = PDF_DRAW::get_line_delta();# * 5;

my $LeftLabelOffset = 10; 
my $LeftTextOffset = $LeftLabelOffset + 90; 

if ($MarginCount < 1)
{
  $MarginCount = 1;	
}
 

#APPDEBUG::WriteDebugMessage("***********");
#APPDEBUG::WriteDebugMessage("PageWidth $PageWidth");
#APPDEBUG::WriteDebugMessage("PageHeight $PageHeight");
#APPDEBUG::WriteDebugMessage("FormWidth $FormWidth"); 
#APPDEBUG::WriteDebugMessage("MarginCount $MarginCount");

#APPDEBUG::WriteDebugMessage("1 FormMargin $FormMargin");
my $FormHeight = ($PageHeight / $EntriesPerPage) - ($MarginCount * $FormMargin) - $FormMargin;

##recalculate margin to spread forms out on page
#$FormMargin = $PageHeight - ($FormHeight * $EntriesPerPage);

#APPDEBUG::WriteDebugMessage("FormHeight $FormHeight");
#APPDEBUG::WriteDebugMessage("2 FormMargin $FormMargin");


my $StartTextY = $PageHeight - PDF_DRAW::get_line_delta();#- 12;#268; #270 #340; #480

my $StartFormY = $PageHeight - PDF_DRAW::get_line_delta();#- 12;#268; #270 #340; #480

#APPDEBUG::WriteDebugMessage("StartTextY $StartTextY");


my $leftXOffset = 20;#60;

my $currY = $StartTextY;

my $leftX = 1;# 7

#my $course_code = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 1);
#my $course_name = $ScheduleInfo->{Title};
#my $location = $ScheduleInfo->{LocationName};


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
	
	my @studentinfo;
    my $MarginAdjust = 0;
	
	while (@studentinfo = $db->get_row())
	{
#warn "1 currY: $currY";
#       if (0 == $EntryCount) 
#	   {
#	     $MarginAdjust = 0;
#       }
#	   elsif (1 == $EntryCount)
#	   {
#	     $MarginAdjust = PDF_DRAW::get_line_delta() * 2;
#       }		
#	   elsif (2 == $EntryCount)
#	   {
#	     $MarginAdjust = PDF_DRAW::get_line_delta() * 2;
#       }		
#	   else
#	   {
#	     $MarginAdjust = PDF_DRAW::get_line_delta() * 2;
#       }		

#        $currY = $StartTextY; - ($EntryCount * $FormHeight) - $MarginAdjust;
#my $t1 = $EntryCount * $FormHeight;
#my $t2 = $StartTextY - $t1;

#warn "2 currY: $currY";
#warn "StartTextY: $StartTextY";
#warn "EntryCount: $EntryCount";
##warn "FormHeight: $FormHeight";
#warn "EntryCount * FormHeight: $t1";
#warn "StartTextY - EntryCount * FormHeight: $t2";

		print_report_header();
		
	    print_student_entry(@studentinfo);  
		$page_number++;
		
        $StartFormY -= PDF_DRAW::get_line_delta() * 1.60;

		$EntryCount++;

		if ($EntriesPerPage == $EntryCount) 
		{
	      $EntryCount = 0;
          $currY = $StartTextY;
          $StartFormY = $PageHeight - PDF_DRAW::get_line_delta();
#APPDEBUG::WriteDebugMessage("+++print_report_header");
#APPDEBUG::WriteDebugMessage("currY $currY");

		  print_report_footer();
		  PDF_DRAW::new_page();
		}

	}

	
}

sub print_doc_header
{   
    #PDF_DRAW::doc_header(1029, 836);
#    PDF_DRAW::doc_header(950, 411);

    PDF_DRAW::doc_header($PageWidth, $PageHeight);

	PDF_DRAW::set_formatting(1);

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

sub print_boiler_plate
{
  my $BPcurrY = $StartFormY;

  my $HeaderStart = $BPcurrY;
  my $HeaderSize = 0;

  my $FontSize = PDF_DRAW::get_default_font_size() + 2;

    PDF_DRAW::set_font_size($FontSize); 

    my $TopLineY = $BPcurrY;
    my $BottomLineY = $TopLineY - $FormHeight;
     
    $StartFormY = $BottomLineY - ($FormMargin * 2);

#	$currY = PDF_DRAW::center_text($PageWidth/2, $TopLineY - PDF_DRAW::get_line_delta() + 2, qq{<b>Student Information Verification</b>});  
    $currY = $TopLineY - PDF_DRAW::get_line_delta() + 2;

	PDF_DRAW::center_text($PageWidth/2, $currY, qq{<b>Student Information Verification</b>});  

    my $CourseLabel = $ScheduledCourseInfo->{LogNumber};
    
    if (1 == $ScheduledCourseInfo->{RequireMedicalClearance})
    {
        $CourseLabel .= " Medical Clearance Required"
    }

	PDF_DRAW::text($leftXOffset + ($LeftLabelOffset/2), $currY, $CourseLabel);  
    
    my $NeatnessNote = "Line out errors with single line. Please write neatly.";

    $currY -= PDF_DRAW::get_line_delta();

#    PDF_DRAW::center_text(($FormWidth/4), $currY, "- On File -");
#    $currY = PDF_DRAW::text($FormWidth - PDF_DRAW::string_length($NeatnessNote), $currY, $NeatnessNote);

    PDF_DRAW::text($leftXOffset + 4, $BottomLineY + 4 + PDF_DRAW::get_line_delta() , $NeatnessNote);  

    $currY -= PDF_DRAW::get_line_delta()/2;
  	
    PDF_DRAW::text($leftXOffset + 4, $BottomLineY+4, qq{Student Signature:});  
    PDF_DRAW::text($FormWidth - (20 * $FontSize), $BottomLineY+4, $ReportDate);  #tgs 20151020

#	$currY = $BPcurrY;

    DrawBoldBox($leftXOffset, $TopLineY, $FormWidth, $BottomLineY);
    # Form Border
    #Left
#    PDF_DRAW::draw_line($FormWidth, $TopLineY, $FormWidth, $BottomLineY);  
#    PDF_DRAW::draw_line($FormWidth-1, $TopLineY, $FormWidth-1, $BottomLineY);  
#
#    #Right
#	PDF_DRAW::draw_line($leftXOffset, $TopLineY, $leftXOffset, $BottomLineY);  
#	PDF_DRAW::draw_line($leftXOffset+1, $TopLineY, $leftXOffset+1, $BottomLineY);  
#
#    #Top
#    PDF_DRAW::draw_line($leftXOffset, $TopLineY, $FormWidth, $TopLineY);
#    PDF_DRAW::draw_line($leftXOffset, $TopLineY-1, $FormWidth, $TopLineY-1);
#
#    #Bottom
#	PDF_DRAW::draw_line($leftXOffset, $BottomLineY, $FormWidth, $BottomLineY);
#	PDF_DRAW::draw_line($leftXOffset, $BottomLineY+1, $FormWidth, $BottomLineY+1);

#	PDF_DRAW::text($FormWidth - (12 * $FontSize), $BottomLineY+4, $ReportDate);  

	PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size());
   return;   
}

sub DrawBoldBox
{
  my $LeftX = shift;
  my $LeftY = shift;
  my $RightX = shift;
  my $RightY = shift;

  #Left
  PDF_DRAW::draw_line($LeftX, $LeftY, $LeftX, $RightY);  
  PDF_DRAW::draw_line($LeftX+1, $LeftY, $LeftX+1, $RightY);  

  #Right
  PDF_DRAW::draw_line($RightX, $LeftY, $RightX, $RightY);  
  PDF_DRAW::draw_line($RightX-1, $LeftY, $RightX-1, $RightY);  

  #Top
  PDF_DRAW::draw_line($LeftX, $LeftY, $RightX, $LeftY);
  PDF_DRAW::draw_line($LeftX, $LeftY-1, $RightX, $LeftY-1);

  #Bottom
  PDF_DRAW::draw_line($LeftX, $RightY, $RightX, $RightY);
  PDF_DRAW::draw_line($LeftX, $RightY+1, $RightX, $RightY+1);
  
  return;	
}

sub PrintLine
{
  my $Label = shift;
  my $DefaultText = shift;
  my $FontSize = shift;
#  my $leftXOffset = shift;
  my $leftXOffset = shift;
  my $TextBoxTopX = shift;
  my $TextBoxBottomX = shift;
  my $LabelY = shift;
  my $TextY = shift;
#  my $LineY = shift;
  my $PrintTopLine = shift;
  my $PrintBottomLine = shift;

  # $LeftTextOffset $FormWidth and $LeftLabelOffset are globally defined

    my $OldFontSize = PDF_DRAW::set_font_size($FontSize); 

    if ( 1 == $PrintTopLine )
    {
		   PDF_DRAW::draw_line($TextBoxTopX, $LabelY + PDF_DRAW::get_line_delta() , $FormWidth - ($LeftLabelOffset/2), $LabelY + PDF_DRAW::get_line_delta() );
	#      PDF_DRAW::draw_line($TextBoxTopX, $LabelY - (PDF_DRAW::get_line_delta() / 5), $TextBoxBottomX, $LabelY - (PDF_DRAW::get_line_delta() / 5));
	#      PDF_DRAW::draw_line($TextBoxBottomX, $LabelY - (PDF_DRAW::get_line_delta() / 5), $FormWidth - ($LeftLabelOffset/2), $LabelY - (PDF_DRAW::get_line_delta() / 5));
    }



#	PDF_DRAW::text($RightLabelOffset, $LabelY, $Label );  
	$LabelY = PDF_DRAW::text($leftXOffset + $LeftLabelOffset, $LabelY, $Label );  
	$TextY = PDF_DRAW::text($leftXOffset + $LeftTextOffset, $TextY, "<b>" . $DefaultText . "</b>");  

    if ( 1 == $PrintBottomLine )
    {
	      PDF_DRAW::draw_line($TextBoxTopX, $LabelY - (PDF_DRAW::get_line_delta() / 5) , $FormWidth - ($LeftLabelOffset/2), $LabelY - (PDF_DRAW::get_line_delta() / 5) );
	#      PDF_DRAW::draw_line($TextBoxBottomX, $LabelY - (PDF_DRAW::get_line_delta() / 5), $FormWidth - ($LeftLabelOffset/2), $LabelY - (PDF_DRAW::get_line_delta() / 5));
	#      PDF_DRAW::draw_line($TextBoxTopX, $LabelY - (PDF_DRAW::get_line_delta() / 5), $TextBoxBottomX, $LabelY - (PDF_DRAW::get_line_delta() / 5));
	#      PDF_DRAW::draw_line($TextBoxBottomX, $LabelY - (PDF_DRAW::get_line_delta() / 5), $FormWidth - ($LeftLabelOffset/2), $LabelY - (PDF_DRAW::get_line_delta() / 5));
    }

#    PDF_DRAW::draw_line($TextBoxTopX, $LabelY - (PDF_DRAW::get_line_delta() / 5), $TextBoxBottomX, $LabelY - (PDF_DRAW::get_line_delta() / 5));
#    PDF_DRAW::draw_line($TextBoxBottomX, $LabelY - (PDF_DRAW::get_line_delta() / 5), $FormWidth - ($LeftLabelOffset/2), $LabelY - (PDF_DRAW::get_line_delta() / 5));

	$LabelY = PDF_DRAW::text($leftXOffset + $LeftLabelOffset, $LabelY, "Correction:" );  




  PDF_DRAW::set_font_size($OldFontSize); 

  return ($LabelY, $LabelY); #$TextY	 
}


sub print_student_entry
{
    my ($StudentRecordID, $last_name, $suffix, $first_name, $middle_name, $SSN, $BirthDate, $Address1, $Address2, $City, $State, $PostCode, $Country, $PrimaryPhoneNumber, $SecondaryPhoneNumber, $Email, $AffiliationName, $AffiliationCompanyNumber) = @_;

    my $TextPlaceHolder = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    my $MESSARequiredLabel = "";
    
    my $student_name;
 
    print_boiler_plate();
  
	my $nameString = MFRI_STRINGS::Build_Name($first_name, $middle_name, $last_name, $suffix, 0);


    my $SSN_Numeric = $SSN + 0;
    
    $SSN = STUREG_MAINT::HyphenateSSN($SSN);       

    

    if (length($nameString) == 0) 
    {
	  $nameString = $TextPlaceHolder;
    }

    my $SSN_Error_Number = MFRI_STRINGS::ValidateSSN($SSN);

    if (length($SSN_Numeric) <= 5) 
    {
        $MESSARequiredLabel = " **** Incomplete SSN On File MESSA Form Required ****";
        $nameString .= $MESSARequiredLabel
    }
    elsif ($SSN_Error_Number == 0) 
    {
	  $MESSARequiredLabel = " **** Incorrect SSN On File ****";
	  $nameString .= $MESSARequiredLabel
    }
    elsif ($SSN_Error_Number < 0) 
    {
	  $MESSARequiredLabel = " **** Invalid SSN number On File ****";
	  $nameString .= $MESSARequiredLabel
    }
    elsif ((length($Address1) == 0) && (length($Address2) == 0) && (length($City) == 0) && (length($State) == 0) && (length($PostCode) == 0) )
    {
	  $MESSARequiredLabel = " **** No Address On File MESSA Form Required ****";
	  $nameString .= $MESSARequiredLabel
    }

    if (length($SSN) == 0) 
    {
	  $SSN = $TextPlaceHolder;
    }

    my $StudentAge = 0;
    
    if ((length($BirthDate) == 0) || ($BirthDate eq "00-00-0000"))
    {
	  $BirthDate = $TextPlaceHolder;
    }
    else
    {
	  $StudentAge = MFRI_UTIL::CalculateAge(DATE_UTIL::ReorderDate($BirthDate, "YMD"), $ScheduledCourseInfo->{StartDate});
	
#APPDEBUG::WriteDebugMessage("BirthDate $BirthDate");
#APPDEBUG::WriteDebugMessage("StudenAge $StudentAge");
    }

    if (length($Address1) == 0) 
    {
	  $Address1 = $TextPlaceHolder;
    }

    if (length($Address2) == 0) 
    {
	  $Address2 = $TextPlaceHolder;
    }

    if (length($City) == 0) 
    {
	  $City = $TextPlaceHolder;
    }

    if (length($State) == 0) 
    {
	  $State = $TextPlaceHolder;
    }

    if (length($PostCode) == 0) 
    {
	  $PostCode = $TextPlaceHolder;
    }

    if (length($PrimaryPhoneNumber) == 0) 
    {
	  $PrimaryPhoneNumber = $TextPlaceHolder;
    }

    if (length($SecondaryPhoneNumber) == 0) 
    {
	  $SecondaryPhoneNumber = $TextPlaceHolder;
    }

    if (length($Email) == 0) 
    {
	  $Email = $TextPlaceHolder;
    }

    if ($AffiliationName eq "NULL")
    {
	  $AffiliationName = "";
    }  

    if (length($AffiliationName) > 50)
    {
	   $AffiliationName = substr($AffiliationName, 0, 45) . "...";
    }

    if ($AffiliationCompanyNumber eq "NULL")
    {
	  $AffiliationCompanyNumber = "";
    }  

    $AffiliationName = $AffiliationCompanyNumber . " " . $AffiliationName;

    my $FontSize = PDF_DRAW::get_default_font_size();# + 2;

    my $LabelY = $currY;
    my $TextY = $currY;
    my $ShowCountry = 0;

    my $RightLabelOffset = ($FormWidth / 2);# + $LeftLabelOffset; 

    my $TextBoxTopX = $leftXOffset + ($LeftLabelOffset/2);
    my $TextBoxTopY = $LabelY + PDF_DRAW::get_line_delta() - (PDF_DRAW::get_line_delta() / 5);

    my $TextBoxBottomX = ($FormWidth / 2);

    my $MCX = $leftXOffset + 620;
    my $MCY = $LabelY;

    ($LabelY, $TextY) = PrintLine( "Name ", $nameString, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 1 );

    if (1 == $ScheduledCourseInfo->{RequireMedicalClearance})
    {
        
      if (1 == MFRI_MED::DoesStudentHaveMedicalClearance($StudentRecordID))
      {
         PDF_DRAW::text($MCX, $MCY, "Medical clearance on file.");   
      }
      else
      {
         PDF_DRAW::text($MCX, $MCY, "No current medical clearance on file.");   
      }

    }


    ($LabelY, $TextY) = PrintLine( "SSN ", $SSN, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 1 );

    my $BirthDateMarker = "";
    if (($StudentAge > 0) && ($StudentAge < 18))
    {
	  $BirthDateMarker = "<18";
    }

    ($LabelY, $TextY) = PrintLine( "Birth Date", $BirthDate . " " . $BirthDateMarker, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 1 );

	$LabelY -= PDF_DRAW::get_line_delta();
	$TextY -= PDF_DRAW::get_line_delta();

    ($LabelY, $TextY) = PrintLine( "Address 1", $Address1, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 1, 1 );

    ($LabelY, $TextY) = PrintLine( "Address 2 (Apt)", $Address2, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 1 );

    ($LabelY, $TextY) = PrintLine( "City, State, Zip", $City . " " . $State . " " . $PostCode, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 1 );

    if ((uc(substr($Country, 0, 2)) ne "US" ) && (length($Country) > 0))
    { 
      ($LabelY, $TextY) = PrintLine( "Country", $Country, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 1 );

      $ShowCountry = 1;
	}

	if (0 == $ShowCountry)
	{ 
	  $LabelY -= PDF_DRAW::get_line_delta();
	  $TextY -= PDF_DRAW::get_line_delta();
	}

    my ($PN1LabelY, $PN1TextY) = PrintLine( "Phone Number 1", $PrimaryPhoneNumber, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 1, 1 );


#    ($LabelY, $TextY) = PrintLine( "Phone Number 2", $SecondaryPhoneNumber, $FontSize, $LeftTextOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 1, 0 );
    ($LabelY, $TextY) = PrintLine( "Phone Number 2", $SecondaryPhoneNumber, $FontSize, ($FormWidth / 2), $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 0 );

#    ($LabelY, $TextY) = PrintLine( "Email", $Email, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 0 );
    my ($EMLabelY, $EMTextY) = PrintLine( "Email", $Email, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 0 );

#    ($LabelY, $TextY) = PrintLine( "Affiliation", $AffiliationName, $FontSize, $leftXOffset, $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 0 );
    ($LabelY, $TextY) = PrintLine( "Affiliation", $AffiliationName, $FontSize, ($FormWidth / 2), $TextBoxTopX, $TextBoxBottomX, $LabelY, $TextY, 0, 0 );

    


    $currY = $LabelY;
    my $TextBoxBottomY = $LabelY + PDF_DRAW::get_line_delta() - (PDF_DRAW::get_line_delta() / 4);

	PDF_DRAW::draw_rectangle_coords($TextBoxTopX, $TextBoxTopY, $FormWidth - ($LeftLabelOffset/2), $TextBoxBottomY);
#	PDF_DRAW::draw_rectangle_coords($TextBoxTopX, $TextBoxTopY, $TextBoxBottomX, $TextBoxBottomY);
#	PDF_DRAW::draw_rectangle_coords($TextBoxBottomX, $TextBoxTopY, $FormWidth - ($LeftLabelOffset/2), $TextBoxBottomY);

  return;    
}




