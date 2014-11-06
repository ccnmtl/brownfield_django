jQuery(function() {
    var crs_id = jQuery("input[name='crs-id']").val();
   	jQuery.ajax(
    {
        url: "/update_course/" + crs_id,
    	type: "GET",
    	success: function (data) 
    	{
    		//console.log(data);
    		
    		//jQuery('#option_area').html();
    		var crs_data = data;
    		//console.log(crs_data.course[0].name);
    	    jQuery('#id_name').val(crs_data.course[0].name);
            jQuery('#id_startingBudget').val(crs_data.course[0].startingBudget);
            jQuery('#id_enableNarrative').val(crs_data.course[0].enableNarrative);
            jQuery('#id_message').val(crs_data.course[0].message);
            jQuery('#id_active').val(crs_data.course[0].active);
            jQuery('#id_archive').val(crs_data.course[0].archive);
            jQuery('#id_professor option:selected' ).text(crs_data.course[0].professor);
            //console.log(data);
        }, 
    	error: function(data) 
    	{
    		console.log(data);
    		alert("There was a problem getting the course details, please try reloading the page.");
        }
    }); // end ajax GET
	
	
    jQuery('#update-crs-btn').on('click', function(e)
    {
    	console.log(data);
    	//console.log(jQuery('#upt-crs-frm').serializeArray());
    	//var array_vars = jQuery('#upt-crs-frm').serializeArray();
    	//console.log(array_vars);
    	//console.log(JSON.stringify(array_vars));
    	//console.log(JSON.stringify(array_vars));
    	var data = $('#upt-crs-frm').serializeArray().reduce(function(obj, item) {
    	    obj[item.name] = item.value;
    	    return obj;
    	}, {});
    	console.log(data);
    	console.log(JSON.stringify(data));
    	var json_data = JSON.stringify(data);
    	
    	jQuery.ajax(
        {
            url: "/update_course/" + crs_id,
            type: "POST",
            data: data,
//            		{'name' : jQuery('#id_name').val(),
//            	   'startingBudget' : jQuery('#id_startingBudget').val(),
//            	   'enableNarrative' : jQuery('#id_enableNarrative').val(),
//            	   'message' : jQuery('#id_message').val(),
//            	   'active' : jQuery('#id_active').val(),
//            	   'archive' : jQuery('#id_archive').val(),
//            	   'professor' : jQuery('#id_professor option:selected' ).text()
//            	   },

            success: function (data) 
            {
        		var crs_data = data;
        		
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
                
                jQuery('#id_professor option:selected' ).text(crs_data.course[0].professor);
                
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
                  
            error: function(data) 
            {
                alert("There was a problem submitting your form, please try again.");
            }
          }); //end ajax UPDATE
    	  e.preventDefault();
    });// end update course on submit function
	
});// end doc on ready