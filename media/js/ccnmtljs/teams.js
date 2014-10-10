//creating team model
// for adding teams to course
var Team= Backbone.Model.extend({
    
    defaults: function() {
        return {
            team_name: "Team Name",
            password1: "password1",
            password2: "password2"
        }
    },

    initialize: function(attributes) 
	{   
    	team_name = attributes.team_name || '<EMPTY>';
	}
	    
});

var TeamCollection = Backbone.Collection.extend({
	 model: Team,
	 url: function() {
		    return '/team/' + crs_id;
	  }
});
//End of Modes/Collections


// Team View is to hold individual li elements in the course team list 
var TeamView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Team Name <%= team_name %>" +
   			             "<button class='btn btn-xs rm-team'>" +
			             "Remove Team From Course" +
			             "</button>"),

   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	events: {
   		'click .rm-team' : 'removeTeam'
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

   	removeTeam: function()
   	{
   		console.log("Removing team from course.");
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
    	console.log(this.course_teams);
    	this.course_teams.on('reset', this.initialRender);
	},

    render: function() {
    },

    initialRender: function() {
        console.log("Team list view re-render");
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
	'click .add-team-btn' : 'showTeamForm',
	'click .team_submit' :	'addTeam'
    },

    showTeamForm: function() {
		//console.log("clicked on show team form");
		jQuery(".add-team-btn").hide();
		jQuery(".add-team-frm-title").show();
		jQuery(".add-team-frm").show();
    },

    addTeam: function(team) {
    	
    	team_collection_view.course_teams.create(
    	{
    		team_name : jQuery(".team-name").val(),
    		password1 : jQuery(".team-pswd-1").val(),
    		password2 : jQuery(".team-pswd-2").val(),
    	});

	    jQuery(".add-team-frm-title").hide();
	    jQuery(".add-team-frm").hide();
	    jQuery(".add-team-btn").show();
    }
    
});// End TeamControlView  

var team_control_view = new TeamControlView({el : jQuery('.team_controls')});