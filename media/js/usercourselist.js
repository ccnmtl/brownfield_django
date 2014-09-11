//jQuery(function() {

	// creating course model
	var Course = Backbone.Model.extend({
		url: 'courses',
	    defaults:
	    {
	    	id: 0,
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
	
	
	// creating course collection with test courses
    var course_collection = new CourseCollection([
        {
    		id: 1,
			name: 'Test Course 1'
		},
		{
			id: 2,
			name: 'Test Course 2'
		},
		{
			id: 3,
			name: 'Test Course 3'
		},
		{
			id: 4,
			name: 'Test Course 4'
		},
		{
			id: 5,
			name: 'Test Course 5'
		},
		{
			id: 6,
			name: 'Test Course 6'
		},
		{
			id: 7,
			name: 'Test Course 7'
		}
    ]);

	// End of Models/Collections
    
    /* Should have two Views - Collection View that holds
    * individual course items and listens for an addCourse
    * event, we also need a CourseView for each individual
    * course that will remove itself when deleted, or 
    * redirect the user to a django DetailView of the
    * individual course.
    */
    
    //Attempting Views Again...
    var CourseView = Backbone.View.extend({

    	tagName : 'li',
    	template: _.template('Course Template <%= name %> <button class="del-crs"> Remove Course</button> <button class="destroy"> Destroy Class</button>'),
    	//$container: null,
    	
    	/* using initialize to re-render the element if anything in its 
    	 * corresponding model changes use listenTo instead of on so it will automatically
    	 *  unbind all events added when it is destroyed */
    	initialize: function () {
    	    this.listenTo(this.model, 'change', this.render);
    	    this.listenTo(this.model, 'destroy', this.remove);
    	},
    	
    	// is there a build in way to remove the model?
    	events: {
    		'click .del-crs' : 'onRemoveCourse',
    		//TODO
    		'click .destroy' : 'clear'
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
    		console.log("You tried to remove course " + this.model.get('id') + this.model.get('name'));
    	},
    	
    	//TODO
        clear: function() {
            this.model.destroy();
        }
    	
    });// End CourseView

    
    var CourseListView = Backbone.View.extend({
    	
    	tagName : 'ul',
    	
    	events: {
    		//TODO
    		'click button .add-crs' : 'addCourse'
  			'submit .add-crs-frm form': 'addSubmit'
    	},
    	
        render: function() {
        	
            // Clean up the view first 
            this.$el.empty();

            // Iterate over the collection and add each name as a list item
            this.collection.each(function(model) {
                this.$el.append(new CourseView({
                    model: model
                }).render().el);
            }, this);

            return this;
        },
        
        //TODO
        addCourse: function(course) {
        	
        	this.$el.append(new CourseView({
        		model: model
            }).render().el);

    	}
	});// End CourseListView    

    


    var course_collection_view = new CourseListView({
        collection: course_collection
    });

    // connecting the views to the html/page
    jQuery('.user_courses').append(course_collection_view.render().el);

    console.log(course_collection); // log collection to console
    
    
    var AppRouter = Backbone.Router.extend({
        routes: {
            'courses': 'showCourses'//,
//            'course/:id': 'showCourseDetails',
//            'course/:id/update': 'updateCourse',
//            'course/:id/remove': 'removeCourse'
        }//,
        
//        showCourses: function () {
//            // Get all the user details from server and
//            // show the users view
//        },
        
//        showCourseDetails: function (userId) {
//                // Get the user details for the user id as received
//        },
//        
//        updateCourse: function (userId) {},
//        
//        removeCourse: function (userId) {}
    });
    
    
    
    
//});
