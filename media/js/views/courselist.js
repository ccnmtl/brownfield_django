App.Views.CourseList = Backbone.View.extend({
	
	events: {
	    'click .controls .add': 'addForm',
	    'submit .controls form': 'addSubmit'
	  },

    initialize: function() {
        _.bindAll(this, 'render', 'addForm', 'addSubmit');
    },

    render: function() {
    	
        var $container = this.$('.listing').empty();

        App.Courses.each(function(course) {
            new App.Views.Course({
            model: course,
            $container: $container
        }).render();
    });

        return this;
    },
    
    addForm: function() {
    	
	    this.$('.controls form').show()
	    .find('input.nameCourse').focus();
	},
	
	addSubmit: function(event) {
	    event.preventDefault();
	    
		var $form = this.$('.controls form');

		var newCourse = new App.Models.Course({
			nameCourse: $('input.nameCourse', $form).val(),
			startingBudget: $('input.startingBudget', $form).val(),
			enableNarrative: $('input.enableNarrative', $form).val(),
			message: $('input.message', $form).val()
		});

		if (newCourse.isValid()) {
		    App.Course.add(newCourse);
		    $form.hide();
		    $('input[type=text]', $form).val('').blur();
		}
		else {
		      alert(newCourse.validationError);
		}
	}

});
