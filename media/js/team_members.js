var student_collection = new StudentCollection([
                                                {
                                            		id: 1,
                                        			first_name: 'Student 1',
                                        			last_name: 'Student 1',
                                        			email: "student@somewhere.com",
                                                    team : ""
                                        		},
                                        		{
                                        			id: 2,
                                        			first_name: 'Student 2',
                                        			last_name: 'Student 2',
                                        			email: "student@somewhere.com",
                                                    team : ""
                                        		},
                                        		{
                                        			id: 3,
                                        			first_name: 'Student 3',
                                        			last_name: 'Student 3',
                                        			email: "student@somewhere.com",
                                                    team : ""
                                        		},
                                        		{
                                        			id: 4,
                                        			first_name: 'Student 4',
                                        			last_name: 'Student 4',
                                        			email: "student@somewhere.com",
                                                    team : ""
                                        		},
                                        		{
                                        			id: 5,
                                        			first_name: 'Student 5',
                                        			last_name: 'Student 5',
                                        			email: "student@somewhere.com",
                                                    team : ""
                                        		},
                                        		{
                                        			id: 6,
                                        			first_name: 'Student 6',
                                        			last_name: 'Student 6',
                                        			email: "student@somewhere.com",
                                                    team : ""
                                        		},
                                        		{
                                        			id: 7,
                                        			first_name: 'Student 7',
                                        			last_name: 'Student 7',
                                        			email: "student@somewhere.com",
                                                    team : ""
                                        		}
                                        ]);


// Team student member container model

var TeamCollection = Backbone.Collection.extend({
	 model: Team,
	 url: function() {
		    return '/team/' + crs_id;
	  }
});

// team model
var Team= Backbone.Model.extend({
    
    defaults: function() {
        return {
            name: "Team Name",
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


//Views 
var TeamView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Team Template Name <%= name %>" +
   			             "<button class='btn btn-xs rm-team'>" +
			             "Remove Team From Course" +
			             "</button>"),

   	initialize: function () {

   	    initialize: function (options)
   	    {
   	    	_.bindAll(this,
   	    			 'render',
   	    			 'initialRender');
   	    	this.course_teams = new TeamCollection();
   	    	this.course_teams.fetch({processData: true, reset: true});
   	    	this.course_teams.on('reset', this.initialRender);
   		},
   		
   		this.team_members = new TeamMemberView();
   		this.team_members.fetch({processData: true, reset: true});
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	// Can probably combine into one function on change
   	events: {
   		'click .rm-team' : 'removeTeam',
   		'click .add-team-member' : 'addTeamMember'
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
    },
    
    addTeamMember: function()
   	{
   		console.log("Adding Team Member.");
    },

    addTeamMember: function()
   	{
   		console.log("Adding Team Member.");
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