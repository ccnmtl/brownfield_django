jQuery(function() {
    var crs_id = jQuery("input[name='crs-id']").val();
   	jQuery.ajax(
    {
        url: "/update_course/" + crs_id,
    	type: "GET",
    	success: function (data) 
    	{
    		var html = '<option value="" selected="selected">---------</option>'; //creating a string to return
    		var prof_list = data.course[0].professor_list;
    		var json = jQuery.parseJSON(prof_list);

    		for(var i=0; i<json.length; i++)
    		{
	            var obj = json;
	            html = html + 
	                   '<option value="' + obj[i].username + '">' 
	                   + obj[i].first_name + ' ' + obj[i].last_name 
	                   + '</option>';
		    }
    		jQuery('#id_professor').html(html)//#option_area').html(html);
    		var crs_data = data;
    	    jQuery('#id_name').val(crs_data.course[0].name);
            jQuery('#id_startingBudget').val(crs_data.course[0].startingBudget);
            jQuery('#id_enableNarrative').val(crs_data.course[0].enableNarrative);
            jQuery('#id_message').val(crs_data.course[0].message);
            jQuery('#id_active').val(crs_data.course[0].active);
            jQuery('#id_archive').val(crs_data.course[0].archive);
            jQuery('#id_professor option:selected' ).val(crs_data.course[0].professor);
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
    	//console.log("professor");
    	//console.log(data.professor);
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
            	console.log(json);
            	var crs_json = json.course[0];///jQuery.parseJSON(json);
        		console.log("crs_json");
        		console.log(crs_json);
        		//data.course[0]
        		var crs_data = crs_json;
        		
        		console.log("crs_data");
        		console.log(crs_data);
        		
        		
        		//simple text replace values in form
        	    jQuery('#id_name').val(crs_data.course[0].name);
                jQuery('#id_startingBudget').val(crs_data.course[0].startingBudget);
                jQuery('#id_message').val(crs_data.course[0].message);
                
                var enableNarrative = crs_data.course[0].enableNarrative;
                var active = crs_data.course[0].active;
                var archive = crs_data.course[0].archive;
                //jQuery('#id_enableNarrative').val();
                //jQuery('#id_active').val();
                //jQuery('#id_archive').val();
                
                jQuery('#id_professor option:selected' ).val(crs_data.course[0].professor);
                
                //replace course message at top of page with new one
                jQuery('#course_message').html(crs_data.course[0].message)
                console.log(crs_data.course[0].enableNarrative);
                console.log(crs_data.course[0].active);
                console.log(crs_data.course[0].archive);
                
                
                if (enableNarrative === 'true')
                {
                        jQuery('#id_enableNarrative').prop('checked', true);
                }
                if (enableNarrative === 'false')
                {
                        jQuery('#id_enableNarrative').prop('checked', false);
                }
// 
//        if (model.get('active') === 'true')
//                {
//                        jQuery('#id_active').prop('checked', true);
//                }
//                if (model.get('active') === 'false')
//                {
//                        jQuery('#id_active').prop('checked', false);
//                }
//
//        if (model.get('archive') === 'true')
//                {
//                        jQuery('#id_archive').prop('checked', true);
//                }
//                if (model.get('archive') === 'false')
//                {
//                        jQuery('#id_archive').prop('checked', false);
//                }
//            jQuery('#id_professor option:selected').text(model.get('professor'));
//        }
                
                //console.log(data);
                //console.log(JSON.stringify(data));
            },
                  
            error: function(json, textStatus, xhr) 
            {
            	console.log(json);
                alert("There was a problem submitting your form, please try again.");
            }
          }); //end ajax UPDATE
    	  e.preventDefault();
    });// end update course on submit function
	
});// end doc on ready