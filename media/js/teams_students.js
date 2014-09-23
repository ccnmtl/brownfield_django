// creating team model
var Team = Backbone.Model.extend({

    urlRoot: '/team/',
    
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


var StudenttCollection = Backbone.Collection.extend({
	 model: Document,
	 url: '/student'
});
	
	
// creating team collection with test courses
var team_collection = new TeamCollection([
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
