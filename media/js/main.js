  var App = {
    Models: {},
    Collections: {},
    Views: {},
    Course: null,
    Courses: null,
    CourseList: null,
    Student: null,
    Students: null,
    StudentList: null,
    Document: null,
    Documents: null,
    DocumentList: null,
    Team: null,
    Teams: null,
    TeamList: null
  };

  
$(function() { 

  // Run this code when the DOM is ready
  
    window.tom = new App.Models.Course({
        nameCourse: 'Test Course Name',
	    startingBudget: '80000',
	    enableNarrative: true,
	    message: '<p>Message to sent everyone.</p>',
	    active: true,
  });
    
    

  App.Courses = new App.Collections.Courses();
  App.Documents = new App.Collections.Documents();
  App.Teams = new App.Collections.Teams();
  App.Students = new App.Collections.Students();
  
  App.Courses.add(window.tom);

  App.Courses.add({
        nameCourse: 'Some Other Course Name',
	    startingBudget: '100,000',
	    enableNarrative: true,
	    message: '<p> Message to send everyone.</p>',
	    active: true,
  });
  
  App.Students.add({
	    firstName: 'First Name 1',
	    lastName: 'Last Name 1',
	    email: 'email@email.com',
	    username: 'username',
  });
  
  
  App.Students.add({
	    firstName: 'First Name 2',
	    lastName: 'Last Name 2',
	    email: 'email@email.com',
	    username: 'username',
  }); 
  
  
  
  
  
  App.CourseList = new App.Views.CourseList({
	    el: $('#course_display')
	  });

	  App.CourseList.render();

	  App.Courses.on('add remove', function() {
	    App.CourseList.render();
  });

});
