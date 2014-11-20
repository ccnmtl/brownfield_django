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
        this.template = _.template(jQuery("#document-list-template").html());
        this.listenTo(this.model, 'change', this.render);
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
    		this.model.save({wait: true});
    	}
    	else if (this.model.attributes.visible === false)
    	{
    		this.model.set('visible', true);
    		this.model.save({wait: true});
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
   	    this.template = _.template(jQuery("#add-course-template").html());
   	},
    	
   	events: {
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
    }

});// End CourseView


var TeamView = BaseItemView.extend({

   	initialize: function (options) {
   		this.template = _.template(jQuery("#team-list-template").html());
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	events: {
   		'click .rm-team' : 'removeTeam'
   	},

   	removeTeam: function()
   	{
   		this.model.destroy();
    }

});// End Team View


var StudentView = BaseItemView.extend({

	initialize: function(options)
	{
		_.bindAll(this, 'editStudent');
		this.template = _.template(jQuery("#student-list-template").html());
        // need to bind the edit form to the model - when change made to form change model
		this.listenTo(this.model, 'change', this.render);
		this.listenTo(this.model, 'destroy', this.remove);
	},

   	events: {
   		'click .ed-st' : 'showEditForm',
   		'click .save-edit-student' : 'editStudent',
   		'click .rm-st' : 'removeStudent'
   	},
    
   	showEditForm: function()
   	{
   	    var html = _.template(jQuery("#student-edit-template").html())(this.model.toJSON());
        this.$el.html(html);
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


var CourseListView = Backbone.View.extend({
	   
    tagName : 'ul',
    
    initialize: function (options)
    {
    	_.bindAll(this, 'initialRender', 'addCourse');
    	
    	//create new collection to hold user courses
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

    tagName : 'ul',

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

    tagName : 'ul',

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
    
});


var InstructorListView = Backbone.View.extend({
	   
    tagName : 'ul',
    
    initialize: function (options)
    {
    	_.bindAll(this, 'initialRender', 'addInstructor');
    	
    	//create new collection to hold user courses
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
