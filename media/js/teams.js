//creating team model
// for adding teams to course
var Team= Backbone.Model.extend({
    
    defaults: function() {
        return {
            username: "Team Name",
            password1: "password1",
            password2: "password2"
        }
    },

    initialize: function(attributes) 
	{   
	    name = attributes.name || '<EMPTY>';
	    password1 = attributes.password1 || '<EMPTY>';
	    password2 = attributes.password2 || '<EMPTY>';
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
   	template: _.template("Team Name <%= username %>" +
   			             "<button class='btn btn-xs rm-team'>" +
			             "Remove Team From Course" +
			             "</button>"),

   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	// Can probably combine into one function on change
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

   	//will need to do save which will automatically call sync
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

    addTeam: function(course) {
    	
    	team_collection_view.course_teams.create(
    	{
    		name : jQuery(".team-name").val(),
    		password1 : jQuery(".team-pswd-1").val(),
    		password2 : jQuery(".team-pswd-2").val()
    	});

	    jQuery(".add-team-frm-title").hide();
	    jQuery(".add-team-frm").hide();
	    jQuery(".add-team-btn").show();
    }
    
});// End TeamControlView  

var team_control_view = new TeamControlView({el : jQuery('.team_controls')});


var TeamButtonView = Backbone.View.extend({
	template: _.template('<button type="button" class="btn btn-success">Team Name <%= username %></button>'),

    render: function ()
    {
        if (!this.model) 
        {
            throw "Model is not set for this view";
        }
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    }
});// End TeamButtonView

var TeamFromView = Backbone.View.extend({
	//template: _.template('<div class="btn-group-vertical btn-group-sm btn-group-justified"></div>');

	className: "btn-group-vertical btn-group-sm btn-group-justified",
	
    initialize: function (options)
    {
    	_.bindAll(this,
    			 'render');
	},
	
    render: function()
    {
        this.$el.empty();
        team_collection_view.course_teams.each(
        	function(model)
        	{
        		this.$el.append(new TeamButtonView(
        		{
           			model: model
        		}).render().el);
        	}, this);

        return this;
    }
});// End TeamFormView

var TeamMemberContainerView = Backbone.View.extend({
	
    initialize: function (options)
    {
    	_.bindAll(this,
    			 'render');
    	this.team_member_list = new TeamCollection();
    	this.team_member_list.fetch({processData: true, reset: true});
    	this.team_member_list.on('reset', this.render);
	},
	
    render: function()
    {
        this.$el.empty();
        team_collection_view.course_teams.each(
        	function(model)
        	{
        		this.$el.append(new TeamButtonView(
        		{
           			model: model
        		}).render().el);
        	}, this);

        return this;
    }
});// End TeamFormView

var team_collection_view = new TeamListView({el : jQuery('.team-member-list')});

