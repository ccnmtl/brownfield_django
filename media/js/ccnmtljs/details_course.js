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
    		var returned_json = jQuery.parseJSON(prof_list);

    		for(var i=0; i<returned_json.length; i++)
    		{
	            var obj = returned_json;
	            html = html + 
	                   '<option value="' + obj[i].username + '">' +
	                   obj[i].first_name + ' ' + obj[i].last_name + 
	                   '</option>';
		    }
    		jQuery('#id_professor').html(html);
    	    jQuery('#id_name').val(crs_data.name);
            jQuery('#id_startingBudget').val(crs_data.startingBudget);
            jQuery('#id_message').val(crs_data.message);
            jQuery('#id_enableNarrative').prop(
            	    'checked', crs_data.enableNarrative === 'true');
            jQuery('#id_active').prop(
            	    'checked', crs_data.active === 'true');
            jQuery('#id_archive').prop(
            	    'checked', crs_data.archive === 'true');
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
    	data.enableNarrative = jQuery('#id_enableNarrative').is(':checked');
        data.active = jQuery('#id_active').is(':checked');
        data.archive = jQuery('#id_archive').is(':checked');

        jQuery.ajax(
        {
            url: "/update_course/" + crs_id,
            type: "POST",
            dataType: 'json',
            data: data,

            success: function (json, textStatus, xhr) 
            {
            	//see if course already has successful save p in it
            	//if (jQuery( "#panel-title-id" ).has( "p" ).length === 1)
            	//{
            	//	console.log("Successful save already visable");
            	//}
        		var crs_data = json.course[0];
        		//simple text replace values in form
        	    jQuery('#id_name').val(crs_data.name);
                jQuery('#id_startingBudget').val(crs_data.startingBudget);
                jQuery('#id_message').val(crs_data.message);
                
                var enableNarrative = crs_data.enableNarrative;
                var active = crs_data.active;
                var archive = crs_data.archive;

                jQuery('#course_message').html(crs_data.message);
                jQuery('#id_enableNarrative').prop(
            	    'checked', crs_data.enableNarrative === 'true');
                jQuery('#id_active').prop(
            	    'checked', crs_data.active === 'true');
                jQuery('#id_archive').prop(
            	    'checked', crs_data.archive === 'true');
                jQuery('#id_professor option:selected' ).val(crs_data.professor);
                jQuery('#collapseForm').removeClass('panel-collapse in').addClass('panel-collapse collapse');
                jQuery('#panel-title-id').append("<p style='color:red;'>Your Edit has been saved</p>");
                
            },  
            error: function(json, textStatus, xhr) 
            {
                alert("There was a problem submitting your form, please try again.");
            }
          }); //end ajax UPDATE
    	  e.preventDefault();
    });// end update course on submit function
   
    
    
    
});// end doc on ready