/* Experimenting with suggestions from Backbone best practices for reducing duplicate code */

/* Might be good to pull out show edit form and remove */

/* All List Element Views have the same render function - creating base class with the render method. */
var BaseView = Backbone.View.extend({

	render: function () 
    {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    }

});

/* Further extending the base view for list elements. */

var BaseItemView = BaseView.extend({

    tagName : 'li',

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
    	    //console.log(this.model.attributes)
    		this.model.set('visible', false);
    		this.model.save({
                success: function(model, response) 
                {
                    //'''This does not appear to be called...'''
                    console.log("Inside success function...");
                    console.log(model);
                    console.log(response);
                },
                error: function(model, response)
                {
                        alert("An error occured!");
                },
                wait: true
            });
    		        //{wait: true});
    	}
    	else if (this.model.attributes.visible === false)
    	{
    	    //console.log(this.model.attributes)
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
    		        //{wait: true});
    	}
   	},
   	
   	viewDocument: function()
   	{
   		if(this.model.get('name') === "Link: Brownfield Action Reference Site")
   		{
   			document.location = "http://brownfieldref.ccnmtl.columbia.edu/";
   		}
   		else
		{
    		window.open("../../media/" + this.model.get('link'));
		}
   	}

});


var CourseView = BaseItemView.extend({
    	
   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.template = _.template(jQuery("#course-list-template").html());
   	    /* As of now cannot think of solution for having the list
   	     * of professors available to the CourseView view and the main ControlView*/
   	    //this.prof_list = new InstructorCollection();
        //this.prof_list.fetch({wait: true});
   	},
    	
   	events: {
   	    'click .edit-crs' : 'showEditForm',
   	    'click .save-edit-course' : 'editCourse',
   	    'click .cncl-edit-crs' : 'hideEditForm',
   		'click .destroy' : 'clear'
   	},
    	
    render: function ()
    {
        if (this.model.get('archive') === true) {
            this.$el.remove();
        } else {
        	BaseView.prototype.render.apply(this, arguments);
        }
        return this;
    },
    
    clear: function() {
        this.model.set('archive', true);
        this.model.save();
    },
    
    showEditForm: function()
    {
        var edit_form = _.template(jQuery("#course-edit-template").html())(this.model.toJSON());
        this.$el.append(edit_form);
    },

    hideEditForm: function()
    {   
    	this.$('#create-edit-form').remove();
    },
    
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        var name = jQuery(this.el).find("input#edit_course_name").val();
        var startingBudget = jQuery(this.el).find("input#edit_course_startingBudget").val();
        var message = jQuery(this.el).find("textarea#edit_course_message").val();
        
        if (name === null || name === "") {
            is_valid = false;
            jQuery('.course-name-block').append("<p style='color:#ff0000'>Please enter a valid course name.</p>");
        }
        if (startingBudget === null || startingBudget === "") {
            is_valid = false;
            jQuery('.course-budget-block').append("<p style='color:#ff0000'>Please enter a valid starting budget for your course.</p>");
        }
        if (message === null || message === "") {
            is_valid = false;
            jQuery('.course-message-block').append("<p style='color:#ff0000'>Please enter a valid course message.</p>");
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
        }
    }
});// End CourseView


var TeamView = BaseItemView.extend({
	
   	initialize: function (options) {
   		this.template = _.template(jQuery("#team-list-template").html());
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	events: {
   		'click .rm-team' : 'removeTeam',
   		'click .hist-team' : 'teamHistory',
   		//'click .cncl-edit-team' : 'hideEditForm',
   		//'click .rm-std' : 'removeStudent'
   	},
   	
//    hideEditForm: function()
//    {   
//    	this.$('#create-edit-form').remove();
//    },

   	removeTeam: function()
   	{
   		this.model.destroy();
    },
   	
//    removeStudent: function()
//    {
//        //this.model.destroy();
//        console.log("removeStudent this.model.attributes");
//        console.log(this.model.attributes);
//    },
    
   	teamHistory: function()
   	{
   		window.open("../../team_csv/" + this.model.get('username') + '/');
   	}
});// End Team View


var StudentView = BaseItemView.extend({

	initialize: function(options)
	{
		_.bindAll(this, 'editStudent', 'hideEditForm');
		this.template = _.template(jQuery("#student-list-template").html());
        // need to bind the edit form to the model - when change made to form change model
		this.listenTo(this.model, 'change', this.render);
		this.listenTo(this.model, 'destroy', this.remove);
	},

   	events: {
   		'click .ed-st' : 'showEditForm',
   		'click .save-edit-student' : 'editStudent',
   		'click .cncl-edit-std' : 'hideEditForm',
   		'click .rm-st' : 'removeStudent'
   	},
    
   	showEditForm: function()
   	{
   	    var html = _.template(jQuery("#student-edit-template").html())(this.model.toJSON());
        this.$el.html(html);
    },
    
    hideEditForm: function(e)
    {   
    	e.preventDefault();
    	this.render();
    },
    
   	editStudent: function(e)
   	{
   		e.preventDefault();
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
            	//this.$el.append("<p>Something went wrong, please try again.</p>");
            },
            wait: true
        });//end save
    },
    
   	removeStudent: function()
   	{
   		this.model.destroy();
    }
});


var InstructorView = BaseItemView.extend({

	initialize: function(options)
	{
		_.bindAll(this, 'editInstructor');
		this.template = _.template(jQuery("#instructor-list-template").html());
        // need to bind the edit form to the model - when change made to form change model
		this.listenTo(this.model, 'change', this.render);
		this.listenTo(this.model, 'destroy', this.remove);
	},

   	events: {
   		'click .ed-inst' : 'showEditForm',
   		'click .save-edit-instructor' : 'editInstructor',
   		'click .rm-inst' : 'removeInstructor'
   	},
    
   	showEditForm: function()
   	{
   	    var html = _.template(jQuery("#instructor-edit-template").html())(this.model.toJSON());
        this.$el.html(html);
    },
    
   	editInstructor: function(e)
   	{
   		e.preventDefault();
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
            	//this.$el.append("<p>Something went wrong, please try again.</p>");
            },
            wait: true
        });//end save
    },
    
   	removeInstructor: function()
   	{
   		this.model.destroy();
    }
});


/* Now the Collection Views */

/* Attempting to remove shared functionality into base class */

var BaseListView = Backbone.View.extend({
    
    /* Will over ride this in the List Views */
    this.ItemSubView = BaseItemView;
    
    tagName : 'ul',
    
//    initialize: function (options)
//    {
//        _.bindAll(this, 'initialRender', 'addItem');
//        this.course_collection = new CourseCollection(options);
//        this.course_collection.fetch({processData: true, reset: true});
//        this.course_collection.on('reset', this.initialRender);
//        this.course_collection.on('add', this.addCourse);
//    },
//    
//    initialRender: function() {
//        // Iterate over the collection and add each model as a list item 
//        this.course_collection.each(function(model) {
//            this.$el.append(new CourseView({
//                   model: model
//            }).render().el);
//        }, this);
//
//        return this;
//    },

    addItem: function(model, collection, options) {
        this.$el.append(new this.ItemSubView({
            model: model
        }).render().el);
    }
});


var CourseListView = Backbone.View.extend({
    
    initialize: function (options)
    {
    	_.bindAll(this, 'initialRender', 'addCourse');
    	this.course_collection = new CourseCollection(options);
    	this.course_collection.fetch({processData: true, reset: true});
    	this.course_collection.on('reset', this.initialRender);
    	this.course_collection.on('add', this.addCourse);
	},
   
	initialRender: function() {
        // Iterate over the collection and add each name as a list item 
        this.course_collection.each(function(model) {
            this.$el.append(new CourseView({
                   model: model
            }).render().el);
        }, this);

        return this;
    },

    addCourse: function(model, collection, options) {
        this.$el.append(new CourseView({
            model: model
        }).render().el);
    }
});


var DocumentListView = Backbone.View.extend({

    initialize: function (options)
    {
        _.bindAll(this, 'initialRender');
  	
  	    this.course_document_collection = new DocumentCollection(options);
  	    this.course_document_collection.fetch({processData: true, reset: true});
  	    this.course_document_collection.on('reset', this.initialRender);
	},

    initialRender: function()
    {
        this.course_document_collection.each(function(model)
        {
            this.$el.append(new DocumentView(
            {
                model: model
            }).render().el);
        }, this);

        return this;
    }
});


var StudentListView = Backbone.View.extend({

    initialize: function (options)
    {
    	_.bindAll(this, 'initialRender', 'addStudent');
    	this.course_students = new StudentCollection(options);
    	this.course_students.fetch({processData: true, reset: true});
    	this.course_students.on('reset', this.initialRender);
    	this.course_students.on('add', this.addStudent);
	},	

    initialRender: function() {
        this.course_students.each(function(model) {
        this.$el.append(new StudentView({
               model: model
        }).render().el);
        }, this);

        return this;
    },
    
    addStudent: function(model, collection, options) {
        this.$el.append(new StudentView({
            model: model
        }).render().el);
    }
    
});// End StudentListView


var TeamListView = Backbone.View.extend({

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
    
});


var InstructorListView = Backbone.View.extend({
    
    initialize: function (options)
    {
    	_.bindAll(this, 'initialRender', 'addInstructor');

    	this.instructor_collection = new InstructorCollection(options);
    	this.instructor_collection.fetch({processData: true, reset: true});
    	this.instructor_collection.on('reset', this.initialRender);
    	this.instructor_collection.on('add', this.addInstructor);
	},
   
	initialRender: function() {
        // Iterate over the collection and add each name as a list item 
        this.instructor_collection.each(function(model) {
            this.$el.append(new InstructorView({
                   model: model
            }).render().el);
        }, this);

        return this;
    },

    addInstructor: function(model, collection, options) {
        this.$el.append(new InstructorView({
            model: model
        }).render().el);
    }
});
