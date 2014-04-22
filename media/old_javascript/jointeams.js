function initStudentDraggable(s) {
    return new Draggable(s, {
	//ghosting:true, //breaks in IE7 SUX!!!
	revert:true,
	scroll:window
    });
}

function initJoinDroppable(t) {
    //logDebug(t);
    //DragDrop.makeListContainer(t); return;

    //uses MochiKit.DragAndDrop
    return new Droppable(t, {
	'accept':['student'],
	ondrop: function (student, group, e) {
	    appendChildNodes(group, student);
	    setNodeAttribute(student,'style','');
	    var student_id = student.id.substr('student'.length);
	    var team_id = group.parentNode.id.substr('team'.length);
	    doXHR('student/'+student_id+'/join',
	          {'method':'POST',
		   'sendContent':'team_id='+team_id,
		   'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
		  }
		  );
	    //logDebug('"' + student_id + '" was dropped on '+team_id);
	    
	}		    
	});
}
function initUnjoinDroppable(g) {
    //DragDrop.makeListContainer(g);    return;
    
    //uses MochiKit.DragAndDrop
    return new Droppable(g, {
	'accept':['student'],
	ondrop: function (student, group) {
	    appendChildNodes(group, student);
	    var student_id = student.id.substr('student'.length);
	    doXHR('student/'+student_id+'/join',
	          {'method':'DELETE'}
		  );
	    //logDebug('"' + student_id + '" was unoined');
	}
    });
}

function initStudents() {
    var students = getElementsByTagAndClassName('li','student');
    forEach(students, initStudentDraggable);
    rejects = $('noteam');
    initUnjoinDroppable(rejects);

}

function initTeams() {
    var teams = getElementsByTagAndClassName('ul','team');
    forEach(teams, initJoinDroppable);
}

function initTeamJoining() {
    initStudents();
    initTeams();
    /*
    var list = document.getElementById("phonetic");
    DragDrop.makeListContainer( list );
    list.onDragOver = function() { this.style["background"] = "#EEF"; };
    list.onDragOut = function() {this.style["background"] = "none"; };
    
    list = document.getElementById("numeric");
    DragDrop.makeListContainer( list );
    list.onDragOver = function() { this.style["border"] = "1px dashed #AAA"; };
    list.onDragOut = function() {this.style["border"] = "1px solid white"; };
    */
}

addLoadEvent(initTeamJoining);
