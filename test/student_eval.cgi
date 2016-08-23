#!/usr/bin/perl

#####################################################################
#  STUDENT_EVAL.CGI    ...    Version: 0.8.5     ...     07/15/2001 #
#####################################################################
#  Written by: Brent D. Ely      --> sfbrent@users.sourceforge.net  #
#            : Stuart Johnston   --> stuartj@users.sourceforge.net  #
#  ---------------------------------------------------------------  #
#               (C)  C O P Y R I G H T   N O T I C E                #
#  ---------------------------------------------------------------  #
# This program is free software; you can redistribute it and/or     #
# modify it under the terms of the GNU General Public License       # 
# as published by the Free Software Foundation; either version 2    #
# of the License, or (at your option) any later version.            #
#                                                                   #
# This program is distributed in the hope that it will be useful,   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     #
# GNU General Public License for more details.                      #
#                                                                   #
# You should have received a copy of the GNU General Public License #
# along with this program; if not, write to the Free Software       #
# Foundation, Inc., 59 Temple Place - Suite 330,                    #
# Boston, MA  02111-1307, USA.                                      #
#####################################################################

#####################################################################
# Notes On How This Script Functions on the UTD [Linux] Server:     #
# Your particular security/admin rules may be quite different.      #
#####################################################################
# * File permissions are as follows: (Note: Group is SGAWEB)        #
#   rwxrws--x  student_eval.cgi   brentely  sgaweb   xxxx bytes     #
#   rwxrwx--x  student_eval.html  brentely  sgaweb   xxxx bytes     #
#   rw-rw----  evalfile.dat       brentely  sgaweb   xxxx bytes     #
#   rw-rw----  tempfile.dat       brentely  sgaweb   xxxx bytes     #
#                                                                   #
# * The security of the evaluation datafile is very simple, set the #
#   Other permissions of the .cgi .html and .dat files to --x or 0. #
#   this provides enough security for us - this isn't the Pentagon! #
#   Now, the best way to get this scheme to work is to set the SUID #
#   of the STUDENT_EVAL.CGI file's group permission.                #
#   Type: "chmod g+s student_eval.cgi"                              #
#   this gives the script Group permissions when run from the net,  #
#   enabling it to read/write to the data files while leaving Other #
#   permissions allowing no read/write access whatsoever.           #
#####################################################################

# SET GLOBAL VARIABLES for Script Locations
# - this is very *IMPORTANT*!
  $web_cgi_dir  = "/cgi-bin";
  $web_html_dir = "/webeval";
  $web_img_dir  = "/webeval/images";
  $filename      = "tempfile.txt";
  $evalfilename  = "datafile.txt";
#  $logfilename    = "logfile.dat";

# Require (find and load) the html part of this script
  require("./student_eval.html");

# Parse the incoming form data
# our variable will come out as $form_data{'key'}.
  use CGI qw(:cgi-lib);
  &ReadParse(*form_data);

# Print the html header first in case our server is running poorly.
# Sending the header first avoids timeouts!
# '$| = 1' sets "no buffered output" and flushes the input buffer.
  $| = 1;
  print "Content-type: text/html\n\n";

# Array for holding client servers
# only these servers are permitted to utilize this service.
  @servers = ('utd.edu', 'utdallas.edu');


#############################################
# Begin the Main Function of the script...
#############################################

	# Get the date before naything else
	&get_date;

	# Check refering URL for validity before proceeding
	# Maybe we only want people using campus computers to use this form.
#	&check_server;

	# Log client into usage file (can be used for counter and/or metrics)
#	&log_client;

	# Begin carrying out client request
	# This is the Decision Tree for the entire Script.
	if ($form_data{'method'} eq "view") {
		&view_eval_main;
	}
	elsif ($form_data{'method'} eq "add") {
		&spin_add_eval_page;
	}
	elsif ($form_data{'subject'} eq "CourseEvaluation") {
		&evaluation_submitted;
	}
	elsif ($form_data{'subject'} eq "SearchEvaluations") {
		&search_evaluations;
	}
	elsif (($form_data{'subject'} eq "BestWorst") || ($form_data{'method'} eq "best")) {
		&search_evaluations;
	}
	else {
		print "Sorry: name/value pairs needed. Please try again.";
	}

	# That's all folks.  Application ends here.
	exit;


######################################################################## 
#                         -- Start FUNCTIONS --                        # 
#                            ^^^^^ ^^^^^^^^^                           #
########################################################################

sub get_date
{
	@days = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');
	@months = ('January','February','March','April','May','June','July','August','September','October','November','December');

	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$mon += 1; # Corrects the Month number (January=0!)
	if ($hour < 10) { $hour = "0$hour"; }
	if ($min  < 10) { $min  = "0$min";  }
	if ($sec  < 10) { $sec  = "0$sec";  }
	if ($mon  < 10) { $mon  = "0$mon";  }
	if ($mday < 10) { $mday = "0$mday"; }

	# Calculate 2-digit year CORRECTLY.
	# The UNIX system gives $year as "years since 1900"...
	$finalYear = (1900 + $year);
		@DECS = split(//, $finalYear);
		$year = @DECS[2] . @DECS[3];
	$date = "$days[$wday], $months[$mon] $mday, $finalYear at $hour\:$min\:$sec";
	$shortDate = "$mon/$mday/$year $hour\:$min\:$sec";
}

#                                  _________________________
###################################________B_R_E_A_K________#####################################
#

sub check_server
{
	if ($ENV{'REMOTE_HOST'}) {
		foreach $server (@servers) {
			if ($ENV{'REMOTE_HOST'} =~ /$server/i) {
				$check_server = '1';
			last;
			}
		}
	}
	else {
		$check_server = '0';
	}

	if ($check_server !~ 1) {
		&error('bad_server');
	}
}

#                                  _________________________
###################################________B_R_E_A_K________#####################################
#

sub evaluation_submitted
{
	# Verify that no required fields on the Eval Form were left blank
	if ($form_data{'profsOnFile'} eq "") {
		@required_fields = (profLast,profFirst,courseName,coursePrefix,courseNumber,semester,
							semesterYear,profGrade,descProfComments,studentMajor,studentStatus,studentGPA);
	}
	else {
		@required_fields = (courseName,coursePrefix,courseNumber,semester,
							semesterYear,profGrade,descProfComments,studentMajor,studentStatus,studentGPA);

	}
	
	# Loop through each required field and check it - build a list of misses.
    foreach $require (@required_fields) {
    	if (($form_data{$require} eq "") || ($form_data{$require} eq " ")) {
			push (@error_fields, $require);
			$error = "missing_fields";
		}
	}
	if ($error ne "") {
		&error('missing_fields', @error_fields)
	}

	# If user chose a prof on file already - split the name and use it.
    if ($form_data{'profsOnFile'} ne "") {
    	($ex_lastname, $ex_firstname) = split(/\, /, $form_data{'profsOnFile'});
    	$form_data{'profLast'} = $ex_lastname;
    	$form_data{'profFirst'} = $ex_firstname;
	}

	# Check Course Number validity
	if (($form_data{'courseNumber'} < 1000) || ($form_data{'courseNumber'} > 9999)) {
		&error('coursenumb');
	}
	
	# Submitted Form passed muster with the check routines, so create HTML Thank You! page.
	&return_post_submission;

	# Replace 'NewLine' chars w/ spaces in ProfComments - they screw with the datafile by actually 
	# feeding newline's into the datafile - the whole idea of synchronous access fails fast!
	# Thanks to Matt Wright for this little gem!
	$form_data{'descProfComments'} =~ s/(\s+)?\n+(\s+)?/ /g;
	$form_data{'descProfComments'} =~ s/(\s+)?~+(\s+)?/-/g;   # strip tilde's or we risk death
	
	# Replace any occurence of the "Seven Dirty Words" (plus some more) in the Comments section...
	# Original Seven: sh*t, p*ss, f*ck, c*nt, c*cksucker, motherf*cker and tits.
	# We decided against using this - uncomment these lines if you want employ the filter.
#	$form_data{'descProfComments'} =~ s/shit/sh*t/gi;
#	$form_data{'descProfComments'} =~ s/piss/p*ss/gi;
#	$form_data{'descProfComments'} =~ s/fuck/f*ck/gi;
#	$form_data{'descProfComments'} =~ s/cunt/cu*t/gi;
#	$form_data{'descProfComments'} =~ s/cock/co*k/gi;
#	$form_data{'descProfComments'} =~ s/tits/t*ts/gi;
#	$form_data{'descProfComments'} =~ s/pussy/pu**y/gi;
#	$form_data{'descProfComments'} =~ s/twat/tw*t/gi;

	# Clean-up entered profs Last & First names, and course name
	$form_data{'profLast'}   =~ s/^\s*(.*?)\s*$/$1/;    # strip leading/trailing spaces
	$form_data{'profFirst'}  =~ s/^\s*(.*?)\s*$/$1/;    # strip leading/trailing spaces
	$form_data{'courseName'} =~ s/^\s*(.*?)\s*$/$1/;    # strip leading/trailing spaces
	$form_data{'profLast'}   =~ s/(\s+)?\,+(\s+)?//g;   # strip any comma's
	$form_data{'profFirst'}  =~ s/(\s+)?\,+(\s+)?//g;   # strip any comma's
	$form_data{'profLast'}   = ucfirst(lc($form_data{'profLast'}));   # make Title Case
	$form_data{'profFirst'}  = ucfirst(lc($form_data{'profFirst'}));  # make Title Case

	# Lock the Datafile before we add to it. 
	&GetFileLock ("evalsite.lock");

	# Add Submittors personal info and evaluation to data file...
	# Lock the datafile so no other processes can collide with us!
	# This section is IMPORTANT - DO NOT SCREW WITH THIS BLOCK OF CODE!
	open (FILE, "$filename") || sleep(1);
		@LINES=<FILE>;
	close(FILE);
	$SIZE=@LINES;
	open (FILE, ">$filename") || &CgiDie ("Cannot Open Data File!!");
	print FILE "[$shortDate]~$form_data{'profLast'}~$form_data{'profFirst'}~$form_data{'courseName'}~$form_data{'coursePrefix'} $form_data{'courseNumber'}~$form_data{'semester'}~$form_data{'semesterYear'}~$form_data{'profGrade'}~$form_data{'descProfComments'}~$form_data{'studentMajor'}~$form_data{'studentStatus'}~$form_data{'studentGPA'}\n";
		for ($i=0 ; $i<=$SIZE ; $i++) {
			$_=$LINES[$i];
			print FILE $_;
		}
	close(FILE);
	open (FILE, "$filename") || &CgiDie ("Cannot Open Data File!!!");
		@LINES=<FILE>;
	close(FILE);
	$SIZE=@LINES;
	open (FILE2, ">$evalfilename") || &CgiDie ("Cannot Open Data File!!!");
		for ($i=0 ; $i<=$SIZE ; $i++) {
			$_=$LINES[$i];
			print FILE2 $_;
		}
	close(FILE2);

	# Unlock the Datafile so other processes can add to it. 
	&ReleaseFileLock ("evalsite.lock");
}

#                                  _________________________
###################################________B_R_E_A_K________#####################################
#

sub search_evaluations
{
	# Let's build the array of prof's and their info that matched search criteria provided.
	# Parse each line of the data file and tokenize into variables.
	open(DB, "$filename") || print "No Instructors on File Yet!\n";
		@datafile_lines = <DB>;
	close(DB);

	if (($form_data{'search'} eq "prof") && ($form_data{'profsOnFile'} eq "") && ($form_data{'type'} ne "exact")) {
		# If client did not enter a name to search for, then fail.
		# Create the html document
		&search_results_header;
		print "<font face=Verdana,Geneva size=3 color=blue><br>";
		print "<b>Sorry!</b></font><br> \n";
		print "<font face=Verdana,Geneva size=2 color=black> \n";
		print "You did not choose anything from the Instructor Name menu. <br>\n";
		print "<b>Please click 'Back!' and choose a Name to begin your search!</b> <br> \n";
		print "<form method=post> <input type=button value='Back!' onclick=\'history.back();\'> </form> \n";
		exit(0);
	}
	elsif (($form_data{'search'} eq "prof") && ($form_data{'profsOnFile'} ne "")) {
		# Get Profs Last & First Name
		($form_data{'profLastName'}, $form_data{'profFirstName'}) = split(/\, /, $form_data{'profsOnFile'});
	}

	# Search each and every evaluation in the data file
	foreach $line (@datafile_lines) {
		($enter_date,$prof_last,$prof_first,$course_name,$course_number,$semester,$semester_year,$prof_grade,$prof_comm,$student_major,$student_status,$student_gpa)
		 = split(/\~/,$line);
		($course_prefix,$c_number) = split(/ /i, $course_number);
		$dup = "N";

		# If search conditions match, then add prof into results array
		if ( (($form_data{'search'} eq "prof") && ($prof_last =~ /^$form_data{'profLastName'}/i) &&
												  ($prof_first =~ /^$form_data{'profFirstName'}/i)) ||
			 (($form_data{'search'} eq "dept") && ($form_data{'departmentName'} =~ /^$course_prefix/i)) ||
			 (($form_data{'method'} eq "best") || ($form_data{'subject'} eq "BestWorst")) ) {

			# Now we build arrays of profs and their respective info.
			# If prof is already in the array, add new grade and increase entry count.
			# Loop through profs found so far and look for the current one.
			for ($a=0 ; $a<=@PROFS ; $a++) {
				if ((@PROFS[$a] =~ /^$prof_last/i) && (@PROFSF[$a] =~ /^$prof_first/i)) {
					@GRADES[$a]  += $prof_grade;
					@ENTRIES[$a] += 1;
					$dup = "Y";
				}
			}

			# If prof is already in array, check this particular evals DEPT
			# Some Profs teach in diff depts - display of only one code is not good enough.
			if ($dup eq "Y") {
				for ($a=0 ; $a<=@PROFS ; $a++) {

					if ((@PROFS[$a] =~ /^$prof_last/i) && (@PROFSF[$a] =~ /^$prof_first/i)
						&& (@DEPTS[$a] !~ /$course_prefix/i)) {
						@DEPTS[$a] .= ",";
						@DEPTS[$a] .= $course_prefix;
					}
				}
			}			
			# If prof not already in the array, add them and their info to results arrays.
			else {
				push(@PROFS,   $prof_last);
				push(@PROFSF,  $prof_first);
				push(@GRADES,  $prof_grade);
				push(@DEPTS,   $course_prefix);
				push(@ENTRIES, 1);
			}

			# Match the correct prof using the length of their name
			# - think about 'Ye', 'Ye Win', 'Yewin' etc...
			if (($form_data{'search'} eq "prof") &&
				(length($prof_last) == length($form_data{'profLastName'}))) { 
				$exactMatch = $prof_last;
			}
		}
	}

	# Calculate final grades for profs with more than one eval. We have to
	# wait until all lines are read before we can add all the prof's grades,
	# then divide by the number of evals on file.
	for ($a=0 ; $a<@PROFS ; $a++) {
		$grade = (@GRADES[$a] / @ENTRIES[$a]);
		@GRADES[$a] = $grade;
	}

	if ($form_data{'search'} eq "prof") {
		@GRADES[0] = $grade;
	}

	# Build arrays to show Prof's by descending GPA:
	# InsertionSort our Array of GRADES and keep the corresponding PROFS, PROFSF, and DEPTS.
	# This is the real bitch - easy to sort profs by name or grade, but we have 5 *different*
	# arrays, so we have to maintain the same index for each one. E.g.: prof[1] has grade[1]...
	for ($a=1 ; $a<@GRADES ; $a++) {
		$temp1 = @GRADES[$a];
		$temp2 = @PROFS[$a];
		$temp3 = @PROFSF[$a];
		$temp4 = @DEPTS[$a];
		$temp5 = @ENTRIES[$a];
		
		for ($b=($a-1) ; ($b>=0 && @GRADES[$b]<$temp1) ; $b--) {
			@GRADES[$b+1]  = @GRADES[$b];
			@PROFS[$b+1]   = @PROFS[$b];
			@PROFSF[$b+1]  = @PROFSF[$b];
			@DEPTS[$b+1]   = @DEPTS[$b];
			@ENTRIES[$b+1] = @ENTRIES[$b];
		}
		
		@GRADES[$b+1]  = $temp1;
		@PROFS[$b+1]   = $temp2;
		@PROFSF[$b+1]  = $temp3;
		@DEPTS[$b+1]   = $temp4;
		@ENTRIES[$b+1] = $temp5;
	}

	# Prevent GPA's without decimal precision and/or trim/round GPA's to 2 decimal points.
	for ($a=0 ; $a<@GRADES ; $a++) {
		($intGPA, $decGPA) = split(/\./, @GRADES[$a]);
		@DECS = split(//, $decGPA);

		if ($decGPA == 0) {									# Extend Prec 3. -> 3.00
			@DECS[0] = 0;
			@DECS[1] = 0;
		}
		elsif (length($decGPA) == 1) {						# Extend Prec 3.0 -> 3.00
			@DECS[1] = 0;
		}
		elsif (length($decGPA) > 2) {
			if ((@DECS[1] != 9) && (@DECS[2] >= 5)) {		# Example: 2.885 -> 2.89
				@DECS[1] += 1;								#             ^
			}
			elsif ((@DECS[0] != 9) && (@DECS[2] >= 5)) { 	# Example: 2.895 -> 2.90
				@DECS[0] += 1; 								#            ^
				@DECS[1]  = 0;
			}
			elsif ((@DECS[0] == 9) && (@DECS[1] == 9) &&
										(@DECS[2] >= 5)) { 	# Example: 2.995 -> 3.00
				$intGPA  += 1; 								#            ^
				@DECS[0]  = 0;
				@DECS[1]  = 0;
			}
		}

		@GRADES[$a] = $intGPA.".".@DECS[0].@DECS[1];
	}

	# Done with building search results and sorting them!
	# ---------------------------------------------------
	#              DISPLAY SEARCH RESULTS
	# depending upon which kind of search was instituted..
	# ---------------------------------------------------

	# Display DEPARTMENT results
	if ($form_data{'search'} eq "dept") {
		# Create the html document
		&rank_depts_header;
		print "<table border=0 cellpadding=1 cellspacing=1 width=90% bgcolor=#696969>
				<tr><td align=center><font size=2 color=black> \n";
		print "<table border=0 cellpadding=5 cellspacing=1 width=100% bgcolor=#d2b48c> \n";
		print "<tr><td width=15% bgcolor=Peru align=center><font face=Arial size=2><b> Overall GPA </td>
				<td width=60% bgcolor=Peru align=left><font face=Arial size=2><b> Instructor's Name </td>
				<td width=15% bgcolor=Peru align=center><font face=Arial size=2><b> Instructor's<br>Dept </td>
				<td width=10% bgcolor=Peru align=center><font face=Arial size=2><b> Number of<br>Evaluations </td>
				</tr> \n";

		for ($a=0 ; $a<@PROFS ; $a++) {
			# BUG FIX: names with spaces do not parse correctly when entered as a link variable
			# (get method sucks maybe?) - anyway, replace spaces in a last name with '%20', 
			# and they parse just fine. (i was losing the latter part - 'Van Ness' became 'Van'!)
			$correctNameLink = @PROFS[$a];
			$correctNameLink =~ s/\s/%20/g;

			print "<tr> \n";
			print "<td bgcolor=Tan align=center><font face=Arial size=2> @GRADES[$a] </td>
					<td bgcolor=Wheat><font face=Arial size=2>
					<a href='$web_cgi_dir/student_eval.cgi?subject=SearchEvaluations&search=prof&type=exact&profLastName=$correctNameLink'>@PROFS[$a], @PROFSF[$a]</a></td>
					<td bgcolor=Wheat><center><font face=Arial size=2> @DEPTS[$a] </td>
					<td bgcolor=Tan><center><font face=Arial size=2> @ENTRIES[$a] </td> \n";
			print "</tr> \n";
		}
		print "</table> </table> <br> \n";

		if (@GRADES > 0) {
			print "<font face=Verdana,Arial size=2 color=black>";
			print "Total Instructors Found: <b>$a</b> <br> <br> \n";
			print "<b>Overall GPA</b> is calculated by summing all grades submitted by student evaluators and dividing <br>
			by the number of entries for that particular instructor (Simple Averaging).<br> \n";
		}
		else {
			print "<font face=Verdana,Arial size=2 color=blue><br>";
			print "<b>Sorry!</b> there are currently no instructors evaluated from the $form_data{'departmentName'} department. <br><br> \n";
		}
	}

	# Display PROFFESOR NAME results
	elsif ($form_data{'search'} eq "prof") {
		# Create the html document
		&search_results_header;

		# If not an exact search, create a table of prof's who hit...
		# Display all profs found in the same table format as the 
		# Department Search (i copied this code from that function!)
		if (($form_data{'type'} ne "exact") && (@PROFS >= 1)) { 
			print "<br> <font face=Verdana,Arial size=2> \n";
			print "Your search for Instructor: \"<b>$form_data{'profsOnFile'}</b>\" generated the following hits... <br><br> \n";
			print "<table border=0 cellpadding=1 cellspacing=1 width=90% bgcolor=#696969><tr><td align=center><font size=2 color=black> \n";
			print "<table border=0 cellpadding=5 cellspacing=1 width=100% bgcolor=#d2b48c> \n";
			print "<tr><th width=15% align=center bgcolor=Peru><font face=Arial size=2> Overall GPA </th>
					<th bgcolor=Peru align=left><font face=Arial size=2> Instructor's Name </th>
					<th width=15% bgcolor=Peru><font face=Arial size=2 nowrap> Instructor's<br>Dept </th>
					<th width=10% bgcolor=Peru nowrap><font face=Arial size=2> Number of<br>Evaluations </th></tr> \n";
			for ($a=0 ; $a<@PROFS ; $a++) {
				# BUG FIX: names with spaces do not parse correctly when entered as a link variable
				# (get method sucks maybe?) - anyway, replace spaces in a last name with '%20', 
				# and they parse just fine. (i was losing the latter part - 'Van Ness' became 'Van'!)
				$correctNameLink = @PROFS[$a];
				$correctNameLink =~ s/\s/%20/g;

				print "<tr> \n";
				print "<th bgcolor=Tan><font face=Arial size=2> @GRADES[$a] </th>
						<td bgcolor=Wheat><font face=Arial size=2>
						<a href='$web_cgi_dir/student_eval.cgi?subject=SearchEvaluations&search=prof&type=exact&profLastName=$correctNameLink'>@PROFS[$a], @PROFSF[$a]</a></td>
						<td bgcolor=Wheat><center><font face=Arial size=2> @DEPTS[$a] </td>
						<td bgcolor=Tan><center><font face=Arial size=2> @ENTRIES[$a] </td> \n";
				print "</tr> \n";
			}
			print "</table></table> <br> \n";

			if (@GRADES > 0) {
				print "<font face=Verdana,Geneva size=2 color=black>";
				print "Total Instructors Found: <b>$a</b> <br> \n";
				print "<font color=blue>Click on an Instructor's Name to display all of their Evaluations.</font> <br> <br> \n";
				print "<b>Overall GPA</b> is calculated by summing all grades submitted by student evaluators and dividing <br>
					by the number of entries for that particular instructor (Simple Averaging).<br> \n";
			}
			$profs_found = 1;
		} #end of if PROFS>1

		# Display Exact Match - DEATAILED TABLE CODE HERE!
		# We were sent the exact prof to search for... display those cool little detailed tables.
		elsif ($form_data{'type'} eq "exact") {

			# Display prof's LastName[form], Overall GPA, and Instructors Statement (if any).
			&instructor_header;

			# Parse each line of the file and break it into tokens/variables.
			foreach $line (@datafile_lines) {
				$proceed = "N";
				# Break each line in the data file into its composite variables - Tokenize!
				($enter_date,$prof_last,$prof_first,$course_name,$course_number,$semester,$semester_year,$prof_grade,$prof_comm,$student_major,$student_status,$student_gpa)
				 = split(/\~/, $line);

				# Shorten "Graduate Student" to just "Graduate" to occupy less real estate.
				if ($student_status =~ /^Graduate/i) {
					$student_status = "Graduate";
				}

				if ($enter_date =~ /\[(.*)\]/) {
					$date = $1;
					($datestamp,$clock) = split(/ /,$date);
				}
				
				if ($prof_last =~ /^$exactMatch/i) {	
					$proceed = "Y";
					$profs_found++;
				}
				
				# If "Professor's Last Name" matches, create a table and display it.
				if ($proceed eq "Y") {
					$profs_found_so_far++;

					# Color-code the top row of table showing eval data - Good idea Mo!
					if    ($prof_grade  < 2) { $var_bg_color = "Red"; }
					elsif ($prof_grade  < 3) { $var_bg_color = "Yellow"; }
					elsif ($prof_grade <= 4) { $var_bg_color = "LimeGreen"; }	#32CD32

					# Calculate Letter Grade before sending data to table function
#					if    ($prof_grade == 4)   { $prof_grade = "A";  }
#					elsif ($prof_grade == 3.5) { $prof_grade = "B+"; }
#					elsif ($prof_grade == 3)   { $prof_grade = "B";  }
#					elsif ($prof_grade == 2.5) { $prof_grade = "C+"; }
#					elsif ($prof_grade == 2)   { $prof_grade = "C";  }
#					elsif ($prof_grade == 1.5) { $prof_grade = "D+"; }
#					elsif ($prof_grade == 1)   { $prof_grade = "D";  }
#					elsif ($prof_grade == 0)   { $prof_grade = "F";  }

					# Extend GPA Precision if necessary
					($intGPA, $decGPA) = split(/\./, $prof_grade);
					@DECS = split(//, $decGPA);
					if (length($decGPA) == 0) {			# Extend Prec 0 -> 0.00
						@DECS[0] = 0;
						@DECS[1] = 0;
					}
					elsif (length($decGPA) == 1) {		# Extend Prec 3.0 -> 3.00
						@DECS[1] = 0;
					}
					$prof_grade = $intGPA.".".@DECS[0].@DECS[1];

					# Call subroutine that builds HTML table code..
					# the variables above will be filled in by this sub routine - SWEET!
					&search_results_table;
				}
			} #end of foreach
		} #end of elsif type=exact

		# Prof Name Search came up with nothing...
		if (($profs_found == 0) || (@PROFS == 0)) {
			print "<font face=Verdana,Geneva size=3 color=blue><br>";
			print "<b>Sorry!</b></font><br> \n";
			print "<font face=Verdana,Geneva size=2 color=black> \n";
			print "there are currently no instructors in the database that match \"<b>$form_data{'profLastName'}</b>\". <br>\n";
			print "<ul> \n";
			print "<li> <b>Please check the spelling of the instructor's name.</b> <br><br> \n";
			print "<li> You can enter only the first few letters of an instructor's last name to begin your search! <br><br> \n";
			print "<li> If the instructor you are searching for is not in the database, why not add them using our \n";
			print "<a href=\"$web_cgi_dir/student_eval.cgi?method=add\">Online Evaluation Form</a>? <br><br> </font> \n";
			print "</ul> \n";
		}
	} #end of elsif search=prof

	# Display BEST 15 results
	elsif (($form_data{'subject'} eq "BestWorst") || ($form_data{'method'} eq "best") || ($form_data{'method'} eq "")) {
		# Best 15 Table
		&bestworst_header;
		print "<font face=Arial,Arial,Verdana size=+1> <b>Best 15 Instructors By GPA</b> <br> \n";
		print "<font size=2><br> \n";
		print "<table border=0 cellpadding=1 cellspacing=1 width=90% bgcolor=#696969><tr><td align=center><font size=2 color=black> \n";
		print "<table border=0 cellpadding=5 cellspacing=1 width=100% bgcolor=#d2b48c> \n";
		print "<tr><th width=15% align=center bgcolor=Peru><font face=Arial size=2> Overall GPA </th>
				<th bgcolor=Peru align=left><font face=Arial size=2> Instructor's Name </th>
				<th width=15% bgcolor=Peru><font face=Arial size=2 nowrap> Instructor's<br>Dept </th>
				<th width=10% bgcolor=Peru nowrap><font face=Arial size=2> Number of<br>Evaluations </th></tr> \n";
		for ($a=0 ; ($a<15 && @GRADES[$a] ne "") ; $a++) {
			print "<tr> \n";
			print "<th bgcolor=Tan><font face=Arial size=2> @GRADES[$a] </th>
					<td bgcolor=Wheat><font face=Arial size=2>
					<a href='$web_cgi_dir/student_eval.cgi?subject=SearchEvaluations&search=prof&type=exact&profLastName=@PROFS[$a]'>@PROFS[$a], @PROFSF[$a]</a> </td>
					<td bgcolor=Wheat><center><font face=Arial size=2> @DEPTS[$a] </td>
					<td bgcolor=Tan><center><font face=Arial size=2> @ENTRIES[$a] </td> \n";
			print "</tr> \n";
		}
		print "</table></table> <br> \n";

		# The Worst (lowest GPA) 15 Table
		print "<font face=Arial,Arial,Verdana size=+1> <b>Worst 15 Instructors By GPA</b> <br> \n";
		print "<font size=2><br> \n";
		print "<table border=0 cellpadding=1 cellspacing=1 width=90% bgcolor=#696969><tr><td align=center><font size=2 color=black> \n";
		print "<table border=0 cellpadding=5 cellspacing=1 width=100% bgcolor=#d2b48c> \n";
		print "<tr><th width=15% align=center bgcolor=Peru><font face=Arial size=2> Overall GPA </th>
				<th bgcolor=Peru align=left><font face=Arial size=2> Instructor's Name </th>
				<th width=15% bgcolor=Peru><font face=Arial size=2 nowrap> Instructor's<br>Dept </th>
				<th width=10% bgcolor=Peru nowrap><font face=Arial size=2> Number of<br>Evaluations </th></tr> \n";
		if (@GRADES < 15) {
			for ($a=0 ; ($a<@GRADES && @GRADES[$a] ne "") ; $a++) {
				$correctNameLink = @PROFS[$a];
				$correctNameLink =~ s/\s/%20/g;
				print "<tr> \n";
				print "<th bgcolor=Tan><font face=Arial size=2> @GRADES[$a] </th>
						<td bgcolor=Wheat><font face=Arial size=2>
						<a href='$web_cgi_dir/student_eval.cgi?subject=SearchEvaluations&search=prof&type=exact&profLastName=$correctNameLink'>@PROFS[$a], @PROFSF[$a]</a> </td>
						<td bgcolor=Wheat><center><font face=Arial size=2> @DEPTS[$a] </td>
						<td bgcolor=Tan><center><font face=Arial size=2> @ENTRIES[$a] </td> \n";
				print "</tr> \n";
			}
		}
		else {
			for ($a=(@GRADES-15) ; ($a<@GRADES && @GRADES[$a] ne "") ; $a++) {
				$correctNameLink = @PROFS[$a];
				$correctNameLink =~ s/\s/%20/g;
				print "<tr> \n";
				print "<th bgcolor=Tan><font face=Arial size=2> @GRADES[$a] </th>
						<td bgcolor=Wheat><font face=Arial size=2>
						<a href='$web_cgi_dir/student_eval.cgi?subject=SearchEvaluations&search=prof&type=exact&profLastName=$correctNameLink'>@PROFS[$a], @PROFSF[$a]</a> </td>
						<td bgcolor=Wheat><center><font face=Arial size=2> @DEPTS[$a] </td>
						<td bgcolor=Tan><center><font face=Arial size=2> @ENTRIES[$a] </td> \n";
				print "</tr> \n";
			}
		}
		print "</table></table> <br> \n";

		print "<font face='Verdana,Arial' size=2 color=black>";
		print "<b>Overall GPA</b> is calculated by summing all grades submitted by student evaluators and dividing <br> \n";
		print "by the number of entries for that particular instructor (Simple Averaging).<br> \n";
	} #end of search=best

&disclaimer_footer;
&search_results_footer;
}


#                                  _________________________
###################################________B_R_E_A_K________#####################################
#

sub error
{
	($error,@error_fields) = @_;

	$client_server = $ENV{'REMOTE_HOST'};
	$client_address = $ENV{'REMOTE_ADDR'};
	
	if ($error eq 'bad_server') {
		print "<html>\n <title>Oops - Access Denied!</title> \n <body bgcolor=white> \n";
		print "<br><center><font face=Arial size=4>Houston, We Have A Problem!</font> \n";
		print "<font face=Arial size=3>It's $date, do you where your server is? \n";
		print "<br><hr align=center width=85%><br> \n";
		print "<h3>For security reasons, only clients accessing this service through a UTD server are allowed.</h3> \n";
		print "<br><hr align=center width=85%> \n";
		print "<h3>Your server is: <font color=red> $client_server </font> \n";
		print "</center> \n </body> \n </html> \n";
	}

	elsif ($error eq 'email') {
		print "<html>\n <head><title>Oops - Bad Email Address!</title></head> \n";
		print "<body bgcolor=white>\n <br><center> \n";
		print "<font face=Arial><font size=5>Error: Bad Email Address</font><hr width=80%> \n";
		print "<font size=3>The email address you entered is not valid.<br> \n";
		print "<br>Please enter a COMPLETE email address.  \n";
		print "Example: <font color=blue><b>cooldude\@utdallas.edu</b> <br> \n";
		print "<FORM><INPUT TYPE=\"button\" VALUE=\"Back To Form\" onclick=\"history.back();\"></FORM> \n";
		print "</center> \n </body> \n </html> \n";
	}

	elsif ($error eq 'coursenumb') {
		print "<html>\n <head><title>Oops - Bad Course Number!</title></head> \n";
		print "<body bgcolor=white>\n <br><center> \n";
		print "<font face=Arial><font size=5 color=red>Error: Bad Course Number</font><hr width=80%> \n";
		print "<font size=3>The course number you entered is not valid.<br> \n";
		print "<FORM><INPUT TYPE=\"button\" VALUE=\"Back To Form\" onclick=\"history.back();\"></FORM> \n";
		print "</center> \n </body> \n </html> \n";
	}

	elsif ($error eq 'missing_fields') {
		print "<html><head><title>Oops - Missing Fields!</title></head> \n";
		print "<!-- Page generated on $date by UTD SGA Student Eval Site --> \n";
		print "<body bgcolor=white><br><center> \n";
		print "<font face=Arial> <font size=5 color=red>Error: Missing Fields</font><hr width=80%> \n";
		print "<font size=3>The following fields need to be filled-in before this form can be submitted: \n";
		print "<font size=2><ul> \n";
		foreach $missing_field (@error_fields) {
			print "<li>";
               	if (($missing_field) eq "profLast") {
					print "Please fill in the Instructor's Last Name.\n";
				}
				elsif (($missing_field) eq "profFirst") {
					print "Please fill in the Instructor's First Name.\n";
				}
				elsif (($missing_field) eq "courseName") {
					print "Please fill in the Course Name.\n";
				}
				elsif (($missing_field) eq "coursePrefix") {
					print "Please fill in the Course Prefix.\n";
				}
				elsif (($missing_field) eq "courseNumber") {
					print "Please fill in the Course Number.\n";
				}
				elsif (($missing_field) eq "semester") {
					print "Please fill in the Semester.\n";
				}
				elsif (($missing_field) eq "semesterYear") {
					print "Please fill in the Semester Year.\n";
				}
				elsif (($missing_field) eq "profGrade") {
					print "Please fill in a Instructor Grade.\n";
				}
				elsif (($missing_field) eq "descProfComments") {
					print "Please fill in some Instructor Comments.\n";
				}
				elsif (($missing_field) eq "studentLast") {
					print "Please fill in Your Last Name.\n";
				}
				elsif (($missing_field) eq "studentFirst") {
					print "Please fill in Your First Name.\n";
				}
				elsif (($missing_field) eq "studentEmail") {
					print "Please fill in Your Email Address.\n";
				}
				elsif (($missing_field) eq "studentMajor") {
					print "Please fill in Your Major.\n";
				}
				elsif (($missing_field) eq "studentStatus") {
					print "Please fill in Your Status.\n";
				}
				elsif (($missing_field) eq "studentGPA") {
					print "Please fill in Your GPA.\n";
				}
		}
		print "</ul><br><hr align=center width=80%> \n";
		print "Please enter the required information into these fields and resubmit your form. \n";
		print "<FORM><INPUT TYPE=\"button\" VALUE=\"Back To Form\" onclick=\"history.back();\"></FORM> \n";
		print "<br></center> \n </body> \n </html> \n";
	}
	exit(0);
}


#                                  _________________________
###################################________B_R_E_A_K________#####################################
#

sub insert_prof_list
{
	# This func is called from student_eval.html and creates an HTML <select>
	# widget of Professor Names already on file.
	open(DB, "$filename");
		@datafile_lines = <DB>;
	close(DB);

	# Populate HTML <select> list.
	print "<select name=\"profsOnFile\" size=\"1\"  onchange=\"clear_name(this.form)\"> \n";
	print "<option value=\"\" selected>Choose an Instructor...\n";

	foreach $line (@datafile_lines) {
		($enter_date,$prof_last,$prof_first,$course_name,$course_number,$semester,$semester_year,$prof_grade,$prof_comm,$student_major,$student_status,$student_gpa) = split(/\~/,$line);
		push(@PROF_LASTS, $prof_last);
		push(@PROF_FIRSTS, $prof_first);
	}

	for ($a=0 ; $a<@PROF_LASTS; $a++) {
		@PROF_FINAL[$a] = @PROF_LASTS[$a] . ", " . @PROF_FIRSTS[$a];
	}

	# Sort into 2-dimensional array to eliminate dups and to count
	# (counting not necessary yet though).
	foreach (@PROF_FINAL) {
		$final{($_)[0]}++;
	}

	foreach (sort keys %final) {
		print "<option value=\"$_\">$_\n";
	}
	print "</select>";
}


#                                  _________________________
###################################________B_R_E_A_K________#####################################
#

sub GetFileLock
{
	my $lock_file = $_;
	sleep (2);
	while (-e $lock_file) {
		sleep (2);
	}
	open (LOCKED, ">$lock_file");
	close (LOCKED);
}


#                                  _________________________
###################################________B_R_E_A_K________#####################################
#

sub ReleaseFileLock
{
	my $lock_file = $_;
	unlink ($lock_data);
}


#                                  _________________________
###################################________B_R_E_A_K________#####################################
#

sub log_client
{
	open(LOGFILE, ">>$logfilename") || die $!;
	print LOGFILE "[$shortDate]~$ENV{'REMOTE_HOST'}~$ENV{'REMOTE_ADDR'}~$ENV{'HTTP_USER_AGENT'}~$form_data{'method'}~$form_data{'subject'}~$form_data{'type'}\n";
	close(LOGFILE);
}

