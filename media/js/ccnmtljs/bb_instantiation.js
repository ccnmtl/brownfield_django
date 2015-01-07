jQuery(document).ready(function () {
	
	var course = jQuery("input[name='crs-id']").val();

    var student_control_view = new StudentControlView({
        el: jQuery('.student_controls'),
        course: course
    });

    var team_control_view = new TeamControlView({
        el: jQuery('.team_controls'),
        course: course
    });

    var document_collection_view = new DocumentListView({
        el: jQuery('.documents_list'),
        course: course
    });
});

