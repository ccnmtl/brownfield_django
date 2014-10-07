//creating student model
var Student= Backbone.Model.extend({
    
    defaults: function() {
        return {
            first_name: "First Name Student",
            last_name: "Last Name Student",
            email: "email@email.com",
        }
    },

    initialize: function(attributes) 
	{   
	    first_name = attributes.first_name || '<EMPTY>';
	    last_name = attributes.last_name || '<EMPTY>';
	    email = attributes.last_name || '<EMPTY>';
	    //last_name = attributes.last_name || '<EMPTY>';
	}
	    
});


var StudentCollection = Backbone.Collection.extend({
	 model: Student,
	 url: function() {
		    return '/student/' + crs_id;
	  }
});
//End of Modes/Collections


//Views 
var StudentView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Student Template Name <%= first_name %>" +
   			             "<%= last_name %> " +
   			             "Email: " +
   			             "<%= email %> " +
   			             "<button class='btn btn-xs st-team'>" +
			             "Put Student In Team" +
			             "</button>" +
   			             "<button class='btn btn-xs rm-st'>" +
			             "Remove Student From Course" +
			             "</button>"),

   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	// Can probably combine into one function on change
   	events: {
   		'click .st-team' : 'joinTeam',
   		'click .rm-st' : 'removeStudent'
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

   	//will need to do save which will automatically call sync
   	removeStudent: function()
   	{
   		console.log("Removing student from course.");//console.log("Revoking Document");
    },

   	//will need to do save which will automatically call sync
    joinTeam: function()
   	{
   		console.log("Putting student in team.");
    }
    
    
    
});// End Student View



/* Container to hold rows of students */
var StudentListView = Backbone.View.extend({

    tagName : 'ul',

    initialize: function (options)
    {
    	_.bindAll(this,
    			 'render',
    			 'initialRender');
    	this.course_students = new StudentCollection();
    	this.course_students.fetch({processData: true, reset: true});
    	this.course_students.on('reset', this.initialRender);
	},

    render: function() {
    },

    initialRender: function() {

        this.$el.empty();

        this.course_students.each(function(model) {
        this.$el.append(new StudentView({
               model: model
        }).render().el);
        }, this);

        return this;
    }
    
});// End StudentListView    



var student_collection_view = new StudentListView({el : jQuery('.student-list')});


var StudentControlView = Backbone.View.extend({

    events: {
	//'click .edit-crs' : 'edit',
	'click .add-std-btn' : 'showStudentForm',
	'click .student_submit' :	'addStudent'
    },

    showStudentForm: function() {
		//console.log("clicked on show student form");
		jQuery(".add-std-btn").hide();
		jQuery(".add-std-frm-title").show();
		jQuery(".add-std-frm").show();
    },

    addStudent: function(course) {
    	
    	student_collection_view.course_students.create(
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

var student_control_view = new StudentControlView({el : jQuery('.student_controls')});
