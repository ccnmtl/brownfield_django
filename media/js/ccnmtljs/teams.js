var Team = Backbone.Model.extend({
	
	   urlRoot: '/admin_team/',
	   url: function() {
	       var url = this.urlRoot;
	       if (this.get('id') !== undefined) {
	           url += this.get('id') + '/';
	       }
	       return url;
	   }
	
});

var TeamCollection = Backbone.Collection.extend({
	
	 model: Team,
	 urlRoot: '/admin_team/',
	 headers: {"content-type": "application/json"},
	 url: function() {
	     var url = this.urlRoot;
	     if (this.course) {
	         url += this.course + '/';
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
   		this.model.destroy();
    }

});// End Team View


/* Container to hold rows of teams */
var TeamListView = Backbone.View.extend({

    tagName : 'ul',

    initialize: function (options)
    {
    	_.bindAll(this, 'initialRender', 'addTeam');
    	this.course_teams = new TeamCollection(options);
    	this.course_teams.fetch({processData: true, reset: true});
    	this.course_teams.on('reset', this.initialRender);
    	this.course_teams.on('add', this.addTeam);
	},

	initialRender: function() {
        this.course_teams.each(function(model) {
        this.$el.append(new TeamView({
               model: model
        }).render().el);
        }, this);

        return this;
    },

    addTeam: function(model, collection, options) {
        this.$el.append(new TeamView({
            model: model
        }).render().el);
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
            course: options.course
        });
    },

    showTeamForm: function() {
		//console.log("clicked on show team form");
		jQuery(".add-team-btn").hide();
		jQuery(".add-team-frm-title").show();
		jQuery(".add-team-frm").show();
    },

    addTeam: function(team) {
    	team.preventDefault();
    	this.team_collection_view.course_teams.create(
    	{
    		username : jQuery(".team-name").val(),
    		password1 : jQuery(".team-pswd-1").val(),
    		password2 : jQuery(".team-pswd-2").val(),
    	},
	    {
	        wait: true,
	    	url: this.team_collection_view.course_teams.url()
	    }
    	);

	    jQuery(".add-team-frm-title").hide();
	    jQuery(".add-team-frm").hide();
	    jQuery(".add-team-btn").show();
	    return false;
    }
    
});// End TeamControlView  

jQuery(document).ready(function () {
    var course = jQuery("input[name='crs-id']").val();
    var team_control_view = new TeamControlView({
        el: jQuery('.team_controls'),
        course: course
    });
});
