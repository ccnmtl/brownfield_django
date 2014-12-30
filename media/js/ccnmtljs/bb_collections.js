/* Almost all of these have same url and initialize funciton - mixin or base class */

var DocumentCollection = Backbone.Collection.extend({
	 model: AppDocument,
	 urlRoot: '/api/document/',
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


var StudentCollection = Backbone.Collection.extend({
	
	 model: Student,
	 urlRoot: '/api/student/',
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


var InstructorCollection = Backbone.Collection.extend({
	
	 model: Instructor,
	 urlRoot: '/api/instructor/',
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


var TeamCollection = Backbone.Collection.extend({
	
	 model: Team,
	 urlRoot: '/admin_team/',
	 headers: {"content-type": "application/json"},
	 url: function() {
	     var url = this.urlRoot;
	     if (this.course) {
	         url += this.course + '/';
	     }
	     return url;
	 },
	 initialize : function(options){
	     if (options && 'course' in options) {
	         this.course = options.course;
	     }
	 }
});


var CourseCollection = Backbone.Collection.extend({
	 model: Course,
	 urlRoot: '/api/course/',
	 url: function() {
	     var url = this.urlRoot;
//	     if (this.exclude_username) {
//	         url += '?exclude_username=' + this.exclude_username;
//	     }
	     return url;
	 },
	 initialize : function(options) {
	     if (options && 'exclude_username' in options) {
	         this.exclude_username = options.exclude_username;
	     }
	 }
});



