/* Almost all of these have same url and initialize funciton - mixin or base class */

var BaseCollection = Backbone.Collection.extend({

    url: function() {
        var url = this.urlRoot;
        if (this.course) {
            url += '?course=' + this.course;
        }
        return url;
    },
    
    initialize : function(options){
        if (options && 'course' in options) {
            this.course = options.course;
        }
    }

});

var DocumentCollection = BaseCollection.extend({
	 model: AppDocument,
	 urlRoot: '/api/document/'
});


var StudentCollection = BaseCollection.extend({
	 model: Student,
	 urlRoot: '/api/student/'
});


var InstructorCollection = BaseCollection.extend({
	 model: Instructor,
	 urlRoot: '/api/instructor/'
});


var TeamCollection = BaseCollection.extend({
	 model: Team,
	 urlRoot: '/api/eteam/'
});


var CourseCollection = Backbone.Collection.extend({
	 model: Course,
	 urlRoot: '/api/course/',
	 url: function() {
	     return this.urlRoot;
	 },
	 initialize : function(options) {
	     if (options && 'exclude_username' in options) {
	         this.exclude_username = options.exclude_username;
	     }
	 }
});



