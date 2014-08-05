var App = {
  Models: {},
  Collections: {},
  View: {},
  Courses: null,
  //Documents: null,
  //Teams: null,
  Students: null,
  CourseList: null,

};


//window.tom???
$(function() { // Run this code when the DOM is ready
	
//	  window.tom = new App.Models.Contact({
//	    firstName: 'Thomas',
//	    lastName: 'Hunter',
//	    phoneNumber: '9895135499',
//	    email: 'me@thomashunter.name'
//	  });
//
	  App.Courses = new App.Collections.Course();

	  App.Contacts.add({
		    name: 'New Course',
		    startingBudget: '60000',
		    enableNarrative: true,
		    message: '<p>Message for Course goes Here</p>',
		    active: true,
	  });

	  App.Contacts.add({});

	  var courseList = '';
	  App.Courses.each(function(course) {
		  courseList += "<div>" +
		  course.get('name') + " " +
		  course.get('message') + " ";

	    if (course.isValid()) {
		  courseList += "(valid)";
	    } else {
		  courseList += "(invalid)";
	    }
	    
	    courseList += "</div>";
	  });
	  $('#course_display').html(courseList);

	});