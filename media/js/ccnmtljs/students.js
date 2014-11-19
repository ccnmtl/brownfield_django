//creating student model
var Student= Backbone.Model.extend({

	   urlRoot: '/api/student/',
	   url: function() {
	       var url = this.urlRoot;
	       if (this.get('id') !== undefined) {
	           url += this.get('id') + '/';
	       }
	       return url;
	   }	    
});

var StudentCollection = Backbone.Collection.extend({
	
	 model: Student,
	 urlRoot: '/api/student/',
	 url: function() {
	     var url = this.urlRoot;
	     if (this.course) {
	         url += '?course=' + this.course;
	     }
	     return url;
	 },
	 initialize : function(options){
	     if (options && 'course' in options) {
	         this.course = options.course;
	     }
	 }
});
//End of Modes/Collections


//Views
var StudentView = Backbone.View.extend({

	tagName : 'li',

	initialize: function(options)
	{
		_.bindAll(this, 'editStudent');
		this.template = _.template(jQuery("#student-list-template").html());
        // need to bind the edit form to the model - when change made to form change model
		this.listenTo(this.model, 'change', this.render);
		this.listenTo(this.model, 'destroy', this.remove);
	},

   	events: {
   		'click .ed-st' : 'showEditForm',
   		'click .save-edit-student' : 'editStudent',
   		'click .rm-st' : 'removeStudent'
   	},

    render: function () {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },
    
   	showEditForm: function()
   	{
   	    var html = _.template(jQuery("#student-edit-template").html())(this.model.toJSON());
        this.$el.html(html);
    },
    
   	editStudent: function(e)
   	{
   		e.preventDefault();
   		var std_fname = jQuery(this.el).find("input.edt-frst-name").val();
   		var std_lname = jQuery(this.el).find("input.edt-last-name").val();
        var std_email = jQuery(this.el).find("input.edt-email").val();
   		/* For some reason setting the attributes below only sets correctly if you edit
   		 * email, pulling the varibles here because here they are correct and then passing.
   		 * */
  		this.model.set('first_name', std_fname);
  		this.model.set('last_name', std_lname);
  		this.model.set('email', std_email);
   		this.model.save({
	        success: function(model, response) 
	        {},
            error: function(model, response)
            {
            	alert("An error occured!");
            	//this.$el.append("<p>Something went wrong, please try again.</p>");
            },
            wait: true
        });//end save
    },
    
   	removeStudent: function()
   	{
   		this.model.destroy();
    }
});// End Student View



/* Container to hold rows of students */
var StudentListView = Backbone.View.extend({

    tagName : 'ul',

    initialize: function (options)
    {
    	_.bindAll(this, 'initialRender', 'addStudent');
    	this.course_students = new StudentCollection(options);
    	this.course_students.fetch({processData: true, reset: true});
    	this.course_students.on('reset', this.initialRender);
    	this.course_students.on('add', this.addStudent);
	},	

    initialRender: function() {
        this.course_students.each(function(model) {
        this.$el.append(new StudentView({
               model: model
        }).render().el);
        }, this);

        return this;
    },
    
    addStudent: function(model, collection, options) {
        this.$el.append(new StudentView({
            model: model
        }).render().el);
    }
    
});// End StudentListView

var StudentControlView = Backbone.View.extend({

    events: {
	'click .add-std-btn' : 'showStudentForm',
	'click .student_submit' :	'validateStudentForm'//'addStudent'
    },
    
    initialize: function (options)
    {
    	_.bindAll(this, 'addStudent', 'validateStudentForm');
        this.student_collection_view = new StudentListView({
            el: jQuery('.student-list'),
            course: options.course
        });
    },

    showStudentForm: function() {
		jQuery(".add-std-btn").hide();
		jQuery(".add-std-frm-title").show();
		jQuery(".add-std-frm").show();
    },
    
    addStudent: function(e) {
    	
    	this.student_collection_view.course_students.create(
    	    {   
    	        	first_name : jQuery(".frst-name").val(),
    	            last_name : jQuery(".last-name").val(),
    	            email : jQuery(".email").val()
    	    },
    	    {
                error: function(model, response)
                {
                	jQuery(".add-team-frm").append("<p>Something went wrong, please try again.</p>");
                },
    	        wait: true,
    	    	url: this.student_collection_view.course_students.url()
    	    }
    	);
	    jQuery(".add-std-frm-title").hide();
	    jQuery(".add-std-frm").hide();
	    jQuery(".add-std-btn").show();
	    return false;
    },
    
    
    validateStudentForm: function(e) {
    	e.preventDefault();
    	
    	//there is probably a better way to do this... should also be it's own method like checkBlank
    	//if((jQuery(".add-std-frm input[class=frst-name").val().length) === 0)
    	if((jQuery(".add-std-frm input.frst-name").val().length) === 0)
    	{
    		if((jQuery(".first-name-box").has('b').length) === 0)
    		{
    			jQuery(".first-name-box").append("<b>Please enter a first name.</b>").css('color', 'red');
    		}
    	}
    	if((jQuery(".add-std-frm input.last-name").val().length) === 0)
    	{
    		if((jQuery(".last-name-box").has('b').length) === 0)
    		{
    			jQuery(".last-name-box").append("<b>Please enter a last name.</b>").css('color', 'red');
    		}
    	}
    	if((jQuery(".add-std-frm input.email").val().length) === 0)
    	{
    		if((jQuery(".email-box").has('b').length) === 0)
    		{
    			jQuery(".email-box").append("<b>Please enter a email.</b>").css('color', 'red');
    		}
    	}
    	//check whatever they put for email looks something like an actual address
    	else if((jQuery(".add-std-frm input.email").val().length) !== 0)
    	{
    	    if((jQuery(".add-std-frm input.email").val().indexOf("@")  === -1) && 
    	       (jQuery(".add-std-frm input.email").val().indexOf(".") === -1))
    	    {
    		    if((jQuery(".email-box").has('b').length) === 0)
    		    {
    			    jQuery(".email-box").append("<b>Please enter a valid email.</b>").css('color', 'red');
    		    }
    	    }
    	}
    	//if above tests pass reasonable to submit
    	this.addStudent();
    }
    
});// End UserControlView  

jQuery(document).ready(function () {
	
	//var crs_active = jQuery("input[name='crs-active']").val();
	var course = jQuery("input[name='crs-id']").val();

    var student_control_view = new StudentControlView({
        el: jQuery('.student_controls'),
        course: course
    });
});
