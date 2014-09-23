//// need to send csrf token with requests
//Backbone._sync = Backbone.sync;
//
//Backbone.sync = function(method, model, options) {
//  //from django docs
//  function getCookie(name) {
//      var cookieValue = null;
//      if (document.cookie && document.cookie != '') {
//          var cookies = document.cookie.split(';');
//
//          for (var i = 0; i < cookies.length; i++)
//          {
//              var cookie = jQuery.trim(cookies[i]);
//              // Does this cookie string begin with the name we want?
//              if (cookie.substring(0, name.length + 1) == (name + '=')) 
//              {
//                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                  break;
//              } // end if
//          }// end for cookie.length
//      } // end if document.cookie
//      return cookieValue;
//  } // end getCookie
//
//  /* only need a token for non-get requests */
//  if (method == 'create' || method == 'update' || method == 'delete') 
//  {
//      var csrfToken = getCookie('csrftoken');
//
//      options.beforeSend = function(xhr)
//      {
//          xhr.setRequestHeader('X-CSRFToken', csrfToken);
//      }; // end options.beforeSend
//  } // end if
//
//      return Backbone._sync(method, model, options);
//};


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

// End of Models/Collections
    
//Views 
//var DocumentView = Backbone.View.extend({
//
//   	tagName : 'li',
//   	template: _.template('Document Template <%= name %> <%= link %> Visibility of Document: <%= visible %> <button class="del-dct"> Remove Document</button> <button class="destroy"> Destroy Document</button>'),
//
//    	
//   	/* using initialize to re-render the element if anything in its 
//   	 * corresponding model changes use listenTo instead of on so it will automatically
//   	 *  unbind all events added when it is destroyed */
//   	initialize: function () {
//   	    this.listenTo(this.model, 'change', this.render);
//   	    this.listenTo(this.model, 'destroy', this.remove);
//   	},
//    	
//   	// is there a built in way to remove the model?
//   	events: {
//   		'click .del-crs' : 'onRemoveCourse',
//   		//TODO
//   		'click .destroy' : 'clear'
//   	},
//    	
//    render: function () {
//        if (!this.model) 
//        {
//            throw "Model is not set for this view";
//        }
//          
//        var html = this.template(this.model.toJSON());
//          
//        this.$el.html(html);
//        return this;
//
//    },
//        
//  	onRemoveCourse: function()
//   	{
//   		//will add delete functionality later
//   		console.log("You tried to remove course " + this.model.get('id') + this.model.get('name'));
//   	},
//    	
//   	//TODO
//   	//This correctly adds the id to the url for the DELETE
//   	//but django still has internal error
//    clear: function() {
//        this.model.destroy({
//           	headers : { 'id' : this.model.id }
//        });
//    }
//
//});// End CourseView
//
//    
///* Container to hold rows of documents */
//var DocumentListView = Backbone.View.extend({
//    	
//    tagName : 'ul',
//    
//    render: function() {
//        	
//        // Clean up the view first 
//        this.$el.empty();
//
//        // Iterate over the collection and add each name as a list item
//        this.collection.each(function(model) {
//        this.$el.append(new DocumentView({
//                model: model
//            }).render().el);
//        }, this);
//
//        return this;
//    },
    
//    releaseDocument: function(current_doc) {
//
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
//  
//    }, //end release Document
//    
//    revokeDocument: function(current_doc) {
//
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
//  
//    }, //end revoke Document
//
//    add_course: function(new_crs) {
//    	console.log("Inside collection add_course ");
//    	var nc = new Course({name : new_crs});
//    	nc.save();
//        this.collection.add(nc, {merge: true});
//        console.log("nc " + nc);
//        this.render();
//        return this;
//  
//    } //end add_course
    
    
});// End CourseListView    

    

// should probably move this code to controller below not sure if that is be
var document_collection_view = new DocumentListView({
    collection: document_collection
});

// connecting the views to the html/page
jQuery('.course_documents').append(document_collection_view.render().el);

console.log(course_collection); // log collection to console


////Need to test create()
//var test = course_collection.create({
//  name: "Othello"
//});
//
//
//
////Need to test model save()
//var mtest = new Course({ name : "why doesn't it use defaults?"});
//mtest.save({data:{name:"why doesn't it use defaults?"},type:'POST' });





///*For some reason I can't get the container of course list to respond on click to the button - because I specified tag ul maybe?*/
//jQuery('.add-crs').on('click',
//		
//		function() {
//            jQuery('.controls form').show();
//            jQuery('input.name').focus();
//});
//    
//jQuery('#add-crs-frm').on('submit',
//    function(event) {
//        event.preventDefault();
//        var new_name = jQuery('#add-crs-frm input.name').val();
//        course_collection_view.addCourse(new_name);
//        //course_collection.create({name : something}]);
//
//});

});
