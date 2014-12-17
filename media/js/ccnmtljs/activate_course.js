// Going to handle buttons here
var activation_status = jQuery("input[name='course_active']").val();

//need to add an onclick to the tab
//#course-active-teams

if(activation_status == "True")
{
	jQuery(".crs-act-info").hide();
	jQuery('#activation-btn').hide();
	jQuery('#edit-team-members').show();
	jQuery(".crs-act-info").hide();
}
if(activation_status == "False")
{
	jQuery('#edit-team-members').hide();
	jQuery('#activation-btn').show();
	jQuery('#course-active-teams').on('click', function(e)
	{
	    jQuery('#edit-team-members').hide();
        //this is complete crap and redundant... need to redo...
        var crs_id = jQuery("input[name='crs-id']").val();
        jQuery(".course-teams").load("/edit_teams/" + crs_id + "/");
        //jQuery('#edit-team-members').hide();
        jQuery('#show-teams').show();
        jQuery('#activation-btn').show();
    });
}

function get_students(){
    //getting students from table
	var data = [];
	
	jQuery('.student-row').each(
        function(){
            var student = {'pk': jQuery(this).find("td input[name='std-id']").val(),
				           'first_name': jQuery(this).find("td input[name='first_name']").val(), 
				           'last_name': jQuery(this).find("td input[name='last_name']").val(), 
				           'email': jQuery(this).find("td input[name='email']").val(),
				           'team_id': jQuery(this).find("td option:selected").val(),
				           'team_name': jQuery(this).find("td option:selected").text()
                           };
            
        data.push({ 'student' : student });
            
    });

    return data;
}

jQuery(function() {

	var crs_id = jQuery("input[name='crs-id']").val();

	jQuery('#activation-btn').on('click', function(e)
    {   
		if(jQuery('#activation-btn').html() === "Save Changes")
		{
			jQuery('#confirmAct').modal('show');
			jQuery('#confirmAct .modal-header .modal-title').html("Course Re-Activation");
			jQuery('#confirmAct .modal-body').html("<p>Are you sure you want to change the teams in your course? This will update the teams, and place the students in the teams. All students will be emailed their teams and team password. Remember if you changed a user's team, the user will still have the original team's login and password unless your request it is changed.</p>");			
			jQuery('#confirmAct .modal-footer #conf-act').html("Continue with Re-Activation");
			
			//jQuery('#confirmAct').modal('show');
		    jQuery('#conf-act').on('click', function(e)
		    {
			    jQuery('#confirmAct').modal('hide');
			    var student_list = get_students();
			    var student_list_2 = JSON.stringify(student_list);

			    jQuery(function()
			    {
			        jQuery.ajax(
			        {
			            url: "/activate_course/" + crs_id + "/",
			            type: "POST",
			            dataType: 'json',
			            data: {'student_list' : student_list_2},
			            success: function (data) 
    	    		    {
			                jQuery('#activationSuccess').modal('show');
			                jQuery('#activationSuccess .modal-header .modal-title').html("Re-Activation Successful");
			                jQuery('#activationSuccess .modal-body').html("<p>Congratulations! Your course has been successfully re-activated!</p>");
			                jQuery("input[name='course_active']").val("True");
			                jQuery(".crs-act-info").hide();
			                jQuery('#activation-btn').hide();
			                jQuery('#edit-team-members').show();
			            },
			            error: function(data) 
	    	    	    {
			               	alert('Something went wrong, please try again');
			            }
			        });// end ajax
			    });// end outer function
    		});// end conf-act on click
        }// end 1st if
		
		if(jQuery('#activation-btn').html() === "Activate Course")
		{
		    jQuery('#confirmAct').modal('show');
		    jQuery('#conf-act').on('click', function(e)
		    {
			    jQuery('#confirmAct').modal('hide');
			    var student_list = get_students();
			    var student_list_2 = JSON.stringify(student_list);

			    jQuery(function()
			    {
			        jQuery.ajax(
			        {
			            url: "/activate_course/" + crs_id + "/",
			            type: "POST",
			            dataType: 'json',
			            data: {'student_list' : student_list_2},
			            success: function (data) 
    	    		    {
			                jQuery('#activationSuccess').modal('show');
			                jQuery("input[name='course_active']").val("True");
			                jQuery(".crs-act-info").hide();
			            },
			            error: function(data) 
	    	    	    {
			               	alert('Something went wrong, please try again');
			            }
			        });// end ajax
			    });// end outer function
    		});// end conf-act on click
        }// end 2nd if
        e.preventDefault();
    });// end activation-btn on click
});// end outer function


/*Set up calls for the get teams/edit teams*/

jQuery(function() {

	var crs_id = jQuery("input[name='crs-id']").val();

	jQuery('#edit-team-members').on('click', function(e)
    {   
		jQuery(".course-teams").load("/edit_teams/" + crs_id + "/");
		jQuery('#edit-team-members').hide();
		jQuery('#show-teams').show();
		jQuery('#activation-btn').html("Save Changes");
		jQuery('#activation-btn').show();
    });
});

jQuery(function() {
	
	var crs_id = jQuery("input[name='crs-id']").val();
	
	jQuery('#show-teams').on('click', function(e)
    {
		jQuery(".course-activation").load("/show_teams/" + crs_id + "/");
		//jQuery('#show-teams').hide();activationSuccess
		jQuery('#activationSuccess').modal('hide');
		jQuery('#edit-team-members').show();
		jQuery('#activation-btn').hide();
		
    });
});



jQuery(function() {
    
    if(activation_status == "False")
    {
        jQuery('#edit-team-members').hide();
        jQuery('#activation-btn').show();
        jQuery('#get_teams').on('click', function(e)
        {
            console.log("get teams clicked");
            jQuery('#edit-team-members').hide();
            //this is complete crap and redundant... need to redo...
            var crs_id = jQuery("input[name='crs-id']").val();
            jQuery(".course-activation").load("/edit_teams/" + crs_id + "/");
            //jQuery('#edit-team-members').hide();
            jQuery('#show-teams').show();
            jQuery('#activation-btn').show();
        });
    }
    
});
//}
