// creating course model
var Course = Backbone.Model.extend({

    urlRoot: '/course/',
    
    defaults: function() {
        return {
        	// should name have '' around it to match django response
            name: "Default Course"
        }
    },
       
	initialize: function(attributes) 
	{   // not sure if this will cause problems
	    name = attributes.name || '<EMPTY>';
	}
	    
});


/*Should this be two different collections or one collection
 * with an over ridden url when instantiated?
 */
var UserCourseCollection = Backbone.Collection.extend({
	 model: Course,
	 headers: {"content-type": "application/json"},
	 url: '/user_courses/'
});
var AllCourseCollection = Backbone.Collection.extend({
	 model: Course,
	 url: '/all_courses/'
});
// End of Models/Collections

//Views 
var CourseView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Course Template <%= name %> <a href='/course/<%= id %>/'>View Course Details </a> <button class='del-crs'> Remove Course</button> <button class='destroy'> Destroy Class</button>"),
   	//$container: null,
    	
   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},
    	
   	events: {
   		'click .del-crs' : 'clear',
   		'click .destroy' : 'clear'
   	},
    	
    render: function () {
        if (!this.model) 
        {
            throw "Model is not set for this view";
        }
         
        var html = this.template(this.model.toJSON());
        console.log("Inside course view");
        this.$el.html(html);
        return this;

    },
        
  	onRemoveCourse: function()
   	{
   		console.log("You tried to remove course " + this.model.get('id') + this.model.get('name'));
   	},
    	
    clear: function() {
        this.model.destroy({
           	headers : { 'id' : this.model.id }
        });
    }

});// End CourseView

/* Container to hold rows of users courses */
var CourseListView = Backbone.View.extend({
   
    tagName : 'ul',
    
    initialize: function (options)
    {
    	_.bindAll(this,
    			 'render',
    			 'initialRender');
    	//create new collection to hold user courses
    	this.user_course_collection = new UserCourseCollection();
    	this.user_course_collection.fetch({processData: true, reset: true});
    	this.user_course_collection.on('reset', this.initialRender);
	},
	
    render: function() {
               
   },
   
   initialRender: function() {
	   
        // Clean up the view first 
        this.$el.empty();

        // Iterate over the collection and add each name as a list item 
        this.user_course_collection.each(function(model) {
        this.$el.append(new CourseView({
               model: model
        }).render().el);
        }, this);

        return this;
    }
    
});// End CourseListView   


var user_course_collection_view = new CourseListView({el : jQuery('.user_courses #userlist')});

/* Container to hold rows of all courses */
var AllCoursesListView = Backbone.View.extend({
   
    tagName : 'ul',
    
    initialize: function (options)
    {
    	_.bindAll(this,
    			 'render',
    			 'initialRender');
    	//create new collection to hold user courses
    	this.all_courses_collection = new AllCourseCollection();
    	this.all_courses_collection.fetch({processData: true, reset: true});
    	this.all_courses_collection.on('reset', this.initialRender);
	},
	
    render: function() {
               
   },
   
   initialRender: function() {
	   
        this.$el.empty();

        this.all_courses_collection.each(function(model) {
        this.$el.append(new CourseView({
               model: model
        }).render().el);
        }, this);

        return this;
    }
    
});// End CourseListView   
var all_courses_collection_view = new CourseListView({el : jQuery('.all_brwn_courses')});


var UserControlView = Backbone.View.extend({
    //el: $(".course_controls"),

    events: {
	//'click .edit-crs' : 'edit',
	'click .add-crs' : 'showCourseForm',
	'click .submit' :	'addCourse'
    },

    //initialize: function() {
    //
    //    this.input = this.$("#new-todo");
    //    this.allCheckbox = this.$("#toggle-all")[0];
    //},

    showCourseForm: function(e) {
		console.log("clicked on show course");
		jQuery(".add-crs").hide();
		jQuery("#frm-title").show();
		jQuery("#add-crs-frm").show();
    },

    addCourse: function(course) {
    	
    	user_course_collection_view.user_course_collection.create(
    	{
    				name : jQuery(".crs-name").val()
    	});

	    jQuery("#frm-title").hide();
	    jQuery("#add-crs-frm").hide()
    }
});// End UserControlView  

var user_control_view = new UserControlView({el : jQuery('.course_controls')});


