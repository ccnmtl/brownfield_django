/* Tests for Models - models are simple, just define base model url
 * function and url for each decendant model*/

module('Model and BaseModel tests', {

    setup: function () {
        this.appdoc = new AppDocument();
        this.id_appdoc = new AppDocument();
        this.user = new User();
        this.id_user = new User();
        this.instructor = new Instructor();
        this.id_instructor = new Instructor();
        this.course = new Course();
        this.id_course = new Course();
        this.team = new Team();
        this.id_team = new Team();
        this.student = new Student();
        this.id_student = new Student();
        this.id_appdoc.set('id', 1);
        this.id_user.set('id', 1);
        this.id_instructor.set('id', 1);
        this.id_course.set('id', 1);
        this.id_team.set('id', 1);
        this.id_student.set('id', 1);
    }
});

test('Test BaseModel url function/attribute', function () {
    equal(this.appdoc.get('id'), undefined);
    equal(this.appdoc.url(), '/api/document/');
    equal(this.id_appdoc.get('id'), 1);
    equal(this.id_appdoc.url(), '/api/document/1/');
    
    equal(this.user.get('id'), undefined);
    equal(this.user.url(), '/api/user/');
    equal(this.id_user.get('id'), 1);
    equal(this.id_user.url(), '/api/user/1/');
    
    equal(this.instructor.get('id'), undefined);
    equal(this.instructor.url(), '/api/instructor/');
    equal(this.id_instructor.get('id'), 1);
    equal(this.id_instructor.url(), '/api/instructor/1/');
    
    equal(this.course.get('id'), undefined);
    equal(this.course.url(), '/api/course/');
    equal(this.id_course.get('id'), 1);
    equal(this.id_course.url(), '/api/course/1/');
    
    equal(this.student.get('id'), undefined);
    equal(this.student.url(), '/api/student/');
    equal(this.id_student.get('id'), 1);
    equal(this.id_student.url(), '/api/student/1/');
    
    equal(this.team.get('id'), undefined);
    equal(this.team.url(), '/api/eteam/');
    equal(this.id_team.get('id'), 1);
    equal(this.id_team.url(), '/api/eteam/1/');

});

/* Tests for Collections
 * again most logic is in the Views, there is BaseCollection
 * with 2 functions and all the decendants define url and model
 * type of collection*/


module('Collection and BaseCollection tests', {

    setup: function () {
        this.doc_collection = new DocumentCollection();
        this.course_doc_collection = new DocumentCollection({ 'course': 5 });
        this.student_collection = new StudentCollection();
        this.course_student_collection = new StudentCollection({ 'course': 5 });
        this.instructor_collection = new InstructorCollection();
        this.course_instructor_collection = new InstructorCollection({ 'course': 5 });
        this.team_collection = new TeamCollection();
        this.course_team_collection = new TeamCollection({ 'course': 5 });
        this.course_collection = new CourseCollection();
        /* the following is pointless and never actually used */
        this.course_course_collection = new CourseCollection({ 'course': 5 });
    }
});

test('Test BaseCollection and Collection url function/attribute and initalization', function () {
    equal(this.doc_collection.url(), '/api/document/');
    equal(this.doc_collection.model, AppDocument);
    equal(this.course_doc_collection.url(), '/api/document/?course=5');
    
    equal(this.student_collection.url(), '/api/student/');
    equal(this.student_collection.model, Student);
    equal(this.course_student_collection.url(), '/api/student/?course=5');
    
    equal(this.instructor_collection.url(), '/api/instructor/');
    equal(this.instructor_collection.model, Instructor);
    equal(this.course_instructor_collection.url(), '/api/instructor/?course=5');
    
    equal(this.team_collection.url(), '/api/eteam/');
    equal(this.team_collection.model, Team);
    equal(this.course_team_collection.url(), '/api/eteam/?course=5');
    
    equal(this.course_collection.url(), '/api/course/');
    equal(this.course_collection.model, Course);
    equal(this.course_course_collection.url(), '/api/course/?course=5');
});


/* Going to attempt to do View tests... */

/* Should figure out how to test the general funcitons of BaseItemView */

module('BaseItemView tests', {

    setup: function () {
        this.base_view = new BaseItemView();
    }
});

test('Test BaseItemView', function () {
    equal(this.base_view.tagName, 'li');
});



