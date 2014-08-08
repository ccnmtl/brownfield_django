App.Models.Course = Backbone.Model.extend({
	
	defaults: {
	    nameCourse: 'Course Name',
	    startingBudget: '60000',
	    enableNarrative: true,
	    message: '<p></p>',
	    active: true,
	  },

	  validate: function(attrs, options) {
	    if (!attrs.message) {
	      return "A valid message must be provided.";
	    }
	  },

    initialize: function(attributes) {
	    var nameCourse = attributes.nameCourse || '<EMPTY>';
	    var startingBudget = attributes.startingBudget || '<EMPTY>';
	    var enableNarrative = attributes.enableNarrative || '<EMPTY>';
	    var message = attributes.message || '<EMPTY>';
	    var active = attributes.active || '<EMPTY>';
	    console.log("Initializing a new course model for '" + nameCourse + "'." );
	  }
	});