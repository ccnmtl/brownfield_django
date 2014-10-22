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
	     return url
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
		this.template = _.template(jQuery("#student-list-template").html()),

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
  		this.model.set('first_name', jQuery(this.el).find("input.edt-frst-name").val());
  		this.model.set('last_name', jQuery(this.el).find("input.edt-last-name").val());
  		this.model.set('email', jQuery(this.el).find("input.edt-email").val());
   		this.model.save(
//	        //wait: true,
//	        null,
//	        {
//	            success: function (model, response) {
//	                console.log("success");
//	            },
//	            error: function (model, response)
//	            {
//	                console.log("error");
//	            }
	//        }
    );
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
	'click .student_submit' :	'addStudent'
    },
    
    initialize: function (options)
    {
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
    	e.preventDefault();
    	this.student_collection_view.course_students.create(
    	    {   
    	        	first_name : jQuery(".frst-name").val(),
    	            last_name : jQuery(".last-name").val(),
    	            email : jQuery(".email").val()
    	    },
    	    {
    	        wait: true,
    	    	url: this.student_collection_view.course_students.url()
    	    }
    	);
    	//this.student_collection_view.course_students.fetch({processData: true, reset: true});
        //console.log(this.student_collection_view.course_students);
	    jQuery(".add-std-frm-title").hide();
	    jQuery(".add-std-frm").hide();
	    jQuery(".add-std-btn").show();
	    return false;
    }
    
});// End UserControlView  

jQuery(document).ready(function () {

	var course = jQuery("input[name='crs-id']").val();

    var student_control_view = new StudentControlView({
        el: jQuery('.student_controls'),
        course: course
    });
});