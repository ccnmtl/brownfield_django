function confirm_reactivation() {

    jQuery('#confirmAct').modal('show');
    jQuery('#confirmAct .modal-header .modal-title')
        .html('Course Re-Activation');
    jQuery('#confirmAct .modal-body')
        .html('<p>Are you sure you want to make changes to the teams in your course? Doing so will update the teams and student users accordingly and will send the student users new login credentials for the system. Note: the updated student users will still have access to their original teams login credentials unless you request it to be changed.</p>');
    jQuery('#confirmAct .modal-footer #conf-act')
        .html('Continue with Re-Activation');
}

function reactivation_success() {
    jQuery('#activationSuccess').modal('show');
    jQuery('#activationSuccess .modal-header .modal-title')
        .html('Re-Activation Successful');
    jQuery('#activationSuccess .modal-body')
        .html('<p>Congratulations! Your course has been successfully re-activated!</p>');
    jQuery('.crs-act-info').hide();
    jQuery('#activation-btn').hide();
    jQuery('#edit-team-members').show();
}

function activation_success() {
    jQuery('#activationSuccess').modal('show');
    jQuery('.crs-act-info').hide();
}

function show_active() {
    jQuery('#edit-team-members').show();
    jQuery('#activation-btn').hide();
    jQuery('.crs-act-info').hide();
}

function show_not_active() {
    jQuery('#edit-team-members').hide();
    jQuery('#show-teams').show();
    jQuery('#activation-btn').show();
}

function get_edit_content(crs_id) {
    jQuery('.course-teams').load('/edit_teams/' + crs_id + '/');
}

function get_active_content(crs_id) {
    jQuery('.course-activation').load('/show_teams/' + crs_id + '/');
    jQuery('#activationSuccess').modal('hide');
    jQuery('#edit-team-members').show();
    jQuery('#activation-btn').hide();
}

function get_students() {
    //getting students from table
    var data = [];
    jQuery('.student-row').each(
        function() {
            var student = {
                'pk': jQuery(this).find('td input[name="std-id"]').val(),
                'first_name': jQuery(this)
                    .find('id input[name="first_name"]').val(),
                'last_name': jQuery(this)
                    .find('td input[name="last_name"]').val(),
                'email': jQuery(this).find('td input[name="email"]').val(),
                'team_id': jQuery(this).find('td option:selected').val(),
                'team_name': jQuery(this).find('td option:selected').text()
            };

            data.push({'student': student});

        });

    return data;
}

jQuery(function() {
    var crs_id = jQuery('input[name="crs-id"]').val();
    var activation_status = jQuery('input[name="course_active"]').val();

    if (activation_status === 'True') {
        show_active();
        jQuery('#activation-btn').html('Save Changes');

    }
    if (activation_status === 'False') {
        show_not_active();
        jQuery('#activation-btn').html('Activate Course');
    }

    jQuery('#get_teams')
        .on('click', function(e) {
            if (activation_status === 'True') {
                jQuery('.course-activation')
                    .load('/show_teams/' + crs_id + '/');
            }
            if (activation_status === 'False') {
                jQuery('.course-activation')
                    .load('/edit_teams/' + crs_id + '/');
            }
        });

    /* button for activating/reactivating course */
    jQuery('#activation-btn')
        .on('click', function(e) {
            if (activation_status === 'True') {
                jQuery('#activation-btn').html('Save Changes');
                confirm_reactivation();
            }
            if (activation_status === 'False') {
                jQuery('#activation-btn').html('Activate Course');
                jQuery('#confirmAct').modal('show');
                confirm_activation();
            }
            e.preventDefault();
        });

    jQuery('#conf-act').on('click', function(e) {
        jQuery('#confirmAct').modal('hide');
        var student_list = get_students();
        var student_list_2 = JSON.stringify(student_list);

        jQuery.ajax({
            url: '/activate_course/' + crs_id + '/',
            type: 'POST',
            dataType: 'json',
            data: {'student_list': student_list_2},
            success: function(data) {
                if (activation_status === 'True') {
                    reactivation_success();
                }

                if (activation_status === 'False') {
                    activation_success();
                }

                jQuery('input[name="course_active"]').val('True');
                activation_status = jQuery('input[name="course_active"]')
                    .val();
                jQuery('#activation-btn').html('Re-Activate Course');
            },
            error: function(data) {
                alert('Something went wrong, please try again');
            }
        });// end ajax
    });// end conf-act on click

    jQuery('#edit-team-members')
        .on('click', function(e) {
            get_edit_content(crs_id);
            show_not_active();
            jQuery('#edit-team-members').hide();
        });

    jQuery('#show-teams').on('click', function(e) {
        get_active_content(crs_id);
    });

});// end outer function
