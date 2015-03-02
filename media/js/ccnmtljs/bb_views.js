/* Experimenting with suggestions from Backbone best practices for reducing duplicate code */

/* Might be good to pull out show edit form and remove */

/* All List Element Views have the same render function - creating base class with the render method. */
var BaseItemView = Backbone.View.extend({

    tagName : 'li',

	render: function () 
    {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },
    
    hideEditForm: function(e)
    {   
        e.preventDefault();
        this.render();
    },
    
    showEditForm: function(e)
    {
        var edit_form =  this.edit_form(this.model.toJSON());
        this.$el.html(edit_form);
    },

    is_empty: function (selector_string, error_element, error_msg)
    {
        var check = jQuery(this.el).find(selector_string).val();
        if(check === null || check === "") 
        {
            if((jQuery(error_element).has('.is-empty').length) === 0)
            {
                jQuery(error_element).append("<b class='error-msg is-empty' style='color:red'>" + String(error_msg) + "</b>");
            }
           return true;
        }
        return false;     
    }

});


var DeletableItemView = BaseItemView.extend({

    removeItem: function ()
    {   
        this.model.destroy();
    },
    
    confirmDeletion: function ()
    {
        if(jQuery(this.el).find('.confirm-del'))
        {
        	jQuery(this.el).find('.confirm-del').show();
        	jQuery(this.el).find('.confirm-del').css('display', 'inline');
        	jQuery(this.el).find('.confirm-del').css('color', 'red');
        	jQuery(this.el).find('.confirm-del').css('font-weight', 'bold');
        	jQuery(this.el).find('.reg-btn').hide();
        }
    },
    
    cancelDeletion: function (evt)
    {
    	jQuery(this.el).find('.reg-btn').show();
    	jQuery(this.el).find('.confirm-del').hide();
    }

});

/* Start with Single Element Views */


var DocumentView = BaseItemView.extend({

   	initialize: function(options) {
   	    _.bindAll(this, 'changeDocument', 'viewDocument');
   	    this.listenTo(this.model, 'change', this.render);
        this.template = _.template(jQuery("#document-list-template").html());
   	},

   	events: {
   		'click .chng-dct' : 'changeDocument',
   		'click .document-click' : 'viewDocument'
   	},
        
    changeDocument: function()
   	{
    	if(this.model.attributes.visible === true)
    	{
    		this.model.set('visible', false);
    		this.model.save({
                success: function(model, response) 
                {
                },
                error: function(model, response)
                {
                        alert("An error occured!");
                },
                wait: true
            });
    	}
    	else if (this.model.attributes.visible === false)
    	{
    		this.model.set('visible', true);
    		this.model.save({
    		        success: function(model, response) 
                    {},
                    error: function(model, response)
                    {
                            alert("An error occured!");
                    },
                    wait: true
                });
    	}
   	},
   	
   	viewDocument: function()
   	{
   		if(this.model.get('name') === "Link: Brownfield Action Reference Site")
   		{
   			document.location = "http://brownfieldref.ccnmtl.columbia.edu/";
   		}
   		else if((this.model.get('name') === "Video: Press Conference Proceedings in Moraine Township") || (this.model.get('name') === "Video: Esker County Community Television: O'Ryan's Express"))
   		{
   			window.open("../../media/" + this.model.get('link'));
   		}
   		else
		{
    		window.open("../../media/flash/" + this.model.get('link'));
		}
   	}

});


var CourseView = BaseItemView.extend({
    	
   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.template = _.template(jQuery("#course-list-template").html());
   	    this.edit_form = _.template(jQuery("#course-edit-template").html());
   	    /* As of now cannot think of solution for having the list
   	     * of professors available to the CourseView view and the main ControlView*/
   	},
    	
   	events: {
   	    'click .course_name' : 'courseDetails',
   	    'click .edit-crs' : 'showEditForm',
   	    'click .save-edit-course' : 'editCourse',
   	    'click .cncl-edit-crs' : 'hideEditForm',
   	    'click .conf-archive-course' : 'confirmArchival',
   	    'click .cancel-arch' : 'cancelArchive',
   	    'click .conf-arch' : 'clear'
   	},
    	
    render: function ()
    {
        if (this.model.get('archive') === true) {
            this.$el.remove();
        } else {
        	BaseItemView.prototype.render.apply(this, arguments);
        }
        return this;
    },
    
    clear: function() {
        this.model.set('archive', true);
        this.model.save();
    },

    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        if(this.is_empty("input#edit_course_name", ".course-name-block", "Please enter a valid course name."))
        {
            is_valid = false;
        }

        if(this.is_empty("input#edit_course_startingBudget", ".course-budget-block", "Please enter a valid starting budget for your course."))
        {
            is_valid = false;
        }
        if(this.is_empty("textarea#edit_course_message", ".course-message-block", "Please enter a valid course message."))
        {
            is_valid = false;
        }

        return is_valid;
    },
    
    editCourse: function(evt)
    {
        evt.preventDefault();
        
        if(this.validEditForm())
        {
            var name = jQuery(this.el).find("input#edit_course_name").val();
            var startingBudget = jQuery(this.el).find("input#edit_course_startingBudget").val();
            var message = jQuery(this.el).find("textarea#edit_course_message").val();

            this.model.set('name', name);
            this.model.set('startingBudget', startingBudget);
            this.model.set('message', message);
            this.model.save({
                success: function(model, response) 
                {},
                error: function(model, response)
                {
                        alert("An error occured!");
                },
                wait: true
            });//end save
        }//end if
    },// end editCourse
    
    confirmArchival: function (evt)
    {
    	jQuery('.conf-del').show();
    	jQuery('.conf-del').css('display', 'inline');
    	jQuery('.conf-del').css('color', 'red');
    	jQuery('.conf-del').css('font-weight', 'bold');
    	jQuery('.reg-btn').hide();
    },
    
    cancelArchive: function (evt)
    {
    	jQuery('.reg-btn').show();
    	jQuery('.conf-del').hide();
    	
    },
    
    courseDetails: function ()
    {
        window.location.href = '/course_details/' + this.model.get('id')  + '/';  
    }
});// End CourseView


var TeamView = DeletableItemView.extend({
	
   	initialize: function (options) {
   		this.template = _.template(jQuery("#team-list-template").html());
   		this.edit_form = _.template(jQuery("#team-edit-template").html());
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	events: {
   		'click .rm-team' : 'removeItem',
   		'click .edit-team' : 'showEditForm',
   		'click .save-edit-team' : 'editTeam',
   		'click .cncl-edit-team' : 'hideEditForm',
   		'click .hist-team' : 'teamHistory'
   	},
    
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        if(this.is_empty("input.edt-team-name", ".div-edt-team-name", "Please enter a team name."))
        {
            is_valid = false;
        }

        return is_valid;
    },

   	editTeam: function(e)
   	{
   		e.preventDefault();

      if(this.validEditForm())
      {
   		
   		    var first_name = jQuery(this.el).find("input.edt-team-name").val();
   		
  		    this.model.set('first_name', first_name);
   		        this.model.save({
	            success: function(model, response) 
	            {},
            error: function(model, response)
            {
            	alert("An error occured!");
            },
            wait: true
            });//end save
      }
    },
    
   	teamHistory: function()
   	{
   		window.open("../../team_csv/" + this.model.get('username') + '/');
   	}
});// End Team View


var StudentView = DeletableItemView.extend({

	initialize: function(options)
	{
		_.bindAll(this, 'editStudent', 'hideEditForm', 'showEditForm');
		this.template = _.template(jQuery("#student-list-template").html());
		this.edit_form = _.template(jQuery("#student-edit-template").html());
		this.listenTo(this.model, 'change', this.render);
		this.listenTo(this.model, 'destroy', this.remove);
	},

   	events: {
   		'click .ed-st' : 'showEditForm',
   		'click .save-edit-student' : 'editStudent',
   		'click .cncl-edit-std' : 'hideEditForm',
   		'click .rm-st' : 'removeItem'
   	},
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        if(this.is_empty("input.edt-frst-name", ".sedt-first-name", "Please enter a first name."))
        {
            is_valid = false;
        }

        if(this.is_empty("input.edt-last-name", ".sedt-last-name", "Please enter a last name."))
        {
            is_valid = false;
        }
        if(this.is_empty("input.edt-email", ".sedt-email", "Please enter a email address."))
        {
            is_valid = false;
        }

        return is_valid;
    },
   	editStudent: function(e)
   	{
   		e.preventDefault();

      if(this.validEditForm())
      {
          var std_fname = jQuery(this.el).find("input.edt-frst-name").val();
          var std_lname = jQuery(this.el).find("input.edt-last-name").val();
          var std_email = jQuery(this.el).find("input.edt-email").val();
          /* For some reason setting the attributes below only sets correctly if you edit
          * email, pulling the varibles here because here they are correct and then passing.
          * */
          this.model.set('first_name', std_fname);
          this.model.set('last_name', std_lname);
          this.model.set('email', std_email);
          this.model.save({
          success: function(model, response) 
          {},
          error: function(model, response)
          {
              alert("An error occured!");
          },
          wait: true
        });//end save
      }
    }

});


var InstructorView = DeletableItemView.extend({

	initialize: function(options)
	{
		_.bindAll(this, 'editInstructor');
		this.template = _.template(jQuery("#instructor-list-template").html());
		this.edit_form =  _.template(jQuery("#instructor-edit-template").html());
        // need to bind the edit form to the model - when change made to form change model
		this.listenTo(this.model, 'change', this.render);
		this.listenTo(this.model, 'destroy', this.remove);
	},

   	events: {
   		'click .ed-inst' : 'showEditForm',
   		'click .save-edit-instructor' : 'editInstructor',
   		'click .cncl-edit-inst' : 'hideEditForm',
   		'click .rm-inst' : 'removeItem',
   		'click .conf-del' : 'confirmDeletion',
   		'click .cancel-del' : 'cancelDeletion'
   	},
    

        	
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        if(this.is_empty("input.edt-frst-name", ".inst-edt-first-name", "Please enter a first name."))
        {
            is_valid = false;
        }
        if(this.is_empty("input.edt-last-name", ".inst-edt-last-name", "Please enter a last name."))
        {
            is_valid = false;
        }
        if(this.is_empty("input.edt-email", ".inst-edt-email", "Please enter a email address."))
        {
            is_valid = false;
        }

        return is_valid;
    },

   	editInstructor: function(e)
   	{
        e.preventDefault();

        if(this.validEditForm())
        {
            var inst_fname = jQuery(this.el).find("input.edt-frst-name").val();
            var inst_lname = jQuery(this.el).find("input.edt-last-name").val();
            var inst_email = jQuery(this.el).find("input.edt-email").val();
            /* For some reason setting the attributes below only sets correctly if you edit
            * email, pulling the varibles here because here they are correct and then passing.
            * */
            this.model.set('first_name', inst_fname);
            this.model.set('last_name', inst_lname);
            this.model.set('email', inst_email);
            this.model.save({
	        success: function(model, response) 
	        {},
            error: function(model, response)
            {
            	alert("An error occured!");
            },
            wait: true
          });//end save
      }
    }
    
});


/* Now the Collection Views */
var BaseListView = Backbone.View.extend({

    renderCollection: function() {
        this.collection.each(function(model)
        {
            this.$el.append(new this.item_view({
                model: model
            }).render().el);
        }, this);
        return this;
    },
    
    addItem: function(model, collection, options)
    {
        this.$el.append(new this.item_view({
            model: model
        }).render().el);
    }

});

var InstructorListView = BaseListView.extend({
    
    initialize: function (options)
    {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new InstructorCollection(options);
        this.collection.fetch({processData: true, reset: true});
        this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.item_view = InstructorView;
    }
});


var CourseListView = BaseListView.extend({
    
    initialize: function (options)
    {
    	_.bindAll(this, 'renderCollection', 'addItem');
    	this.collection = new CourseCollection(options);
    	this.collection.fetch({processData: true, reset: true});
    	this.collection.on('reset', this.renderCollection);
    	this.collection.on('add', this.addItem);
    	this.item_view = CourseView;
	}

});


var DocumentListView = BaseListView.extend({

    initialize: function (options)
    {
        _.bindAll(this, 'renderCollection');
  	
  	    this.collection = new DocumentCollection(options);
  	    this.collection.fetch({processData: true, reset: true});
  	    this.collection.on('reset', this.renderCollection);
  	    this.item_view = DocumentView;
	}
});


var StudentListView = BaseListView.extend({

    initialize: function (options)
    {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new StudentCollection(options);
        this.collection.fetch({processData: true, reset: true});
        this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.item_view = StudentView;
	}
    
});


var TeamListView = BaseListView.extend({

    initialize: function (options)
    {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new TeamCollection(options);
        this.collection.fetch({processData: true, reset: true});
    	this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.item_view = TeamView;
	}
    
});



