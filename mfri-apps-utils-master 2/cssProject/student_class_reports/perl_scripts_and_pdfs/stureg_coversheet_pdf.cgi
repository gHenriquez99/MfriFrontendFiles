#!/usr/bin/perl

use MFRI;
use MFRI_APPS;
use STUREG_MAINT;
use SEMINAR_MAINT;
use Database;
use CGI;
use SCHEDULE_MAINT;
use strict;

#The two modules needed for drawing PDF documents
use PDF::Reuse;
use PDF_DRAW;




my $ScheduledCourseID = CGI::param( 'SCID' );
$ScheduledCourseID = 0 if (not defined $ScheduledCourseID);

if(!MFRI::is_authenticated())
{
	MFRI::set_parameter( "error", "You must be logged in to use the system." );
	MFRI::redirect( "error.cgi" );
	exit;
}

my $ScheduleInfo = SCHEDULE_MAINT::get_schedule_info_by_id_new($ScheduledCourseID);

print_doc_header();

PDF_DRAW::set_font_size(45);

#Get the info that we will be printing to the screen.
my $title = $ScheduleInfo->{Title};
my $start_date = $ScheduleInfo->{StartDate};
my $location = $ScheduleInfo->{LocationName};
my $course_number_new = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 0);
my $course_number_old = STUREG_MAINT::get_log_number_by_id($ScheduledCourseID, 1);

#Format the date into something that's more sane.
$start_date =~ /(\d+)-(\d+)-(\d+)/;
$start_date = "$2-$3-$1" if ($start_date ne "");

#Get the base offset for printing the text
my $baseX = 515;
my $baseY = 525;

#Print all of our text centered on the screen with reasonable spacing.
PDF_DRAW::center_text($baseX, $baseY, $title);
$baseY -= 75;
PDF_DRAW::center_text($baseX, $baseY, $start_date);
$baseY -= 75;
PDF_DRAW::center_text($baseX, $baseY, $location);
$baseY -= 75;
PDF_DRAW::center_text($baseX, $baseY, $course_number_new);
$baseY -= 75;
PDF_DRAW::center_text($baseX, $baseY, $course_number_old);
$baseY -= 75;

print_doc_footer();

#Print all the stuff that is needed to start up a PDF file
sub print_doc_header
{
    print "Content-type: application/pdf\n\n";
    prFile();
    prMbox(0, 0, 1029, 836);
    PDF_DRAW::set_font(PDF_DRAW::get_default_font());
}

#Close up our PDF file and print it to the screen
sub print_doc_footer
{
    prEnd();
}


