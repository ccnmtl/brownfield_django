// creating course model
var Course = Backbone.Model.extend({

    urlRoot: '/course/',
    
    defaults: function() {
        return {
            name: "Default Course"
        }
    },

	url : function() {
	    if (this.isNew())
	    	{
	    	console.log("Model is new"); 
	    	console.log("Model urlRoot : " + this.urlRoot);
	    	console.log("Model name : " + this.name); 
	    	return this.urlRoot + encodeURIComponent(this.name) + '/';
	    	}
		return this.urlRoot + this.id + '/';
    },
    

	    
	initialize: function(attributes) 
	{   // not sure if this will cause problems
	    this.name = attributes.name || '<EMPTY>';
	    console.log("Initializing a new course model for '" +
	      name + "'."); 
	}
	    
});

	
var CourseCollection = Backbone.Collection.extend({
	 model: Course,
	 url: '/course'
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
    
//Views 
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
   	//This correctly adds the id to the url for the DELETE
   	//but django still has internal error
    clear: function() {
        this.model.destroy({
           	headers : { 'id' : this.model.id }
        });
    }

});// End CourseView

    
/* Container to hold rows of courses */
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
    },
    
    addCourse: function(new_crs) {

        this.collection.create(
        		{name : new_crs}, 
        		{wait: true,
            	success: function(data_array){
            		data = data_array.models[0].attributes;
            		data = JSON.stringify(data);
            		console.log("data is " + data);
                    console.log("in success");
                    //console.log(data);
                },
                error: function(data_array){
                	data = data_array.models[0].attributes;
            		data = JSON.stringify(data);
                	console.log("data is " + data);
                    console.log("in error");
                }}
        );
        this.render();
        return this;
  
    }, //end add course
    

    add_course: function(new_crs) {
    	console.log("Inside collection add_course ");
    	var nc = new Course({name : new_crs});
    	nc.save();
        this.collection.add(nc, {merge: true});
        console.log("nc " + nc);
        this.render();
        return this;
  
    } //end add_course
    
    
});// End CourseListView    

    

// should probably move this code to controller below not sure if that is be
var course_collection_view = new CourseListView({
    collection: course_collection
});

// connecting the views to the html/page
jQuery('.user_courses').append(course_collection_view.render().el);

console.log(course_collection); // log collection to console


//Need to test create()
var test = course_collection.create({
  name: "Othello"
});



//Need to test model save()
var mtest = new Course({ name : "why doesn't it use defaults?"});
mtest.save({data:{name:"why doesn't it use defaults?"},type:'POST' });





/*For some reason I can't get the container of course list to respond on click to the button - because I specified tag ul maybe?*/
jQuery('.add-crs').on('click',
		
		function() {
            jQuery('.controls form').show();
            jQuery('input.name').focus();
});
    
jQuery('#add-crs-frm').on('submit',
    function(event) {
        event.preventDefault();
        var new_name = jQuery('#add-crs-frm input.name').val();
        course_collection_view.addCourse(new_name);
        //course_collection.create({name : something}]);

});

var CourseRouter = Backbone.Router.extend({
	routes: {
	'teacher/:id': 'showCourses',
	//'user/:id': 'showUserDetails'//,
	//'user/:id/update': 'updateUser',
	//'user/:id/remove': 'removeUser'
	},
	showUsers: function () {
	// Get all the courses from server and show
		console.log("Router method running...");
	    course_collection_view.render().el
	}//,
//	showUserDetails: function (userId) {
//	// Get the user details for the user id as received
//	},
//	updateUser: function (userId) {},
//	removeUser: function (userId) {}
});
