// creating course model
var Course = Backbone.Model.extend({

    urlRoot: '/update_course/',
    
    defaults: function() {
        return {
            name: "Default name",
            //password: "password",
            startingBudget: "startingBudget",
            enableNarrative: "enableNarrative",
            message: "message",
            active: false,
            archive: false,
            professor: "Default professor"
        }
    },
       
	initialize: function(attributes) 
	{
	    name = attributes.name || '<EMPTY>';
	}
	    
});

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
        console.log("Inside course view");
        this.$el.html(html);
        return this;

    },
    	
    clear: function() {
        this.model.destroy();
        //{
        //   	headers : { 'id' : this.model.id }
        //});
    }

});// End CourseView


var UserControlView = Backbone.View.extend({
    //el: $(".course_controls"),

    events: {
	//'click .edit-crs' : 'edit',
	'click .add-crs' : 'showCourseForm',
	'click .submit' :	'addCourse'
    },

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