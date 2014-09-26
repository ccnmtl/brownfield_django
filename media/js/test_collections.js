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