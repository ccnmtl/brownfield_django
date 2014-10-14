var Document = Backbone.Model.extend({
    urlRoot: '/document/',
});

var DocumentCollection = Backbone.Collection.extend({
	 model: Document,
	 urlRoot: '/document/',
     url: function() {
        return this.urlRoot + this.course_id;
    }
});
// End of Models/Collections


// Views 
var DocumentView = Backbone.View.extend({

   	tagName : 'li',
   	initialize: function(options) {
        this.template = _.template(jQuery("#document-list-template").html());

        this.listenTo(this.model, 'change', this.render);
   	},

   	events: {
   		'click .chng-dct' : 'changeDocument'
   	},

    render: function () {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },
        
    changeDocument: function()
   	{   
        this.model.save({
        	wait: true
        });// end model save
   	}

});// End DocumentView


/* Container to hold rows of documents */
var DocumentListView = Backbone.View.extend({

    tagName : 'ul',

    initialize: function (options)
    {
    	_.bindAll(this,
    			 'initialRender');
    	
    	//create new collection to hold course documents
    	this.course_document_collection = new DocumentCollection();
    	this.course_document_collection.course_id = options.course_id;

    	this.course_document_collection.fetch({processData: true, reset: true});
    	this.course_document_collection.on('reset', this.initialRender);
	},

    initialRender: function() {
        this.course_document_collection.each(function(model) {
        this.$el.append(new DocumentView({
               model: model,
               
        }).render().el);
        }, this);

        return this;
    }
});// End DocumentListView    

jQuery(document).ready(function () {
    var crs_id = jQuery("input[name='crs-id']").val();

    var document_collection_view = new DocumentListView({
        el: jQuery('.documents_list'),
        course_id: crs_id
    });
});
