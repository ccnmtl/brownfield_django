jQuery(function() {
    var crs_id = jQuery("input[name='crs-id']").val();
   	jQuery.ajax(
    {
        url: "/update_course/" + crs_id,
    	type: "GET",
    	success: function (data) 
    	{
    		var crs_data = data;
            //console.log(crs_data.course[0].professor);
    	    jQuery('#id_name').val(crs_data.course[0].name);
            jQuery('#id_startingBudget').val(crs_data.course[0].startingBudget);
            jQuery('#id_enableNarrative').val(crs_data.course[0].enableNarrative);
            jQuery('#id_message').val(crs_data.course[0].message);
            jQuery('#id_active').val(crs_data.course[0].active);
            jQuery('#id_archive').val(crs_data.course[0].archive);
            jQuery('#id_professor option:selected' ).text(crs_data.course[0].professor);
            
        },
    	           
    	error: function(data) 
    	{
    	     console.log("There was an error getting course details.");
        }
    }); // end ajax GET
	
	
    jQuery('#update-crs-btn').on('click', function(e)
    {
    	jQuery.ajax(
        {
            url: "/update_course/" + crs_id,
            type: "POST",
            data: {'name' : jQuery('#id_name').val(),
            	   'startingBudget' : jQuery('#id_startingBudget').val(),
            	   'enableNarrative' : jQuery('#id_enableNarrative').val(),
            	   'message' : jQuery('#id_message').val(),
            	   'active' : jQuery('#id_active').val(),
            	   'archive' : jQuery('#id_archive').val(),
            	   'professor' : jQuery('#id_professor option:selected' ).text()
            	   },

            success: function (data) 
            {
        		var crs_data = data;

        	    jQuery('#id_name').val(crs_data.course[0].name);
                jQuery('#id_startingBudget').val(crs_data.course[0].startingBudget);
                jQuery('#id_enableNarrative').val(crs_data.course[0].enableNarrative);
                jQuery('#id_message').val(crs_data.course[0].message);
                jQuery('#id_active').val(crs_data.course[0].active);
                jQuery('#id_archive').val(crs_data.course[0].archive);
                jQuery('#id_professor option:selected' ).text(crs_data.course[0].professor);
                
            },
                  
            error: function(data) 
            {
                console.log("There was an error submitting your form.");
            }
          }); //end ajax UPDATE
    	  e.preventDefault();
    });// end update course on submit function
	
});// end doc on ready