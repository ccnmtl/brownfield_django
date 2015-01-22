jQuery(document).ready(function () {

	var course = jQuery("input[name='crs-id']").val();

    var student_control_view = new StudentControlView({
        el: jQuery('.course-students'),
        course: course
    });

    var team_control_view = new TeamControlView({
        el: jQuery('.team-creation-area'),
        course: course
    });

    var document_collection_view = new DocumentListView({
        el: jQuery('.documents_list'),
        course: course
    });

});

