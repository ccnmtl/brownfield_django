App.Models.Student = Backbone.Model.extend({
	
	defaults: {
	    firstName: 'First Name',
	    lastName: 'Last Name',
	    email: 'email@email.com',
	    username: 'username',
	  },

	  validate: function(attrs, options) {
	    if (!attrs.username) {
	      return "A valid username must be provided.";
	    }
	  },

    initialize: function(attributes) {
	    var firstName = attributes.firstName || '<EMPTY>';
	    var lastName = attributes.lastName || '<EMPTY>';
	    var enableNarrative = attributes.enableNarrative || '<EMPTY>';
	    var email = attributes.email || '<EMPTY>';
	    var username = attributes.username || '<EMPTY>';
	    console.log("Initializing a new course model for '" + username + "'." );
	  }
	});
