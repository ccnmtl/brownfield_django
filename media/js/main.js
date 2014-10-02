  var App = {
    Models: {},
    Collections: {},
    Views: {},
    //Routers: {},
    Course: null,
    CourseCollection: null,
    Document: null,
    DocumentCollection: null,
    Student: null,
    StudentCollection: null,
    Team: null,
    TeamCollection: null,
  };

  
$(function() { 

  // Run this code when the DOM is ready
  
	
	App.CourseCollection = new App.Collections.CourseCollection();
	App.DocumentCollection = new App.Collections.DocumentCollection();
	App.TeamCollection = new App.Collections.TeamCollection();
	App.StudentCollection = new App.Collections.StudentCollection();
  
  App.CourseList = new App.Views.CourseList({
	    el: $('#course_display')
	  });

	  App.CourseList.render();

	  App.Courses.on('add remove', function() {
	    App.CourseList.render();
  });

});
