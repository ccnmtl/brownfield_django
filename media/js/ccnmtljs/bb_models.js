var Document = Backbone.Model.extend({
   urlRoot: '/api/document/',
   url: function() {
       var url = this.urlRoot;
       if (this.get('id') !== undefined) {
           url += this.get('id') + '/';
       }
       return url;
   }
});


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


var Team = Backbone.Model.extend({
	
	   urlRoot: '/admin_team/',
	   url: function() {
	       var url = this.urlRoot;
	       if (this.get('id') !== undefined) {
	           url += this.get('id') + '/';
	       }
	       return url;
	   }
	
});


var Student= Backbone.Model.extend({

	   urlRoot: '/api/student/',
	   url: function() {
	       var url = this.urlRoot;
	       if (this.get('id') !== undefined) {
	           url += this.get('id') + '/';
	       }
	       return url;
	   }	    
});