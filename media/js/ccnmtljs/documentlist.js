
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
   		var link = this.model.get('link').replace("{{STATIC_URL}}", window.location.hostname + ':8000/media/'); 
   		console.log("link");
   		console.log(link);
//   		var winl = (screen.width - w) / 2;
//   		var wint = (screen.height - h) / 2;
//   	    winprops = 'height='+h+',width='+w+',top='+wint+',left='+winl+',
//						resizable='+resizing+',scrollbars='+scrolling+',location=no,status=no,menubar=no,directories=no,toolbar=no';
//   	    console.log("link before window.open - seems to be adding %3");
//   	    console.log(link);
//   	    console.log("Try explicitly casting to string");
//   	    console.log(String(link));
//   	    console.log(link.toString());
   	    //popwin = window.open(String(link), winname, winprops);
   	    
   	    //popwin = window.open(str.replace("{{STATIC_URL}}", window.location.hostname + ':8000/media/'), winname, winprops);
//   	    popwin = window.open(link.toString(), winname, winprops);
//   	    
//   	    if (/\.jpg$/.test(link)) {
//   		popwin.document.write(
//   				'<a href="javascript:void(0)" onclick="window.print()">print article</a><br />' + 
//   				'<img src="' + link + '" alt="news article"/>');
//   		//popwin.document.write('<img src="'+link+'" alt="news article"/>');
//   		popwin.document.close();
//   	    }
//   	    if (closeOnLogout) {
//   		windows_to_close_on_logout.push(popwin);
//   	    }
//   	    if (parseInt(navigator.appVersion) >= 4) { popwin.window.focus(); }
//   	    if (popwin.opener == null) { popwin.opener = self; }
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
