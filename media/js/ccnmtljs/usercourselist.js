var User = Backbone.Model.extend({
   urlRoot: '/api/user/',
   url: function() {
       var url = this.urlRoot;
       if (this.get('id') !== undefined) {
           url += this.get('id') + '/';
       }
       return url;
   }
});

var Course = Backbone.Model.extend({
    urlRoot: '/api/course/',
    url: function() {
        var url = this.urlRoot;
        if (this.get('id') !== undefined) {
            url += this.get('id') + '/';
        }
        return url;
    }
});

var CourseCollection = Backbone.Collection.extend({
	 model: Course,
	 urlRoot: '/api/course/',
	 url: function() {
	     var url = this.urlRoot;
	     if (this.exclude_username) {
	         url += '?exclude_username=' + this.exclude_username;
	     }
	     return url;
	 },
	 initialize : function(options) {
	     if (options && 'exclude_username' in options) {
	         this.exclude_username = options.exclude_username;
	     }
	 }
});
// End of Models/Collections


//Views 
var CourseView = Backbone.View.extend({

   	tagName : 'li',
    	
   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    
   	    this.template = _.template(jQuery("#add-course-template").html());
   	},
    	
   	events: {
   		'click .destroy' : 'clear'
   	},
    	
    render: function () {
        if (this.model.get('archive') === true) {
            this.$el.remove();
        } else {
            var html = this.template(this.model.toJSON());
            this.$el.html(html);
        }
        return this;
    },

    clear: function() {
        this.model.set('archive', true);
        this.model.save();
    }

});// End CourseView

/* Container to hold rows of users courses */
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
});// End CourseListView   


var ManageCoursesView = Backbone.View.extend({
    events: {
    	//'click .edit-crs' : 'edit',
    	'click .add-crs': 'showCourseForm',
    	'click .submit': 'addCourse'
    },
    
    initialize: function (options) {
        _.bindAll(this,
                  'addCourse',
                  'fetchCourses',
                  'showCourseForm');

        this.options = options;
        
        this.user = new User({id: options.user_id});
        this.user.on('change', this.fetchCourses);
        this.user.fetch();
    },
    
    fetchCourses: function() {
        this.user_course_view =  new CourseListView({
            el: this.options.elUserCourses
        });
        
        if ('elOtherCourses' in this.options) {
            this.other_course_view =  new CourseListView({
                el: this.options.elOtherCourses,
                exclude_username: this.user.get('username')
            });
        }
    },

    showCourseForm: function(e) {
		jQuery(".add-crs").hide();
		jQuery("#add-crs-frm").show();
    },

    addCourse: function(evt) {
        evt.stopPropagation();
    	this.user_course_view.course_collection.create({
    		name: jQuery(".crs-name").val(),
    		message: 'default message',
    		professor: this.user.get('url')
    	}, {wait: true});

	    jQuery("#add-crs-frm").hide();
	    jQuery(".add-crs").show();
	    return false;
    }
});// End UserControlView  
