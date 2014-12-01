// Going to handle buttons here
var activation_status = jQuery("input[name='course_active']").val();

//need to add an onclick to the tab
//#course-active-teams

if(activation_status == "True")
{
	console.log("True");
	jQuery('#activation-btn').hide();
	jQuery('#edit-team-members').show();
	//jQuery('#activation-btn').innerHTML = 'Edit Students/Teams';
}
if(activation_status == "False")
{
	console.log("False");
	//console.log(jQuery('#activation-btn').text());
	// text of button
	jQuery('#edit-team-members').hide();
	jQuery('#activation-btn').show();
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
        	    	},
        	    	error: function(data) 
	    	    	{
        	    		alert('Something went wrong, please try again');
	    	    	}
        		});// end ajax
    		  });// end outer function
    		});// end conf-act on click
		
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
		jQuery('#show-teams').hide();
		jQuery('#edit-team-members').show();
		
    });
});
