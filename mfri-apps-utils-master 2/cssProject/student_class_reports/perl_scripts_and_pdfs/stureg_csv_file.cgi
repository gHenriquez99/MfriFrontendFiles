#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use REG_PREFS;
use Database;
use CGI;
use strict;
use MFRI_WIDGETS;
use MFRI_STRINGS;
use DATE_UTIL;
#use PDF::Reuse;
#use PDF_DRAW;
#use POSIX;

use DBK;

#use APPDEBUG;

#APPDEBUG::WriteDebugMessage("+++++++++++++");      

#tgs 01182007my $InstructorsToPrint = CGI::param( 'ITP' );

#tgs 01182007if ((not defined $InstructorsToPrint) || (length($InstructorsToPrint) < 1))
#tgs 01182007{
#tgs 01182007   MFRI::set_parameter( "error", "Nothing to print." );
#tgs 01182007   MFRI::redirect( "error.cgi" );
#tgs 01182007   exit;
#tgs 01182007}


if(!MFRI::is_authenticated())
{
    MFRI::set_parameter( "error", "You must be logged in to use the system." );
    MFRI::redirect( "error.cgi" );
    exit;
}

my $VendorFileToken = 'Medical#mfri$EMT';

my $UserID = MFRI::get_current_userid();

my ($ImportPermission, $ExportPermission) = REG_PREFS::Get_UserPermissionsImportExport($UserID);

if ($ExportPermission != 1)
{
  MFRI::set_cookie( "error", "You are not allowed to export student data." );
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
    MFRI::set_parameter( "error", "Invalid Scheduled Course. ($ScheduledCourseID)" );
    MFRI::redirect( "error.cgi" );
    exit;
}

my $DownloadFileName = CGI::param( 'DFN' );

if (not defined $DownloadFileName)
{
  $DownloadFileName = "";
}

if (length($DownloadFileName) < 1)
{
    MFRI::set_parameter( "error", "Invalid Download File Name. ($DownloadFileName)" );
    MFRI::redirect( "error.cgi" );
    exit;
}

my $ExportStatus = CGI::param( "ExStat" ); 

if (not defined $ExportStatus)
{
  $ExportStatus = 2;
}

my $ExportType = CGI::param( "ExportType" ); 

if (not defined $ExportType)
{
  $ExportType = "Kaplan";
}

my $MIEMSSCourseCode = CGI::param( "MCC" ); 

my $MIEMSSDate = CGI::param( "DDMM" ); 

my $MIEMSSCCPrefix = CGI::param( "MCCPrefix" ); 

my $CourseName = CGI::param( "CN" ); 

if ($ExportType eq "MIEMSS")
{
    
  if ((not defined $MIEMSSCourseCode) || (length($MIEMSSCourseCode) != 5))
  {
    MFRI::set_parameter( "error", "Invalid MIEMSS Course Code. ($MIEMSSCourseCode)" );
    MFRI::redirect( "error.cgi" );
    exit;
  }

  if ((not defined $MIEMSSDate) || (length($MIEMSSDate) != 4))
  {
    MFRI::set_parameter( "error", "Invalid MIEMSS Course Date. ($MIEMSSDate)" );
    MFRI::redirect( "error.cgi" );
    exit;
  }
  
  if ((not defined $MIEMSSCCPrefix) || (length($MIEMSSCCPrefix) != 2))
  {
    MFRI::set_parameter( "error", "Invalid MIEMSS Course Code Year Prefix. ($MIEMSSCCPrefix)" );
    MFRI::redirect( "error.cgi" );
    exit;
  }
  
  #$MIEMSSDate = $MIEMSSCCPrefix . $MIEMSSDate;
  $MIEMSSCourseCode = $MIEMSSCCPrefix . $MIEMSSCourseCode;
  
  if ((not defined $CourseName) || (length($CourseName) < 1))
  {
    MFRI::set_parameter( "error", "Invalid Course Name." );
    MFRI::redirect( "error.cgi" );
    exit;
  }
}


my $EncryptKey = qq{"} . DBK::Encrypt_Key() . qq{"};

my @PlaceHolders;

push(@PlaceHolders, $ScheduledCourseID);

#AES_DECRYPT(ST.IDNumber, $EncryptKey) AS SSN, 

my $StudentOutcomeClause = qq{(SR.StatusID = 3) };

if (1 == $ExportStatus)
{
  $StudentOutcomeClause = qq{(SR.StatusID = 9) };
}

my $QueryString = "";

if ($ExportType eq "MIEMSS")
{
  $QueryString = qq{
SELECT
CD.Category,
CD.Level,
SC.FundingSourceCode,
SC.SectionNumber,
SC.FiscalYear,
ST.FirstName,
ST.MiddleName,
ST.LastName,
ST.Suffix,
AES_DECRYPT(ST.StateProviderNumber, $EncryptKey) AS StateProviderNumber,  
DATE_FORMAT(ST.CertificationExpirationDate, "%Y-%m-%d") AS CertificationExpirationDate,
ST.Address1,
ST.Address2,
ST.City,
ST.State,
ST.PostCode,
ST.PrimaryPhoneNumber,
ST.Email
FROM StudentRecords AS ST,
StudentRegistration AS SR,
ScheduledCourses AS SC,
CourseDescriptions AS CD
WHERE (SR.StudentID = ST.ID) AND
(SR.SchedCourseID = SC.ID) AND
(SC.CourseID = CD.ID) AND
(SR.SchedCourseID = ?) AND
$StudentOutcomeClause 
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, SR.Created    
};
}
elsif ($ExportType eq "NPI")
{
  $QueryString = qq{
SELECT
CD.Category,
CD.Level,
SC.FundingSourceCode,
SC.SectionNumber,
SC.FiscalYear,
ST.FirstName,
ST.MiddleName,
ST.LastName,
ST.Suffix,
AES_DECRYPT(ST.StateProviderNumber, $EncryptKey) AS StateProviderNumber,  
DATE_FORMAT(ST.CertificationExpirationDate, "%Y-%m-%d") AS CertificationExpirationDate,
ST.Address1,
ST.Address2,
ST.City,
ST.State,
ST.PostCode,
ST.PrimaryPhoneNumber,
ST.Email
FROM StudentRecords AS ST,
StudentRegistration AS SR,
ScheduledCourses AS SC,
CourseDescriptions AS CD
WHERE (SR.StudentID = ST.ID) AND
(SR.SchedCourseID = SC.ID) AND
(SC.CourseID = CD.ID) AND
(SR.SchedCourseID = ?) AND
$StudentOutcomeClause 
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, SR.Created    
};
}
elsif ($ExportType eq "Kaplan")
{
  $QueryString = qq{
SELECT
CD.Category,
CD.Level,
SC.FundingSourceCode,
SC.SectionNumber,
SC.FiscalYear,
ST.FirstName,
ST.MiddleName,
ST.LastName,
ST.Suffix,
AES_DECRYPT(ST.StateProviderNumber, $EncryptKey) AS StateProviderNumber,  
DATE_FORMAT(ST.CertificationExpirationDate, "%Y-%m-%d") AS CertificationExpirationDate,
ST.Address1,
ST.Address2,
ST.City,
ST.State,
ST.PostCode,
ST.PrimaryPhoneNumber,
ST.Email
FROM StudentRecords AS ST,
StudentRegistration AS SR,
ScheduledCourses AS SC,
CourseDescriptions AS CD
WHERE (SR.StudentID = ST.ID) AND
(SR.SchedCourseID = SC.ID) AND
(SC.CourseID = CD.ID) AND
(SR.SchedCourseID = ?) AND
$StudentOutcomeClause 
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, SR.Created    
};
}
elsif ($ExportType eq "NFA")
{
  $QueryString = qq{
SELECT
CD.Category,
CD.Level,
SC.FundingSourceCode,
SC.SectionNumber,
SC.FiscalYear,
CD.NFACode,
DATE_FORMAT(SC.StartDate,\"%m-%d-%Y\") AS StartDate,
DATE_FORMAT(SC.EndDate,\"%m-%d-%Y\") AS EndDate,
ST.FirstName,
ST.LastName,
ST.Suffix,
DATE_FORMAT(ST.BirthDate,"%m-%d-%Y") AS BirthDate,
AES_DECRYPT(ST.IDNumber, $EncryptKey) AS SSN,  
AES_DECRYPT(ST.StateProviderNumber, $EncryptKey) AS StateProviderNumber,  
DATE_FORMAT(ST.CertificationExpirationDate, "%Y-%m-%d") AS CertificationExpirationDate,
L.City AS LocationCity,
L.State AS LocationState,
A.Name AS AffiliationName,
A.StreetAddress1 AS AffiliationAddress1,
A.StreetAddress2 AS AffiliationAddress2,
A.StreetCity AS AffiliationCity,
A.StreetState AS AffiliationState,
A.StreetPostCode AS AffiliationPostCode
FROM 
StudentRecords AS ST,
StudentRegistration AS SR,
ScheduledCourses AS SC,
CourseDescriptions AS CD,
Locations AS L,
Affiliations AS A
WHERE 
(SR.StudentID = ST.ID) AND
(SR.SchedCourseID = SC.ID) AND
(SC.CourseID = CD.ID) AND
(SR.AffiliationID = A.ID) AND
(SC.LocationID = L.ID) AND
(SR.SchedCourseID = ?) AND
$StudentOutcomeClause 
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, SR.Created    
};
}
elsif ($ExportType eq "Canvas")
{
  $QueryString = qq{
SELECT
ST.FirstName,
ST.MiddleName,
ST.LastName,
ST.Suffix,
ST.Email
FROM StudentRecords AS ST,
StudentRegistration AS SR
WHERE (SR.StudentID = ST.ID) AND
(SR.SchedCourseID = ?) AND
$StudentOutcomeClause 
ORDER BY ST.LastName, ST.FirstName, ST.MiddleName, SR.Created    
};
}
elsif ($ExportType eq "PreRegCanvas")
{
  $QueryString = qq{
SELECT
PR.FirstName,
PR.MiddleName,
PR.LastName,
PR.Suffix,
PR.Email
FROM 
PreRegistrations AS PR
WHERE 
(PR.ScheduledCourseID = ?) AND
(PR.StatusID in (2,7))
ORDER BY PR.LastName, PR.FirstName, PR.MiddleName, PR.Created    
};
}
#20171127+
elsif ($ExportType eq "CheckInEasy")
{
  $QueryString = qq{
SELECT
ST.FirstName,
ST.MiddleName,
ST.LastName,
ST.Suffix,
ST.Email,
ST.PrimaryPhoneNumber,
AES_DECRYPT(ST.IDNumber, $EncryptKey) AS SSN
FROM StudentRecords AS ST,
StudentRegistration AS SR
WHERE (SR.StudentID = ST.ID) AND
(SR.SchedCourseID = ?) AND
$StudentOutcomeClause 
ORDER BY ST.LastName, ST.Suffix, ST.FirstName, ST.MiddleName, SR.Created    
};
}
elsif ($ExportType eq "PreRegCheckInEasy")
{
  $QueryString = qq{
SELECT
PR.FirstName,
PR.MiddleName,
PR.LastName,
PR.Suffix,
PR.Email,
PR.PrimaryPhoneNumber,
AES_DECRYPT(PR.SSN, $EncryptKey) AS SSN
FROM 
PreRegistrations AS PR
WHERE 
(PR.ScheduledCourseID = ?) AND
(PR.StatusID in (2,7))
ORDER BY PR.LastName, PR.Suffix, PR.FirstName, PR.MiddleName, PR.Created    
};
}
#20171127-

#my $tmp = join(", ",@PlaceHolders);
#APPDEBUG::WriteDebugMessage("Query $QueryString"); 
#APPDEBUG::WriteDebugMessage("PlaceHolders $tmp");  

#tgs 01182007my $QueryString = "";

#tgs 01182007  $QueryString = qq
#tgs 01182007  {
#tgs 01182007  SELECT
#tgs 01182007  M.LastName,
#tgs 01182007  M.Suffix,
#tgs 01182007  M.FirstName,
#tgs 01182007  LEFT(M.MiddleName, 1) AS MiddleName,
#tgs 01182007  M.Address1,
#tgs 01182007  M.Address2,
#tgs 01182007  M.City,
#tgs 01182007  M.State,
#tgs 01182007  M.PostCode,
#tgs 01182007  M.Country
#tgs 01182007  FROM MfriInstructors AS M
#tgs 01182007  WHERE 
#tgs 01182007  M.ID in ($InstructorsToPrint)
#tgs 01182007  ORDER BY M.LastName, M.FirstName, M.MiddleName, M.Suffix
#tgs 01182007  };


#APPDEBUG::WriteDebugMessage("QueryString $QueryString");       
  
my $db = new Database( DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName() );
my $need_to_query = "YES";

my $i = 0;
my $InstructorCounter = 1;

#APPDEBUG::WriteDebugMessage("print instructor mailing labels");        


print_doc_header($DownloadFileName);
my $page_number = 1;
my $page_count = 0;
print_report($ExportType, $MIEMSSCourseCode, $MIEMSSDate, $CourseName);
print_doc_footer();
$db->finish(); #03-14-2005 WPL Added DB Finish

sub print_report
{
    my $ExportType = shift;
    my $MIEMSSCourseCode = shift;
    my $MIEMSSDate = shift;
    my $CourseName = shift;


#APPDEBUG::WriteDebugMessage("1 ExportType $ExportType");       
#APPDEBUG::WriteDebugMessage("1 MIEMSSCourseCode $MIEMSSCourseCode");       
#APPDEBUG::WriteDebugMessage("1 MIEMSSDate $MIEMSSDate");       
#APPDEBUG::WriteDebugMessage("1 CourseName $CourseName");       

  if (not defined $ExportType)
  {
    return 0;   
  }

  if ($ExportType eq "MIEMSS")  
  {
    if (not defined $MIEMSSCourseCode)
    {
      return 0; 
    }

    if (not defined $MIEMSSDate)
    { 
      return 0; 
    }

    if (not defined $CourseName)
    {
      return 0; 
    }
  }
    
    if ($need_to_query eq "YES")
    {
    #$db->query($QueryString);  
    $db->query( $QueryString, @PlaceHolders );
    $need_to_query = "NO";
    }
    
    
    #my $tmp = $db->num_rows();
#    warn "numrows: $tmp";

    if ($db->num_rows() == 0)
    {
      print_report_header();
      print qq{No Data to print\n};
      print_report_footer();
      return;
    }
    
    my $AddressInfo;
    
    my $PrintedRecord = 1;

    print_report_header();
#APPDEBUG::WriteDebugMessage("*****Start"); 
    
    while ($AddressInfo = $db->get_rowh())
    {
       $PrintedRecord = Print_Entry($ExportType, $MIEMSSCourseCode, $MIEMSSDate, $CourseName, $AddressInfo);  
    }

    print_report_footer();
#APPDEBUG::WriteDebugMessage("*****End");   
    
}

sub print_doc_header
{   
  my $DownlaodFileName = shift;

#  print qq{HTTP/1.1 200 OK};
#  print qq{\n};

  if (length($DownlaodFileName) > 0 )   
  {
    print qq{Content-Disposition: filename=$DownlaodFileName};
  } 
#attachment; 
  print qq{\n};

  print qq{Content-type: text/plain};
 
  print qq{\n\n};

}

sub print_doc_footer
{
#    PDF_DRAW::doc_footer();
}

sub print_report_header
{

  return;
}

   

sub print_report_footer
{
  return;    
}

sub PrintNPIReport
{
  my $Columnsh = shift;

  if (not defined $Columnsh)
  {
    return 0;   
  }

#APPDEBUG::WriteDebugMessage("2 PrintNPIReport");       
 
    #   my $Address1 = $Columnsh->{Address1}; 
    #   my $Address2 = $Columnsh->{Address2};
        my $City = "College Park";#$Columnsh->{City};
        my $State = "MD"; #$Columnsh->{State};
        my $PostCode = "20742";#$Columnsh->{PostCode};
        my $PhoneNumber = "3012269900";#$Columnsh->{PostCode};

        my $CertificationExpirationDate = $Columnsh->{CertificationExpirationDate};
        my $Email = $Columnsh->{Email};


    #   my $Country = $Columnsh->{Country};

        my ($LogNumberReturnCode, $LogNumber) = MFRI_STRINGS::Build_Log_Number($Columnsh->{Category}, $Columnsh->{Level}, $Columnsh->{FundingSourceCode}, $Columnsh->{SectionNumber}, $Columnsh->{FiscalYear}, "");

        #20191108+
        my $ReturnLastNameFirst = 1;
        my $Name = MFRI_STRINGS::Build_Name($Columnsh->{FirstName},  "", $Columnsh->{LastName}, $Columnsh->{Suffix}, $ReturnLastNameFirst, 0, 80, 1); 

        warn "Name $Name\n";
        my @NameParts = split(/,/, $Name);

        my $LastNameToPrint = $NameParts[0];
        my $FirstNameToPrint = $NameParts[-1];
        warn "LastNameToPrint $LastNameToPrint\n";
        warn "FirstNameToPrint $FirstNameToPrint\n";

        #20191108-
        #my $FirstName = $Columnsh->{FirstName};
        #my $MiddleName = $Columnsh->{MiddleName};
        #my $LastName = $Columnsh->{LastName};
        #my $Suffix = $Columnsh->{Suffix};
        #my $ReturnLastNameFirst = 0;
        #my $TruncateName = 0;
        #my $MaxLength = 20;
        #my $UseTitleCase = 1; #20171208
        #my $UsePeriodMI = shift; #20180404

         #20191108if (length($Columnsh->{Suffix}) > 0)
         #20191108{
         #20191108  $Columnsh->{LastName} .= " " . $Columnsh->{Suffix};
         #20191108}

        my $StateProviderNumber = $Columnsh->{StateProviderNumber};

    #   $nameString =~ s/,/ /g;
        $StateProviderNumber =~ s/,/ /g;

    #   $nameString = uc($nameString);

    #   $Address1 =~ s/,/ /g;
    #   $Address2 =~ s/,/ /g;
        $City =~ s/,/ /g;
        $State =~ s/,/ /g;
        $PostCode =~ s/,/ /g;

        my $LineToPrint = "";

        my $i = 0;
        #20191108$LineToPrint .= $Columnsh->{FirstName};
        $LineToPrint .= $FirstNameToPrint;#20191108

        $LineToPrint .= ",";

        #20191108$LineToPrint .= $Columnsh->{LastName};
        $LineToPrint .= $LastNameToPrint;#20191108

        $LineToPrint .= ",";

        $LineToPrint .= $State;

        $LineToPrint .= ",";

        $LineToPrint .= $StateProviderNumber;

        $LineToPrint .= ",";

        $LineToPrint .= $CertificationExpirationDate;

        $LineToPrint .= ",";

        $LineToPrint .= "EMTB";

        $LineToPrint .= ",";

        $LineToPrint .= $LogNumber;

        $LineToPrint .= ",";


    #   $LineToPrint .= $Address1;

    #    $LineToPrint .= ",";

    #   $LineToPrint .= $Address2;

    #    $LineToPrint .= ",";

        $LineToPrint .= $City;

        $LineToPrint .= ",";

        $LineToPrint .= $State;

        $LineToPrint .= ",";

        $LineToPrint .= $PostCode;

        $LineToPrint .= ",";

        $LineToPrint .= $PhoneNumber;

        $LineToPrint .= ",";

        $LineToPrint .= $Email;

        $LineToPrint .= ",";

        $LineToPrint .= $StateProviderNumber;

        $LineToPrint .= ",";

        $LineToPrint .= $VendorFileToken;

        $LineToPrint .= "\n";

        print $LineToPrint;
    return 1;    
}

sub PrintKaplanReport
{
  my $Columnsh = shift;

  if (not defined $Columnsh)
  {
    return 0;   
  }

  my ($CurrentYear, $CurrentMonth, $CurrentDay) = DATE_UTIL::CurrentDate();
  my $Current_Date = $CurrentYear . "-" . $CurrentMonth . "-" . $CurrentDay;
#APPDEBUG::WriteDebugMessage("2 PrintKaplanReport");        
 
    #   my $Address1 = $Columnsh->{Address1}; 
    #   my $Address2 = $Columnsh->{Address2};
#       my $City = "College Park";#$Columnsh->{City};
#       my $State = "MD"; #$Columnsh->{State};
#       my $PostCode = "20742";#$Columnsh->{PostCode};
#       my $PhoneNumber = "3012269900";#$Columnsh->{PostCode};

#       my $CertificationExpirationDate = $Columnsh->{CertificationExpirationDate};
        my $Email = $Columnsh->{Email};


    #   my $Country = $Columnsh->{Country};

        my ($LogNumberReturnCode, $LogNumber) = MFRI_STRINGS::Build_Log_Number($Columnsh->{Category}, $Columnsh->{Level}, $Columnsh->{FundingSourceCode}, $Columnsh->{SectionNumber}, $Columnsh->{FiscalYear}, "");

    #20191108+
    my $ReturnLastNameFirst = 1;
    my $Name = MFRI_STRINGS::Build_Name($Columnsh->{FirstName},  "", $Columnsh->{LastName}, $Columnsh->{Suffix}, $ReturnLastNameFirst, 0, 80, 1); 

    warn "Name $Name\n";
    my @NameParts = split(/,/, $Name);

    my $LastNameToPrint = $NameParts[0];
    my $FirstNameToPrint = $NameParts[-1];
    warn "LastNameToPrint $LastNameToPrint\n";
    warn "FirstNameToPrint $FirstNameToPrint\n";

    #20191108-
    #my $FirstName = $Columnsh->{FirstName};
    #my $MiddleName = $Columnsh->{MiddleName};
    #my $LastName = $Columnsh->{LastName};
    #my $Suffix = $Columnsh->{Suffix};
    #my $ReturnLastNameFirst = 0;
    #my $TruncateName = 0;
    #my $MaxLength = 20;
    #my $UseTitleCase = 1; #20171208
    #my $UsePeriodMI = shift; #20180404


        #20191108if (length($Columnsh->{Suffix}) > 0)
        #20191108{
        #20191108  $Columnsh->{LastName} .= " " . $Columnsh->{Suffix};
        #20191108}

        my $StateProviderNumber = $Columnsh->{StateProviderNumber};

    #   $nameString =~ s/,/ /g;
        $StateProviderNumber =~ s/,/ /g;

        my $LineToPrint = "";
#LastName,FirstName,Email,No,Log Number,EPINS
        my $i = 0;
        #20191108$LineToPrint .= $Columnsh->{LastName};
        $LineToPrint .= $LastNameToPrint;#20191108
        
        $LineToPrint .= ",";

        #20191108$LineToPrint .= $Columnsh->{FirstName};
        $LineToPrint .= $FirstNameToPrint;#20191108
        
        $LineToPrint .= ",";

        $LineToPrint .= $Email;

        $LineToPrint .= ",";

        $LineToPrint .= "No";

        $LineToPrint .= ",";

        $LineToPrint .= $LogNumber;

        $LineToPrint .= ",";

        $LineToPrint .= $StateProviderNumber;

        $LineToPrint .= "\n";

        print $LineToPrint;
    return 1;    
}

sub PrintCanvasReport
{
  my $Columnsh = shift;

  if (not defined $Columnsh)
  {
    return 0;   
  }

        my $LineToPrint = "";

        my $i = 0;
    
        #20191108my $ReverseNameOrder = 0;
        
        #20191108my $Name = MFRI_STRINGS::Build_Name(ucfirst(lc($Columnsh->{FirstName})), ucfirst(lc($Columnsh->{MiddleName})), ucfirst(lc($Columnsh->{LastName})), uc($Columnsh->{Suffix}), $ReverseNameOrder);
        #20191108+
        my $ReturnLastNameFirst = 0;
        my $Name = MFRI_STRINGS::Build_Name($Columnsh->{FirstName},  $Columnsh->{MiddleName}, $Columnsh->{LastName}, $Columnsh->{Suffix}, $ReturnLastNameFirst, 0, 80, 1); 
        #20191108-
        
        $LineToPrint .= $Name;

        $LineToPrint .= ", ";

        $LineToPrint .= lc($Columnsh->{Email});

        $LineToPrint .= "\n";

        print $LineToPrint;
    return 1;    
}

sub PrintMIEMSSCEReport
{
    my $MIEMSSCourseCode = shift;
    my $MIEMSSDate = shift;
    my $CourseName = shift;

    my $Columnsh = shift;
    
#APPDEBUG::WriteDebugMessage("2 PrintMIEMSSCEReport");      
#APPDEBUG::WriteDebugMessage("2 MIEMSSCourseCode $MIEMSSCourseCode");       
#APPDEBUG::WriteDebugMessage("2 MIEMSSDate $MIEMSSDate");       
#APPDEBUG::WriteDebugMessage("2 CourseName $CourseName");       
    

      if (not defined $MIEMSSCourseCode)
      {
        return 0;   
      }

      if (not defined $MIEMSSDate)
      {
        return 0;   
      }

      if (not defined $CourseName)
      {
        return 0;   
      }

      if (not defined $Columnsh)
      {
        return 0;   
      }

#   Provider Name
#   Provider Number
#   Class Code
#   Date End Date ddmm
#   Class Title

        #20191108my $ProviderName = MFRI_STRINGS::Build_Name($Columnsh->{FirstName}, $Columnsh->{MiddleName}, $Columnsh->{LastName}, $Columnsh->{Suffix}, 0);
        #20191108+
        my $ReturnLastNameFirst = 0;
        my $ProviderName = MFRI_STRINGS::Build_Name($Columnsh->{FirstName},  $Columnsh->{MiddleName}, $Columnsh->{LastName}, $Columnsh->{Suffix}, $ReturnLastNameFirst, 0, 80, 1); 
        #20191108-

        my $StateProviderNumber = $Columnsh->{StateProviderNumber};

        $StateProviderNumber =~ s/,/ /g;
        $MIEMSSCourseCode =~ s/,/ /g;
        $MIEMSSDate =~ s/,/ /g;
        $CourseName =~ s/,/ /g;

        my $LineToPrint = "";

        my $i = 0;
        $LineToPrint .= $ProviderName;

        $LineToPrint .= ",";

        $LineToPrint .= $StateProviderNumber;

        $LineToPrint .= ",";

        $LineToPrint .= $MIEMSSCourseCode;

        $LineToPrint .= ",";

        $LineToPrint .= $MIEMSSDate;

        $LineToPrint .= ",";

        $LineToPrint .= $CourseName;

        $LineToPrint .= "\n";

        print $LineToPrint;

    return 1;    
}


sub PrintNFAReport
{
  my $Columnsh = shift;

  if (not defined $Columnsh)
  {
    return 0;   
  }

    #20191108my $LastNameToPrint = $Columnsh->{LastName};
    #20191108
    #20191108if (length($Columnsh->{Suffix}) > 0)
    #20191108{
    #20191108  $LastNameToPrint .= " " . $Columnsh->{Suffix};
    #20191108}


    #20191108+
    my $ReturnLastNameFirst = 1;
    my $Name = MFRI_STRINGS::Build_Name($Columnsh->{FirstName},  "", $Columnsh->{LastName}, $Columnsh->{Suffix}, $ReturnLastNameFirst, 0, 80, 1); 
    
    warn "Name $Name\n";
    my @NameParts = split(/,/, $Name);
    
    my $LastNameToPrint = $NameParts[0];
    my $FirstNameToPrint = $NameParts[-1];
    warn "LastNameToPrint $LastNameToPrint\n";
    warn "FirstNameToPrint $FirstNameToPrint\n";
    
    #20191108-
    #my $FirstName = $Columnsh->{FirstName};
    #my $MiddleName = $Columnsh->{MiddleName};
    #my $LastName = $Columnsh->{LastName};
    #my $Suffix = $Columnsh->{Suffix};
    #my $ReturnLastNameFirst = 0;
    #my $TruncateName = 0;
    #my $MaxLength = 20;
    #my $UseTitleCase = 1; #20171208
    #my $UsePeriodMI = shift; #20180404
    

#       my $StateProviderNumber = $Columnsh->{StateProviderNumber};

    #   $nameString =~ s/,/ /g;
#       $StateProviderNumber =~ s/,/ /g;

    #   $nameString = uc($nameString);

    #   $Address1 =~ s/,/ /g;
    #   $Address2 =~ s/,/ /g;
#       $City =~ s/,/ /g;
#       $State =~ s/,/ /g;
#       $PostCode =~ s/,/ /g;

        #convert date separaters
        $Columnsh->{StartDate} =~ s/-/\//g;
        $Columnsh->{EndDate} =~ s/-/\//g;
        $Columnsh->{BirthDate} =~ s/-/\//g;

        my $LineToPrint = "";
    
        my $GenderPlaceHolder = "";
        my $USCitizenPlaceHolder = "";

        my $i = 0;
        $LineToPrint .= MFRI_STRINGS::TruncateString($LastNameToPrint, 20) . "\t";

        #20191108$LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{FirstName}, 20) . "\t";
        $LineToPrint .= MFRI_STRINGS::TruncateString($FirstNameToPrint, 20) . "\t";#20191108

        $LineToPrint .= MFRI_STRINGS::TruncateString(MFRI_STRINGS::HyphenateSSN($Columnsh->{SSN}), 11) . "\t";

        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{BirthDate}, 10) . "\t"; 

        $LineToPrint .= $GenderPlaceHolder . "\t"; #MFRI_STRINGS::TruncateString($GenderPlaceHolder, 0) . "\t";

        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{NFACode}, 4) . "\t";       
        
        $LineToPrint .= $USCitizenPlaceHolder . "\t"; #MFRI_STRINGS::TruncateString($USCitizenPlaceHolder, 0) . "\t";       

        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{LocationCity}, 30) . "\t";
        
        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{LocationState}, 2) . "\t";
        
        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{StartDate}, 10) . "\t";
        
        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{EndDate}, 10) . "\t";
        
        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{AffiliationName}, 25) . "\t";          
        
        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{AffiliationAddress1}, 25) . "\t";              

        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{AffiliationAddress2}, 25) . "\t";              
        
        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{AffiliationCity}, 21) . "\t";                      
        
        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{AffiliationState}, 2) . "\t";                                  
        
        $LineToPrint .= MFRI_STRINGS::TruncateString($Columnsh->{AffiliationPostCode}, 10);                                 
                        
        $LineToPrint .= "\n";

        print $LineToPrint;
        
    return 1;    
}




sub Print_Entry
{
    my $ExportType = shift;
    my $MIEMSSCourseCode = shift;
    my $MIEMSSDate = shift;
    my $CourseName = shift;
    my $Columnsh = shift;


  if (not defined $Columnsh)
  {
    return 0;   
  }

  if (not defined $ExportType)
  {
    return 0;   
  }

#APPDEBUG::WriteDebugMessage("3 Print_Entry");      
#APPDEBUG::WriteDebugMessage("3 ExportType $ExportType");       

  if ($ExportType eq "MIEMSS")
  {
     return PrintMIEMSSCEReport($MIEMSSCourseCode, $MIEMSSDate, $CourseName, $Columnsh);
  }
  elsif ($ExportType eq "Kaplan")
  {
     return PrintKaplanReport($Columnsh);
  }
  elsif ($ExportType eq "NPI")
  {
     return PrintNPIReport($Columnsh);
  }
  elsif ($ExportType eq "NFA")
  {
     return PrintNFAReport($Columnsh);
  }
  elsif (($ExportType eq "Canvas") || ($ExportType eq "PreRegCanvas"))
  {
     return PrintCanvasReport($Columnsh);
  }
  #20171127+
  elsif (($ExportType eq "CheckInEasy") || ($ExportType eq "PreRegCheckInEasy"))
  {
     return PrintCheckInEasyReport($Columnsh);
  }
  #20171127-

  return 0;

##  my $Address1 = $Columnsh->{Address1}; 
##  my $Address2 = $Columnsh->{Address2};
#   my $City = "College Park";#$Columnsh->{City};
#   my $State = "MD"; #$Columnsh->{State};
#   my $PostCode = "20742";#$Columnsh->{PostCode};
#   my $PhoneNumber = "3012269900";#$Columnsh->{PostCode};
#
#   my $CertificationExpirationDate = $Columnsh->{CertificationExpirationDate};
#   my $Email = $Columnsh->{Email};
#       
#   
##  my $Country = $Columnsh->{Country};
#
#    my ($LogNumberReturnCode, $LogNumber) = MFRI_STRINGS::Build_Log_Number($Columnsh->{Category}, $Columnsh->{Level}, $Columnsh->{FundingSourceCode}, $Columnsh->{SectionNumber}, $Columnsh->{FiscalYear}, "");
#
##  my $nameString = MFRI_STRINGS::Build_Name($Columnsh->{FirstName}, $Columnsh->{MiddleName}, $Columnsh->{LastName}, $Columnsh->{Suffix}, 0);
#
#    if (length($Columnsh->{Suffix}) > 0)
#    {
#     $Columnsh->{LastName} .= " " . $Columnsh->{Suffix};
#    }
#
#   my $StateProviderNumber = $Columnsh->{StateProviderNumber};
#
##  $nameString =~ s/,/ /g;
#   $StateProviderNumber =~ s/,/ /g;
#    
##  $nameString = uc($nameString);
#   
##  $Address1 =~ s/,/ /g;
##  $Address2 =~ s/,/ /g;
#   $City =~ s/,/ /g;
#   $State =~ s/,/ /g;
#   $PostCode =~ s/,/ /g;
#   
#    my $LineToPrint = "";
#   
#   my $i = 0;
#   $LineToPrint .= $Columnsh->{FirstName};
#
#    $LineToPrint .= ",";
#   
#   $LineToPrint .= $Columnsh->{LastName};
#
#    $LineToPrint .= ",";
#   
#   $LineToPrint .= $State;
#
#    $LineToPrint .= ",";
#
#    $LineToPrint .= $StateProviderNumber;
#   
#    $LineToPrint .= ",";
#
#    $LineToPrint .= $CertificationExpirationDate;
#
#    $LineToPrint .= ",";
#
#   $LineToPrint .= "EMTB";
#   
#    $LineToPrint .= ",";
#
#   $LineToPrint .= $LogNumber;
#   
#    $LineToPrint .= ",";
#   
#
##  $LineToPrint .= $Address1;
#   
##    $LineToPrint .= ",";
#
##  $LineToPrint .= $Address2;
#   
##    $LineToPrint .= ",";
#
#    $LineToPrint .= $City;
#
#    $LineToPrint .= ",";
#
#   $LineToPrint .= $State;
#
#    $LineToPrint .= ",";
#
#    $LineToPrint .= $PostCode;
#   
#    $LineToPrint .= ",";
#
#    $LineToPrint .= $PhoneNumber;
#
#    $LineToPrint .= ",";
#
#    $LineToPrint .= $Email;
#
#    $LineToPrint .= ",";
#
#    $LineToPrint .= $StateProviderNumber;
#
#    $LineToPrint .= ",";
#
#    $LineToPrint .= $VendorFileToken;
#
#    $LineToPrint .= "\n";
#
#   print $LineToPrint;
#
#   
#  return 1;    
}

#20171127+
sub AddQuotes
{
    my $StringToQuote = shift;
    
    if (not defined $StringToQuote)
    {
      return qq{""};
    }
    
    if (index($StringToQuote, qq{"}) >= 0)
    {
       $StringToQuote =~ s/\"/\\"/gm; #replace " with \"
    }
    
    return qq{"$StringToQuote"};
    
}

sub PrintCheckInEasyReport
{
  my $Columnsh = shift;

  if (not defined $Columnsh)
  {
    return 0;   
  }

        my $LineToPrint = "";

        my $i = 0;
    
        my $ReverseNameOrder = 0;
        
#        my $Name = MFRI_STRINGS::Build_Name(ucfirst(lc($Columnsh->{FirstName})), "", ucfirst(lc($Columnsh->{LastName})), uc($Columnsh->{Suffix}), $ReverseNameOrder);
        $LineToPrint .= AddQuotes(ucfirst(lc($Columnsh->{FirstName})));

        $LineToPrint .= ",";

        $LineToPrint .= AddQuotes(ucfirst(lc($Columnsh->{MiddleName})));

        $LineToPrint .= ",";

        $LineToPrint .= AddQuotes(ucfirst(lc($Columnsh->{LastName})));

        $LineToPrint .= ",";

        $LineToPrint .= AddQuotes(uc($Columnsh->{Suffix}));

        $LineToPrint .= ",";

        $LineToPrint .= AddQuotes(lc($Columnsh->{Email}));

        $LineToPrint .= ",";

        $LineToPrint .= AddQuotes(lc($Columnsh->{PrimaryPhoneNumber}));
        
        $LineToPrint .= ",";

        $LineToPrint .= AddQuotes(uc(MFRI_STRINGS::HyphenateSSN($Columnsh->{SSN})));

        $LineToPrint .= "\n";

        print $LineToPrint;
    return 1;    
}
#27101127-


