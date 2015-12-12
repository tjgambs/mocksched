# -*- coding: UTF-8 -*-

#Created by Timothy Gamble
#mocksched@gmail.com

from BeautifulSoup import BeautifulSoup as Soup
import urllib
import json
import csv
import os
import unidecode
import rmp_reviews

#The id number of your school can be found in the ratemyprofessor link. For example
#the link of a universities page might look like this: 
#		http://www.ratemyprofessors.com/campusRatings.jsp?sid=1389
#The universities id number would be 1389, the number following 'sid='.
school_id_number = '1389'

#Please specify how many teachers you want in your data set. You can have all of 
#them if you enter in 'all' or you can enter in a number with in quotations.
#	Either this: how_many_teachers = '10'
#	or this: how_many_teachers = 'all'
how_many_teachers = 'all' 

#Write true next to the items you want to have and false to the items you do not want.
teacher_id 			= True
teacher_first_name 		= True
teacher_last_name 		= True
number_of_ratings 		= True
overall_rating 			= True
helpfulness_rating 		= True
clarity_rating 			= True
easiness_rating 		= True

#Creates a url with the predefined url parameters.
def generate_url():
	url ='http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=10&callback=jQuery111003276446736417711_1446762506495&q=*%3A*+AND+schoolid_s%3A' + school_id_number + '&defType=edismax&qf=teacherfullname_t%5E1000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=&siteName=rmp&rows='	
	
	#Adds the amount of teachers wanted to a url paramater
	if(how_many_teachers.lower() == 'all'):
		url += total_teachers() + '&start=0&fl='
	else:
		url += how_many_teachers + '&start=0&fl='

	#Adds the url parameters as specified above
	if(teacher_id):
		url += 'pk_id+'
	if(teacher_first_name):
		url += 'teacherfirstname_t+'
	if(teacher_last_name):
		url += 'teacherlastname_t+'
	if(number_of_ratings):
		url += 'total_number_of_ratings_i+'
	if(overall_rating):
		url += 'averageratingscore_rf+'
	if(helpfulness_rating):
		url += 'averagehelpfulscore_rf+'
	if(clarity_rating):
		url += 'averageclarityscore_rf+'
	if(easiness_rating):
		url += 'averageeasyscore_rf+'
	if(url[-1] == '+'): 
		url = url[:-1]
	return url

#Takes the url generated and takes all of the data to be formatted.
def gather_data():
	url = generate_url()
	#Formats the data to be used in a list
	page_content = urllib.urlopen(url).read()
	begin = page_content.index('"docs":')+7

	#Characters with accents screwing everything up
	page = page_content[begin:-5].replace('í','i') 
	data = json.loads(page)

	#Creates a url for each professor, this is where all of the student reviews can be found
	for key in data:
		key['teacher_profile'] = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='+ str(key['pk_id'])
		key['univerity_id'] = str(school_id_number)
	
	return data

#Totals all of the teachers that are associated with the specified university
def total_teachers():
	url = 'http://search.mtvnservices.com/typeahead/suggest/?callback=jQuery11100050687990384176373_1446754108140&q=*:*+AND+schoolid_s:' + school_id_number + '&siteName=rmp'
	page_content = urllib.urlopen(url).read()

	begin = page_content.index('"numFound":')+11
	end = page_content.index(',"start":')

	return page_content[begin:end]

#Takes all of the data and stores it in a csv called teachers.csv
def export_to_csv():
	data = gather_data()
	keys = data[0].keys()

	with open('../teachers.csv', 'wb') as output_file:
	    dict_writer = csv.DictWriter(output_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(data)

def create_teacher_webpage(id,name,values):
	if (values[0] == '0' or values[0] == '0.0'): return
	if (os.path.exists('../teachers/' + name.replace(' ','-').replace('/','').lower() + '.html')): return
	reviews = rmp_reviews.format_reviews(id)
	name = name.encode('utf-8').replace('í','i')
	print name

	with open('../teachers/' + name.replace(' ','-').replace('/','').lower() + '.html','w') as output:
		html = '<!DOCTYPE html><html><head><title>' + name + ' - ' + values[0] + '</title>'
		html +=	'''<meta charset="UTF-8">
					<script src="../../../js/jquery.min.js"></script>
					<script src="../../../js/select2.full.js"></script>
					<script src="../js/teacher-pages.min.js"></script>

				    <link href="../../../css/select2.css" rel="stylesheet"/>
					<link rel="stylesheet" href="../../../css/stylesheet.css" type="text/css" media="print, projection, screen" />
					<script type="text/javascript" src="../../../js/jquery.tablesorter.min.js"></script>
					<link href="http://fonts.googleapis.com/css?family=Open+Sans:300,400|Merriweather:300,300italic" rel="stylesheet">
					<link rel="shortcut icon" href="../../../icon.png">
				    <link rel="stylesheet" id="tipue3" type="text/css" href="../../../css/tipuesearch.css">
					<script>
						(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
						(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
						m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
						})(window,document,'script','http://www.google-analytics.com/analytics.js','ga');
						ga('create', 'UA-70030211-1', 'auto');
						ga('send', 'pageview');
					 </script>
				</head>
						<style type="text/css">img.alignleft{ float: left; 
									margin: 0 1em 1em 0;}.alignleft{ float: left; }#left{width: 200px;height: 150px;float: left;padding-bottom:30px;padding-top: 20px;}
									#right{height: 150px;margin-left: 200px; padding-bottom: 30px;padding-top: 20px;}</style><body id="body">
				<div>
					<span>
					<h3>
						<a href="../course-cart" style="text-decoration:none; float:right; color:#333;" id="course-cart">Course Cart (0)</a>
						<div style="color:#333; float:right;">&nbsp;|&nbsp;</div>
						<a href="javascript:;" style="text-decoration:none; color:#333; float:right;" onclick="help()">Help</a>
					</h3>
					</span>
					<span>
						<h1 style="float:left; padding: 0px; padding-right:2%;"><a href="../search" style="text-decoration:none; color:#333;">MockSched</a></h1>
						<div id="search-box" style="visibility: hidden;">
						<div style="display: inline-block; padding-right:10px">
							<select class="prefix" style="width:200px;">
								<option value="ACC">ACC - Accountancy</option>
								<option value="A&amp;S">A&amp;S - Administration &amp; Supervision</option>
								<option value="ABD">ABD - African&amp;Black Diaspora Studies</option>
								<option value="AHT">AHT - Allied Health Technology</option>
								<option value="ASL">ASL - American Sign Language</option>
								<option value="AMS">AMS - American Studies</option>
								<option value="ANI">ANI - Animation</option>
								<option value="ANT">ANT - Anthropology</option>
								<option value="APB">APB - Applied Brass</option>
								<option value="APK">APK - Applied Keyboard</option>
								<option value="APM">APM - Applied Music</option>
								<option value="APP">APP - Applied Percussion</option>
								<option value="AP">AP - Applied Professional Studies</option>
								<option value="APS">APS - Applied Strings</option>
								<option value="AT">AT - Applied Technology</option>
								<option value="APV">APV - Applied Voice</option>
								<option value="APW">APW - Applied Woodwinds</option>
								<option value="ARB">ARB - Arabic</option>
								<option value="ART">ART - Art</option>
								<option value="HAA">HAA - Art And Architecture, History Of</option>
								<option value="AI">AI - Arts And Ideas</option>
								<option value="BBE">BBE - Bilingual-Bicultural Education</option>
								<option value="BIO">BIO - Biological Sciences</option>
								<option value="BLW">BLW - Business Law</option>
								<option value="CTH">CTH - Catholic Studies</option>
								<option value="CTU">CTU - Catholic Theological Union</option>
								<option value="CHE">CHE - Chemistry</option>
								<option value="CHN">CHN - Chinese</option>
								<option value="CMN">CMN - Communication</option>
								<option value="CMNS">CMNS - Communication Studies</option>
								<option value="CSS">CSS - Community Service Studies</option>
								<option value="CPL">CPL - Comparative Literature</option>
								<option value="COM">COM - Composition</option>
								<option value="GPH">GPH - Computer Graphics &amp; Motion Technology</option>
								<option value="CSC">CSC - Computer Science</option>
								<option value="CNS">CNS - Computer, Information And Network Security</option>
								<option value="CCA">CCA - Core Curriculum Arts And Ideas</option>
								<option value="CCH">CCH - Core Curriculum Human Community</option>
								<option value="CCS">CCS - Core Curriculum Scientific World</option>
								<option value="CSL">CSL - Counseling</option>
								<option value="CES">CES - Critical Ethnic Studies</option>
								<option value="CS">CS - Curriculum Studies</option>
								<option value="DA">DA - Decision Analytics</option>
								<option value="DES">DES - Design</option>
								<option value="DC">DC - Digital Cinema</option>
								<option value="DHS">DHS - Digital Humanities</option>
								<option value="DMA">DMA - Digital Media Arts</option>
								<option value="ECE">ECE - Early Childhood Education</option>
								<option value="ECT">ECT - E-Commerce Technology</option>
								<option value="ECO">ECO - Economics</option>
								<option value="EA">EA - Educating Adults</option>
								<option value="EDU">EDU - Education - General</option>
								<option value="EE">EE - Elementary Education</option>
								<option value="ENG">ENG - English</option>
								<option value="ELA">ELA - English Language Academy</option>
								<option value="ENV">ENV - Environmental Science</option>
								<option value="EXP">EXP - Experience Design</option>
								<option value="FIN">FIN - Finance</option>
								<option value="FA">FA - Focus Area</option>
								<option value="FCH">FCH - French</option>
								<option value="GAM">GAM - Game Development</option>
								<option value="GEO">GEO - Geography</option>
								<option value="GER">GER - German</option>
								<option value="AAS">AAS - Global Asian Studies</option>
								<option value="GSB">GSB - Graduate School Of Business</option>
								<option value="GD">GD - Graphic Design</option>
								<option value="GRK">GRK - Greek</option>
								<option value="HTHC">HTHC - Health Communication</option>
								<option value="HIT">HIT - Health Information Technology</option>
								<option value="HLTH">HLTH - Health Science</option>
								<option value="HST">HST - History</option>
								<option value="HON">HON - Honors</option>
								<option value="HSP">HSP - Hospitality Leadership</option>
								<option value="HCD">HCD - Human Centered Design</option>
								<option value="HC">HC - Human Community</option>
								<option value="HCI">HCI - Human-Computer Interaction</option>
								<option value="ICE">ICE - Illinois Institute Of Technology</option>
								<option value="ILL">ILL - Illustration</option>
								<option value="IS">IS - Information Systems</option>
								<option value="IT">IT - Information Technology</option>
								<option value="IPD">IPD - Institute For Professional Development</option>
								<option value="IN">IN - Integrative Learning</option>
								<option value="ISM">ISM - Interactive And Social Media</option>
								<option value="IM">IM - Interactive Media</option>
								<option value="INTC">INTC - Intercultural Communication</option>
								<option value="ICS">ICS - Interdisciplinary Commerce Studies</option>
								<option value="IDS">IDS - Interdisciplinary Studies</option>
								<option value="ISP">ISP - Interdisciplinary Studies Program</option>
								<option value="IB">IB - International Business</option>
								<option value="INT">INT - International Studies</option>
								<option value="IRE">IRE - Irish Studies</option>
								<option value="IWS">IWS - Islamic World Studies</option>
								<option value="ITA">ITA - Italian</option>
								<option value="JPN">JPN - Japanese</option>
								<option value="JZZ">JZZ - Jazz Studies</option>
								<option value="JOUR">JOUR - Journalism</option>
								<option value="LE">LE - Labor Education</option>
								<option value="LAT">LAT - Latin</option>
								<option value="LST">LST - LatinAmerican &amp; Latino Studies</option>
								<option value="LAW">LAW - Law</option>
								<option value="LGQ">LGQ - Lesbian, Gay, Bisexual, Transgender, Queer Studies</option>
								<option value="LLS">LLS - Liberal Learning Seminars</option>
								<option value="LSE">LSE - Liberal Studies In Education</option>
								<option value="LSP">LSP - Liberal Studies Program</option>
								<option value="LL">LL - Lifelong Learning</option>
								<option value="LSI">LSI - Literacy &amp; Specialized Instruction</option>
								<option value="MGT">MGT - Management</option>
								<option value="MIS">MIS - Management Information Systems</option>
								<option value="MKT">MKT - Marketing</option>
								<option value="MPH">MPH - Master Of Public Health</option>
								<option value="MSW">MSW - Masters In Social Work</option>
								<option value="MLS">MLS - Masters Of Liberal Studies</option>
								<option value="MAT">MAT - Mathematical Sciences</option>
								<option value="MMT">MMT - Mathematics For Middle School Teaching</option>
								<option value="MCS">MCS - Media Studies</option>
								<option value="MGE">MGE - Middle Grades Education</option>
								<option value="MSC">MSC - Military Science</option>
								<option value="MOL">MOL - Modern Languages</option>
								<option value="MED">MED - Music Education</option>
								<option value="MEN">MEN - Music Ensemble</option>
								<option value="MUS">MUS - Musicianship</option>
								<option value="NMS">NMS - New Media Studies</option>
								<option value="NSG">NSG - Nursing</option>
								<option value="ORGC">ORGC - Organizational Communication</option>
								<option value="PAX">PAX - Peace, Justice And Conflict Studies</option>
								<option value="PRF">PRF - Performance</option>
								<option value="PAM">PAM - Performing Arts Management</option>
								<option value="PHL">PHL - Philosophy</option>
								<option value="PE">PE - Physical Education</option>
								<option value="PHY">PHY - Physics</option>
								<option value="POL">POL - Polish</option>
								<option value="PSC">PSC - Political Science</option>
								<option value="POR">POR - Portuguese</option>
								<option value="PM">PM - Project Management</option>
								<option value="PSY">PSY - Psychology</option>
								<option value="PPS">PPS - Public Policy Studies</option>
								<option value="PRAD">PRAD - Public Relations And Advertising</option>
								<option value="MPS">MPS - Public Services</option>
								<option value="RE">RE - Real Estate</option>
								<option value="FMS">FMS - Refugee And Forced Migration Studies</option>
								<option value="RELC">RELC - Relational Communication</option>
								<option value="REL">REL - Religious Studies</option>
								<option value="RUS">RUS - Russian</option>
								<option value="STEM">STEM - Science, Technology, Engineering And Math</option>
								<option value="SW">SW - Scientific World</option>
								<option value="SEC">SEC - Secondary Education</option>
								<option value="DCM">DCM - SNL Degree Completion Major</option>
								<option value="SNC">SNC - SNL Liberal Studies</option>
								<option value="SCG">SCG - Social &amp; Cultural Studies Ed Human Dev Grad</option>
								<option value="SCU">SCU - Social/Cultural Studies Education/Human Dev Ugrd</option>
								<option value="SOC">SOC - Sociology</option>
								<option value="SE">SE - Software Engineering</option>
								<option value="REC">REC - Sound Recording Technology</option>
								<option value="SPN">SPN - Spanish</option>
								<option value="SEV">SEV - Strategy Execution Valuation</option>
								<option value="SAP">SAP - Study Abroad Program</option>
								<option value="SUD">SUD - Sustainable Urban Development</option>
								<option value="TCH">TCH - TEACH Program</option>
								<option value="T&amp;L">T&amp;L - Teaching And Learning</option>
								<option value="TDC">TDC - Telecommunications</option>
								<option value="TV">TV - Television Production</option>
								<option value="THE">THE - Theatre Studies</option>
								<option value="TEC">TEC - Theatre Technology</option>
								<option value="UIP">UIP - University Internship Program</option>
								<option value="VFX">VFX - Visual Effects</option>
								<option value="WGS">WGS - Women's And Gender Studies</option>
								<option value="WLE">WLE - World Language Education</option>
								<option value="MWR">MWR - Writing</option>
								<option value="WRD">WRD - Writing Rhetoric And Discourse</option>
							</select>
						</div>
						<div style="display: inline-block; padding-right:10px">
							<input type="text" class="number inputbox" placeholder="NUMBER" style="width:100px;">
						</div>
						<div style="display: inline-block;">
							<div style="style=padding: 5%;">
								<form onsubmit="submitForm()" action="../search" id="field">
									<input class="inputbox" type="hidden" name="q" id="tipue_search_input" autocomplete="off" required value="">
									<input class="inputbox" type="submit" value="SEARCH">
								</form>
							</div>
						</div>
						</div>
					</span>
				<div>
				<br />
				<hr>
				<div id="overlay">
				<div id="advanced-container">
	        <form action="../search">
				<input type="text" name="q" id="tipue_search_input" autocomplete="off" required style="width: 100%" placeholder="Enter a Professor, Course Title, or General Keyword">
			</form>
			<h2 align="left" style="padding-top: 10px; color: #aaa; font-size: 12px;">
			If searching for a phrase, please surround the phrase in quotation marks (i.e. "Computer Science"). In doing so, you will receive more accurate results.
			</h2>
			<h2 align="center" style="padding-top: 10px;">
				Filter Courses by Credit Hour
			</h2>
			<p align="center">
				<select class="credit-prefix" style="width:50%">
					<option value="ACC">ACC - Accountancy</option>
					<option value="A&amp;S">A&amp;S - Administration &amp; Supervision</option>
					<option value="ABD">ABD - African&amp;Black Diaspora Studies</option>
					<option value="AHT">AHT - Allied Health Technology</option>
					<option value="ASL">ASL - American Sign Language</option>
					<option value="AMS">AMS - American Studies</option>
					<option value="ANI">ANI - Animation</option>
					<option value="ANT">ANT - Anthropology</option>
					<option value="APB">APB - Applied Brass</option>
					<option value="APK">APK - Applied Keyboard</option>
					<option value="APM">APM - Applied Music</option>
					<option value="APP">APP - Applied Percussion</option>
					<option value="AP">AP - Applied Professional Studies</option>
					<option value="APS">APS - Applied Strings</option>
					<option value="AT">AT - Applied Technology</option>
					<option value="APV">APV - Applied Voice</option>
					<option value="APW">APW - Applied Woodwinds</option>
					<option value="ARB">ARB - Arabic</option>
					<option value="ART">ART - Art</option>
					<option value="HAA">HAA - Art And Architecture, History Of</option>
					<option value="AI">AI - Arts And Ideas</option>
					<option value="BBE">BBE - Bilingual-Bicultural Education</option>
					<option value="BIO">BIO - Biological Sciences</option>
					<option value="BLW">BLW - Business Law</option>
					<option value="CTH">CTH - Catholic Studies</option>
					<option value="CTU">CTU - Catholic Theological Union</option>
					<option value="CHE">CHE - Chemistry</option>
					<option value="CHN">CHN - Chinese</option>
					<option value="CMN">CMN - Communication</option>
					<option value="CMNS">CMNS - Communication Studies</option>
					<option value="CSS">CSS - Community Service Studies</option>
					<option value="CPL">CPL - Comparative Literature</option>
					<option value="COM">COM - Composition</option>
					<option value="GPH">GPH - Computer Graphics &amp; Motion Technology</option>
					<option value="CSC">CSC - Computer Science</option>
					<option value="CNS">CNS - Computer, Information And Network Security</option>
					<option value="CCA">CCA - Core Curriculum Arts And Ideas</option>
					<option value="CCH">CCH - Core Curriculum Human Community</option>
					<option value="CCS">CCS - Core Curriculum Scientific World</option>
					<option value="CSL">CSL - Counseling</option>
					<option value="CES">CES - Critical Ethnic Studies</option>
					<option value="CS">CS - Curriculum Studies</option>
					<option value="DA">DA - Decision Analytics</option>
					<option value="DES">DES - Design</option>
					<option value="DC">DC - Digital Cinema</option>
					<option value="DHS">DHS - Digital Humanities</option>
					<option value="DMA">DMA - Digital Media Arts</option>
					<option value="ECE">ECE - Early Childhood Education</option>
					<option value="ECT">ECT - E-Commerce Technology</option>
					<option value="ECO">ECO - Economics</option>
					<option value="EA">EA - Educating Adults</option>
					<option value="EDU">EDU - Education - General</option>
					<option value="EE">EE - Elementary Education</option>
					<option value="ENG">ENG - English</option>
					<option value="ELA">ELA - English Language Academy</option>
					<option value="ENV">ENV - Environmental Science</option>
					<option value="EXP">EXP - Experience Design</option>
					<option value="FIN">FIN - Finance</option>
					<option value="FA">FA - Focus Area</option>
					<option value="FCH">FCH - French</option>
					<option value="GAM">GAM - Game Development</option>
					<option value="GEO">GEO - Geography</option>
					<option value="GER">GER - German</option>
					<option value="AAS">AAS - Global Asian Studies</option>
					<option value="GSB">GSB - Graduate School Of Business</option>
					<option value="GD">GD - Graphic Design</option>
					<option value="GRK">GRK - Greek</option>
					<option value="HTHC">HTHC - Health Communication</option>
					<option value="HIT">HIT - Health Information Technology</option>
					<option value="HLTH">HLTH - Health Science</option>
					<option value="HST">HST - History</option>
					<option value="HON">HON - Honors</option>
					<option value="HSP">HSP - Hospitality Leadership</option>
					<option value="HCD">HCD - Human Centered Design</option>
					<option value="HC">HC - Human Community</option>
					<option value="HCI">HCI - Human-Computer Interaction</option>
					<option value="ICE">ICE - Illinois Institute Of Technology</option>
					<option value="ILL">ILL - Illustration</option>
					<option value="IS">IS - Information Systems</option>
					<option value="IT">IT - Information Technology</option>
					<option value="IPD">IPD - Institute For Professional Development</option>
					<option value="IN">IN - Integrative Learning</option>
					<option value="ISM">ISM - Interactive And Social Media</option>
					<option value="IM">IM - Interactive Media</option>
					<option value="INTC">INTC - Intercultural Communication</option>
					<option value="ICS">ICS - Interdisciplinary Commerce Studies</option>
					<option value="IDS">IDS - Interdisciplinary Studies</option>
					<option value="ISP">ISP - Interdisciplinary Studies Program</option>
					<option value="IB">IB - International Business</option>
					<option value="INT">INT - International Studies</option>
					<option value="IRE">IRE - Irish Studies</option>
					<option value="IWS">IWS - Islamic World Studies</option>
					<option value="ITA">ITA - Italian</option>
					<option value="JPN">JPN - Japanese</option>
					<option value="JZZ">JZZ - Jazz Studies</option>
					<option value="JOUR">JOUR - Journalism</option>
					<option value="LE">LE - Labor Education</option>
					<option value="LAT">LAT - Latin</option>
					<option value="LST">LST - LatinAmerican &amp; Latino Studies</option>
					<option value="LAW">LAW - Law</option>
					<option value="LGQ">LGQ - Lesbian, Gay, Bisexual, Transgender, Queer Studies</option>
					<option value="LLS">LLS - Liberal Learning Seminars</option>
					<option value="LSE">LSE - Liberal Studies In Education</option>
					<option value="LSP">LSP - Liberal Studies Program</option>
					<option value="LL">LL - Lifelong Learning</option>
					<option value="LSI">LSI - Literacy &amp; Specialized Instruction</option>
					<option value="MGT">MGT - Management</option>
					<option value="MIS">MIS - Management Information Systems</option>
					<option value="MKT">MKT - Marketing</option>
					<option value="MPH">MPH - Master Of Public Health</option>
					<option value="MSW">MSW - Masters In Social Work</option>
					<option value="MLS">MLS - Masters Of Liberal Studies</option>
					<option value="MAT">MAT - Mathematical Sciences</option>
					<option value="MMT">MMT - Mathematics For Middle School Teaching</option>
					<option value="MCS">MCS - Media Studies</option>
					<option value="MGE">MGE - Middle Grades Education</option>
					<option value="MSC">MSC - Military Science</option>
					<option value="MOL">MOL - Modern Languages</option>
					<option value="MED">MED - Music Education</option>
					<option value="MEN">MEN - Music Ensemble</option>
					<option value="MUS">MUS - Musicianship</option>
					<option value="NMS">NMS - New Media Studies</option>
					<option value="NSG">NSG - Nursing</option>
					<option value="ORGC">ORGC - Organizational Communication</option>
					<option value="PAX">PAX - Peace, Justice And Conflict Studies</option>
					<option value="PRF">PRF - Performance</option>
					<option value="PAM">PAM - Performing Arts Management</option>
					<option value="PHL">PHL - Philosophy</option>
					<option value="PE">PE - Physical Education</option>
					<option value="PHY">PHY - Physics</option>
					<option value="POL">POL - Polish</option>
					<option value="PSC">PSC - Political Science</option>
					<option value="POR">POR - Portuguese</option>
					<option value="PM">PM - Project Management</option>
					<option value="PSY">PSY - Psychology</option>
					<option value="PPS">PPS - Public Policy Studies</option>
					<option value="PRAD">PRAD - Public Relations And Advertising</option>
					<option value="MPS">MPS - Public Services</option>
					<option value="RE">RE - Real Estate</option>
					<option value="FMS">FMS - Refugee And Forced Migration Studies</option>
					<option value="RELC">RELC - Relational Communication</option>
					<option value="REL">REL - Religious Studies</option>
					<option value="RUS">RUS - Russian</option>
					<option value="STEM">STEM - Science, Technology, Engineering And Math</option>
					<option value="SW">SW - Scientific World</option>
					<option value="SEC">SEC - Secondary Education</option>
					<option value="DCM">DCM - SNL Degree Completion Major</option>
					<option value="SNC">SNC - SNL Liberal Studies</option>
					<option value="SCG">SCG - Social &amp; Cultural Studies Ed Human Dev Grad</option>
					<option value="SCU">SCU - Social/Cultural Studies Education/Human Dev Ugrd</option>
					<option value="SOC">SOC - Sociology</option>
					<option value="SE">SE - Software Engineering</option>
					<option value="REC">REC - Sound Recording Technology</option>
					<option value="SPN">SPN - Spanish</option>
					<option value="SEV">SEV - Strategy Execution Valuation</option>
					<option value="SAP">SAP - Study Abroad Program</option>
					<option value="SUD">SUD - Sustainable Urban Development</option>
					<option value="TCH">TCH - TEACH Program</option>
					<option value="T&amp;L">T&amp;L - Teaching And Learning</option>
					<option value="TDC">TDC - Telecommunications</option>
					<option value="TV">TV - Television Production</option>
					<option value="THE">THE - Theatre Studies</option>
					<option value="TEC">TEC - Theatre Technology</option>
					<option value="UIP">UIP - University Internship Program</option>
					<option value="VFX">VFX - Visual Effects</option>
					<option value="WGS">WGS - Women's And Gender Studies</option>
					<option value="WLE">WLE - World Language Education</option>
					<option value="MWR">MWR - Writing</option>
					<option value="WRD">WRD - Writing Rhetoric And Discourse</option>
				</select>
				&nbsp;&nbsp;
				<input class="inputbox credit-input" style="width:15%" type="text" placeholder="Credits">
				&nbsp;&nbsp;
				<input class="inputbox" type="submit" value="SEARCH" onclick="creditSearch()">
			</p>
	    </div>
	</div>
	<div id="help">
	    <div id="help-container">
	    	<h2>How to Use Mocksched.com</h2>
			<h2 align="left" style="color: #aaa; font-size: 12px;">
			1) Choose the course prefix you are looking for.<br />
			2) If you know the course number, enter that into the number input box to narrow down the search results. If you do not know the course number, no problem, mocksched will display all courses available within that prefix.<br />
			3) After searching, choose the course you are looking for by pressing the course title.<br />
			4) Interact with the data on the course page by clicking the headers of the table. To sort multiple columns at once, simply hold down shift and click different headers. For example, let's say you want to arrange all open classes by professor ranking. Easy, hold down shift and click the "Class Status" header then the "Overall Rating" header. Voila! <br />
			5) Pressing "+" in the leftmost column will place that selected course into a specialized course cart located in the top left.<br />
			6) After adding courses you want to your course cart, you can create a mock schedule. Press "Generate Mock Schedule" and you will automatically be scrolled to the mock schedule. If you want to remove a course simply press "-"" in the table and re-click "Generate Mock Schedule" for your new schedule. <br /><br />

			If you need any more help please e-mail me at <a href="mailto:mocksched@gmail.com?subject=MockSched" style="color:#aaa;">mocksched@gmail.com</a>. Thanks!
			</h2>
	    </div>
	</div>
				<button class="generate" style="top:-20px; align: center;" onclick='overlay()'>ADVANCED SEARCH</button>
				<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
	<!-- Test -->
	<ins class="adsbygoogle"
	     style="display:block"
	     data-ad-client="ca-pub-6459268015898332"
	     data-ad-slot="6431202807"
	     data-ad-format="auto"></ins>
	<script>
	(adsbygoogle = window.adsbygoogle || []).push({});
	</script>'''
		html += '<h1>'+name + '</h1><hr><div><h2>'

		#Adds the professors overall rankings
		html += 'Overall Quality: ' + values[0] + '<br><br>'
		html += 'Helpfulness: ' + values[1] + '<br>'
		html += 'Clarity: ' + values[2] + '<br>'
		html += 'Easiness: ' + values[3]
		html += '</h2></div><h1>Student Reviews</h1><hr>'

		#Adds the student reviews to the webpage
		for i in reviews:
			html += '<div id="container" class="review"><div id="left">'
			
			html += 'Date: ' + str(i['date']) + '<br>'
			html += 'Class Name: ' + str(i['class_name']) + '<br>'
			html += 'Helpfulness: ' + str(i['helpful']) + '<br>'
			html += 'Clarity: ' + str(i['clarity']) + '<br>'
			html += 'Easiness: ' + str(i['easy']) + '<br>'
			html += 'Grade Received: ' + str(i['grade_received'])

			html += '</div><div id="right"><div>'
			html += i['comments']
			html += '</div></div></div>'
		html += '</div>'
		html += '<div class="center ital" style="padding-top: 1%;">Ratings and reviews credited to <a href="http://www.ratemyprofessors.com" target="_blank">Rate My Professors</a></div>'
		html += '<div class="center ital" style="padding-top: .5%;">Contact the <a href="mailto:mocksched@gmail.com?subject=MockSched">Developer</a></div>';
		html += '</body>'
		html += '''<script>
					$('#help').mousedown(function(e) 
					{
						var clicked = $(e.target);
						if (clicked.is('#help-container') || clicked.parents().is('#help-container')) 
						{
							return;
				    	} 
				    	else 
				    	{ 
				    		el = document.getElementById("help");
							el.style.visibility = (el.style.visibility == "hidden") ? "visible" : "hidden";
				    	}
					});

					$('#overlay').mousedown(function(e) 
					{
						var clicked = $(e.target);
						if (clicked.is('#advanced-container') || clicked.parents().is('#advanced-container')) 
						{
							return;
				    	} 
				    	else 
				    	{ 
				    		el = document.getElementById("overlay");
							el.style.visibility = (el.style.visibility == "hidden") ? "visible" : "hidden";
				    	}
					});

					$.fn.select2.amd.require(['select2/compat/matcher'], function (oldMatcher) 
					{
						$("select").select2({
					    	matcher: oldMatcher(matchStart)
					    })
					});

					$(".number").keyup(function (e) 
					{
					    if (e.keyCode == 13) 
					    {
					        submitForm();
					    }
					});

				 	$( document ).ready(function() {
				 		updateCourseCartCount();
    					$(".prefix").select2();
    					setTimeout(function(){ document.getElementById('search-box').style.visibility = 'visible'; }, 200);
					});
				</script>'''
		html += '</html>'

		output.write(html.encode("utf-8", "ignore"))


def create_all_teacher_webpages():
	data = gather_data()
	for i in data:
		try: 
			name = i['teacherfirstname_t'] + ' ' + i['teacherlastname_t']
		except: 
			name = None
		try: 
			rating = str(i['averageratingscore_rf'])
		except: 
			rating = '0'
		try: 
			helpful = str(i['averagehelpfulscore_rf'])
		except: 
			helpful = '0'
		try: 
			clarity = str(i['averageclarityscore_rf'])
		except: 
			clarity = '0'
		try: 
			easy = str(i['averageeasyscore_rf'])
		except: 
			easy = '0'

		if name != None:
			create_teacher_webpage(str(i['pk_id']),name,[rating,helpful,clarity,easy])

def main():
    export_to_csv()
    create_all_teacher_webpages()

if __name__ == '__main__':
	main()