App.Models.Team = Backbone.Model.extend({
	
	defaults: {
		teamName: 'Team Name',
		course: 'Course Name',
		signed_contract: false,
	  },

	  validate: function(attrs, options) {
	    if (!attrs.teamName) {
	      return "A valid team name must be provided.";
	    }
	  },

    initialize: function(attributes) {
	    var teamName = attributes.teamName || '<EMPTY>';
	    var course = attributes.course || '<EMPTY>';
	    var signed_contract = attributes.signed_contract || '<EMPTY>';
	    console.log("Initializing a new team model for '" + nameCourse + "'." );
	  }
	});
