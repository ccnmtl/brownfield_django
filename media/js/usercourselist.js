var Course = Backbone.Model.extend({

    urlRoot: '/course/',
    
    defaults: function() {
        return {
            name: "Default Course"
        }
    },
    
	initialize: function(attributes) 
	{   // not sure if this will cause problems
	    this.name = attributes.name || '<EMPTY>';
	    //console.log("Initializing a new course model for '" +
	    //  name + "'."); 
	}
	    
});

/*Should this be two different collections or one collection
 * with an over ridden url when instantiated?
 */
var UserCourseCollection = Backbone.Collection.extend({
	 model: Course,
	 url: '/user_course'
});
var AllCourseCollection = Backbone.Collection.extend({
	 model: Course,
	 url: '/all_course'
});
// End of Models/Collections


//Views 
var CourseView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Course Template <%= name %>" +
   			              "<a href='/course/<%= id %>/'>" +
   			              "View Course Details </a>" +
   			              "<button class='view-crs'>" +
   			              "View Course Details </button>" +
   			              "<a href='/course/<%= id %>/'>" +
			              "Edit Course Details </a>" +
			              "<button class='edit-crs'>" +
			              "Edit Course Details </button>" +
   			              "<button class='del-crs'>" +
   			              "Remove Course</button>" +
   			              "<button class='destroy'>" +
   			              "Destroy Class</button>"),
   			  
   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	events: {
   		// 'click .del-crs' : 'onRemoveCourse',
   		'click .edit-crs' : 'edit',
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

   	// Adds the id to the url for the DELETE
    clear: function() {
        this.model.destroy({
           	headers : { 'id' : this.model.id }
        });
    }    

});// End CourseView


var userCourseCollection = new UserCourseCollection;
var allCourseCollection = new AllCourseCollection;

/* Container to hold rows of courses */
var UserCourseListView = Backbone.View.extend({

	//setting its element to the outermost div so it has access to whole page
	el: $(".user_courses"),
	collection: userCourseCollection,
    
    initialize: function() {
    	this.smtbutton = this.$("#submit-crs");
    	this.addcrsfrm = this.$("#add-crs-frm");
        this.course_list = this.$("#userlist .courselistview");
        console.log(this.course_list);
        this.listenTo(userCourseCollection, 'add', this.addCourse);
        this.listenTo(userCourseCollection, 'reset', this.addAllCourses);
        this.listenTo(userCourseCollection, 'all', this.render);
        
        userCourseCollection.fetch();
        //console.log("userCourseCollection");
        //console.log(userCourseCollection);
    },

    render: function()
    {        
        this.collection.each(function(model)
        {
        	console.log(model['name']);
            var new_course_view = new CourseView({ model: model });
            this.course_list.append(new_course_view.render());
            return this;
        });
        return this;
    }//,
    

    
//    addCourse: function(new_crs) {
//        var view = new CourseView({model: new_crs});
//        this.$(".user_courses").append(view.render().el);
//    }

});// End CourseListView    

var App = new UserCourseListView;
// should probably move this code to controller below not sure if that is be
//var UserCourseView = new CourseListView({
//    collection: course_collection
//});
//var AllCourseView = new CourseListView({
//    collection: course_collection
//});
//course_collection_view.render().el;

//jQuery('.user_courses').append(course_collection_view.render().el);

