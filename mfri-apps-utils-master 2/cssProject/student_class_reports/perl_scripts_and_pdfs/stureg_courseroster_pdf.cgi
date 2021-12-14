#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use MFRI_UTIL;
use STUREG_MAINT;
use SEMINAR_MAINT;
use Database;
use CGI;
use strict;
use PDF_DRAW;
use POSIX;
use SCHEDULE_MAINT;
use DATE_UTIL;
use MFRI_MED;

use DBK;


#APPDEBUG::WriteDebugMessage("+++++++ print roster");
#Kick the user out if they aren't logged in
if(!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}

my ($CurrentYear, $CurrentMonth, $CurrentDay) = DATE_UTIL::CurrentDate();
my ($CurrentHour, $CurrentMinute, $CurrentSecond) = DATE_UTIL::CurrentTime();

my $ReportDate =  qq{Report Date: } . $CurrentMonth . "-" . $CurrentDay . "-" . $CurrentYear . " " . $CurrentHour . ":" . $CurrentMinute;

#Get the scheduled course ID.
my $ScheduledCourseID = CGI::param( 'SCID' ) || 0;

#Build the query string.
#SSN
#tgs 20050909 changed to MIEMSSNumber #tgs 20050909 changed to StateProviderNumber - was: ID Num.  We dont appear to be using this so I'll retrieve it then blank it out.
my $EncryptKey = qq{""} . DBK::Encrypt_Key() . qq{""};

#AES_DECRYPT(ST.IDNumber, $EncryptKey) AS IDNumber, 
#AES_DECRYPT(ST.StateProviderNumber, $EncryptKey) AS StateProviderNumber,  

#20170405
#20170823
my $Student_Query_String = qq
{
SELECT
ST.ID,
ST.LastName,
ST.Suffix,
ST.FirstName,
LEFT(ST.MiddleName, 1),
ST.PrimaryPhoneNumber,
ST.SecondaryPhoneNumber,
DATE_FORMAT(ST.BirthDate, "%m-%d-%Y") AS BirthDate,
ST.Email,
ST.PrimaryEmail,
ST.SecondaryEmail,
A.miemss_number AS AffiliatedCompanyNumber,
SR.is_web_reg,
SR.owes_course_fee 
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

#Get info about this course
my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($ScheduledCourseID);



#Connect to the database
my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";


my $i = 0;

print_doc_header();

my $ShowLegalQuestionLegend = 0;
my $ShowUnder18Legend = 0;
my $ShowMedicalClearanceLegend = 0;
my $ShowAffiliationVerificationLegend = 0;#20170405

my $FontSizeOffset = PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size() + 4); #12;

my $student_counter = 1;   #The total number of student entries
my $students_on_page_counter = 1;   #The total number of student entries on each page
my $maxEntries = 35;#30;#25;   #27    #The max number of entries to be printed on the current page
my $currEntries = 0;       #The number of entries printed on the current page

my $maxNameLength = 26; #max length for student name
my $maxEmailLength = 40; #max length for student email

my $cellHeight = $FontSizeOffset + ($FontSizeOffset /2); #25;                                  #The height of each cell
my $topY = 760;                                       #The topmost part of the grid
my $cellTopY = 733;                                   #The topmost cell
my $bottomY = $cellTopY - ($cellHeight * $maxEntries);  #The bottom of the cells/report
my $leftX = 7;                                        #The left margin of the report
my $rightX = 1020;                                    #The right margin of the report

my $StudentRowStartY = 720;
my $currY = $StudentRowStartY;

my $StartDateYMD;

#20140804 my $ColumnLeftBorder_left_margin = $leftX;
#20140804 my $ColumnLeftBorder_line_number_right_side = 75;#;50;
#20140804 my $ColumnLeftBorder_name_right_side = 320;#295;#225;
#20140804 my $ColumnLeftBorder_birth_date_right_side = 425;#375;#325;
#20140804 my $ColumnLeftBorder_phone_number_right_side = 525;#470;
#20140804 my $ColumnLeftBorder_email_address_left_side =  960; #725;
#20140804 my $ColumnLeftBorder_affiliation_left_side =  960; 
#20140804 my $ColumnLeftBorder_right_margin =  $rightX; 
#20140804 
#20140804 
#20140804 my $ColumnCenterX0 = $ColumnLeftBorder_left_margin + ($ColumnLeftBorder_line_number_right_side -  $ColumnLeftBorder_left_margin) / 2;
#20140804 my $ColumnCenterX1 = $ColumnLeftBorder_line_number_right_side + ($ColumnLeftBorder_name_right_side -  $ColumnLeftBorder_line_number_right_side) / 2;
#20140804 my $ColumnCenterX2 = $ColumnLeftBorder_name_right_side + ($ColumnLeftBorder_birth_date_right_side -  $ColumnLeftBorder_name_right_side) / 2;
#20140804 my $ColumnCenterX3 = $ColumnLeftBorder_birth_date_right_side + ($ColumnLeftBorder_phone_number_right_side -  $ColumnLeftBorder_birth_date_right_side) / 2;
#20140804 my $ColumnCenterX4 = $ColumnLeftBorder_phone_number_right_side + ($ColumnLeftBorder_email_address_left_side -  $ColumnLeftBorder_phone_number_right_side) / 2;
#20140804 my $ColumnCenterX5 = $ColumnLeftBorder_email_address_left_side + ($ColumnLeftBorder_affiliation_left_side -  $ColumnLeftBorder_email_address_left_side) / 2;
#20140804 my $ColumnCenterX6 = $ColumnLeftBorder_affiliation_left_side + ($ColumnLeftBorder_right_margin -  $ColumnLeftBorder_affiliation_left_side) / 2;


#20140804 my $ColumnCenterX0 = $ColumnLeftBorder_left_margin + ($ColumnLeftBorder_line_number_right_side -  $ColumnLeftBorder_left_margin) / 2;
#20140804 my $ColumnCenterX1 = $ColumnLeftBorder_line_number_right_side + ($ColumnLeftBorder_name_right_side -  $ColumnLeftBorder_line_number_right_side) / 2;
#20140804 my $ColumnCenterX2 = $ColumnLeftBorder_name_right_side + ($ColumnLeftBorder_birth_date_right_side -  $ColumnLeftBorder_name_right_side) / 2;
#20140804 my $ColumnCenterX3 = $ColumnLeftBorder_birth_date_right_side + ($ColumnLeftBorder_phone_number_right_side -  $ColumnLeftBorder_birth_date_right_side) / 2;
#20140804 my $ColumnCenterX4 = $ColumnLeftBorder_phone_number_right_side + ($ColumnLeftBorder_email_address_left_side -  $ColumnLeftBorder_phone_number_right_side) / 2;
#20140804 my $ColumnCenterX5 = $ColumnLeftBorder_email_address_left_side + ($ColumnLeftBorder_affiliation_left_side -  $ColumnLeftBorder_email_address_left_side) / 2;
#20140804 my $ColumnCenterX6 = $ColumnLeftBorder_affiliation_left_side + ($ColumnLeftBorder_right_margin -  $ColumnLeftBorder_affiliation_left_side) / 2;



my $ColumnLeftBorder_left_margin = $leftX;
my $ColumnLeftBorder_line_number_right_side  = 75;
my $ColumnLeftBorder_name_right_side         = 375; #320;
#my $ColumnLeftBorder_birth_date_right_side   = 525;#425;
my $ColumnLeftBorder_phone_number_right_side = 480; #425; #525;
my $ColumnLeftBorder_email_address_left_side = 960;
my $ColumnLeftBorder_affiliation_left_side   = 960; 
my $ColumnLeftBorder_right_margin            = $rightX; 


my $ColumnCenterX0 = $ColumnLeftBorder_left_margin + ($ColumnLeftBorder_line_number_right_side -  $ColumnLeftBorder_left_margin) / 2;
my $ColumnCenterX1 = $ColumnLeftBorder_line_number_right_side + ($ColumnLeftBorder_name_right_side -  $ColumnLeftBorder_line_number_right_side) / 2;
my $ColumnCenterX2 = $ColumnLeftBorder_name_right_side + ($ColumnLeftBorder_phone_number_right_side -  $ColumnLeftBorder_name_right_side) / 2;
my $ColumnCenterX3 = $ColumnLeftBorder_phone_number_right_side + ($ColumnLeftBorder_email_address_left_side -  $ColumnLeftBorder_phone_number_right_side) / 2;
my $ColumnCenterX4 = $ColumnLeftBorder_email_address_left_side + ($ColumnLeftBorder_affiliation_left_side -  $ColumnLeftBorder_email_address_left_side) / 2;
my $ColumnCenterX5 = $ColumnLeftBorder_affiliation_left_side + ($ColumnLeftBorder_right_margin -  $ColumnLeftBorder_affiliation_left_side) / 2;


#Print the document

my $page_number = 1;
my $page_count = 0;
print_roster();
print_doc_footer();
$db->finish(); #03-11-2005 WPL Added DB Finish

my $NumberOfRows;

sub print_roster
{
    if ($need_to_query eq "YES") 
    {
	$db->query( $Student_Query_String );	

	$need_to_query = "NO";
    }

	$NumberOfRows = $db->num_rows();

    #Calculate the number of pages that we will use
    $page_count = POSIX::ceil($NumberOfRows / $maxEntries);

    if ($page_count == 0)
    {
      $page_count = 1;
    }

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
	  	    print_roster_footer($currY); #Print a page footer
	  	    PDF_DRAW::new_page();  #Start a new page
	  	    $ShowLegalQuestionLegend = 0;
	  	    $ShowUnder18Legend = 0;
	  	    $ShowMedicalClearanceLegend = 0;
	  	    $ShowAffiliationVerificationLegend = 0;#20170405
	  	    $students_on_page_counter = 1;
             #APPDEBUG::WriteDebugMessage("------- new page");		
	  	    $currY = $StudentRowStartY;
	  	    $page_number++;        #Increment the page counter
	  	    print_roster_header(); #Print a page header
	  	    $currEntries = 0;
	      }
	      
	      $currY = print_student_entry($currY, @studentroster);    
	      $student_counter++;
	      $students_on_page_counter++;
	      $currEntries++;	    	    
	  }

    }

#APPDEBUG::WriteDebugMessage("finish page with blank entries");		
    #Fill out the rest of the page with empty entries
    while (($currEntries > 0) && ($currEntries < $maxEntries))
    {
	  $currY = print_student_entry($currY);
	  $student_counter++;
	  $students_on_page_counter++;
	  $currEntries++;
    }

    print_roster_footer($currY);
    
}

#Used to setup our page for printing PDF documents
sub print_doc_header
{
    PDF_DRAW::doc_header(1029, 836);
    PDF_DRAW::set_formatting(1); #Turn on formatting so we can use tags (optional)
    PDF_DRAW::set_font("Times-Roman"); #Set the font (optional)
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+ 4); #Set the font size (optional)
}

#Ends the pdf document and prints it to the screen
sub print_doc_footer
{
   PDF_DRAW::doc_footer();
}


sub segment_title_string
{
    my $str = shift;
    my $max_len = shift;
    my $offset = 0;
    my $size;
    my $index = 0;
    my $indexW = 0;
    my @result;
    my $PriorWord = "";
    my $len = length($str);
    my @brLines;
	my $brLine;
	my $word;

	my $subword;
    my $LastIndex;
    
    $max_len = $max_len + 200;
    
    if (PDF_DRAW::get_formatting() == 1)
    {
	  @brLines = split(/<br>/, $str);
    }
    else
    {
	  @brLines[0] = $str;
    }

    foreach $brLine (@brLines)
    {

	  my @words = split(/\s+/, $brLine);
	
	  foreach $word (@words)
	  {
	    if (PDF_DRAW::string_length($result[$index].$PriorWord.$word) < $max_len)
	    {
		  if (length($PriorWord) > 0)
		  {
		    $result[$index] .= $PriorWord . " ";
		  }
		  
		  $PriorWord = $word;
	    }
	    else #Otherwise, start a new line
	    {
		  $LastIndex = $index;

		  $index++;		
		  
		  if (length($PriorWord) > 0)
		  {
            if (length($word) > 2)
		    {
		      $result[$LastIndex] .= $PriorWord . " ";
			  $PriorWord = "";
		    } 
            else
		    {
 	          $result[$index] .= $PriorWord . " ";
		      $PriorWord = "";
            }
            
		  }
		  else
		  {
		    if (length($word) < 4)
		    {
		      $index--;
		    }
		  }
		  
		  #If the whole word fits on this new line put it there.
		  if (PDF_DRAW::string_length($word) < $max_len)
		  {
		    $result[$index] .= $word . " ";
		  }
		  else #Otherwise, split it over many lines.
		  {
		    my @newLines = PDF_DRAW::split_word($word, $max_len);
		    
		    foreach $subword (@newLines)
		    {
			  #Start a new line
			  $result[$index++] .= $subword . " ";
			  #warn "new line";
		    }
		  }
	    }


	  }

	  #Start a new line
	  $LastIndex = $index;
	  $index++;
    }

    if (length($PriorWord) > 0)
	{
	  $result[$LastIndex] .= $PriorWord;
	}
    return @result;
}


#A header printed at the start of EACH PAGE
sub print_roster_header
{
    my $CourseCode = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 1);
    my $instName = $ScheduleInfo->{InstructorName};
    my $location = $ScheduleInfo->{LocationName};
    my $course_title = $ScheduleInfo->{Title};
    my $StartDate = DATE_UTIL::ReorderDate($ScheduleInfo->{StartDate}, "MDY");
    $StartDateYMD = $ScheduleInfo->{StartDate};
        
    my $pagenum = get_page_num();
    my $i;
    my $currX;
    my $currY;
    
    my $InstructorData;
    my $InstructorUID = "";

    my $HeaderColumn1X = 8;
    my $HeaderColumn2X = 500;
    my $HeaderColumn3X = 760;
    my $HeaderColumn4X = 954;
    
    my $TitleLength = 500; #600
    my $LocationLength = 400;

    if ($ScheduleInfo->{InstructorID} > 0)
    {
      $InstructorData = MFRI_UTIL::GetStaff($ScheduleInfo->{InstructorID}, "", 0);

	  if ( defined $InstructorData)
	  {
 	    $InstructorUID = $InstructorData->{UniversityIDNumber};
	  }
    }

    if (($instName eq "MFRI Instructor") || ($instName eq "MFRI Staff"))
    {
      $instName = "";
      $InstructorUID = "";
    }

    if ($location eq "TBD - To be determined")
    {
	  $location = "";
    }

    my $OldFontSize = PDF_DRAW::set_font_size($FontSizeOffset + 10);

    my $Calculated_title_length = PDF_DRAW::string_length($course_title);
    
    my $FontSizeHold = $FontSizeOffset + 10;
	
    if (($Calculated_title_length > $TitleLength) && ($Calculated_title_length <= ($TitleLength + 200)))
    {
  	  $FontSizeHold = PDF_DRAW::set_font_size($FontSizeOffset + 4);
    }
 #warn "1 calculated title length: " . PDF_DRAW::string_length($course_title) . "\n";
 #warn "max title length: " . $TitleLength . "\n";

    my @cNameSeg = segment_title_string($course_title, $TitleLength);
#    my @cNameSeg = PDF_DRAW::segment_string($course_title, $TitleLength);
    
	my $CourseNameLines = @cNameSeg; 


    if ($CourseNameLines > 3)
    {
	  $FontSizeHold = PDF_DRAW::set_font_size($FontSizeOffset - 4);
    }
    elsif ($CourseNameLines > 1)
    {
	  $FontSizeHold = PDF_DRAW::set_font_size($FontSizeOffset );
    }
#    elsif ($CourseNameLines > 1)
#    {
#	  $FontSizeHold = PDF_DRAW::set_font_size($FontSizeOffset + 4);
#    }
   #warn "2 calculated title length: " . PDF_DRAW::string_length($course_title) . "\n";

    my $TitleY = 814;
    my $i;
    for ($i = 0; $i < $CourseNameLines; $i++)
    {
	  $TitleY = PDF_DRAW::text($HeaderColumn1X, $TitleY, $cNameSeg[$i]);
	  $TitleY += 3; #leading adjustment for font
    }
    
    PDF_DRAW::set_font_size($FontSizeHold);
#PDF_DRAW::text($courseX, $TitleY - (8 * $i), $cNameSeg[$i]);
    
    
    PDF_DRAW::text($HeaderColumn1X, 769, "Course Roster");
    
    PDF_DRAW::set_font_size($OldFontSize + 2);
    PDF_DRAW::text($HeaderColumn2X, 814, "Course \#: $CourseCode");

    if (1 == $ScheduleInfo->{RequireMedicalClearance})
    {
      my $MCRFontSizeHold = PDF_DRAW::set_font_size($OldFontSize - 2);
      $TitleY = PDF_DRAW::text($HeaderColumn3X, 814, "Medical Clearance Required");
      PDF_DRAW::set_font_size($MCRFontSizeHold);    
    }

    PDF_DRAW::text($HeaderColumn2X, 800, "Start Date: $StartDate");

    if (length($instName) > 0)
    {
	  PDF_DRAW::text($HeaderColumn2X, 784, "Primary Instructor: $instName UID: $InstructorUID");
    }
    else
    {
      PDF_DRAW::text($HeaderColumn2X, 784, "Primary Instructor: ");
    }

######

    #my @cLocationSeg = PDF_DRAW::segment_string($location, $LocationLength);
    
    #my $CourseLocationLines = @cLocationSeg; 

    my $LocationY = 769;
    PDF_DRAW::text($HeaderColumn2X, $LocationY, "Location: ");
    
    if (length($location) >= 48)
    {
        $FontSizeHold = PDF_DRAW::set_font_size($FontSizeOffset);
    }
    
    $LocationY = PDF_DRAW::text($HeaderColumn2X + 75, $LocationY, $location);
    
    
    PDF_DRAW::set_font_size($FontSizeHold);


######

#    PDF_DRAW::text($HeaderColumn2X, 773, "Location: $location");
	
    PDF_DRAW::set_font_size($OldFontSize );
#    PDF_DRAW::center_text($ColumnCenterX0, 742, "INIT");
    PDF_DRAW::center_text($ColumnCenterX1, 742, "Name");
    #20140804 PDF_DRAW::center_text($ColumnCenterX2, 742, "Birth Date");
    PDF_DRAW::center_text($ColumnCenterX2, 742, "Phone");
    PDF_DRAW::center_text($ColumnCenterX3, 742, "Email Address");
    #PDF_DRAW::center_text($ColumnCenterX5, 742, "City, State, Zip");
    PDF_DRAW::set_font_size($OldFontSize - 2);
    PDF_DRAW::center_text($ColumnCenterX5, 742, "Affiliation");
    PDF_DRAW::set_font_size($OldFontSize);

    my $LineBottomY = 736 - (PDF_DRAW::get_line_delta() / 5);

    PDF_DRAW::draw_line($leftX, $topY, $rightX, $topY); #horizontal line above header

    print_column_separators($topY, $LineBottomY);



    PDF_DRAW::draw_line($rightX, $topY, $rightX, $LineBottomY); #Last vertical Line

    PDF_DRAW::draw_line($leftX, $LineBottomY , $rightX, $LineBottomY ); #horizontal line below header

    PDF_DRAW::set_font_size($OldFontSize - 2);
    PDF_DRAW::text($HeaderColumn4X, 820, "Page $page_number of $page_count");

    
    PDF_DRAW::set_font_size($OldFontSize);
}

sub print_column_separators
{
#  my $currY = shift;	
  my $topY = shift;
  my $bottomY = shift;

#  my $topY = $currY + PDF_DRAW::get_line_delta();
#  my $bottomY = $currY - 2;
	
  PDF_DRAW::draw_line($leftX, $topY, $leftX, $bottomY); #Left Line
	
  PDF_DRAW::draw_line($ColumnLeftBorder_line_number_right_side, $topY, $ColumnLeftBorder_line_number_right_side, $bottomY);         #name left
  PDF_DRAW::draw_line($ColumnLeftBorder_name_right_side, $topY, $ColumnLeftBorder_name_right_side, $bottomY);       #birthdate left
#  PDF_DRAW::draw_line($ColumnLeftBorder_birth_date_right_side, $topY, $ColumnLeftBorder_birth_date_right_side, $bottomY);       #phone left
  PDF_DRAW::draw_line($ColumnLeftBorder_phone_number_right_side, $topY, $ColumnLeftBorder_phone_number_right_side, $bottomY);       #address1 left

  PDF_DRAW::draw_line($ColumnLeftBorder_affiliation_left_side, $topY, $ColumnLeftBorder_affiliation_left_side, $bottomY);       #affiliation

  PDF_DRAW::draw_line($rightX, $topY, $rightX, $bottomY); #Last Line
	
  return;	
}


#A footer printed at the bottom of EACH PAGE   
sub print_roster_footer
{
  my $currY = shift;
    #It's easier to draw all the lines of the form at the end of each page.
    #This way, we already know how many entries to account for.


    my $LineCunter = 0;
    if ((1 == $ScheduleInfo->{RequireMedicalClearance}) && (1 == $ShowMedicalClearanceLegend))
    {
        PDF_DRAW::text($leftX, $currY - PDF_DRAW::get_line_delta() , "MC = Student has Medical Clearance on file");
        $LineCunter += 1;
    }
    
    if (1 == $ShowLegalQuestionLegend)
    {
        PDF_DRAW::text($leftX, $currY - (PDF_DRAW::get_line_delta() * (1 + $LineCunter)), "L = Student Has Indicated 'Yes' for one of the legal questions on the MESSA form. 1,2,3 indicates which question.");
        $LineCunter += 1;
    }
    
    if (1 == $ShowUnder18Legend)
    {
        PDF_DRAW::text($leftX, $currY - (PDF_DRAW::get_line_delta() * (1 + $LineCunter)), "<18 = Student under 18");
        $LineCunter += 1;
    }
    
    if (1 == $ShowAffiliationVerificationLegend)#20170405
    {#20170405
        PDF_DRAW::text($leftX, $currY - (PDF_DRAW::get_line_delta() * (1 + $LineCunter)), "AV = Student must complete Affiliation Verification form");#20170405
        $LineCunter += 1;#20170405
    }#20170405

	PDF_DRAW::text($leftX, $currY - (PDF_DRAW::get_line_delta() * (1 + $LineCunter)) , $ReportDate);  

}


sub PrintLine
{
	my $currY = shift;
	my $LineNumber = shift;	
	my $LineNumberText = shift;	
	my $Name = shift;
	my $BirthDate = shift;
	my $PrimaryPhoneNumber = shift;
	my $SecondaryPhoneNumber = shift;
	my $Email = shift;
	my $PrimaryEmail = shift;
	my $SecondaryEmail = shift;
#	my $Address1 = shift;#
#	my $Address2 = shift;
#	my $CityStateZip = shift;
	my $Affiliation = shift;
    my $is_web_reg = shift;#20170405
    my $owes_course_fee = shift;#20170823
    
    my $LineY = $currY;

    my $TextXOffset = 5;

    my $OldFontSize = PDF_DRAW::set_font_size($FontSizeOffset); # - 1 

    my $LineYOffset = (PDF_DRAW::get_line_delta() / 5);

    warn "PrintLine Name $Name Affiliation $Affiliation\n";

#    if ($Affiliation eq "NANONE") #NANONE means there is no affiliation listed for this student.
#    {
#        $Affiliation = "";
#    }
    

#    if ($currY == $StudentRowStartY)
    if (0 == $currEntries )
    {
      PDF_DRAW::draw_line($leftX, $currY - $LineYOffset , $rightX, $currY - $LineYOffset );
    }
    elsif ($student_counter > $NumberOfRows)
    {
      PDF_DRAW::draw_line($leftX, $currY - $LineYOffset , $rightX, $currY - $LineYOffset );
    } 

    my $CurrentLineY = $currY;
    $currY = PDF_DRAW::text($ColumnLeftBorder_left_margin + $TextXOffset, $CurrentLineY, $LineNumber);  
    
    my $FontSizeHold;
	if (length($LineNumberText) > 6)
	{
    	if (length($LineNumberText) >= 10)#20170405
    	{
    	  $FontSizeHold = PDF_DRAW::set_font_size($OldFontSize - 6);
    	}
    	else
    	{
    	  $FontSizeHold = PDF_DRAW::set_font_size($OldFontSize - 3);
    	}
	}


    PDF_DRAW::text($ColumnLeftBorder_left_margin + $TextXOffset + (8 * length($LineNumber)), $CurrentLineY, $LineNumberText);  

    if (length($LineNumberText) > 6)
    {
      PDF_DRAW::set_font_size($FontSizeHold);
    }

    my $ShrinkFont = 0;
#    my $Calculated_name_length1 = PDF_DRAW::string_length($Name);

    my $columndifference = ($ColumnLeftBorder_name_right_side - $ColumnLeftBorder_line_number_right_side) - $TextXOffset;

#    my $Calculated_name_length2 = PDF_DRAW::string_length($Name, PDF_DRAW::get_font(), ($OldFontSize - 4));
    my $Calculated_length = PDF_DRAW::string_length($Name);

    my $new_font_size = PDF_DRAW::get_font_size();
    my $ShrinkFont = 0;
    
    while (($Calculated_length > $columndifference) && ($new_font_size > 4))
    {
        $Calculated_length = PDF_DRAW::string_length($Name, PDF_DRAW::get_font(), $new_font_size);
        $new_font_size--;
        $ShrinkFont = 1;
    }

#    my $str = shift;
#    my $font = shift;
#    my $font_size = shift;
    
    
#warn "name: " . $Name . "max length = " . $maxNameLength . " calculated name legnth 1 = " . $Calculated_name_length1 . " calculated name legnth = " . $Calculated_name_length . " simple length = " . length($Name) . "\n";
#warn "name: " . $Name . "max length = " . $maxNameLength . " new font size = " . $new_font_size . " calculated name legnth = " . $Calculated_name_length . " simple length = " . length($Name) . "\n";
#warn "difference between columns $ColumnLeftBorder_name_right_side - $ColumnLeftBorder_line_number_right_side - $TextXOffset = " . $columndifference . "\n";
    #$ShrinkFont = (($Name =~ /\.\.\./) || (length($Name) > ($maxNameLength + 8)));
    
    if (1 == $ShrinkFont)
    {
        $FontSizeHold = PDF_DRAW::set_font_size($new_font_size);
    }
    #####if (1 == $ShrinkFont)
    #####{
  	#####  $FontSizeHold = PDF_DRAW::set_font_size($OldFontSize - 4);
  	#####  if (length($Name) > ($maxNameLength + 10))
  	#####  {
    #####  	  PDF_DRAW::set_font_size($OldFontSize - 5);
  	#####  }
    #####}
    
    PDF_DRAW::text($ColumnLeftBorder_line_number_right_side + $TextXOffset, $CurrentLineY, $Name); #55

    if (1 == $ShrinkFont)
    {
      PDF_DRAW::set_font_size($FontSizeHold);
    }

#20140804    PDF_DRAW::text($ColumnLeftBorder_name_right_side + $TextXOffset, $CurrentLineY, $BirthDate);  #140
    PDF_DRAW::text($ColumnLeftBorder_name_right_side + $TextXOffset, $CurrentLineY, $PrimaryPhoneNumber); #230

#        if (length($Address2) > 0)
#        {
#	      $Address1 .= ", " . $Address2;
#        }
        my $AllEmailAddresses = "";
        
        if (length($Email) > 0)
        {
          if (length($AllEmailAddresses) > 0)
          {
            $AllEmailAddresses .= " , ";
          }
	      $AllEmailAddresses .=  $Email;
        }

        if ((length($PrimaryEmail) > 0) && ($PrimaryEmail ne $Email) && (length($AllEmailAddresses) < $maxEmailLength))
        {
          if (length($AllEmailAddresses) > 0)
          {
            $AllEmailAddresses .= " , ";
          }
	      $AllEmailAddresses .=  $PrimaryEmail;
        }

        if ((length($SecondaryEmail) > 0) && ($SecondaryEmail ne $Email) && ($PrimaryEmail ne $SecondaryEmail) && (length($AllEmailAddresses) < $maxEmailLength))
        {
          if (length($AllEmailAddresses) > 0)
          {
            $AllEmailAddresses .= " , ";
          }
	      $AllEmailAddresses .= $SecondaryEmail;
        }

        $columndifference = ($ColumnLeftBorder_email_address_left_side - $ColumnLeftBorder_phone_number_right_side) - $TextXOffset;
        
        $Calculated_length = PDF_DRAW::string_length($AllEmailAddresses);
        
        $new_font_size = PDF_DRAW::get_font_size();
        $ShrinkFont = 0;
        
        while (($Calculated_length > $columndifference) && ($new_font_size > 0))
        {
            $Calculated_length = PDF_DRAW::string_length($AllEmailAddresses, PDF_DRAW::get_font(), $new_font_size);
            $new_font_size--;
            $ShrinkFont = 1;
        }

        if (1 == $ShrinkFont)
        {
            $FontSizeHold = PDF_DRAW::set_font_size($new_font_size);
        }

        #if (length($AllEmailAddresses) > $maxEmailLength)
        #{
      	#  $FontSizeHold = PDF_DRAW::set_font_size($OldFontSize - 4);
      	#  if (length($AllEmailAddresses) > ($maxEmailLength + 20))
      	#  {
        #  	  PDF_DRAW::set_font_size($OldFontSize - 8);
      	#  }
        #}

	    PDF_DRAW::text($ColumnLeftBorder_phone_number_right_side + $TextXOffset, $CurrentLineY, $AllEmailAddresses); #540
	    
	    if (1 == $ShrinkFont)
        {
          PDF_DRAW::set_font_size($FontSizeHold);
        }
        
        #if (length($AllEmailAddresses) > $maxEmailLength)
        #{
        #  PDF_DRAW::set_font_size($FontSizeHold);
        #}
        
#	    PDF_DRAW::text($ColumnLeftBorder_phone_number_right_side + $TextXOffset, $CurrentLineY, $Address1); #540

#	    PDF_DRAW::text($ColumnLeftBorder_email_address_left_side + $TextXOffset, $CurrentLineY, $CityStateZip); #890

        print_column_separators(($CurrentLineY + PDF_DRAW::get_line_delta()), ($CurrentLineY - 2));

        $columndifference = ($ColumnLeftBorder_right_margin - $ColumnLeftBorder_affiliation_left_side) - $TextXOffset;
        
        $Calculated_length = PDF_DRAW::string_length($Affiliation);
        
        $new_font_size = PDF_DRAW::get_font_size();
        $ShrinkFont = 0;
        


        while (($Calculated_length > $columndifference) && ($new_font_size > 0))
        {
            $Calculated_length = PDF_DRAW::string_length($Affiliation, PDF_DRAW::get_font(), $new_font_size);
            $new_font_size--;
            $ShrinkFont = 1;
        }

        if (1 == $ShrinkFont)
        {
            $FontSizeHold = PDF_DRAW::set_font_size($new_font_size);
        }


	    PDF_DRAW::text($ColumnLeftBorder_affiliation_left_side + $TextXOffset, $CurrentLineY, $Affiliation); #993

	    if (1 == $ShrinkFont)
        {
          PDF_DRAW::set_font_size($FontSizeHold);
        }

	    if ( ($students_on_page_counter < $maxEntries) && ($student_counter < $NumberOfRows) )
	    {
	      PDF_DRAW::draw_line($leftX, $currY - $LineYOffset , $rightX, $currY - $LineYOffset );
	    } 
	    elsif (($students_on_page_counter < $maxEntries) && (length($Name) < 1))
	    {
	      PDF_DRAW::draw_line($leftX, $currY - $LineYOffset , $rightX, $currY - $LineYOffset );
	    } 

	    PDF_DRAW::set_font_size($OldFontSize);


	   return $currY


}


#Print a single student entry
sub print_student_entry
{
	my $currY = shift;
	my $StudentRecordID = shift;
	my $last_name = shift;
	my $suffix = shift;
	my $first_name = shift;
	my $MI = shift;
	my $PrimaryPhoneNumber = shift;
	my $SecondaryPhoneNumber = shift;
	my $DOB = shift;
	my $Email = shift;
    my $PrimaryEmail = shift;
    my $SecondaryEmail = shift;
#	my $street = shift;
#	my $apt = shift;
#	my $city = shift;
#	my $state = shift;
#	my $zip = shift;
	my $COMP = shift;
    my $is_web_reg = shift;#20170405
    my $owes_course_fee = shift;#20170823


###    my $LineY = $currY;

#APPDEBUG::WriteDebugMessage("1 currY $currY");
    $MI = substr($MI, 0, 1);
    my $pagenum = get_page_num();
	
	
	if ((not defined $StudentRecordID) || ($StudentRecordID < 1))
	{
      $currY = PrintLine($currY, $student_counter, "", "", "", "", "", "", "", "", "" ); 
		
	  return $currY;	
	}
	

    my ($LegalQuestionReturnCode, $LegalQuestion1, $LegalQuestion2, $LegalQuestion3) = MFRI_UTIL::GetStudentRegistrationLegalQuestionAnswers($ScheduledCourseID, $StudentRecordID);


    my $LegalQuestionFlag = "";
    if ($LegalQuestionReturnCode > 0 )
    {
	  $LegalQuestionFlag = "L";
	
	  if (1 == $LegalQuestion1)
	  {
	    $ShowLegalQuestionLegend = 1;
		$LegalQuestionFlag .= "1";
	  }
	 
	  if (1 == $LegalQuestion2)
	  {
  	    $ShowLegalQuestionLegend = 1;
		$LegalQuestionFlag .= "2";
	  }
	 
	  if (1 == $LegalQuestion3)
	  {
  	    $ShowLegalQuestionLegend = 1;
		$LegalQuestionFlag .= "3";
	  }
	 
    }

    my $StudentAge = 0;
    my $BirthDateFlag = "";
    my $BirthDateMarker = "";
 
    if ($DOB ne "00-00-0000")
    {
  	  #warn "\n*** $last_name\n";
	  $StudentAge = MFRI_UTIL::CalculateAge(DATE_UTIL::ReorderDate($DOB, "YMD"), $StartDateYMD);
      #warn "birthdate: " . DATE_UTIL::ReorderDate($DOB, "YMD") . "\n";
      #warn "age: $StudentAge\n";
      
      if (($StudentAge > 0) && ($StudentAge < 18))
      {
        $ShowUnder18Legend  = 1;
	    $BirthDateMarker = "<18";
      }

      $DOB .= " " . $BirthDateMarker; #. "(" . $StudentAge . ")"

    }
    else
    {
	  $DOB = "";
    }
	
    #my $LineNumberText = $student_counter . " " .  $LegalQuestionFlag . " ". $BirthDateMarker; #$BirthDateMarker
    my $LineNumberText = $LegalQuestionFlag . " ". $BirthDateMarker; #$BirthDateMarker
    
    if (1 == $ScheduleInfo->{RequireMedicalClearance})
    {
      my $StudentHasMedicalClearance = MFRI_MED::DoesStudentHaveMedicalClearance($StudentRecordID);
      
      if (1 == $StudentHasMedicalClearance)
      {
          $ShowMedicalClearanceLegend = 1;
          $LineNumberText .= " MC";
      }
    }
    
    if (0 == $is_web_reg)#20170405
    {#20170405
        $ShowAffiliationVerificationLegend = 1;#20170405
        $LineNumberText .= " AV";#20170405
    }#20170405
    
    #20170823+
    if (1 == $ScheduleInfo->{require_payment})
    {
        if (1 == $owes_course_fee)
        {
            $ShowAffiliationVerificationLegend = 1;
            $LineNumberText .= " FEE";
        }
    }
    #20170823-

	my $StudentName = MFRI_STRINGS::Build_Name($first_name, $MI, $last_name, $suffix, 1, ($maxNameLength > 0), $maxNameLength, 1);#20190418

    warn "print_student_entry StudentName $StudentName COMP $COMP\n";
#    $currY = PrintLine($currY, $LineNumberText, $StudentName, $DOB, $PrimaryPhoneNumber, $SecondaryPhoneNumber, $street, $apt, $city . " " . $state . " " . $zip, $COMP ); 
    $currY = PrintLine($currY, $student_counter, $LineNumberText, $StudentName, $DOB, $PrimaryPhoneNumber, $SecondaryPhoneNumber, $Email, $PrimaryEmail, $SecondaryEmail, $COMP, $is_web_reg, $owes_course_fee ); #20170405 #20170823


   return $currY
}

#Get the current page number
sub get_page_num
{
    return $page_number;
}

