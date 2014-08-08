App.Models.Document = Backbone.Model.extend({
	
	defaults: {
		documentName: 'Course Name',
	    course: 'Course Name',
	    link: 'somelink',
	  },

	  validate: function(attrs, options) {
	    if (!attrs.documentNam) {
	      return "A valid document name must be provided.";
	    }
	  },

    initialize: function(attributes) {
	    var documentName = attributes.nameCourse || '<EMPTY>';
	    var course = attributes.course || '<EMPTY>';
	    var link = attributes.link || '<EMPTY>';
	    console.log("Initializing a new document model for '" + documentName + "'." );
	  }
	});
