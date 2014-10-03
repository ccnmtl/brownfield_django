/* This file is to hold test data for the Collections and models,
 * need some 'instances' to work with, fake data, before moving on
 * to views and templates, and eventually syncing with django.
 * 
 */


// creating course collection with test courses
var course_collection = new CourseCollection([
        {
    		id: 1,
			name: 'Test Course 1'
		},
		{
			id: 2,
			name: 'Test Course 2'
		},
		{
			id: 3,
			name: 'Test Course 3'
		},
		{
			id: 4,
			name: 'Test Course 4'
		},
		{
			id: 5,
			name: 'Test Course 5'
		},
		{
			id: 6,
			name: 'Test Course 6'
		},
		{
			id: 7,
			name: 'Test Course 7'
		}
]);


//creating course collection with test courses
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




//should probably move this code to controller below not sure if that is be
var course_collection_view = new CourseListView({
    collection: course_collection
});

// connecting the views to the html/page
jQuery('.user_courses').append(course_collection_view.render().el);

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
////Need to test create()
//var test = course_collection.create({
//name: "Othello"
//});
//
//
//
////Need to test model save()
//var mtest = new Course({ name : "why doesn't it use defaults?"});
//mtest.save({data:{name:"why doesn't it use defaults?"},type:'POST' });


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































