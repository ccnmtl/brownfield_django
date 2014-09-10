jQuery(document).ready(function(){

    // handle hash tag navigation
    var hash = window.location.hash;
    hash && jQuery('.instructor-nav a[href="' + hash + '"]').tab('show');
  
    // when the nav item is selected update the page hash
    jQuery('.instructor-nav a').on('shown', function (e) {
        window.location.hash = e.target.hash;
        scrollTo(0,0);
    });
	
    //BEGINING OF BB CODE
	var Course = Backbone.Model.extend({
		
	    defaults:
	    {
	          name: "Course"
	    },
	    
	    initialize: function(attributes) 
	    {
	        var name = attributes.name || '<EMPTY>';
	        console.log("Initializing a new course model for '" +
	          name + "'.");
	    }
	});

	var CourseCollection = Backbone.Collection.extend({
		model: Course,
	});

	// some sites have
	//var course_collection = new CourseCollection;
	//others have
    var course_collection = new CourseCollection();

    course_collection.add({
		    name: 'Test Course 1'
    });
	
	
	var courseListing = '';
	course_collection.each(function(course) {
		console.log("Adding course model for '" + course.get('name') + "'.");
		courseListing += "<div>" +
	    course.get('name') + " ";
	    courseListing += "</div>";
	  });
	
	console.log("Attempting to view courseListing '" + courseListing + "'.");
	
	jQuery('#bb_main').html(courseListing);
	

});


/* Need to create a Router, should model have a url?
 * 
 * url is location of model on server
 * if you do get request on /courses a JSON array of courses should be returned
 * presumably also means if we do a POST to courses it will store a new course in the db
 * array must be returned as JSON the content type must be application/json
 * 
 * */
//var CourseView = Backbone.View.extend({
//
//		initialize: function(){
//         this.render();
//     },
//	
//		render: function() {
//			//Pass variables in using Underscore.js Template
//			var course_vars = { course_name: "Course Name" };
//			// Compile the template using underscore
//			var template = _.template( jQuery("#course_template").html(), course_vars );
//			// Load the compiled HTML into the Backbone "el"
//	        this.jQuery(el).html( template );
//		}
//	
//	});

//	var CourseListView = Backbone.View.extend({
//	
//		template: _.template('<h4>All Courses</h4><ul></ul><br><button data-toggle="modal" class="btn btn-sm btn-success" type="button"> Add Course </button></br>'),
//	
//		render: function() {
//		
//			this.el.innerHTML = this.template();
//			var ul = this.jQuery(el).find("ul");
//			this.collection.forEach(function course)
//			{
//				ul.append(new CourseListView)({
//					model: course
//				}).render().el);
//			});
//			return this;
//		}
//	});
//

//jQuery("#bb_main").append(new CourseListView({
//collection: courses
//}).render().el);
//});