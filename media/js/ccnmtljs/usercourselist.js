// creating course model
var Course = Backbone.Model.extend({

    urlRoot: '/course/',
    
    defaults: function() {
        return {
            name: "Default Course"
        }
    },
       
	initialize: function(attributes) 
	{
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
   	template: _.template("Course Template <%= name %> <a href='/course/<%= id %>/'>View Course Details </a> <button class='destroy del-crs'> Destroy Class</button>"),
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
        this.$el.html(html);
        return this;

    },
    	
    clear: function() {
        this.model.destroy();
    }

});// End CourseView

/* Container to hold rows of users courses */
var CourseListView = Backbone.View.extend({
   
    tagName : 'ul',
    
    initialize: function (options)
    {
    	_.bindAll(this,
    			 'initialRender');
    	//create new collection to hold user courses
    	this.user_course_collection = new UserCourseCollection();
    	this.user_course_collection.fetch({processData: true, reset: true});
    	this.user_course_collection.on('reset', this.initialRender);
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

    showCourseForm: function(e) {
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


