// creating separate course model for updates
var UpdateCourse = Backbone.Model.extend({

    url: '/update_course/' + crs_id,
    
    defaults: function() {
        return {
            name: "Default name",
            //password: "password",
            startingBudget: "startingBudget",
            enableNarrative: "enableNarrative",
            message: "message",
            active: false,
            archive: false,
            professor: "Default professor"
        };
    },
       
	initialize: function(attributes) 
	{
	    this.name = attributes.name || '<EMPTY>';
	}
	    
});

var UpdateCourseView = Backbone.View.extend({

   	tagName : 'upt-crs-frm',
    	
   	initialize: function () {
    	_.bindAll(this,
   			 'render'
   		);
   	//create new model to hold course attributes
   	this.update_course = new UpdateCourse({id: crs_id});
   	console.log(this.update_course);
   	this.update_course.fetch({processData: true, reset: true});
   	this.update_course.on('reset', this.render);
   	//    this.listenTo(this.model, 'change', this.render);
   	},
    	
   	events: {
   		'click .submit-edit' : 'sendEdit',
   	},
    	
    render: function () {
    	this.update_course.fetch({processData: true, reset: true});
        jQuery('#id_name').val(this.update_course.name);
        jQuery('#id_startingBudget').val(this.update_course.startingBudget);
        jQuery('#id_enableNarrative').val(this.update_course.enableNarrative);
        jQuery('#id_message').val(this.update_course.message);
        jQuery('#id_active').val(this.update_course.active);
        jQuery('#id_archive').val(this.update_course.archive);
        jQuery('#id_professor').val(this.update_course.professor);
     },
    	
    sendEdit: function() {
        this.model.destroy();
    }

});// End UpdateCourseView

var update_course = new UpdateCourseView();
