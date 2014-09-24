
  Backbone._sync = Backbone.sync;

  Backbone.sync = function(method, model, options) {
      //from django docs
      function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie != '') {
              var cookies = document.cookie.split(';');
              for (var i = 0; i < cookies.length; i++) {
                  var cookie = jQuery.trim(cookies[i]);
                  // Does this cookie string begin with the name we want?
                  if (cookie.substring(0, name.length + 1) == (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }

      /* only need a token for non-get requests */
      if (method == 'create' || method == 'update' || method == 'delete') {
          var csrfToken = getCookie('csrftoken');

          options.beforeSend = function(xhr){
              xhr.setRequestHeader('X-CSRFToken', csrfToken);
          };
      }

      return Backbone._sync(method, model, options);
};


// creating document model
var Document = Backbone.Model.extend({

    urlRoot: '/document/',
    
    defaults: function() {
        return {
        	id: 0,
            name: "Default Document",
            course: "Default Doc Course",
            link: "",
            visible : false
        }
    },

    initialize: function(attributes) 
	{   
	    this.name = attributes.name || '<EMPTY>';
	    console.log("Initializing a new document model for '" +
	      name + "'."); 
	}
	    
});

	
var DocumentCollection = Backbone.Collection.extend({
	 model: Document,
	 url: '/document'
});
	
	
// creating course collection with test courses
var document_collection = new DocumentCollection([
        {
    		id: 1,
			name: 'Test Course 1',
			link: "<a href='/path/to/document/link/download/'></a>",
            visible : false
		},
		{
			id: 2,
			name: 'Test Course 2',
			link: "<a href='/path/to/document/link/download/'></a>",
            visible : false
		},
		{
			id: 3,
			name: 'Test Course 3',
			link: "<a href='/path/to/document/link/download/'></a>",
            visible : false
		},
		{
			id: 4,
			name: 'Test Course 4',
			link: "<a href='/path/to/document/link/download/'></a>",
            visible : false
		},
		{
			id: 5,
			name: 'Test Course 5',
			link: "<a href='/path/to/document/link/download/'></a>",
            visible : false
		},
		{
			id: 6,
			name: 'Test Course 6',
			link: "<a href='/path/to/document/link/download/'></a>",
            visible : false
		},
		{
			id: 7,
			name: 'Test Course 7',
			link: "<a href='/path/to/document/link/download/'></a>",
            visible : false
		}
]);

console.log(document_collection); // log collection to console
// End of Models/Collections
    
// Views 
var DocumentView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Document Template <%= name %>" +
   			             "<%= link %> " +
   			             "Visibility of Document: " +
   			             "<%= visible %> " +
   			             "<button class='btn btn-xs rel-dct'>" +
   			             "Release Document" +
   			             "</button>" +
   			             "<button class='btn btn-xs rev-dct'>" +
   			             "Revoke Document" +
   			             "</button>"),

   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	// Can probably combine into one function on change
   	events: {
   		'click .rel-dct' : 'releaseDocument',
   		'click .rev-dct' : 'revokeDocument'
   	},

    render: function () {
        if (!this.model) 
        {
            throw "Model is not set for this view";
        }
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },
        
    releaseDocument: function()
   	{   
    	console.log("Releasing Document");
        this.model.save({
           	headers : { 'method_called' : 'release', 'document' : this.model.id }
        });
   	},

   	//will need to do save which will automatically call sync
   	revokeDocument: function()
   	{
   		console.log("Revoking Document");
        this.model.save({
           	headers : { 'method_called' : 'revoke', 'document' : this.model.id }
        });
    }

});// End DocumentView

    
/* Container to hold rows of documents */
var DocumentListView = Backbone.View.extend({
    	
    tagName : 'ul',
    
    render: function() {
        // Clean up the view first 
        this.$el.empty();
        // Iterate over the collection and add each name as a list item
        this.collection.each(function(model) {
        this.$el.append(new DocumentView({
                model: model
            }).render().el);
        }, this);
        return this;
    },

//    releaseDocument: function(current_doc) {
//        this.collection.create(
//        		{name : current_doc}, 
//        		{wait: true,
//            	success: function(data_array){
//            		data = data_array.models[0].attributes;
//            		data = JSON.stringify(data);
//            		console.log("data is " + data);
//                    console.log("in success");
//                    //console.log(data);
//                },
//                error: function(data_array){
//                	data = data_array.models[0].attributes;
//            		data = JSON.stringify(data);
//                	console.log("data is " + data);
//                    console.log("in error");
//                }}
//        );
//        this.render();
//        return this;
//    }, //end release Document
//
//    revokeDocument: function(current_doc) {
//        this.collection.create(
//        		{name : new_dct}, 
//        		{wait: true,
//            	success: function(data_array){
//            		data = data_array.models[0].attributes;
//            		data = JSON.stringify(data);
//            		console.log("data is " + data);
//                    console.log("in success");
//                    //console.log(data);
//                },
//                error: function(data_array){
//                	data = data_array.models[0].attributes;
//            		data = JSON.stringify(data);
//                	console.log("data is " + data);
//                    console.log("in error");
//                }}
//        );
//        this.render();
//        return this;
//    }, //end revoke Document
    
});// End CourseListView    

    

//should probably move this code to controller below not sure if that is be
var document_collection_view = new DocumentListView({
    collection: document_collection
});
// connecting the views to the html/page
jQuery('.documents_list').append(document_collection_view.render().el);

