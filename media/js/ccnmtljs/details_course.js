jQuery(function() {
    var crs_id = jQuery("input[name='crs-id']").val();
   	jQuery.ajax(
    {
        url: "/update_course/" + crs_id,
    	type: "GET",
    	success: function (json, textStatus, xhr) 
    	{
    		var crs_data = json.course[0];
    		var html = '<option value="" selected="selected">---------</option>'; 
    		var prof_list = crs_data.professor_list;
    		var json = jQuery.parseJSON(prof_list);

    		for(var i=0; i<json.length; i++)
    		{
	            var obj = json;
	            html = html + 
	                   '<option value="' + obj[i].username + '">' 
	                   + obj[i].first_name + ' ' + obj[i].last_name 
	                   + '</option>';
		    }
    		jQuery('#id_professor').html(html)
    	    jQuery('#id_name').val(crs_data.name);
            jQuery('#id_startingBudget').val(crs_data.startingBudget);
            jQuery('#id_message').val(crs_data.message);

            if (crs_data.enableNarrative === 'true')
            {
                    jQuery('#id_enableNarrative').prop('checked', true);
            }
            if (crs_data.enableNarrative === 'false')
            {
                    jQuery('#id_enableNarrative').prop('checked', false);
            }
            
            if (crs_data.active === 'true')
            {
                    jQuery('#id_active').prop('checked', true);
            }
            if (crs_data.active === 'false')
            {
                    jQuery('#id_active').prop('checked', false);
            }
            
            if (crs_data.archive === 'true')
            {
                    jQuery('#id_archive').prop('checked', true);
            }
            if (crs_data.archive === 'false')
            {
                    jQuery('#id_archive').prop('checked', false);
            }
            
            //not sure what problem with this is...
            jQuery('#id_professor option:selected' ).val(crs_data.professor);
            //jQuery('#id_professor option:selected' ).text(crs_data.course[0].professor.first_name + " " + crs_data.course[0].professor.last_name);
            // come back to this to fill out the professor name
            //jQuery('#id_professor option:selected' ).text(crs_data.course[0].professor);
        }, 
    	error: function(data) 
    	{
    		alert("There was a problem getting the course details, please try reloading the page.");
        }
    }); // end ajax GET
	
	
    jQuery('#update-crs-btn').on('click', function(e)
    {
    	//Setting the values to send here
    	var data = $('#upt-crs-frm').serializeArray().reduce(function(obj, item) {
    	    obj[item.name] = item.value;
    	    return obj;
    	}, {});
    	
    	data.professor = jQuery('#id_professor').val();

    	// now for the booleans
        if (jQuery('#id_enableNarrative').is(':checked'))
        {
        	data.enableNarrative = 'true';
        }
        if (jQuery('#id_enableNarrative').is(':checked') === false)
        {
        	data.enableNarrative = 'false';
        }

        if (jQuery('#id_active').is(':checked'))
        {
        	data.active = 'true';
        }
        if (jQuery('#id_active').is(':checked') === false)
        {
        	data.active = 'false';
        }

       if (jQuery('#id_archive').is(':checked'))
       {
    	   data.archive = 'true';
       }
       if (jQuery('#id_archive').is(':checked') === false)
       {
    	   data.archive = 'false';
       }
    	
    	jQuery.ajax(
        {
            url: "/update_course/" + crs_id,
            type: "POST",
            dataType: 'json',
            data: data,


            success: function (json, textStatus, xhr) 
            {
        		var crs_data = json.course[0];
        		//simple text replace values in form
        	    jQuery('#id_name').val(crs_data.name);
                jQuery('#id_startingBudget').val(crs_data.startingBudget);
                jQuery('#id_message').val(crs_data.message);
                
                var enableNarrative = crs_data.enableNarrative;
                var active = crs_data.active;
                var archive = crs_data.archive;

                jQuery('#course_message').html(crs_data.message)
                
                if (crs_data.enableNarrative === 'true')
                {
                        jQuery('#id_enableNarrative').prop('checked', true);
                }
                if (crs_data.enableNarrative === 'false')
                {
                        jQuery('#id_enableNarrative').prop('checked', false);
                }
                
                if (crs_data.active === 'true')
                {
                        jQuery('#id_active').prop('checked', true);
                }
                if (crs_data.active === 'false')
                {
                        jQuery('#id_active').prop('checked', false);
                }
                
                if (crs_data.archive === 'true')
                {
                        jQuery('#id_archive').prop('checked', true);
                }
                if (crs_data.archive === 'false')
                {
                        jQuery('#id_archive').prop('checked', false);
                }
                jQuery('#id_professor option:selected' ).val(crs_data.professor);

            },
                  
            error: function(json, textStatus, xhr) 
            {
                alert("There was a problem submitting your form, please try again.");
            }
          }); //end ajax UPDATE
    	  e.preventDefault();
    });// end update course on submit function
	
});// end doc on ready