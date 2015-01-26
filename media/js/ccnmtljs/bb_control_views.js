var BaseManagementView = Backbone.View.extend({

    showAddItemForm: function(e)
    {
        e.preventDefault();
        this.add_form.show();
        this.add_btn.hide();
    },
    
    hideAddItemForm: function(e)
    {
        //assume its probably good practice to remove form errors here while were at it
        this.add_form.find('.error-msg').remove();
        this.add_form.hide();
        this.add_btn.show();
    },
    
    showFormError: function(form_selector)
    {
    	if((jQuery(form_selector).has('.form_error').length) === 0)
		{
        	this.add_form.append("<p class='.form-error'><b>Something went wrong, please try again.</b></p>");
		}
    },
    
    removeFormError: function(form_selector)
    {
    	/* upon successful submission we want to remove any form errors if there are any */
        if((jQuery(form_selector).has('.form_error').length) > 0)
        {
            this.add_form.remove("<p class='.form-error'><b>Something went wrong, please try again.</b></p>");
        }
    },

    onlyLetters: function (selector_string, error_element)
    {
        var check = jQuery(selector_string).val();
        
        if( /[^a-zA-Z]/.test(check))
        {
           if((jQuery(error_element).has('.chars-only').length) === 0)
           {
                jQuery(error_element).append("<b class='error-msg chars-only' style='color:red'> Please only use letters of the alphabet</b>");
           }
           return false;
        }
        return true;     
     },

    is_empty: function (selector_string, error_element, error_msg){
        var check = jQuery(selector_string).val();
        if(check === null || check === "") 
        {
            if((jQuery(error_element).has('.is-empty').length) === 0)
            {
                jQuery(error_element).append("<b class='error-msg is-empty' style='color:red'>" + String(error_msg) + "</b>");
            }
           return true;
        }
        return false;     
     },

    clear_form_errors: function (selector_string){
        
        jQuery(selector_string + ' .error-msg').remove();
  
    }
    
});

var ManageCoursesView = Backbone.View.extend({
    events: {
    	'click .add-crs': 'showCourseForm',
    	'click .cncl-add-crs' : 'hideAddForm',
    	'click .submit': 'addCourse'
    },
    
    initialize: function (options) {
        _.bindAll(this,
                  'addCourse',
                  'showCourseForm',
                  'hideAddForm',
                  'validateForm');
        this.options = options;
        this.current_user = new User({id: options.user_id});
        this.current_user.fetch();
        this.course_list_view = new CourseListView({el: this.options.listEl});
        this.course_list_view.collection.fetch({wait: true});
        this.user_list = new InstructorCollection();
        this.user_list.fetch({wait: true});
    },

    showCourseForm: function(e) {
		jQuery(".add-crs").hide();
		//how to bind this/make it wait for results from server
		this.user_list.fetch({wait: true});
		this.user_list.each(function(model) {
	        jQuery('#id_professor').append("<option value='" + String(model.attributes.url) + "'>" + 
	                String(model.attributes.first_name) + 
	                " " + String(model.attributes.last_name)  + 
	                "</option>");
	    });
		jQuery("#create-course-form").show();
    },
    
    hideAddForm: function()
    {   
        if(jQuery("#create-course-form").has('.error-msg').length !==0 )
        {
            jQuery('#create-course-form .error-msg').remove();
        }
        if(jQuery("#create-course-form").has('.form-error').length !==0 )
        {
            jQuery('#create-course-form .form-error').remove();
        }
    	this.$('#create-course-form').css('display', 'none');
    	jQuery(".add-crs").show();
    },
    
    validateForm: function()
    {
        var is_valid = true;
        
        var course_name = jQuery('#id_course_name').val();
        var startingBudget = jQuery('#id_course_startingBudget').val();
        var course_message = jQuery('#id_course_message').val();
        
        
        if(course_name === null || course_name === "")
        {   
            is_valid = false;
            if((jQuery('.course-name-block').has('.error-msg').length) === 0)
            {
                jQuery('.course-name-block').append("<p class='error-msg' style='color:#ff0000'>Please enter a valid course name.</p>");
            }
            
        }
        if(startingBudget === null || startingBudget === "")
        {   
            is_valid = false;

            if((jQuery('.course-budget-block').has('.error-msg').length) === 0)
            {
                jQuery('.course-budget-block').append("<p class='error-msg' style='color:#ff0000'>Please enter a valid starting budget for your course.</p>");
            }
        }
        if(course_message === null || course_message === "")
        {   
            is_valid = false;

            if((jQuery('.course-message-block').has('.error-msg').length) === 0)
            {
                jQuery('.course-message-block').append("<p class='error-msg' style='color:#ff0000'>Please enter a valid course message.</p>");
            }
        }
        return is_valid;
    },

    addCourse: function(evt) {
        evt.preventDefault();
        var professor = jQuery('#id_professor').find("option:selected").val();

        if(professor === null || professor === undefined)
        {   
        	/* Seems this needs to be user url - maybe if
        	 * I changed to model instead of hyperlink
        	 * serializer ID will be acceptable? */
            professor = this.current_user.get('url');
        }

        if (this.validateForm())
        {
    	    this.course_list_view.collection.create(
            {
    	        name: jQuery("#id_course_name").val(),
    	    	startingBudget: jQuery("#id_course_startingBudget").val(),
    	    	message: jQuery("#id_course_message").val(),
    		    professor: professor
    	    },
            {
                success: function(model, response) 
                {

                    jQuery('#id_course_name').val("");
                    jQuery('#id_course_startingBudget').val("");
                    jQuery('#id_course_message').val("");
                    jQuery("#create-course-form").hide();
                    jQuery(".add-crs").show();
                    if(jQuery("#create-course-form").has('.error-msg').length !==0 )
                    {
                        jQuery('#create-course-form .error-msg').remove();
                    }
                    if(jQuery("#create-course-form").has('.form-error').length !==0 )
                    {
                        jQuery('#create-course-form .form-error').remove();
                    }

                },
                error: function(model, response)
                {
                    if((jQuery("#create-course-form").has('.form-error').length) === 0)
                    {
                        jQuery("#create-course-form").append("<p class='error-msg form-error'>Something went wrong, please try again.</p>");
                    }
                },
            wait: true
        });

        }
	    return false;
    }
});// End UserControlView  


var ManageInstructorsView = BaseManagementView.extend({
    events: {
    	'click .add-instructor-btn': 'showAddItemForm',
    	'click .cncl-add-inst' : 'hideAddItemForm',
    	'click .save-instructor': 'addInstructor'
    },
    
    initialize: function (options) {
        _.bindAll(this,
                  'addInstructor',
                  'showAddItemForm',
                  'hideAddItemForm',
                  'is_empty');
        this.instructor_collection_view = new InstructorListView({
            el: jQuery('.instructor-list'),
        });
        this.add_form = jQuery(".add-instructor-frm");
   	    this.add_btn = jQuery(".add-instructor-btn");
    },
    
    validAddForm: function() {
    	var is_valid = true;
    	
    	if(this.is_empty(".add-instructor-frm input.instructor-frst-name", ".inst-first-name", "Please enter a first name."))
    	{
    		is_valid = false;
    	}
        if(this.is_empty(".add-instructor-frm input.instructor-last-name", ".inst-last-name", "Please enter a last name."))
        {
            is_valid = false;
        }
        if(this.is_empty(".add-instructor-frm input.instructor-email", ".inst-email", "Please enter a email address."))
        {
            is_valid = false;
        }
    	//check whatever they put for email looks something like an actual address
    	else if((jQuery(".add-instructor-frm input.instructor-email").val().length) !== 0)
    	{
    	    if((jQuery(".add-instructor-frm input.instructor-email").val().indexOf("@")  === -1) && 
    	       (jQuery(".add-instructor-frm input.instructor-email").val().indexOf(".") === -1))
    	    {
                is_valid = false;
    		    if((jQuery(".inst-email").has('b').length) === 0)
    		    {
    			    jQuery(".inst-email").append("<b class='error-msg' style='color:red'>Please enter a valid email.</b>");
    		    }
    	    }
    	}
    	
    	return is_valid;
    },
        addInstructor: function(e) {
        e.stopPropagation();
         
        if(this.validAddForm())
        {
            this.instructor_collection_view.collection.create(
            {
                first_name : jQuery(".instructor-frst-name").val(),
                last_name : jQuery(".instructor-last-name").val(),
                email : jQuery(".instructor-email").val()
            },
            {
                success: function(model, response) 
                {
                    jQuery(".add-instructor-frm").hide();
                    jQuery(".add-instructor-btn").show();
                    jQuery(".instructor-frst-name").val("");
                    jQuery(".instructor-last-name").val("");
                    jQuery(".instructor-email").val("");
                    if(jQuery(".add-instructor-frm").has('.error-msg').length !==0 )
                    {
                        jQuery('.add-instructor-frm .error-msg').remove();
                    }
                    if(jQuery(".add-instructor-frm").has('.form-error').length !==0 )
                    {
                        jQuery('.add-instructor-frm .form-error').remove();
                    }

                },
                error: function(model, response)
                {
                    if((jQuery(".add-instructor-frm").has('.form-error').length) === 0)
                    {
                        jQuery(".add-instructor-frm").append("<p class='error-msg form-error'>Something went wrong, please try again.</p>");
                    }
                },
                wait: true
            }); //end create
        }       
        return false;
    }
    
});  


var StudentControlView = BaseManagementView.extend({

    events: {
        'click .add-std-btn' : 'showAddItemForm',
        'click .cncl-add-std' : 'hideAddItemForm',
        'click .student_submit' : 'addStudent'
    },
    
    initialize: function (options)
    {
    	_.bindAll(this, 'addStudent', 'hideAddItemForm', 'showAddItemForm');

        this.student_collection_view = new StudentListView({
            el: jQuery('.student-list'),
            course: options.course
        });
        this.add_form = jQuery(".add-std-frm");
   	    this.add_btn = jQuery(".add-std-btn");
    },
    
    addStudent: function(e) {
    	e.preventDefault();

        if(this.validAddForm())
        {
    	    this.student_collection_view.collection.create(
    	    {   
    	        	first_name : jQuery(".frst-name").val(),
    	            last_name : jQuery(".last-name").val(),
    	            email : jQuery(".email").val()
    	    },
    	    {
    	    	success: function(model, response){
                    /* seems you cannot access outer function from here... */
    	    		jQuery(".add-std-frm").hide();
                    jQuery(".add-std-btn").show();
                    jQuery(".frst-name").val("");
                    jQuery(".last-name").val("");
                    jQuery(".email").val("");
                    if(jQuery(".add-std-frm").has('.error-msg').length !==0 )
                    {
                        jQuery('.add-std-frm .error-msg').remove();
                    }
                    if(jQuery(".add-std-frm").has('.form-error').length !==0 )
                    {
                        jQuery('.add-std-frm .form-error').remove();
                    }
    	    	},
                error: function(model, response)
                {
                    if((jQuery(".add-std-frm").has('.form-error').length) === 0)
                    {
                	    jQuery(".add-std-frm").append("<p class='error-msg form-error'>Something went wrong, please try again.</p>");
                    }
                },
    	        wait: true,
    	    	url: this.student_collection_view.collection.url()
    	    });
        }
	    return false;
    },
    
    
    validAddForm: function() {
        var is_valid = true;

        if(this.is_empty(".add-std-frm input.frst-name", ".first-name-box", "Please enter a first name."))
    	{
            is_valid = false;
    	}
        if(this.is_empty(".add-std-frm input.last-name", ".last-name-box", "Please enter a last name."))
    	{
            is_valid = false;
    	}
        if(this.is_empty(".add-std-frm input.email", ".email-box", "Please enter a email."))
    	{
            is_valid = false;
    	}
    	//check whatever they put for email looks something like an actual address
    	else if((jQuery(".add-std-frm input.email").val().length) !== 0)
    	{
    	    if((jQuery(".add-std-frm input.email").val().indexOf("@")  === -1) && 
    	       (jQuery(".add-std-frm input.email").val().indexOf(".") === -1))
    	    {
                is_valid = false;
    		    if((jQuery(".email-box").has('b').length) === 0)
    		    {
    			    jQuery(".email-box").append("<b class='error-msg' style='color:red'>Please enter a valid email.</b>");
    		    }
    	    }
    	}
    	
        return is_valid;
    }
    
});


var TeamControlView = BaseManagementView.extend({

    events: {
        'click .add-team-btn' : 'showAddItemForm',
        'click .cncl-add-team' : 'hideAddItemForm',
	    'click .team_submit' : 'addTeam'
    },
    
    initialize: function (options) {
        this.team_collection_view = new TeamListView({
            el: jQuery('.team-list'),
            course: options.course
        });
        this.add_form = jQuery(".add-team-frm");
   	    this.add_btn = jQuery(".add-team-btn");
    },

    validAddForm: function() {
        var is_valid = true;

        if((jQuery(".add-team-frm input.team-name").val().length) === 0)
        {
            is_valid = false;
            if((jQuery(".add-team-frm .team-name-box").has('b').length) === 0)
            {
                jQuery(".team-name-box").append("<b class='error-msg' style='color:red'>Please enter a team name.</b>");
            }
        }
        return is_valid;
    },

    addTeam: function(evt) {
    	evt.preventDefault();

        if(this.validAddForm())
        {

        	this.team_collection_view.collection.create(
    	    {
        		team_name : jQuery(".team-name").val()
        	},
	        {
    	        success: function(model, response) 
        	    {
                    if(jQuery(".add-team-frm").has('.error-msg').length !==0 )
                {
                    jQuery('.add-team-frm .error-msg').remove();
                }
                    if(jQuery(".add-team-frm").has('.form-error').length !==0 )
                {
                    jQuery('.add-team-frm .form-error').remove();
                }
                    jQuery(".team-name").val("");
                    jQuery(".add-team-frm").hide();
                    jQuery(".add-team-btn").show();
                },
                error: function(model, response) {
                	if((jQuery(".add-team-frm").has('.form-error').length) === 0)
                    {
                        jQuery(".add-team-frm").append("<p class='error-msg form-error'>Something went wrong, please try again.</p>");
                    }
                },
	            wait: true,
	    	    url: this.team_collection_view.collection.url()
	        });
        }
    	
	    return false;
    }
    
});// End TeamControlView  





