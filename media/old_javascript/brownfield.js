var windows_to_close_on_logout = [];

addLoadEvent(function() {
    var lgout = $('userlogout');
    if (lgout) {
	lgout.innerHTML = "<span><a href=\"javascript:logOut('/logout')\">Log out</a></span>";
    }
    //ajaxify all forms
    try {
	AjaxFormManager.init(document,brownfieldAjaxFormDecorator);
    } catch(e) { /*oops, maybe no ajaxformmanager here, like in play window */ }
});

function openPopWin(theURL,w,h,resizing,scrolling,winname,closeOnLogout) {
	var winl = (screen.width - w) / 2;
	var wint = (screen.height - h) / 2;
    winprops = 'height='+h+',width='+w+',top='+wint+',left='+winl+',resizable='+resizing+',scrollbars='+scrolling+',location=no,status=no,menubar=no,directories=no,toolbar=no';
    popwin = window.open(theURL, winname, winprops);
    if (/\.jpg$/.test(theURL)) {
	popwin.document.write('<a href="javascript:void(0)" onclick="window.print()">print article</a><br /><img src="'+theURL+'" alt="news article"/>');
	popwin.document.close();
    }
    if (closeOnLogout) {
	windows_to_close_on_logout.push(popwin);
    }
    if (parseInt(navigator.appVersion) >= 4) { popwin.window.focus(); }
    if (popwin.opener == null) { popwin.opener = self; }
}

function logOut(url) {
    if (window.opener) {//we're the popup window
	window.opener.location = url;
	window.close();
    }
    else {
	forEach(iter(windows_to_close_on_logout),function(w) {
	    w.close();
	});
	document.location = url;
    }
}

function showUserList() {
	hideElement("courselistblock");
	hideElement("courseadmin");
	hideElement("demo");
        
	showElement("siteadmin");
	removeElementClass("courselist","active")
	removeElementClass("userlist","active")
	addElementClass("userlist","active")
	removeElementClass("demolink","active")
}

function showCourseList() {
    hideElement("courseadmin");
    hideElement("demo");

    showElement("courselistblock");
    showElement("courseadmin");
    removeElementClass("courselist","active")
    removeElementClass("demolink","active")
    addElementClass("courselist","active")

    try {
	hideElement("siteadmin");
	removeElementClass("userlist","active")
	
    } catch(e) {/*pass*/}	
}

function showDemo() {
    hideElement("courseadmin");
    hideElement("courselistblock");
    hideElement("courseadmin");
    showElement("demo");
    
    removeElementClass("courselist","active")
    addElementClass("demolink","active")

    try {
	hideElement("siteadmin");
	removeElementClass("userlist","active")
    } catch(e) {/*pass*/}
}

function showTSList() {
	hideElement("courseinfoblock");
	showElement("teamstudentsblock");
	removeElementClass("courseinfo","active")
	removeElementClass("teamstudent","active")
	addElementClass("teamstudent","active")
}

function showCourseInfo() {
	hideElement("teamstudentsblock");
	showElement("courseinfoblock");
	removeElementClass("courseinfo","active")
	removeElementClass("teamstudent","active")
	addElementClass("courseinfo","active")
}

function brownfieldAjaxFormDecorator(ajaxform) {
    /*
      form_to_areas includes specs on specific named forms
      all forms with class="docform" (doc release/revoke)
         get the same functionality
    */
    var f = ajaxform.form; //the actual HTMLForm object

    var fname = (f.attributes['name'])?f.attributes['name'].nodeValue : '';
    var fdocform = hasElementClass(f,'docform');

    var form_to_areas = {
	'course_update': {'refresh_sections':['leftside']},
	'course_delete': {'refresh_sections':['courselistblock']},
	'course_create': {'refresh_sections':['courselistblock'],
			  'reset':true
			 },
	'user_delete': {'refresh_sections':['userlistblock']},
	'user_create': {'refresh_sections':['userlistblock'],
			'reset':true
	               },
	'team_delete': {'refresh_sections':['teams','noteam']},
	'student_delete': {'refresh_sections':['noteam','teams']}
    };

    if (typeof(initStudents) =='function') {
	update(form_to_areas,{
	    'student_create': {'refresh_sections':['noteam'],
			       'after_refresh':initStudents,
			       'reset':true	    
			      },
	    'team_create': {'refresh_sections':['teams'],
			    'after_refresh':initTeamJoining,
			    'reset':true
			   },
	    'team_delete': {'refresh_sections':['teams','noteam'],
			    'after_refresh':initTeamJoining
			   },
	    'student_delete': {'refresh_sections':['teams','noteam'],
			       'after_refresh':initTeamJoining
			      }
	});
    }
    
    if (fname in form_to_areas) {
	update(ajaxform.options, form_to_areas[fname]);
    }
    if (fdocform) {
	ajaxform.options.refresh_sections = ['narrative_resources'];
	//ajaxform.after_refresh = partial(ajaxifyForms,'narrative_resources'); 
    }

    ajaxform.success = noop;
    ajaxform.failure = noop;

    var adjoin_message=function(message) {
	var self = this;
	var f;
	var msgid;

	if (self.form.id) {
	    f = $(self.form.id);
	    msgid=self.form.id + '_message';
	} else {
	    f = self.form;
	    msgid='form_'+self.index+'_message';
	}

	var dest = $(msgid);

	if (dest) {
	    //essentially a node swap
	    insertSiblingNodesAfter(dest, message);
	    removeElement(dest);
	} else {
	    var button = getElementsByTagAndClassName(null,'submitbutton',f)[0];
	    insertSiblingNodesAfter(button, message);
	}
	message.id = msgid;
    }

    var afterrefresh = function() {
	var self = this;
	var message = SPAN({'class':'successmessage'},' Save successful!');
	adjoin_message.call(self, message);
	forEach(getElementsByTagAndClassName(null,'errormessage',self.form), function(e) {
	    removeElement(e);
	});
	forEach(getElementsByTagAndClassName(null,'fielderror',self.form), function(e) {
	    removeElement(e);
	});

	//not in adjoin_message() since errors shouldn't fade
	fade(message,{
	    duration:5,
	    afterFinish:function() {
		removeElement(message);
	    }
	});

    }
    connect(ajaxform,'afterrefresh',afterrefresh);
    
    ajaxform.failure = function(error) {
	var self = this;
	//logDebug(self);
	//logDebug(arguments.length, error);
	switch(error.number) {
	  case 401:
	      error.message = "Request unauthorized.  If you have permission, please login and try again.";
          case 400:
	      error.message = 'Are you sure?';
	      break;
	  case 409:
	      error.message = 'Request failed due to a conflict with another record.';
	      break;
	}

	if (self.replaceForm(error.req)) {
	    //logDebug('replacing the form worked');
	}
	adjoin_message.call(self,SPAN({'class':'errormessage'},error.message));
    }
    
}
