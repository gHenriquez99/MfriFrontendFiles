#! /usr/bin/perl

use MFRI;
use CGI;
use Database;
use MFRI_APPS;
use MESSR_MAINT;
use Data::Dumper;
use DBK;

#tgs 8-30-2004
#don't care about page side anymore use this form only for updating prerege table, which doesn't care about grades, etc

#warn "stureg_confirm_MESSR_data.cgi\n";


my $db = new Database(DBK::HostName(), DBK::CGIUserName(), DBK::CGIUserPassword(), DBK::MFRIDBName());
 
my $AddRecords = CGI::param( 'ADD' ); #are we adding (1) or updating (0) the pre-registration records.

$AddRecords = 1 if (not defined $AddRecords); #adding is the default

my $PageSide = CGI::param( 'PageSide' );

#warn "Current Page Side: $PageSide\n";

$PageSide = 1 if (not defined $PageSide);
$PageSide = 1 if ($PageSide == 0);

#warn "Corrected Page Side: $PageSide\n";

my $SCID = CGI::param( 'SCID' );

#warn "SCID: $SCID\n";

my $action = CGI::param( 'action' );

#warn "action: $action\n";

my $onLoad = "";

my $startPos = CGI::param( 'start' );

#warn "startPos: $startPos\n";

$startPos = 0 if( !( $startPos =~ m/^\d+$/ ) );

#warn "Corrected startPos: $startPos\n";


my @oldMergeIDs =  ( '', CGI::param( 'oldMergeID1' ), CGI::param( 'oldMergeID2' ), CGI::param( 'oldMergeID3' ), CGI::param( 'oldMergeID4' ), CGI::param( 'oldMergeID5' ), );

my $mergeID = CGI::param( 'mergeID' );
$mergeID = -1 if( !( $mergeID =~ m/^\d+$/ ) );

my $isSet = 0;
for( $i=1; $i<=5; $i++ )
{
    if( !( $oldMergeIDs[$i] =~ m/^\d+$/ ) )
    {
	if( $isSet == 0 )
	{
	    $oldMergeIDs[$i] = $mergeID;
	    $isSet = 1;
	}
	else
	{
	    $oldMergeIDs[$i] = -1;
	}
    }
}

sub update_record
{

}

$SelectClause = qq
{
    M.ID,
    M.TitleID,
    MT.Name AS Title,
    M.FirstName,
    M.MiddleName,
    M.LastName,
    M.Suffix,
    M.BirthDate,
    M.GenderID,
    MG.Name AS Gender,
    M.RaceID,
    MR.Name AS Race,
    M.StreetAddress,
    M.Apt,
    M.City,
    M.State,
    M.PostCode,
    M.HomePhone, 
    M.WorkPhone, 
    M.GradeLevelID,
    MGr.Name AS GradeLevel,
    M.CollegeLevelID,
    MC.Name AS CollegeLevel,
    M.LogNumber, 
    M.SponsorID,
    MSp.Name as SponsorType,
    M.ApplicationTypeID,
    MAT.Name AS ApplicationType,
    M.ProviderNumber, 
    M.IDNumber, 
    M.CompanyNumber, 
    M.LegalQuestion1, 
    M.LegalQuestion2, 
    M.LegalQuestion3,
    M.StatusID,
    MS.Name as Status,
    M.Priority 
};
    
$FromClause = qq
{
    MESSRHold AS M,
    MESSRTitleTypes AS MT,
    MESSRGenderTypes AS MG,
    MESSRRaceTypes AS MR,
    MESSRGradeLevelTypes AS MGr,
    MESSRCollegeLevelTypes AS MC,
    MESSRApplicationTypes AS MAT,
    MESSRHoldStatus as MS,
    MESSRSponsorTypes as MSp
};
    
$WhereClause = qq
{
    ( M.TitleID = MT.ID ) AND
    ( M.GenderID = MG.ID ) AND
    ( M.RaceID = MR.ID ) AND
    ( M.GradeLevelID = MGr.ID ) AND
    ( M.CollegeLevelID = MC.ID ) AND
    ( M.ApplicationTypeID = MAT.ID ) AND
    ( M.StatusID = MS.ID ) AND
    ( M.StatusID != 2 ) AND
    ( M.StatusID != 6 ) AND
    ( M.StatusID != 8 ) AND
    ( M.SponsorID = MSp.ID ) AND
    ( M.ScheduledCourseID = $SCID ) AND
    ( ( M.ID > $startPos ) OR ( M.ID = $mergeID OR M.ID = $oldMergeIDs[1] OR M.ID = $oldMergeIDs[2] OR M.ID = $oldMergeIDs[3] OR M.ID = $oldMergeIDs[4] OR M.ID = $oldMergeIDs[5] ) )
};
    
#warn "WHereclase = $WhereClause";
#$WhereClause = "M.ScheduledCourseID = $SCID";
    
$main_query = "SELECT $SelectClause FROM $FromClause WHERE $WhereClause ORDER BY M.ID";


#warn "Query is $query";

$db->query( $main_query );
$num_rows=$db->num_rows();

#warn "1 Number of rows returned: $num_rows";
#warn "Have Front Page PageSide $PageSide\n" if ($PageSide == 1);
#warn "Have Back Page PageSide $PageSide\n" if ($PageSide == 2);

if( $action eq "Add marked students to Pre-Registration list and continue" )
{
    $num_records = CGI::param( 'count' );
#warn "Starting at $num_records";

    for( $i=0; $i<$num_records; $i++ )
    {
	  my $ID = CGI::param( "id_$i" );
	#warn "ID=$ID";
	  my $rec = STUREG_MAINT::extract_from_edit_form( $i );
	  $rec->{HomePhone} = $rec->{PrimaryPhone};
	  $rec->{WorkPhone} = $rec->{SecondaryPhone};

	  $db->auto_quoteh( "MESSRHold", $rec );    
	  $db->updateh( "MESSRHold", $rec, "WHERE ID=$ID" );
    }

    for( $i=0; $i<$num_records; $i++ )
    {
	  my $temp = CGI::param( "add_to_pre_reg_$i" );
	  my $module_count = CGI::param( "module_count_$i" );

	  if( $temp eq 'add' )
	  {
	    my $ID_to_copy = CGI::param( "id_$i" );
	    my $CopyResult = STUREG_MAINT::copy_MESSR_to_PreReg( $ID_to_copy, $AddRecords );
		
		if (($CopyResult > 0) && ($AddRecords == 1))
		{ 
		  my $PreRegCount = MESSR_MAINT::MESSR_PreReg_Count($SCID);
		  
		  if ($PreRegCount >= 0)
		  {
		    $PreRegCount++;
			my $UpdateResult = MESSR_MAINT::Update_Last_MESSR_PreReg_Count($SCID, $PreRegCount);
			
			if ($UpdateResult <= 0)
            {		 
              warn "Error ($UpdateResult) updating PreRegistration count ($PreRegCount) in StudentMESSRData for ScheduledCourseID $SCID.\n";
            }   

		  }
		}
		
#	    add_to_pre_reg( $i );
	    
	    #tgs 8-30-2004( my $grades, my @modular_grades, my @evaluation_results ) = MESSR_MAINT::extract_grades_edit_form( $i );

	   #tgs 8-30-2004 my $grades_id = CGI::param( "grades_id_$i" );
	   #tgs 8-30-2004 $grades->{MESSRHoldID} = $ID_to_copy;

	   #tgs 8-30-2004 $tempNum = @modular_grades + 0;
	    
	   #tgs 8-30-2004 if( $grades_id =~ m/^\d+$/ )
	    #tgs 8-30-2004{
		  #warn "updating";
		#tgs 8-30-2004  $db->updateh( "Grades", $grades, "WHERE ID=$grades_id" );
	   #tgs 8-30-2004 }
	    
	    #foreach $key ( keys %{$modular_grades[$j]} )
	    #{
		#warn "Modular Grade: $i $key $modular_grades[$j]->{$key}";
	    #}

	    #tgs 8-26-2004
		#No idea what this does
		#for( $j=1; $j<=$module_count; $j++ )
	    #{
		 # next if( (keys %{$modular_grades[$j]}) + 0 == 0 ); # if this modular grade is empty
		
		 # if( ( $grades_id =~ m/^\d+$/ ) == 0 )
		 # {
		 #   $grades_id = $db->inserth( "Grades", $grades );
		 # }

		 # my $modular_grade_id = CGI::param( "modular_grade_id_$j-$i" );
		 # $modular_grades[$j]->{GradesID} = $grades_id;
		
		 # if( defined $modular_grade_id )
		 # {
		 #   $db->updateh( "ModularGrades", $modular_grades[$j], "WHERE ID=$modular_grade_id" );
		 # }
		 # else
		 # {
		 #   $db->inserth( "ModularGrades", $modular_grades[$j] );
		 # }
	    #}
      }
    }
}

$db->query( $main_query );
$num_rows = $db->num_rows();

#warn "2 Number of rows returned: $num_rows";
    
if( $num_rows <= 0 )
{
    $onLoad = qq{
	<script type='text/javascript'>
	    onload=function()
	{
	    window.opener.location.reload();
	    self.close();
	}
	<\/script>
	};
}
else
{
    $onLoad = qq{
	<script type='text/javascript'>
	    onload=function()
	{
	    window.opener.location.reload();
	}
	<\/script>
	};
}

my $Students_from_MESSR = "";
my $count = 0;
my $max_count = 5;

#for( $i=1; $i<$startPos; $i++ )
#{
#    warn "0";
#    $db->get_row();
#}

#$newStartPos = $startPos + 5;

$lastID = 0;

for( $i=1; $i<=5; $i++ )
{
    delete $oldMergeIDs[$i] if( $oldMergeIDs[$i] == -1 );
}


#warn "Before While\n";
#warn "count $count\n";
#warn "max_count $max_count\n";
#warn "--Before While\n";

my $GradesQueryString = "";
my $MESSRHoldID = 0;
my $NumberOfGrades = 0;

while( my $row = $db->get_rowh() and $count < $max_count )
{
#warn "In While\n";
#warn "count $count\n";
#warn "max_count $max_count\n";
#warn "--In While\n";

  $MESSRHoldID = $row->{ID};
  
  warn "MESSRHoldID $MESSRHoldID\n";
  
#tgs 8-30-2004	if ($PageSide == 1)
#tgs 8-30-2004	{
      $row->{PrimaryPhoneNumber} = $row->{HomePhone};
      $row->{SecondaryPhoneNumber} = $row->{WorkPhone};
      $row->{Address1} = $row->{StreetAddress};

      $Students_from_MESSR .= MESSR_MAINT::print_front_page_edit_form( $row, $count );
#tgs 8-30-2004    }#if ($PageSide == 1)
#tgs 8-30-2004    elsif ($PageSide == 2)
#tgs 8-30-2004	{
#tgs 8-30-2004      $Students_from_MESSR .= MESSR_MAINT::print_front_page_view_form( $row, $count );
#tgs 8-30-2004    }#if ($PageSide == 1)
	  
	  
	$Students_from_MESSR .= "<br><br>";

#tgs 8-30-2004	if ($PageSide == 2)
#tgs 8-30-2004	{
#tgs 8-30-2004	  $GradesQueryString = qq{SELECT ID from Grades where MESSRHoldID=$MESSRHoldID};
	
#tgs 8-30-2004      $db_for_grades->query( "$GradesQueryString" );

#tgs 8-30-2004	  $NumberOfGrades = 0;
	
#tgs 8-30-2004      $NumberOfGrades = $db_for_grades->num_rows();
	
#tgs 8-30-2004      $GradesID = ( $db_for_grades->get_row() )[0];		

#tgs 8-30-2004      $Students_from_MESSR .= MESSR_MAINT::print_grades_edit_form( $GradesID, $count );
#tgs 8-30-2004    }#if ($PageSide == 2)
	
    $Students_from_MESSR .= "<br><center>";
    $Students_from_MESSR .= qq{ <center><br><a href="stureg_merge_MESSR_data.cgi?ID=$row->{ID}&start=$startPos&oldMergeID1=$oldMergeIDs[1]&oldMergeID2=$oldMergeIDs[2]&oldMergeID3=$oldMergeIDs[3]&oldMergeID4=$oldMergeIDs[4]&oldMergeID5=$oldMergeIDs[5]" title="Click to merge above record with another record" style="color : #FFFFFF; background-color : #777; text-decoration : none; padding:4px; border:1px solid black;" onmouseOver="style.border=('1px solid red');" onmouseOut="style.border=('1px solid black');">Merge with another record&nbsp</center></a><br> };

    $Students_from_MESSR .= qq{ <h2><input align=left type=checkbox checked name=add_to_pre_reg_$count value="add">Add/Update this Pre-Registration Record<br><br><br></h2><hr><br> };
    $Students_from_MESSR .= "</center>";

    $count++;
    $lastID = $row->{ID};
}

#warn "After While\n";
#warn "count $count\n";
#warn "max_count $max_count\n";
#warn "--After While\n";

#$add_button = qq{ <center><br><a href="stureg_confirm_MESSR_data.cgi" onClick="document.form.submit()" style="color : #FFFFFF; background-color : #777; text-decoration : none; padding:4px; border:1px solid black;" onmouseOver="style.border=('1px solid red');" onmouseOut="style.border=('1px solid black');">Add/Update marked students and continue&nbsp</center></a><br><br> };

$add_button = qq{<center><input type=submit value="Add marked students to Pre-Registration list and continue" name="action" ></center><br><br>}; #onClick="return confirm('Add marked students to Pre-Registrations list?')"
$saveall_button = qq{<center><input type=submit value="Save all" name="action" onClick="return confirm('Save all changes?')"></center><br><br>};


MESSR_MAINT::print_header( "MFRI :: Review MESSR Data" , STUREG_MAINT::app_name(), "200%");

print $onLoad; 
print qq{<a style="color:white;font-size:x-large;width:100%;background-color:707070;">Review MESSR Data</a>};    

#print "</table>";
print qq{
    <span style="font-family:sans-serif;font-size:normal">
    <br><p><a style="margin-left=.25in">A total of $num_rows MESSR forms are left to be reviewed, displayed here 5 at a time.</a>
    <p><a style="margin-left=.25in">Please review (and edit as needed) these entries from the MESSR forms.</p>
    <p><a style="margin-left=.25in">If you do not want a particular entry to be sent to the Pre-Registration list, uncheck the corresponding box next to that entry.<br><a style="margin-left=.25in"> When you are finished, click the 'Add Students and continue' button, located at either the top or bottom of the page.</p>
    <hr width="80%"></a>

    <form name="form" action="stureg_confirm_MESSR_data.cgi" method=post>
    $add_button
    $Students_from_MESSR
    $add_button
	<input type=hidden name="PageSide" value=$PageSide>
    <input type=hidden name="start" value=$lastID>
    <input type=hidden name="SCID" value=$SCID>
    <input type=hidden name="count" value=$count>
    </form>
    </span>
};
    
MESSR_MAINT::print_footer();

  
   
