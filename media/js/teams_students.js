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
	    console.log("Initializing a new team model for '" +
	      name + "'."); 
	}
	    
});

	
var TeamCollection = Backbone.Collection.extend({
	 model: Team,
	 url: '/team'
});


//creating team collection with test courses
var team_collection = new TeamCollection([
        {
    		id: 1,
			name: 'Test Team 1',
			//course: "Default Doc Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
		},
		{
			id: 2,
			name: 'Test Team 2',
			//course: "Default Doc Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
		},
		{
			id: 3,
			name: 'Test Team 3',
			//course: "Default Doc Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
		},
		{
			id: 4,
			name: 'Test Team 4',
			//course: "Default Doc Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
		},
		{
			id: 5,
			name: 'Test Team 5',
			//course: "Default Doc Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
		},
		{
			id: 6,
			name: 'Test Team 6',
			//course: "Default Doc Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
		},
		{
			id: 7,
			name: 'Test Team 7',
			//course: "Default Doc Course",
            team_entity: "",
            signed_contract : false,
            budget: 65000
		}
]);


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
var student_collection = new StudentCollection([
        {
    		id: 1,
			first_name: 'Student 1',
			last_name: 'Student 1',
			email: "student@somewhere.com",
            team : ""
		},
		{
			id: 2,
			first_name: 'Student 2',
			last_name: 'Student 2',
			email: "student@somewhere.com",
            team : ""
		},
		{
			id: 3,
			first_name: 'Student 3',
			last_name: 'Student 3',
			email: "student@somewhere.com",
            team : ""
		},
		{
			id: 4,
			first_name: 'Student 4',
			last_name: 'Student 4',
			email: "student@somewhere.com",
            team : ""
		},
		{
			id: 5,
			first_name: 'Student 5',
			last_name: 'Student 5',
			email: "student@somewhere.com",
            team : ""
		},
		{
			id: 6,
			first_name: 'Student 6',
			last_name: 'Student 6',
			email: "student@somewhere.com",
            team : ""
		},
		{
			id: 7,
			first_name: 'Student 7',
			last_name: 'Student 7',
			email: "student@somewhere.com",
            team : ""
		}
]);


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
    
});// End CourseListView    

    

//should probably move this code to controller below not sure if that is be
var document_collection_view = new DocumentListView({
    collection: document_collection
});
// connecting the views to the html/page
jQuery('.documents_list').append(document_collection_view.render().el);

