var BaseModel = Backbone.Model.extend({

	url: function() {
       var url = this.urlRoot;
       if (this.get('id') !== undefined) {
           url += this.get('id') + '/';
       }
       return url;
   }
});

var AppDocument = BaseModel.extend({
    urlRoot: '/api/document/'
});


var User = BaseModel.extend({
	   urlRoot: '/api/user/'
});


var Instructor = BaseModel.extend({
	   urlRoot: '/api/instructor/'
});


var Course = BaseModel.extend({
	    urlRoot: '/api/course/'
});


var Team = BaseModel.extend({
	   urlRoot: '/admin_team/'
});


var Student= BaseModel.extend({
	   urlRoot: '/api/student/'   
});