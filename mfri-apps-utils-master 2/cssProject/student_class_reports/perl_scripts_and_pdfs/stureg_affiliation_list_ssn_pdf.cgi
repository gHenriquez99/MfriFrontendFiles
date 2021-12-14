#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use Database;
use CGI;
use strict;
use PDF_DRAW;
use SCHEDULE_MAINT;
use DATE_UTIL;
use STUREG_MAINT;

use DBK;

#use APPDEBUG;

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

#Check the user's permissions...
my $UserID = MFRI::get_current_userid();
#my ($IDReadPermission, $IDWritePermission) = TRANS_PREFS::Get_UserPermissionsID($UserID);
my $IDReadPermission = 1;

if ($IDReadPermission == 0)
{
    MFRI::set_parameter("error", "You do not have permission to access this feature.");
      MFRI::redirect("error.cgi");
}

my $SCID = CGI::param('SCID') || 0;
my $orderBySSN = CGI::param('OBS') || 0;

if ($orderBySSN != 0)
{
  $orderBySSN = 1;
}

if ($SCID <= 0)
{
    MFRI::set_parameter("error", "You must specify a course to print this letter for.");
      MFRI::redirect("error.cgi");
}


my $logNum;
my $locationName;
my $courseTitle;
my $instructorName;
my $startDate;
my $endDate;
my $topY = 1010;
my $currY = $topY;
my $leftX = 30;
my $pageNum = 1;
my $maxLinesPage = 70;
my $minYPage = $topY - $maxLinesPage * PDF_DRAW::get_line_delta();
my @affilGroup;

my $RecordCounter = 0;
my $CompanyRecordCounter = 0;
my $NeedExtraLineAfterHeader = 0;
my $CountInCompany = 0;

#tgs 20050923 my $EncryptKey = qq{"} . TRANS_MAINT::Encrypt_Key() . qq{"};
my $orderBy = qq
{SRec.LastName, SRec.FirstName, SRec.MiddleName, SRec.Suffix };

if ($orderBySSN == 1)
{
#tgs 20050923   $orderBy = "AES_DECRYPT(SRec.SSN, $EncryptKey)";
  $orderBy = "SRec.SSN";
}

#warn "SCID $SCID";

#tgs 20050923 my $CourseQueryString = qq{SELECT Title, InstructorName, LocationName, DATE_FORMAT(StartDate, '%m/%d/%y'), DATE_FORMAT(EndDate, '%m/%d/%y'), LogNumber FROM ScheduledCoursees WHERE (ID = $SCID)};
my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($SCID);

#tgs 20050923 $db->query($CourseQueryString);

#tgs 20050923 if ($db->num_rows() < 1)
#tgs 20050923 {
#tgs 20050923     $db->finish();
#tgs 20050923     MFRI::set_parameter("error", "Unable to get information about this class.");
#tgs 20050923     MFRI::redirect("error.cgi");
#tgs 20050923 }

#tgs 20050923my @resultRow = $db->get_row();
#tgs 20050923$courseTitle = $resultRow[0];
#tgs 20050923$instructorName = $resultRow[1];
#tgs 20050923$locationName = $resultRow[2];
#tgs 20050923$startDate = $resultRow[3];
#tgs 20050923$endDate = $resultRow[4];
#tgs 20050923$logNum = $resultRow[5];

$courseTitle = MFRI_STRINGS::UnHTMLize_String($ScheduleInfo->{Title});
$instructorName = $ScheduleInfo->{InstructorName};
$locationName = $ScheduleInfo->{LocationName};
$startDate = $ScheduleInfo->{StartDate};
$endDate = $ScheduleInfo->{EndDate};

my ($courseTitleString1, $courseTitleString2) = MFRI_STRINGS::Split_String_At_Word( $courseTitle, 75);
my ($courseTitleString2, $courseTitleString3) = MFRI_STRINGS::Split_String_At_Word( $courseTitleString2, 75);	

$instructorName = "" if (($instructorName eq "MFRI Instructor") || ($instructorName eq "MFRI Staff"));

$locationName = "" if ($locationName eq "TBD - To be determined");


my $DefaultYearVal; 
my $DefaultMonthVal; 
my $DefaultDayVal; 
my $rest;

($DefaultYearVal, $DefaultMonthVal, $DefaultDayVal, $rest) = ($startDate =~ /(\d+)-(\d+)-(\d+)/);
$startDate = ($DefaultMonthVal + 0) . "/" . ($DefaultDayVal + 0) . "/" . $DefaultYearVal;

($DefaultYearVal, $DefaultMonthVal, $DefaultDayVal, $rest) = ($endDate =~ /(\d+)-(\d+)-(\d+)/);
$endDate = ($DefaultMonthVal + 0) . "/" . ($DefaultDayVal + 0) . "/" . $DefaultYearVal;

my $CourseCode    = $ScheduleInfo->{CourseCode};
my $OldLogNumber = $ScheduleInfo->{LogNumber};
my $MIEMSSLogNumber = $ScheduleInfo->{MIEMSSLogNumber};
  
my $Category = $ScheduleInfo->{Category};
my $Level = $ScheduleInfo->{Level};
my $FundingSourceCode = $ScheduleInfo->{FundingSourceCode};
my $SectionNumber = $ScheduleInfo->{SectionNumber};
my $FiscalYear = $ScheduleInfo->{FiscalYear};


#if (length($MIEMSSLogNumber) == 0)
#{
  if (length($Category) > 0)
  {
    $logNum = $Category . "-" . $Level . "-" . $FundingSourceCode . $SectionNumber . "-" . $FiscalYear;
  }
  else 
  {
    $logNum = $CourseCode . "-" . $OldLogNumber;
  }
#}
#else
#{
#  $logNum = $MIEMSSLogNumber;
#}

#my $QueryString = qq{SELECT SRec.Suffix, SRec.LastName, SRec.MiddleName, SRec.FirstName, AES_DECRYPT(SRec.SSN, $EncryptKey) AS SSN, SReg.AffiliationID, SReg.MFRICompanyCode, A.Name, SReg.Grade, SReg.PercentageScore 
#FROM StudentRecords AS SRec, Affiliations AS A, StudentRegistration AS SReg 
#WHERE (SReg.ArchivedScheduledCourseID = $SCID) AND (SReg.StudentID = SRec.ID) AND (SReg.AffiliationID = A.ID) ORDER BY A.Name, $orderBy};
my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );

if (not defined $db)
{
  MFRI::set_parameter("error", "null db");
  MFRI::redirect("error.cgi");
  exit;
}

my $QueryString = "";

$QueryString = qq{SELECT SRec.Suffix, SRec.LastName, SRec.MiddleName, SRec.FirstName, AES_DECRYPT(SRec.IDNumber, "} . DBK::Encrypt_Key() . 
qq{") AS SSN, SReg.AffiliationID, A.MFRICode AS MFRICompanyCode, A.miemss_number AS MIEMSSCompanyCode, A.Name, SReg.Grade, SReg.GradeNote, SReg.PercentageScore FROM StudentRecords AS SRec, Affiliations AS A, StudentRegistration AS SReg WHERE (SReg.SchedCourseID = $SCID) AND (SReg.StatusID != 4) AND (SReg.StatusID != 22) AND (SReg.StudentID = SRec.ID) AND (SReg.AffiliationID = A.ID) ORDER BY A.Name, AES_DECRYPT(SRec.IDNumber, "} . DBK::Encrypt_Key() . qq{")};

#APPDEBUG::WriteDebugMessage("QueryString $QueryString");	

$db->query($QueryString);

#warn "logNum $logNum";
#warn "call num_rows";
my $numRows = $db->num_rows();

if ($numRows < 1)
{
    $db->finish();
    MFRI::set_parameter("error", "No students in class.");
    MFRI::redirect("error.cgi");
  exit;
}
#tgs 20050923my $tmp = $db->num_rows();
#warn "numrows: $tmp";

print_doc_header();
print_page_header();
my $rowH;
my $i = 0;
my %groupH;
for ($i = 0; $i < $numRows; $i++)
{
    $rowH = $db->get_rowh();
    my $affilName = $rowH->{Name};
    push(@{$groupH{$affilName}}, $rowH);
}


my $aRef;
foreach $aRef (sort(keys(%groupH)))
{
    my @grpArray = @{$groupH{$aRef}};    
    print_entry(@grpArray);
}

$currY = $minYPage - PDF_DRAW::get_line_delta();

#PDF_DRAW::text(772, $pageNumY, "Page: $pageNum");

#$leftX
PDF_DRAW::text(650, $currY, $ReportDate);  


print_doc_footer(); #End the pdf document and print it to the screen

sub print_entry
{
    my @group = @_;
    my $affilName;
    my $MFRICompanyCode;
	my $MIEMSSCompanyCode;
    my $outStr;
    my $currEntry;
    my $numLines = 4 + scalar @group;
    my $height = $numLines * PDF_DRAW::get_line_delta();

	#if ($pageNum != 1)
	#{
     # if ($currY - $height <= $minYPage)
#	  if ($RecordCounter >= ($maxLinesPage - 27))
#      {
#	    PDF_DRAW::new_page();
#	    $pageNum++;
#	    $currY = $topY;
#	    print_page_header();	  
#     }
	#}

    $CountInCompany = @group;
	 
    my $firstEntry = $group[0];
	
	
    $affilName = $firstEntry->{Name};
    $MFRICompanyCode = $firstEntry->{MFRICompanyCode};
	$MIEMSSCompanyCode = $firstEntry->{MIEMSSCompanyCode};
	
	my $CompanyNumberDisplay = "";
	
	if (length($MFRICompanyCode) > 0)
	{
	  $CompanyNumberDisplay .= qq{MFRI: } . $MFRICompanyCode;
	}
	
	if (length($MIEMSSCompanyCode) > 0)
	{
	  if (length($CompanyNumberDisplay) > 0)
	  {
	    $CompanyNumberDisplay .= qq{ }
	  }
	  $CompanyNumberDisplay .= qq{MIEMSS: } . $MIEMSSCompanyCode;
	}

    if (length($CompanyNumberDisplay) > 0)
	{
	  $CompanyNumberDisplay = qq{(} . $CompanyNumberDisplay . qq{)};
	}

    $currY = PDF_DRAW::text($leftX, $currY, "<br><br><b>$affilName</b>     $CompanyNumberDisplay"); # + 50

	$CompanyRecordCounter = 0;
    #$NeedExtraLineAfterHeader = 0;
	
    foreach $currEntry (@group)
    {
	  $CountInCompany--;
	  $CompanyRecordCounter++;
	  #$NeedExtraLineAfterHeader = 1;
	my $SSN = STUREG_MAINT::HyphenateSSN($currEntry->{SSN});       
#APPDEBUG::WriteDebugMessage("1 SSN $currEntry->{SSN}");	
	$SSN =~ s/(\d\d\d)(\d\d)(\d\d\d\d)/$1-$2-$3/;
#	my $suffix = "";
#	$suffix = " " . $currEntry->{Suffix} if (length($currEntry->{Suffix}) > 0);
#	my $Name = qq{$currEntry->{LastName}$suffix, $currEntry->{FirstName} $currEntry->{MiddleName}};

	my $suffix = "";
	if (length($currEntry->{Suffix}) > 0)
	{
	  $suffix = " " . $currEntry->{Suffix};
	}
	
	#my $Name = qq{$currEntry->{LastName}$suffix, $currEntry->{FirstName} $currEntry->{MiddleName}};
	my $Name = qq{$currEntry->{LastName}$suffix, };
    my $MiddleName = $currEntry->{MiddleName};
	my $MaxNameLength = 45;
	my $NameLength = length($currEntry->{LastName}) + length($suffix) + length($currEntry->{FirstName}) + length($MiddleName);
	
	if ($NameLength > $MaxNameLength)
	{
	  $MiddleName = substr($currEntry->{MiddleName}, 0, 1);
	  $NameLength = length($currEntry->{LastName}) + length($suffix) + length($currEntry->{FirstName}) + length($MiddleName);
	  
  	  if ($NameLength > $MaxNameLength)
	  {
	    $Name .= substr($currEntry->{FirstName}, 0, 1);
        $Name .= " " . substr($currEntry->{MiddleName}, 0, 1);
      }
	  else
	  {
	    $Name .= $currEntry->{FirstName};
        $Name .= " " . substr($currEntry->{MiddleName}, 0, 1);
	  }
	}
	else
	{
        $Name .= " $currEntry->{FirstName} " . $MiddleName;
	}

	my $Grade = MFRI_STRINGS::trim($currEntry->{Grade});
	my $GradeNote = MFRI_STRINGS::trim($currEntry->{GradeNote});
	my $PercentageScore = MFRI_STRINGS::trim($currEntry->{PercentageScore});

	if ($Grade eq "Unknown")
	{
	  $Grade = "";
	}
	
	if (($PercentageScore eq "0%") || ($PercentageScore eq "0"))
    {
	  $PercentageScore = "";
	}
		
    PDF_DRAW::text(650, $currY, $Grade);
	PDF_DRAW::text(750, $currY, $PercentageScore);
	
	#if there is  no greade or percentage score, but there is a grade note, print the note instead.
	#otherwise ptint the note on the next line down.
	my $MaxGradeNoteLength = 20;
	my $GradeNote2 = "";
	
	if ($GradeNote eq "None 0")
	{
	  $GradeNote = "";	
	}
	
	if ((length($Grade) == 0) && (length($PercentageScore) == 0) && (length($GradeNote) > 0))
	{
	  ($GradeNote, $GradeNote2) = MFRI_STRINGS::Split_String_At_Word( $GradeNote, $MaxGradeNoteLength);
#APPDEBUG::WriteDebugMessage("1 GradeNote $GradeNote");	  
#APPDEBUG::WriteDebugMessage("1 GradeNote2 $GradeNote2");	  
	  if ((length($GradeNote) == 0) && (length($GradeNote2) > 0))
	  {
	    $GradeNote = $GradeNote2;
		$GradeNote2 = "";
	  }
      PDF_DRAW::text(650, $currY, $GradeNote);
	  $GradeNote = $GradeNote2;
	}

	if ($orderBySSN == 1)
	{
	    my $outputText = "$SSN   $Name";
	    $currY = PDF_DRAW::text($leftX, $currY, $outputText); # + 50
	}
	else
	{
#APPDEBUG::WriteDebugMessage("SSN $SSN");
#APPDEBUG::WriteDebugMessage("Name $Name");
	    PDF_DRAW::text($leftX, $currY, $Name); # + 50
	    $currY = PDF_DRAW::text(450, $currY, $SSN);
	}
	
	if (length($GradeNote) > 0)
	{
	  my $NoteX = 650;
	  
	  if (length($GradeNote) >= (2*$MaxGradeNoteLength))
	  {
	    $NoteX = 40;
	  }
	  elsif (length($GradeNote) >= $MaxGradeNoteLength)
	  {
	    $NoteX = 540;
	  }

#APPDEBUG::WriteDebugMessage("2 GradeNote $GradeNote");	  
#APPDEBUG::WriteDebugMessage("2 currY $currY");	  
	   
      $currY = PDF_DRAW::text($NoteX, $currY, $GradeNote);
#APPDEBUG::WriteDebugMessage("2a currY $currY");	  
	  $CompanyRecordCounter++;
	 # $minYPage -= PDF_DRAW::get_line_delta();
	}
	
	$RecordCounter++;
    
	#APPDEBUG::WriteDebugMessage("RecordCounter $RecordCounter");
    #APPDEBUG::WriteDebugMessage("maxLinesPage $maxLinesPage");
    
	#if ($RecordCounter >= ($maxLinesPage - 27))
	#if ($currY - $height <= $minYPage)
	if ($currY <= $minYPage)
    {
      #APPDEBUG::WriteDebugMessage("RecordCounter $RecordCounter >= maxLinesPage $maxLinesPage");

      $currY -= PDF_DRAW::get_line_delta();

      PDF_DRAW::text(650, $currY, $ReportDate);  

	  PDF_DRAW::new_page();
	  $pageNum++;
	  $currY = $topY;

	  if (($CompanyRecordCounter > 0) && ($CountInCompany >= 1))
	  {
        $NeedExtraLineAfterHeader = 1;
	  }
	  else
	  {
        $NeedExtraLineAfterHeader = 0;
	  }

	  print_page_header();	  

      if (1 == $NeedExtraLineAfterHeader)
	  #if ($RecordCounter > 0)
	  {
        #$currY = PDF_DRAW::text($leftX, $currY, " "); # + 50
        $currY = PDF_DRAW::text($leftX, $currY, "<br><br><b>$affilName</b>     $CompanyNumberDisplay (Continued)");
	  }
	  
      $NeedExtraLineAfterHeader = 0;

    }
	
  }
}



sub print_doc_header
{
    PDF_DRAW::doc_header(836, 1029); #Create the document
    PDF_DRAW::set_formatting(1); #Turn on formatting so we can use tags (optional)
    PDF_DRAW::set_font("Times-Roman"); #Set the font (optional)
    PDF_DRAW::set_font_size(PDF_DRAW::get_default_font_size()+ 4); #Set the font size (optional)
}

sub print_doc_footer
{
    PDF_DRAW::doc_footer(); #Finish and print the document
}


sub print_page_header
{
	  my $CourseTitleToShow = "";

		if (length($courseTitleString3) > 0)
		{
	      $CourseTitleToShow .=  $courseTitleString1 . "<br>" . $courseTitleString2 . "<br>" . $courseTitleString3;
		}
		elsif (length($courseTitleString2) > 0)
		{
	      $CourseTitleToShow .=  $courseTitleString1 . "<br>" . $courseTitleString2;
		}
		else
		{
	      $CourseTitleToShow .=  $courseTitleString1;
		}
	
    my $headerText = qq
    {
      COMPANY BREAKDOWN<br>
      LOG NUMBER: $logNum<br>
      $CourseTitleToShow<br>
      INSTRUCTOR: $instructorName<br>
      LOCATION: $locationName
    };

    my $StartDateText = qq
    {
      START: $startDate<br>
    };

    my $EndDateText = qq
    {
      END: $endDate<br>
    };

	$RecordCounter = 0;
    my $pageNumY = $currY;
    my $StartDateY = $currY - PDF_DRAW::get_line_delta() * 2;
    my $EndDateY = $currY - PDF_DRAW::get_line_delta() * 3;

    $currY = PDF_DRAW::wrap_text($leftX, $currY, 730, $headerText);
    PDF_DRAW::text(772, $pageNumY, "Page: $pageNum");
    PDF_DRAW::text(600, $StartDateY, $StartDateText);
    PDF_DRAW::text(600, $EndDateY, $EndDateText);
	
   $CompanyRecordCounter = 0;	
}
