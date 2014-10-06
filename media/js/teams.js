//creating team model
var Team= Backbone.Model.extend({
    
    defaults: function() {
        return {
            first_name: "First Name Team",
            last_name: "Last Name Team",
            email: "email@email.com",
        }
    },

    initialize: function(attributes) 
	{   
	    first_name = attributes.first_name || '<EMPTY>';
	    last_name = attributes.last_name || '<EMPTY>';
	    console.log("Initializing a new team model for '" +
	    		first_name + " " +  last_name + "'.");
	}
	    
});


var TeamCollection = Backbone.Collection.extend({
	 model: Team,
	 url: function() {
		    return '/team/' + crs_id;
	  }
});
//End of Modes/Collections


//Views 
var TeamView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Team Template Name <%= first_name %>" +
   			             "<%= last_name %> " +
   			             "Email: " +
   			             "<%= email %> " +
   			             "<button class='btn btn-xs rm-st'>" +
			             "Remove Team From Course" +
			             "</button>"),

   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	// Can probably combine into one function on change
   	events: {
   		'click .rm-st' : 'removeTeam'
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
   	removeTeam: function()
   	{
   		console.log("Removing team from course.");//console.log("Revoking Document");
//        this.model.save({
//           	headers : { 'id' : this.model.id }//{ 'method_called' : 'revoke'}//, 'document' : this.model.id }
//        });
    }

});// End Team View



/* Container to hold rows of teams */
var TeamListView = Backbone.View.extend({

    tagName : 'ul',

    initialize: function (options)
    {
    	_.bindAll(this,
    			 'render',
    			 'initialRender');
    	this.course_teams = new TeamCollection();
    	this.course_teams.fetch({processData: true, reset: true});
    	this.course_teams.on('reset', this.initialRender);
	},

    render: function() {
    },

    initialRender: function() {

        this.$el.empty();

        this.course_teams.each(function(model) {
        this.$el.append(new TeamView({
               model: model
        }).render().el);
        }, this);

        return this;
    }
    
});// End TeamListView    



var team_collection_view = new TeamListView({el : jQuery('.team-list')});


var TeamControlView = Backbone.View.extend({

    events: {
	//'click .edit-crs' : 'edit',
	'click .add-std-btn' : 'showTeamForm',
	'click .team_submit' :	'addTeam'
    },

    showTeamForm: function() {
		//console.log("clicked on show team form");
		jQuery(".add-std-btn").hide();
		jQuery(".add-std-frm-title").show();
		jQuery(".add-std-frm").show();
    },

    addTeam: function(course) {
    	
    	team_collection_view.course_teams.create(
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

var team_control_view = new TeamControlView({el : jQuery('.team_controls')});


//var team_collection_view = new TeamListView({el : jQuery('#course-teams')});
//
//
//var TeamControlView = Backbone.View.extend({
//
//    events: {
//	//'click .edit-crs' : 'edit',
//	'click .add-std' : 'showTeamForm',
//	'click .submit' :	'addTeam'
//    },
//
//    showTeamForm: function(e) {
//		console.log("clicked on show team form");
//		jQuery(".add-std").hide();
//		jQuery(".add-std-frm-title").show();
//		jQuery(".add-std-frm").show();
//    },
//
//    addTeam: function(course) {
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
//var team_control_view = new TeamControlView({el : jQuery('.team_controls')});