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
	    //console.log("Initializing a new document model for '" +
	    //  name + "'."); 
	}
	    
});

//creating document collection	
var DocumentCollection = Backbone.Collection.extend({
	 model: Document,
	 url: '/document'
});
	
	
// creating document collection with test documents
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

//console.log(document_collection); // log collection to console
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
    	/*Can't figure out how to use backbone without getting authentication errors...*/
    	//console.log("Releasing Document");
        this.model.save(
        	{id : this.model.id, visible : true}, {
        	wait:true,
        	success:function(model, response) {
        	        console.log('Successfully saved!');
        	},
        	error: function(model, error) {
                console.log(model.toJSON());
                console.log('error.responseText');
            }
        });// end model save
   	},

   	//will need to do save which will automatically call sync
   	revokeDocument: function()
   	{
        this.model.save({
        });// end model save
    }

});// End DocumentView


/* Container to hold rows of documents */
var DocumentListView = Backbone.View.extend({
    	
    tagName : 'ul',
   	events: {
   		'click .rel-dct' : 'releaseDocument',
   		'click .rev-dct' : 'revokeDocument'
   	},
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
    }
    
});// End CourseListView    

    

//should probably move this code to controller below not sure if that is be
var document_collection_view = new DocumentListView({
    collection: document_collection
});
// connecting the views to the html/page
jQuery('.documents_list').append(document_collection_view.render().el);

//jQuery("#good_con input[name='conversation']").val();.course-activation .crs-activate 
//jQuery('#activation-btn').click(console.log("button clicked"));
//'click',
//    function(){
//        console.log("you clicked on the button");
//});


//        this.activationForm = this.$(".crs-activate");
//	    this.activationButton = this.$(".crs-activate .btn btn-mini btn-success");
//	    
//	    this.activationButton.on('click', this.activateCourse);
