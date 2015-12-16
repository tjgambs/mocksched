function run()
{
	$(".number").keyup(function (e) 
	{
	    if (e.keyCode == 13) 
	    {
	        submitForm();
	    }
	});
	$(".credit-input").keyup(function (e) 
	{
	    if (e.keyCode == 13) 
	    {
	        creditSearch();
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
    		var el = document.getElementById("overlay");
			el.style.visibility = (el.style.visibility == "hidden") ? "visible" : "hidden";
    	}
	});
	$('#userInput').mousedown(function(e) 
	{
		var clicked = $(e.target);
		if (clicked.is('#userInput-container') || clicked.parents().is('#userInput-container')) 
		{
			return;
    	} 
    	else 
    	{ 
    		var el = document.getElementById("userInput");
			el.style.visibility = (el.style.visibility == "hidden") ? "visible" : "hidden";
    	}
	});
	$('#books').mousedown(function(e) 
	{
		var clicked = $(e.target);
		if (clicked.is('#books-container') || clicked.parents().is('#books-container')) 
		{
			return;
    	} 
    	else 
    	{ 
    		var el = document.getElementById("books");
			el.style.visibility = (el.style.visibility == "hidden") ? "visible" : "hidden";
    	}
	});
	$('#help').mousedown(function(e) 
	{
		var clicked = $(e.target);
		if (clicked.is('#help-container') || clicked.parents().is('#help-container')) 
		{
			return;
    	} 
    	else 
    	{ 
    		var el = document.getElementById("help");
			el.style.visibility = (el.style.visibility == "hidden") ? "visible" : "hidden";
    	}
	});
}

function updateStatus()
{
	var courses = document.getElementsByClassName('course');
	var urls = [];
	for(var i = 0; i < courses.length; i++)
	{
		var prefix = courses[i].getElementsByClassName('name')[0].innerHTML.split(' ')[0];
		var number = courses[i].getElementsByClassName('name')[0].innerHTML.split(' ')[1];
		var url = 'https://crossorigin.me/http://offices.depaul.edu/_layouts/DUC.SR.ClassSvc/DUClassSvc.ashx?action=getclasses&strm=0965&subject=' + prefix + '&catalog_nbr=' + number;
		if(urls.indexOf(url) == -1)
		{
			urls.push(url);
		}
	}
	for(var i = 0; i < urls.length; i++)
	{
		$.ajax({
			url:urls[i],
			async : true,
			type:'GET',
			success: function(response)
		    {
		    	formatStatus(response);
		    }
		});
	}
}

function formatStatus(response)
{
	var courses = document.getElementsByClassName('course');
	var data = jQuery.parseJSON(response);
	var courseIndex = [];
	var courseStatus = [];
	for(var i = 0; i < courses.length; i++)
	{
		var number = courses[i].getElementsByClassName('number')[0].innerHTML;
		for(course of data)
		{
			if(course.class_nbr == number)
			{
				var tempStatus = course.enrl_stat;
				switch(tempStatus) 
				{
				    case 'O':
				    	if(courses[i].getElementsByClassName('status')[0].innerHTML != 'Open')
				    	{
				    		fixCookieStatus(courses[i],'Open');
				    	}
				        break;
				    case 'C':
				    	if(courses[i].getElementsByClassName('status')[0].innerHTML != 'Closed')
				    	{
				    		fixCookieStatus(courses[i],'Closed');
				    	}
				        break;
				    case 'W':
				    	if(courses[i].getElementsByClassName('status')[0].innerHTML != 'Waitlist')
				    	{
				    		fixCookieStatus(courses[i],'Waitlist');
				    	}
				    	break;
				}
			}
		}
	}
}

function fixCookieStatus(course,status)
{
	var cookies = document.cookie.split(';');
	var firstName = course.getElementsByClassName('fname')[0].innerHTML.toLowerCase();
	var lastName = course.getElementsByClassName('lname')[0].innerHTML.toLowerCase();
	var number = course.getElementsByClassName('number')[0].innerHTML;
	var cookieName = [firstName,lastName,'add',number].join('-').split(' ').join('-');
	var oldCookie = readCookie(cookieName);
	var saveCookies = [];
	for(i of cookies)
	{
		if(i.indexOf('saved-') != -1)
		{
			saveCookies.push(i);
		}
	}
	if(oldCookie.split(',').length == 11)
	{
		oldCookie = ['0.0'].concat(oldCookie.split(',')).join();
	}
	var newCookie = [];
	for(var i = 0; i < course.getElementsByTagName('td').length; i++)
	{
		if(i == 2) newCookie.push(status);
		else newCookie.push(oldCookie.split(',')[i]);
	}
	newCookie = newCookie.filter(Boolean);
	for(j of saveCookies)
	{
		var savedCookieName = j.split('|')[0].split('=')[0];
		var arr = j.split('|').slice(1);
		var completeArr = [j.split('|')[0].split('=')[1]];
		for(k of arr)
		{
			var tempArr = k.split(',');
			tempArr[2] = status;
			completeArr.push(tempArr.join());
		}
		writeCookie(savedCookieName,completeArr.join('|'),365);
	}
	writeCookie(cookieName,newCookie,365);
	formatCookies();
}

function readSaved()
{
	var allCookies = document.cookie.split(';');
	var savedCookies = [];
	for(i of allCookies)
	{
		var course = [];
		if(i.indexOf('saved-') != -1)
		{
			var name = i.split('|')[0].split('=')[1];
			var number = i.split('|')[0].split('=')[0];
			var classArray = i.split('|');
			course.push(name);
			course.push(number);
			for(var j = 1; j < classArray.length; j++)
			{
				var temp = classArray[j].split('=')[1].split(',');
				if(classArray[j].split('=')[1].split(',').length == 11)
				{
					temp = ['0.0'].concat(temp);
				}
				course.push(temp);
			}
		}
		if(course.length > 0)
		{
			savedCookies.push(course);
		}
	}
	return savedCookies;
}

function saveSelected(table)
{
	document.getElementsByClassName('userinput')[0].value = '';
	var all_courses = document.getElementById('myTable'+table).getElementsByClassName("course");
	var checkedCourses = [];
	for(var i = 0; i < all_courses.length; i++)
	{
		if(all_courses[i].getElementsByClassName("checked")[0])
		{
			var value = all_courses[i].getElementsByTagName('input')[0].id;
			var name = all_courses[i].getElementsByTagName('input')[0].className.replace('-add','') + '-' + value.split(',')[9];
			var together = name + '=' + value;
			checkedCourses.push(together);
		}
	}
	if(!readCookie('numberSaved'))
	{
		writeCookie('numberSaved','0',365);
	}
	writeCookie('numberSaved',String(parseInt(readCookie('numberSaved'))+1),365);
	if(checkedCourses.length > 0)
	{
		userInput();
	}
	$(".userinput").keyup(function (e)
	{
	    if (e.keyCode == 13 && document.getElementsByClassName('userinput')[0].value.length > 0) 
	    {
	        var title = document.getElementsByClassName('userinput')[0].value;
	        var courses = [title].concat(checkedCourses);
			var name = 'saved-' + String(parseInt(readCookie('numberSaved')));
			writeCookie(name,courses.join('|'),365);
			if(table != 0)
			{
				formatCookies(table);
			}
			else
			{
				formatCookies();
			}
			document.getElementById("userInput").style.visibility = 'hidden';
		}
	});
}

function convertDate(date)
{
	var hours = date.getHours();
	var minutes = date.getMinutes();
	var ampm = 'AM';
	if(hours > 12)
	{
		hours -= 12;
		ampm = 'PM';
	}
	if(minutes < 10)
	{
		minutes = '0' + String(minutes);
	}
	return String(date.getMonth() + 1) + '/' + String(date.getDate()) + '/' + String(date.getFullYear()) + ' ' + hours + ":" + minutes + ampm;
}

function removeAll()
{
	deleteCookie('unchecked0');
	for(i of document.cookie.split(';'))
	{
		if(i.indexOf('-add')!=-1) 
		{
			deleteCookie(i.split('=')[0]);
		}
	}
	formatCookies();
	updateCourseCartCount();
}

function excludeOrInclude()
{
	var howMany = document.getElementsByClassName('tab-links')[0].getElementsByTagName('li').length;
	for(var i = 0; i < howMany; i++)
	{
		if(document.getElementById('myTable'+i))
		{
			var tags = document.getElementById('myTable'+i).getElementsByClassName('checked');
			if(tags.length == 0)
			{
				if(document.getElementById('excludeAll'+i))
				{
					document.getElementById('excludeAll'+i).innerHTML = 'Include All';
					var button = document.getElementById('excludeAll'+i);
					button.setAttribute('onclick','includeAll('+i+')');
					document.getElementById('excludeAll'+i).id = 'includeAll'+i;
				}
			}
			else
			{
				if(document.getElementById('includeAll'+i))
				{
					document.getElementById('includeAll'+i).innerHTML = 'Exclude All';
					var button = document.getElementById('includeAll'+i);
					button.setAttribute('onclick','excludeAll('+i+')');
					document.getElementById('includeAll'+i).id = 'excludeAll'+i;
				}
			}
		}
	}
}

function excludeAll(table)
{
	var tags = document.getElementById('myTable'+table).getElementsByClassName('checked');
	var flag = true;
	var index = 0;
	while(flag)
	{
		if(tags.length == 0)
		{
			flag = false;
			break;
		}
		tags[index].checked = false;
		tags[index].className = 'unchecked';
	}
	saveUnchecked();
	if(document.getElementById('excludeAll'+table))
	{
		document.getElementById('excludeAll'+table).innerHTML = 'Include All';
		var button = document.getElementById('excludeAll'+table);
		button.setAttribute('onclick','includeAll("'+table+'")');
		document.getElementById('excludeAll'+table).id = 'includeAll'+table;
	}
}

function includeAll(table)
{
	var tags = document.getElementById('myTable'+table).getElementsByClassName('unchecked');
	var flag = true;
	var index = 0;
	while(flag)
	{
		if(tags.length == 0)
		{
			flag = false;
			break;
		}
		tags[index].checked = true;
		tags[index].className = 'checked';
	}
	saveUnchecked();
	if(document.getElementById('includeAll'+table))
	{
		document.getElementById('includeAll'+table).innerHTML = 'Exclude All';
		var button = document.getElementById('includeAll'+table);
		button.setAttribute('onclick','excludeAll("'+table+'")');
		document.getElementById('includeAll'+table).id = 'excludeAll'+table;
	}
}

function creditSearch()
{
	var prefix = document.getElementsByClassName('credit-prefix')[0].value;
	var credit = document.getElementsByClassName('credit-input')[0].value;
	var search = prefix.toLowerCase() + '-credits=' + credit;
	document.getElementById('tipue_search_input').value = '"' + search + '"';
	document.getElementById('field').submit();
}

function updateCourseCartCount()
{
	var length = '0';
	if(document.getElementById('0'))
	{
		length = document.getElementById('0').getElementsByClassName('course').length;
	}
	document.getElementById('course-cart').innerHTML = 'Course Cart (' + length + ')';
}

function books(data) 
{
	loadBooks(data);
	var el = document.getElementById("books");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function help() 
{
	var el = document.getElementById("help");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function userInput() 
{
	var el = document.getElementById("userInput");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function overlay() 
{
	var el = document.getElementById("overlay");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function formatCookies(value)
{
	var classes = [];
	var allHtml = '<div class="tabs" style="padding:0px;">';
	for(i of document.cookie.split(';'))
	{
		if(i.indexOf('-add') != -1) 
		{
			temp = i.substring(i.indexOf('=')+1).split(',');
			if(temp.length == 11) 
			{
				temp = (['0.0'].concat(temp));
			}
			classes.push(temp);
		}
	}
	var classes = ([['Current Cart',''].concat(classes)]).concat(readSaved());
	var ul = '<ul style="display: inline-block; padding: 0px;" class="tab-links">';
	for(var index = 0; index < classes.length; index++)
	{
		var tabName = classes[index][0];
		if (readSaved().length > 0)
		{
			if(index == 0)
			{
				ul += '<li class="active"><a href="#' + index + '">' + tabName + '</a></li>';
			}
			else
			{
				ul += '<li><a href="#' + index + '">' + tabName + '</a></li>';
			}
		}
	}
	ul += '</ul><div class="tab-content">';
	allHtml += ul;
	var html = '';
	for(var index = 0; index < classes.length; index++)
	{	
		var unchecked = Array(readCookie('unchecked'+index).split(','))[0];
		var tabName = classes[index][0];
		if (classes[index].slice(2).length > 0)
		{
			if(index == 0)
			{
				html = '<div id="' + index + '" class="tab active">';
				html += '<div align="left" style="padding-bottom: 10px;"><button class="generate" id="removeAll' + index + '" style="display: inline;" onclick="removeAll()">Remove All</button>&nbsp;&nbsp;<button class="generate" id="excludeAll' + index + '" style="display: inline;" align="left" onclick="excludeAll(';
				html += "'"+index+"'";
				html += ')">Exclude All</button></div>';
			}
			else
			{
				html = '<div id="' + index + '" class="tab">';
				html += '<div align="left" style="padding-bottom: 10px;"><button class="generate" id="deleteSelected' + index + '" style="display: inline;" align="left" onclick="deleteSave(';
				html += "'" + classes[index][1] + "',";
				html += "'" + index + "'";
				html += ')">Delete</button>&nbsp;&nbsp;';
				html += '<button class="generate" id="excludeAll' + index + '" style="display: inline;" align="left" onclick="excludeAll(';
				html += "'"+index+"'";
				html += ')">Exclude All</button></div>';
			}
			html += '<table id="myTable' + index + '" class="tablesorter">';
			html += '<thead><tr><th class="header">Remove</th><th class="header">Include Below</th><th class="header">Course</th><th class="header">Overall Rating</th><th class="header">Class Status</th><th class="header">Credit Hours</th><th class="header">Teacher First Name</th><th class="header">Teacher Last Name</th><th class="header">Class Start Time</th><th class="header">Class End Time</th><th class="header">Class Section</th><th class="header">Class Number</th><th class="header">Location</th><th class="header">Days</th></tr></thead><tbody>';
			var courseNumbers = [];
			for(i of classes[index].slice(2))
			{
				var classValue = i[4].toLowerCase() + '-' + i[5].toLowerCase() + '-add';
				var href = 'teachers/' + i[4].toLowerCase() + '-' + i[5].toLowerCase() + '';
				var course_name = 'classes/' + i[1].replace(' ','-').toLowerCase() + '';
				if(index != 0)
				{
					html += '<tr class=course><td><input class="' + classValue + '" id="' + i.join(',') + '" type="image" src="../../minus.png" width="20" onclick="removeFromSave(';
					html += "'"+i[9]+"','" + index + "'";
					html +=')"></td>';
				}
				else
				{
					html += '<tr class=course><td><input class="' + classValue + '" id="' + i.join(',') + '" type="image" src="../../minus.png" width="20" onclick="removeFromCart(this)"></td>';
				}

				if (i[0] == '0.0') 
				{
					if(document.getElementById(i[9]+'-checkbox-'+index))
		    		{
		    			if(document.getElementById(i[9]+'-checkbox-'+index).className == "checked")
		    			{
		    				html += '<td><input type="checkbox" class="checked" id="'+i[9]+'-checkbox-'+index+'" onclick="updateCheck(this)" checked></td>';
		    			}
		    			else
		    			{
		    				html += '<td><input type="checkbox" class="unchecked" id="'+i[9]+'-checkbox-'+index+'" onclick="updateCheck(this)"></td>';
		    			}
		    		}
		    		else
		    		{
		    			if(unchecked.indexOf(i[9]) == -1)
		    			{
		    				html += '<td><input type="checkbox" class="checked" id="'+i[9]+'-checkbox-'+index+'" onclick="updateCheck(this)" checked></td>';
		    			}
		    			else
		    			{
		    				html += '<td><input type="checkbox" class="unchecked" id="'+i[9]+'-checkbox-'+index+'" onclick="updateCheck(this)"></td>';
		    			}
		    		}
					html += '<td><a class="name" style="text-decoration: none;" href="' + course_name + '">' + i[1] + '</a></td>';
					html += '<td class="overall">' + i[0] + '</td>';
					if(i[2] == 'Closed')
					{
						html += '<td style="color:red;" class="status">' + i[2] + '</td>';
					}
					else
					{
						html += '<td style="color:green;" class="status">' + i[2] + '</td>';
					}
			    	html += '<td class="hours">' + i[3] + '</td>';
			    	html += '<td class="fname">' + i[4] + '</td>';
			    	html += '<td class="lname">' + i[5] + '</td>';
				}
		    	else 
		    	{
		    		if(document.getElementById(i[9]+'-checkbox-'+index))
		    		{
		    			if(document.getElementById(i[9]+'-checkbox-'+index).className == "checked")
		    			{
		    				html += '<td><input type="checkbox" class="checked" id="'+i[9]+'-checkbox-'+index+'" onclick="updateCheck(this)" checked></td>';
		    			}
		    			else
		    			{
		    				html += '<td><input type="checkbox" class="unchecked" id="'+i[9]+'-checkbox-'+index+'" onclick="updateCheck(this)"></td>';
		    			}
		    		}
		    		else
		    		{
		    			if(unchecked.indexOf(i[9]) == -1)
		    			{
		    				html += '<td><input type="checkbox" class="checked" id="'+i[9]+'-checkbox-'+index+'" onclick="updateCheck(this)" checked></td>';
		    			}
		    			else
		    			{
		    				html += '<td><input type="checkbox" class="unchecked" id="'+i[9]+'-checkbox-'+index+'" onclick="updateCheck(this)"></td>';
		    			}
		    		}
		    		html += '<td><a class="name" style="text-decoration: none;" href="' + course_name + '">' + i[1] + '</a></td>';
		    		html += '<td><a class="overall" style="text-decoration:none;" href="' + href + '">' + i[0] + '</a></td>';
		    		if(i[2] == 'Closed')
					{
						html += '<td style="color:red;" class="status">' + i[2] + '</td>';
					}
					else
					{
						html += '<td style="color:green;" class="status">' + i[2] + '</td>';
					}
			    	html += '<td class="hours">' + i[3] + '</td>';
			    	html += '<td><a class="fname" style="text-decoration:none;" href="' + href + '">' + i[4] + '</td>';
			    	html += '<td><a class="lname" style="text-decoration:none;" href="' + href + '">' + i[5] + '</td>';	
		    	}
		    	html += '<td class="start">' + i[6] + '</td>';
		    	html += '<td class="end">' + i[7] + '</td>';
		    	html += '<td class="section">' + i[8] + '</td>';
		    	html += '<td class="number">' + i[9] + '</td>';
		    	html += '<td class="location">' + i[10] + '</td>';
		    	html += '<td class="days">' + i[11] + '</td>';
				html += '</tr>'
			}
			html += '<tbody></table>';
			html += '<div align="left" style="padding-top: 10px;">';
			html += '<button class="generate" id="saveSelected' + index + '" style="display: inline;" align="left" onclick="saveSelected(';
			html += "'" + index + "'";
			html += ')"">Save Selected</button><div style="padding-top: 2%;"><button class="generate" id="displayBooks' + index + '" onclick="books(';
			html += "'" + index + "'";
			html += ')" style="font-size: 15px;">Buy Required Books</button></div><div style="padding-top: 2%;"><button class="generate" id="mocksched' + index + '" onclick="createCalendarData(';
			html += "'myTable" + index + "'";
			html += ')" style="font-size: 15px;">Mock Schedule</button></div><div style="width: 75%; margin: 0 auto;"class="calendar' + index + '" id="calendar' + index + '" style="padding-top:1%; visibility: hidden"></div></div>';
		}
		else
		{
			html = '<div id="' + index + '" class="tab active"><h2>Your course cart is currently empty. Search for courses <a href="search" style="color: #333;">here.</a></h2>';
		}
		allHtml += (html + '</div>');
	}
	document.getElementById('cart').innerHTML = allHtml;
	if(value && document.getElementById(value))
	{
		document.getElementById(value).className = 'tab active';
		document.getElementById('0').className = 'tab';
		document.getElementsByClassName('tab-links')[0].getElementsByTagName('li')[0].className = '';
		document.getElementsByClassName('tab-links')[0].getElementsByTagName('li')[value].className = 'active';
	}
	saveUnchecked();
	jQuery('.tabs .tab-links a').on('click', function(e)  
    {
        var currentAttrValue = jQuery(this).attr('href');
        jQuery('.tabs ' + currentAttrValue).fadeIn(400).siblings().hide();
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');
        e.preventDefault();
    });
}

function deleteSave(name,index)
{
	deleteCookie('unchecked'+index);
	deleteCookie(name);
	formatCookies(index-1);
}

function saveUnchecked()
{
	var howMany = document.getElementsByClassName('tab-links')[0].getElementsByTagName('li').length;
	if(howMany == 0) howMany = 1;
	for(var j = 0; j < howMany; j++)
	{
		if(document.getElementById('myTable'+j))
		{
			var all_courses = document.getElementById('myTable'+j).getElementsByClassName("course");
			var courses = [];
			for(var i = 0; i < all_courses.length; i++)
			{
				if(all_courses[i].getElementsByClassName("unchecked")[0])
				{
					courses.push(all_courses[i]);
				}
			}
			var save = [];
			for(var i = 0; i < courses.length; i++)
			{
				save.push(courses[i].getElementsByClassName('number')[0].innerHTML);
			}
			writeCookie('unchecked'+j,save,1);
		}
	}
	excludeOrInclude();
}

function updateCheck(data)
{
	var tag = document.getElementById(data.id);
	if(tag.checked)
	{
		tag.className = "checked";
	}
	else
	{
		tag.className = "unchecked";
	}
	saveUnchecked();
}

function removeFromSave(number,table)
{
	var allCookies = document.cookie.split(';');
	var savedCookies = [];
	for(i of allCookies)
	{
		if(i.indexOf('saved-') != -1)
		{
			savedCookies.push(i.split('|'));
		}
	}
	var cookieNames = [];
	for(i of savedCookies)
	{
		cookieNames.push(i[0].split('=')[0]);
	}
	var cookieTableName = cookieNames[table-1];
	var _old = '';
	for(i of savedCookies)
	{
		if(i[0].indexOf(cookieTableName) != -1)
		{
			_old = i;
		}
	}
	var _new = [];
	for(i of _old)
	{
		if(i.indexOf(number) == -1)
		{
			_new.push(i);
		}
	}
	var name = _new.join('|').split('=')[0];
	var value = _new.join('|').split('=').slice(1).join('=');
	if(value.indexOf('|') == -1)
	{
		deleteSave(name,table);
	}
	else
	{
		writeCookie(name,value,365);
	}
	formatCookies(table);
}

function removeFromCart(contents)
{
	var index = 9;
	var value = contents.getAttribute('id');
	if(value.split(',').length < 12) 
	{
		index = 8;
	}
	var className = contents.getAttribute('class').split(' ').join('-');
	deleteCookie(className + '-' + value.split(',')[index]);
	formatCookies();
	updateCourseCartCount();
}

function writeCookie(name,value,days) 
{
    var date, expires;
    if (days) 
    {
        date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toGMTString();
    }
    else
    {
        expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) 
{
	var i, c, ca, nameEQ = name + "=";
	ca = document.cookie.split(';');
	for(i=0;i < ca.length;i++) 
	{
   		c = ca[i];
    	while (c.charAt(0)==' ') 
    	{
        	c = c.substring(1,c.length);
    	}
        if (c.indexOf(nameEQ) == 0) 
        {
            return c.substring(nameEQ.length,c.length);
        }
	}
	return '';
}

function deleteCookie(name) 
{
	document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function createCalendar(events,number)
{
	$('#calendar'+number).fullCalendar('destroy');
	$('#calendar'+number).fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek'
		},
		defaultDate: '2016-01-04',
		selectable: true,
		selectHelper: true,
		scrollTime: '08:00:00',
		defaultView: 'agendaWeek',
		select: function(start, end) {
			var title = prompt('Event Title:');
			var eventData;
			if (title) {
				eventData = {
					title: title,
					description: description,
					start: start,
					end: end,
					dow: dow
				};
				$('#calendar'+number).fullCalendar('renderEvent', eventData, true);
			}
			$('#calendar'+number).fullCalendar('unselect');
		},
		editable: false,
		eventLimit: true,
		selectable: false,
		events: events,
		eventRender: function (event, element, view) {
			element.find('.fc-title').append('<div class="hr-line-solid-no-margin"></div><span style="font-size: 6px;">' + event.description + '</span></div>');
		},
	});
	$('html, body').animate({
		scrollTop: $("#calendar"+number).offset().top
	}, 1000);
}

function createCalendarData(table)
{
	var all_courses = document.getElementById(table).getElementsByClassName("course");
	var courses = [];
	for(var i = 0; i < all_courses.length; i++)
	{
		if(all_courses[i].getElementsByClassName("checked")[0])
		{
			courses.push(all_courses[i]);
		}
	}
	var events = [];
	for(var i = 0; i < courses.length; i++)
	{
		var start = convertTime(courses[i].getElementsByClassName('start')[0].innerHTML);
		var end = convertTime(courses[i].getElementsByClassName('end')[0].innerHTML);
		var firstname = courses[i].getElementsByClassName('fname')[0].innerHTML;
		var lastname = courses[i].getElementsByClassName('lname')[0].innerHTML;
		var courseLocation = courses[i].getElementsByClassName('location')[0].innerHTML;
		var days = convertDays(courses[i].getElementsByClassName('days')[0].innerHTML);
		var course = courses[i].getElementsByClassName('name')[0].innerHTML;
		var description = "Teacher: " + firstname + ' ' + lastname +"<br>" + "Location: " + courseLocation;
		events.push({'title':course,'description':description,'start':start,'end':end,'dow':days});
	}
	var number = table.substring(table.length-1);
	createCalendar(events,number);
	document.getElementById('calendar'+number).style.visibility = 'visible';
}

function convertDays(days)
{
	var ret = [];
	if (days.indexOf('M') != -1) ret.push(1);
	if (days.indexOf('Tu') != -1) ret.push(2);
	if (days.indexOf('W') != -1) ret.push(3);
	if (days.indexOf('Th') != -1) ret.push(4);
	if (days.indexOf('F') != -1) ret.push(5);
	if (days.indexOf('Sat') != -1) ret.push(6);
	return ret;
}

function convertTime(time)
{
	if(time == 'TBD') 
	{
		return;
	}
	var hours = time.split(' ')[0].split(':')[0];
	var minutes = time.split(' ')[0].split(':')[1];
	if(time.split(' ')[1].toLowerCase() == 'pm' && time.split(' ')[0].split(':')[0].length < 2) 
	{
		hours = String(parseInt(hours)+12);
	}
	var ret = hours + ':' + minutes + ':00';
	if (ret.length == 7) 
	{
		ret = '0' + ret;
	}
	return ret;
}

function submitForm()
{
	var prefix = document.getElementsByClassName('prefix')[0].value;
	var number = document.getElementsByClassName('number')[0].value;
	if(isNaN(number) == false)
	{
		var search = prefix.toUpperCase() + '  ' + number;
		document.getElementById('tipue_search_input').value = '" ' + search + '"';
		document.getElementById('field').submit();
	}
}

function matchStart(term, text) 
{
	return text.toUpperCase().indexOf(term.toUpperCase()) == 0;
}

$.fn.select2.amd.require(['select2/compat/matcher'], function (oldMatcher) 
{
	$("select").select2({
    	matcher: oldMatcher(matchStart)
    })
});

function loadBooks(number)
{
	$.ajax({
		url:'http://mocksched.com/schools/depaul-university/books.json',
		type:'GET',
		success: function(response)
	    {
	    	var all_courses = document.getElementById('myTable'+number).getElementsByClassName("course");
			var names = [];
			var numbers = [];
			for(var i = 0; i < all_courses.length; i++)
			{
				if(all_courses[i].getElementsByClassName("checked")[0])
				{
					names.push(all_courses[i].getElementsByClassName('name')[0].innerHTML);
					numbers.push(all_courses[i].getElementsByClassName('number')[0].innerHTML);
				}
			}
	     	var html = '<h1 align="center">Required Books</h1>';
	     	html += '<h3><hr><button class="generate" onclick="openAllBooks()" style="top:-20px; align: center;">Buy All Books</button><h3>';
	     	html +='<h3 align="center">Books are updated once a week</h3>';
	    	for(var i = 0; i < names.length; i++)
	    	{
	    		html += '<span style="display: block;"><h2><strong><big>' + names[i] + ' - ' + numbers[i] + '</big></strong></h2>';
		    	if(response[numbers[i]] != undefined && response[numbers[i]].length != 0)
		    	{
		    		for(var j = 0; j < response[numbers[i]].length; j++)
		    		{
		    			var status = response[numbers[i]][j][0];
		    			if (status == 'Required')
		    			{
			    			var url = response[numbers[i]][j][1];
			    			var name = response[numbers[i]][j][2];
			    			var isbn = url.split('/')[5];
			    			if(isbn != undefined)
			    			{
				    			var imageHtml = '';
				    			if(isbn != '#')
				    			{
				    				imageHtml = '<img style="float: left;" height="110px" width="90px" border="0" src="http://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=' + isbn + '&Format=_SL110_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=mock09-20" ></a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=mock09-20&l=as2&o=1&a=' + isbn + '" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />';
				    				html += '<a target="_blank" style="color:#333;" href="' + url + '">';
				    				html += imageHtml +'</a>';
				    				html += '<a target="_blank" style="color:#333;" href="' + url + '"><h3 style="padding-left:100px; height:110px;">' + name + '</h3></a></span>';
				    			}
				    			else
				    			{
				    				imageHtml = '<img style="float: left;" height="110px" width="90px" border="0" src="http://ebookbay.co/images/default_cover.jpg"></a><img src="http://ebookbay.co/images/default_cover.jpg" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />';
				    				html += imageHtml;
				    				html += '<h3 style="padding-left:100px; height:110px;">' + name + '</h3></span>';
				    			}
			    			}
			    			else
			    			{
			    				imageHtml = '<span style="display: block; height: 150px;"><img style="float: left;" height="110px" width="90px" border="0" src="http://ebookbay.co/images/default_cover.jpg"></a><img src="http://ebookbay.co/images/default_cover.jpg" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />';
			    				html += imageHtml;
			    				html += '<h3 style="padding-left:100px;">' + name + '</h3></span></span>';
			    			}
			    		}
		    		}
		    	}
		    	else
		    	{
		    		html += '<h3 style="padding-left:100px;">No Books Needed</h3>';
		    	}
	    	}
	    	html += '<p>If the book required for a class is not clickable, then the book is not availabe on Amazon and must be purchased elsewhere.</p>';
	    	html += '<p style="font-size:8px; text-transform: none;">Mocksched.com is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to amazon.com.</p>';
	    	document.getElementById('books-container').innerHTML = html;
	    }
	});
}

function openAllBooks()
{
	var inner = document.getElementById('books-container').getElementsByTagName('a');
	var a = [];
	for(var i = 0; i < inner.length; i++)
	{
		if(a.indexOf(inner[i].href) == -1)
		{
			a.push(inner[i].href);
		}
	}
	for(url of a)
	{
		window.open(url);
	}
}