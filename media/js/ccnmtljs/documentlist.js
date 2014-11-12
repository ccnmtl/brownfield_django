
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

var DocumentCollection = Backbone.Collection.extend({
	 model: Document,
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
// End of Models/Collections


// Views 
var DocumentView = Backbone.View.extend({

   	tagName : 'li',
   	//className: 'document-click',
   	initialize: function(options) {
        this.template = _.template(jQuery("#document-list-template").html());
        this.listenTo(this.model, 'change', this.render);
   	},

   	events: {
   		'click .chng-dct' : 'changeDocument',
   		'click .document-click' : 'viewDocument'
   	},

    render: function () {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },
        
    changeDocument: function()
   	{
    	if(this.model.attributes.visible === true)
    	{
    		this.model.set('visible', false);
    		//this.model.save({wait: true});
    		this.model.save();
    	}
    	else if (this.model.attributes.visible === false)
    	{
    		this.model.set('visible', true);
    		//this.model.save({wait: true});
    		this.model.save();
    	}
   	},
   	
   	viewDocument: function()
   	{  //theURL,w,h,resizing,scrolling,winname,closeOnLogout
   		console.log(this.model.attributes);
   		console.log(this.model.get('link'));
   		window.open("../../media/" + this.model.get('link'));
   		//user origin or hostname?
   		//var link = '<a href="' + window.location.hostname + ':8000/media/' + this.model.get('link') + '">' + this.model.get('name') + '</a>'
   		//var link = this.model.get('link').replace("{{STATIC_URL}}", window.location.hostname + ':8000/media/'); 
   		//console.log("link");
   		//console.log(link);
   		//window.open(link);
   		//var href = jQuery(link).attr('href');
   		//console.log("Does link attr() work");
   		//console.log(href);
   		//window.open(href.replace('%3', ''));
   		//window.open(href.replace('"', ''));
   	}
   	

});// End DocumentView

/* Container to hold rows of documents */
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
});// End DocumentListView    

jQuery(document).ready(function () {
    var course = jQuery("input[name='crs-id']").val();

    var document_collection_view = new DocumentListView({
        el: jQuery('.documents_list'),
        course: course
    });
});
