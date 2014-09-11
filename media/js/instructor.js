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
    
    
    
    
    
    
    //Attempting Views Again...
    var CourseView = Backbone.View.extend({
    	// You can stick template HTML directly in view as a variable
    	// did not know that...
    	template: _.template('Course Template <%= name %> <button class="del-crs"> Remove Course</button> '),
    	//$container: null,
    	
    	events: {
    		'click .del-crs' : 'onRemoveCourse'
    	},
    	
        render: function () {
            if (!this.model) 
            {
                throw "Model is not set for this view";
            }
            
            var html = this.template(this.model.toJSON());
            
            this.$el.html(html);
            return this;
        },
        
    	onRemoveCourse: function()
    	{
    		//will add delete functionality later
    		console.log("You tried to remove a course...");
    	}
    	
    });// End CourseView

    //Instantiate and see if it works...
    //Works in Console...???
    var test_crs = new CourseView({
    	
    	model: new Course({
    		
    	    name: 'Test Course Model In View'
    	    
    	})
    	
    });

    
    jQuery('.user_courses').append(test_crs.render().el);
    
    
    

 	  
//            initialize: function()//options)
//            {
//            	this.render();
//               // _.bindAll(this, 'render', 'insert');
//               // this.$container = options.$container;
//               // this.listenTo(this.model, 'change', this.render);
//               // this.insert();
    //
//            },
//        	
//            //render: function()
//            //{
//            //    this.$el.html(this.template(this.model.attributes));
//            //    return this;
//            //},   
//            
////            render: function(){
////                //Pass variables in using Underscore.js Template
////                var variables = { name: "Test Course Template Vars" };
////                // Compile the template using underscore
////                var template = _.template( $("#ctemp").html(), variables );
////                // Load the compiled HTML into the Backbone "el"
////                this.$el.html( template );
////            },
//            
//            //insert: function()
//            //{
//            //    this.$container.append(this.$el);
//            //}
//            
//            
//            render: function(){
//                this.$el.html('<li>' + this.model.get('name') + '</li>');
    //
//                // Returning the object is a good practice
//                // that makes chaining possible
//                return this;
//            }
    //
//            
//            
//            

    //
    //
//        var CourseListView = Backbone.View.extend({
    //
//            initialize: function() 
//            {
//                this.bbmain = $('#bb_main');
    //
//                this.listenTo(course_collection, 'change', this.render);
    //
//                course_collection.each(function(course){
    //
//                    var view = new CourseView({ model: course });
//                    $('#bb_main').append(view.render().el);
    //
//                }, this);	// "this" is the context in the callback
//                //_.bindAll(this, 'render');
//                //console.log("Initializing a new CourseListView for '" + this + "'.");
//            },
//            
//    		render: function() 
//    		{
//    		    var $container = this.$('#courselistview').empty();
    //
//    		    course_collection.each(function(course) 
//    		    {
//    		        new CourseView(
//    		        {
//    		            model: course,
//    		            $container: $container
//    		        }).render();
//    			});
    //
//    		    return this;
//    		    
//    		 }//End render()
//           
//    	});// End CourseListView
    //    
    //    
    //    
    //    
    //
//        new CourseListView();
    //
    ////render: function(){
    ////
////        _.each(course_collection.getChecked(), function(elem){
////            total += elem.get('price');
////        });
    ////
////        // Update the total price
////        this.total.text('$'+total);
    ////
////        return this;
    ////}
    ////
//        var course_list = new CourseListView({
//            el: $('#bb_main')
//        });
    //
//        course_list.render();
    //
    //   // course_collection.on('add remove', function() {
    //   //     course_list.render();
    //   // });
        

        /*Testing Course View with very simple code from book
         * */
        
//        var CourseView = Backbone.View.extend({
//        	el: '#uniq_id_test'
//            render: function () {
//                var html = "Test Course Name Here";
//                this.$el.html(html);
//                return this;
//            }
//        });
    //
//        // create an instance
//        //var courseView = new CourseView();
//        //$('#uniq_id_test').append(courseView.render().el);
//        new CourseView.render();
    
    
    
    
    
    
    
    
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