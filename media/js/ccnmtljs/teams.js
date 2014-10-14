//creating team model
// for adding teams to course
var Team = Backbone.Model.extend({
});

var TeamCollection = Backbone.Collection.extend({
    model: Team,
	headers: {"content-type": "application/json"},
	urlRoot: '/team/',
	url: function() {
	    return this.urlRoot + this.course_id;
	}
});
//End of Modes/Collections


// Team View is to hold individual li elements in the course team list 
var TeamView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Team Name <%= username %>" +
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
    			 'initialRender');
    	this.course_teams = new TeamCollection();
    	this.course_teams.course_id = options.course_id;
    	
    	this.course_teams.fetch({processData: true, reset: true});
    	this.course_teams.on('reset', this.initialRender);
	},

	initialRender: function() {
        this.course_teams.each(function(model) {
        this.$el.append(new TeamView({
               model: model
        }).render().el);
        }, this);

        return this;
    }
    
});// End TeamListView    



var TeamControlView = Backbone.View.extend({

    events: {
	//'click .edit-crs' : 'edit',
	'click .add-team-btn' : 'showTeamForm',
	'click .team_submit' :	'addTeam'
    },
    
    initialize: function (options) {
        this.team_collection_view = new TeamListView({
            el: jQuery('.team-list'),
            course_id: options.course_id});
    },

    showTeamForm: function() {
		//console.log("clicked on show team form");
		jQuery(".add-team-btn").hide();
		jQuery(".add-team-frm-title").show();
		jQuery(".add-team-frm").show();
    },

    addTeam: function(team) {
    	
    	this.team_collection_view.course_teams.create(
    	{
    		username : jQuery(".team-name").val(),
    		password1 : jQuery(".team-pswd-1").val(),
    		password2 : jQuery(".team-pswd-2").val(),
    	});

	    jQuery(".add-team-frm-title").hide();
	    jQuery(".add-team-frm").hide();
	    jQuery(".add-team-btn").show();
    }
    
});// End TeamControlView  

jQuery(document).ready(function () {
    var crs_id = jQuery("input[name='crs-id']").val();
    var team_control_view = new TeamControlView({
        el: jQuery('.team_controls'),
        course_id: crs_id
    });
});