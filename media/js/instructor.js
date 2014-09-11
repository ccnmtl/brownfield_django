//jQuery(function() {

	// creating course model
	var Course = Backbone.Model.extend({
		
	    defaults:
	    {
	          name: "Default Course"
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

	
	// creating course collection
    var course_collection = new CourseCollection();

    
    // adding courses to the collection
    course_collection.add({
		name: 'Test Course 1'
    });

    course_collection.add({
	    name: 'Test Course 2'
    });
    
    
//    var UserView = Backbone.View.extend({
//        
//        //el: '#container',
//    	
//        render: function () 
//        {
//            var html = "Backbone.js rocks!";
//            this.$el.html(html);
//            return this;
//        }
//    });
//    	 //create an instance
//    var userView = new UserView();
//    console.log("Initializing a new user view for '" + userView + "'.");
//    console.log("Initializing a new user view for '" + userView.name + "'.");
//    $('#container').append(userView.render().el);
//    //new UserView.render();
    
    
    
    
    
    
    
    
    
    
    
//});


/* Need to create a Router, should model have a url?
 * 
 * url is location of model on server
 * if you do get request on /courses a JSON array of courses should be returned
 * presumably also means if we do a POST to courses it will store a new course in the db
 * array must be returned as JSON the content type must be application/json
 * 
 * */
//jQuery("#bb_main").append(new CourseListView({
//collection: courses
//}).render().el);
//});