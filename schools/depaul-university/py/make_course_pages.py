# -*- coding: utf-8 -*-
#Created by Timothy Gamble
#tjgambs@gmail.com

import json
import urllib
import sys
import take_lsld_data as lsld
import urllib

lsld_data = lsld.take()

def create_page(full_name,description,course_url,termname):
	ignore = ['a','an','the','and','at','around','by','after','along','for','from','of','on','to','with','without']
	tempArr = []
	for index,i in enumerate(full_name.replace(';','').split(' ')[2:]):
		if index == 0:
			tempArr.append(i.capitalize())
		elif i.lower() in ignore:
			tempArr.append(i.lower())
		else:
			tempArr.append(i.capitalize())
	short_url = ' '.join(full_name.split()[:2]).replace(';','')
	html = '<!DOCTYPE html><html><head><title>'
	html += ' '.join(full_name.replace(';','').split(' ')[:2]) + ' - ' + ' '.join(tempArr).replace('Ii','II').replace('Iii','III').replace('IIi','III')
	html +='''</title>
	<meta charset="UTF-8">
	<script src="../../../../../js/jquery.min.js"></script>
	<script src="../../../../../js/select2.full.js"></script>
	<script src="../../../js/course-pages.min.js"></script>

    <link href="../../../../../css/select2.css" rel="stylesheet"/>
	<link rel="stylesheet" href="../../../../../css/stylesheet.css" type="text/css" media="print, projection, screen" />
	<script type="text/javascript" src="../../../../../js/jquery.tablesorter.min.js"></script>
	<link href="http://fonts.googleapis.com/css?family=Open+Sans:300,400|Merriweather:300,300italic" rel="stylesheet">
	<link rel="shortcut icon" href="../../../../../icon.png">
    <link rel="stylesheet" id="tipue3" type="text/css" href="../../../../../css/tipuesearch.css">
	<script>
		(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
		})(window,document,'script','http://www.google-analytics.com/analytics.js','ga');
		ga('create', 'UA-70030211-1', 'auto');
		ga('send', 'pageview');
	 </script>
</head>
<body id="body">
<div>
	<span>
		<h3>
			<a href="../../../course-cart" style="text-decoration:none; float:right; color:#333;" id="course-cart">Course Cart (0)</a>
			<div style="color:#333; float:right;">&nbsp;|&nbsp;</div>
			<a href="javascript:help();" style="text-decoration:none; color:#333; float:right;">Help</a>
		</h3>
	</span>
	<span>
		<h1 style="float:left; padding: 0px; padding-right:2%;"><a href="../../../search" style="text-decoration:none; color:#333;">MockSched</a></h1>
		<div id="search-box" style="visibility: hidden;">
		<div style="display: inline-block; padding-right:10px">
			<select class="prefix" style="width:200px;" onchange="saveSelections()">
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
				<form onsubmit="submitForm()" action="../../../search" id="field">
					<input class="inputbox" type="hidden" name="q" id="tipue_search_input" autocomplete="off" required value="">
					<input class="search-button" type="submit" value="SEARCH">
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
	        <form action="../../../search">
				<input type="text" name="q" id="tipue_search_input" autocomplete="off" required style="width: 100%" placeholder="Enter a Professor, Course Title, or General Keyword">
			</form>
			<h2 align="left" style="padding-top: 10px; color: #aaa; font-size: 12px;">
			If searching for a phrase, please surround the phrase in quotation marks (i.e. "Computer Science"). In doing so, you will receive more accurate results.
			</h2>
			<h2 align="center">
				Filter Courses by Credit Hour
			</h2>
			<span align="center">
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
				<input class="search-button" type="submit" value="SEARCH" onclick="creditSearch()">
			</span>

			<h2 align="center">
				Filter Courses by Learning Domain
			</h2>
			<span align="center" style="padding-top: -10px;">
				<select class="learning-domain-prefix" style="width:50%">
					<option value="Arts and Literature">Arts and Literature</option>
					<option value="Philosophical Inquiry">Philosophical Inquiry</option>
					<option value="Religious Dimensions">Religious Dimensions</option>
					<option value="Scientific Inquiry">Scientific Inquiry</option>
					<option value="Social, Cultural, and Behavioral Inquiry">Social, Cultural, and Behavioral Inquiry</option>
					<option value="Understanding the Past">Understanding the Past</option>
				</select>
				&nbsp;&nbsp;
				<input class="search-button" type="submit" value="SEARCH" onclick="learningDomainSearch()">
			</span>
	    </div>
	</div>
	<div id="help"></div>
<button class="generate" style="top:-20px; align: center;" onclick='overlay()'>ADVANCED SEARCH</button>
	<div id="ads"></div>
	<h1>'''

	html += full_name.replace(';','')
	html +='</h1><h2 id="description">'
	html += description

	html += '</h2></body>'
	html += '''<script>

	$(document).ready(function() 
	{setTimeout(function(){ document.getElementById('search-box').style.visibility = 'visible'; }, 200);'''
	html += 'updateTable("' + "{0}".format(course_url) + '","' + short_url + '");'
	html += '''
		$('#ads').load('http://mocksched.com/ads.html');
		$('#help').load('http://mocksched.com/help.html');
		$(".prefix").select2();
		updateRanking();
		updateCourseCartCount();
		$("#myTable").tablesorter({
			sortInitialOrder: 'desc',
	    	headers: {
	        	6: { sorter: 'time'},
	        	7: { sorter: 'time'}
	   		}
		});
		run();
	});
	</script>
</html>'''
	webpage_name = ('terms/' + termname + '/classes/' + '-'.join(full_name.split()[:2]).replace(';','').lower()+'.html')
	with open('../'+webpage_name,'w') as output:
			output.write(html)
	data = json.loads(urllib.urlopen(course_url).read())
	tags = []

	for name, value in lsld_data.iteritems():
		if ' '.join(full_name.split(' ')[:2]) in value:
			tags.append('lsld=' + name)
			break

	for i in data:
		tags.append(i['first_name'] + ' ' + i['last_name'])
		tags.append(i['class_nbr'])
		tags.append('location=' + i['location_descr'])
		if not course_url.split('=')[-2].split('&')[0].lower()+'-credits='+i['units_minimum'] in tags:
			tags.append(course_url.split('=')[-2].split('&')[0].lower()+'-credits='+i['units_minimum'])

	return [full_name.replace(';',''),description,tags,'terms/' + termname + '/classes/' + '-'.join(full_name.split()[:2]).replace(';','').lower()+'']

def create_all(termname):
	with open('../terms/' + termname + '/classes.json','r') as input:
		data = json.loads(input.read())
		to_be_indexed = []
		for i in data: 
			to_be_indexed.append(create_page(i[0],i[1],i[2],termname))
		send_to_be_indexed(to_be_indexed,termname)

def send_to_be_indexed(items,term):
	with open('../terms/' + term + '/tipuesearch/tipuesearch_content.js','w') as output:
		output.write('var tipuesearch = {"pages": [\n')
		for i in items:
			title = '""'
			text = '""'
			tags ='""'
			url = '""'

			if i[0]:
				temp = i[0].split(' ')
				temp[0] = ' '+temp[0]+' '
				title = clean_index(' '.join(temp))
			if i[1]:
				text = clean_index(i[1])
			if i[2]:
				tags = clean_index(','.join(i[2]))
			if i[3]:
				url = clean_index(i[3])

			output.write('{"title":'+ title +',"text":'+ text +',"tags":'+ tags +',"url": '+url+'},\n')
		output.write(']};')

def clean_index(item):
	return '"{0}"'.format(item.replace("\"",'').replace("\r\n",'').replace("\n",''))

if __name__ == '__main__':
	create_all(sys.argv[1])

