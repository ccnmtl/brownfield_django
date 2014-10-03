// creating team model
var Team = Backbone.Model.extend({

    urlRoot: '/team/',
    
    defaults: function() {
        return {
        	id: 0,
            name: "Default Team",
            course: "Default Team Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
        }
    },

    initialize: function(attributes) 
	{   
	    name = attributes.name || '<EMPTY>';
	    //console.log("Initializing a new team model for '" +
	    //  name + "'."); 
	}
	    
});

	
var TeamCollection = Backbone.Collection.extend({
	 model: Team,
	 url: '/team'
});





//creating student model
var Student= Backbone.Model.extend({

    urlRoot: '/student/',
    
    defaults: function() {
        return {
        	id: 0,
            first_name: "First Name Student",
            last_name: "Last Name Student",
            email: "email@email.com",
            //course: "Default Student Course",
            team: "Member of Team....()"
        }
    },

    initialize: function(attributes) 
	{   
	    first_name = attributes.first_name || '<EMPTY>';
	    last_name = attributes.last_name || '<EMPTY>';
	    console.log("Initializing a new student model for '" +
	    		first_name + " " +  last_name + "'.");
	}
	    
});


var StudentCollection = Backbone.Collection.extend({
	 model: Student,
	 url: '/student'
});
	
	


	
// creating student collection with test courses


//End of Modes/Collections

//Views 
var StudentView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Student Template Name <%= first_name %>" +
   			             "<%= last_name %> " +
   			             "Email: " +
   			             "<%= email %> " +
   			             "Team Status: " +
   			             "<%= team %> " +
   			             "<button class='btn btn-xs jn-tm'>" +
   			             "Add to Team" +
   			             "</button>" +
   			             "<button class='btn btn-xs rm-tm'>" +
   			             "Remove From Team" +
   			             "</button>"),

   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	// Can probably combine into one function on change
   	events: {
   		'click .jn-tm' : 'joinTeam',
   		'click .rm-tm' : 'removeTeam'
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

    joinTeam: function()
   	{   
    	//console.log("Releasing Document");
        this.model.destroy({
           	headers : { 'id' : this.model.id }//{ 'method_called' : 'release'}//, 'document' : this.model.id }
        });
   	},

   	//will need to do save which will automatically call sync
   	removeTeam: function()
   	{
   		//console.log("Revoking Document");
        this.model.save({
           	headers : { 'id' : this.model.id }//{ 'method_called' : 'revoke'}//, 'document' : this.model.id }
        });
    }

});// End DocumentView


