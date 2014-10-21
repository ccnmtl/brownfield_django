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

    //editTemplate: _.template(jQuery("#student-edit-template").html()),
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

//    renderEditForm: function () {
//        var html = this.editTemplate(this.model.toJSON());
//        this.$el.html(html);
//        return this;
//    },
    
   	showEditForm: function()
   	{
   		//console.log("Show edit form.");
   	    var html = _.template(jQuery("#student-edit-template").html())(this.model.toJSON());
        this.$el.html(html);
    },
    
   	editStudent: function(e)
   	{
   		e.preventDefault();
   		//console.log(jQuery(this.el).find("input.edt-frst-name").val());
  		this.model.set('first_name', jQuery(this.el).find("input.edt-frst-name").val());
  		this.model.set('last_name', jQuery(this.el).find("input.edt-last-name").val());
  		this.model.set('email', jQuery(this.el).find("input.edt-email").val());
   		this.model.save();
    },
    
   	removeStudent: function()
   	{
   		//console.log("Removing student from course.");
   		this.model.destroy();
    }
});// End Student View



/* Container to hold rows of students */
var StudentListView = Backbone.View.extend({

    tagName : 'ul',

    initialize: function (options)
    {
    	_.bindAll(this, 'initialRender');
    	this.course_students = new StudentCollection(options);    	
    	this.course_students.fetch({processData: true, reset: true});
    	this.course_students.on('reset', this.initialRender);
	},	
	
    initialRender: function() {
        this.course_students.each(function(model) {
        this.$el.append(new StudentView({
               model: model
        }).render().el);
        }, this);

        return this;
    }
    
});// End StudentListView

var StudentControlView = Backbone.View.extend({

	course: jQuery("input[name='crs-id']").val(),

    events: {
	'click .add-std-btn' : 'showStudentForm',
	'click .student_submit' :	'addStudent'
    },
    
    initialize: function (options)
    {
    	/* HERE WE INITIALIZE THE LIST VIEW WITE A COURSE, SHOULD BE INCLUDED
    	 * IN ALL COLLECTION ACTIONS BUT IS NOT BEING INCLUDED IN ADD STUDENT
    	 * FOR SOME REASON. 
    	 * Ahhh... because right now we are in the control view not the collection view
    	 * */
        this.student_collection_view = new StudentListView({
            el: jQuery('.student-list'),
            course: this.course
        });
    },

    showStudentForm: function() {
		//console.log("clicked on show student form");
    	//console.log(this.student_collection_view.url),
		jQuery(".add-std-btn").hide();
		jQuery(".add-std-frm-title").show();
		jQuery(".add-std-frm").show();
    },

    addStudent: function(course) {
    	this.student_collection_view.course_students.create(
    	{   
    		first_name : jQuery(".frst-name").val(),
    	    last_name : jQuery(".last-name").val(),
    	    email : jQuery(".email").val(),
    	});

	    jQuery(".add-std-frm-title").hide();
	    jQuery(".add-std-frm").hide();
	    jQuery(".add-std-btn").show();
    }
    
});// End UserControlView  

jQuery(document).ready(function () {
    var student_control_view = new StudentControlView({
        el: jQuery('.student_controls')
    });
});
