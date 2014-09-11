//jQuery(function() {

	// creating course model
	var Course = Backbone.Model.extend({
		
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

    
    /* Should have two Views - Collection View that holds
    * individual course items and listens for an addCourse
    * event, we also need a CourseView for each individual
    * course that will remove itself when deleted, or 
    * redirect the user to a django DetailView of the
    * individual course.
    */
    
    //Attempting Views Again...
    // NOTE: this is NOT the best way to do it, should be using document fragments
    var CourseView = Backbone.View.extend({

    	tagName : 'li',
    	template: _.template('Course Template <%= name %> <button class="del-crs"> Remove Course</button> '),
    	//$container: null,
    	
    	/* using initialize to rerender the element if anything in its 
    	 * corresponding model changes use listenTo instead of on so it will automatically
    	 *  unbind all events added when it is destroyed */
    	initialize: function () {
    	    this.listenTo(this.model, 'change', this.render);
    	},
    	
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
//            var tpl = _.template(this.template),
//            html = tpl(this.model.toJSON());
//
//            this.$el.html(html);
//            return this;
        },
        
    	onRemoveCourse: function()
    	{
    		//will add delete functionality later
    		console.log("You tried to remove course " + this.model.get('id') + this.model.get('name'));
    	}
    	
    });// End CourseView

	// End of Models/Collections
    
    var CourseListView = Backbone.View.extend({
    	
    	tagName : 'ul',
    	
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
        }
    
	});// End CourseListView    

    


    var course_collection_view = new CourseListView({
        collection: course_collection
    });

    jQuery('.user_courses').append(course_collection_view.render().el);

    console.log(course_collection)    
    
    
    
    
    
//    jQuery('.user_courses').append(test_crs.render().el);
    
    
    

 	  


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