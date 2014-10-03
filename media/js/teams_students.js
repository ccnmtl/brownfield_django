// creating team model
var Team = Backbone.Model.extend({

    urlRoot: '/team/',
    
    defaults: function() {
        return {
        	id: 0,
            name: "Default Team",
            course: "Default Team Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
        }
    },

    initialize: function(attributes) 
	{   
	    name = attributes.name || '<EMPTY>';
	    //console.log("Initializing a new team model for '" +
	    //  name + "'."); 
	}
	    
});

	
var TeamCollection = Backbone.Collection.extend({
	 model: Team,
	 url: '/team'
});


//creating student model
var Student= Backbone.Model.extend({

    urlRoot: '/student/',
    
    defaults: function() {
        return {
        	id: 0,
            first_name: "First Name Student",
            last_name: "Last Name Student",
            email: "email@email.com",
            //course: "Default Student Course",
            team: "Member of Team....()"
        }
    },

    initialize: function(attributes) 
	{   
	    first_name = attributes.first_name || '<EMPTY>';
	    last_name = attributes.last_name || '<EMPTY>';
	    console.log("Initializing a new student model for '" +
	    		first_name + " " +  last_name + "'.");
	}
	    
});


var StudentCollection = Backbone.Collection.extend({
	 model: Student,
	 url: '/student'
});
	

	
// creating student collection with test courses


//End of Modes/Collections

//Views 
var StudentView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Student Template Name <%= first_name %>" +
   			             "<%= last_name %> " +
   			             "Email: " +
   			             "<%= email %> " +
   			             "Team Status: " +
   			             "<% if (team) { %> <%=team%><% } %>  " +
   			             "<button class='btn btn-xs jn-tm'>" +
   			             "Add to Team" +
   			             "</button>" +
   			             "<button class='btn btn-xs rm-tm'>" +
   			             "Remove From Team" +
   			             "</button>"),

   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	// Can probably combine into one function on change
   	events: {
   		'click .ad-st' : 'addStudent',
   		'click .rm-sm' : 'removeStudent'
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

    joinTeam: function()
   	{   
    	//console.log("Releasing Document");
        this.model.destroy({
           	headers : { 'id' : this.model.id }
        });
   	},

   	//will need to do save which will automatically call sync
   	removeTeam: function()
   	{
   		//console.log("Revoking Document");
        this.model.save({
           	headers : { 'id' : this.model.id }//{ 'method_called' : 'revoke'}//, 'document' : this.model.id }
        });
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
    	console.log(crs_id);
    	console.log('inside initialize');
    	//create new collection to hold students
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
    
});// End DocumentListView    



var student_collection_view = new StudentListView({el : jQuery('.student-list')});


var StudentControlView = Backbone.View.extend({

    events: {
	//'click .edit-crs' : 'edit',
	'click .add-std-btn' : 'showStudentForm',
	//'click .submit' :	'addStudent'
    },

    showStudentForm: function() {
		console.log("clicked on show student form");
		jQuery(".add-std-btn").hide();
		jQuery(".add-std-frm-title").show();
		jQuery(".add-std-frm").show();
    },

//    addStudent: function(course) {
//    	
//    	user_course_collection_view.user_course_collection.create(
//    	{
//    				name : jQuery(".crs-name").val()
//    	});
//
//	    jQuery(".add-std-frm-title").hide();
//	    jQuery(".add-std-frm").hide()
//    }
});// End UserControlView  

var student_control_view = new StudentControlView({el : jQuery('.student_controls')});


//var team_collection_view = new TeamListView({el : jQuery('#course-teams')});
//
//
//var StudentControlView = Backbone.View.extend({
//
//    events: {
//	//'click .edit-crs' : 'edit',
//	'click .add-std' : 'showStudentForm',
//	'click .submit' :	'addStudent'
//    },
//
//    showStudentForm: function(e) {
//		console.log("clicked on show student form");
//		jQuery(".add-std").hide();
//		jQuery(".add-std-frm-title").show();
//		jQuery(".add-std-frm").show();
//    },
//
//    addStudent: function(course) {
//    	
//    	user_course_collection_view.user_course_collection.create(
//    	{
//    				name : jQuery(".crs-name").val()
//    	});
//
//	    jQuery(".add-std-frm-title").hide();
//	    jQuery(".add-std-frm").hide()
//    }
//});// End UserControlView  
//
//var student_control_view = new StudentControlView({el : jQuery('.team_controls')});

