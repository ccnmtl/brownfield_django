jQuery(function() {

    jQuery('#activation-btn').on('click', function()
    {   
    	console.log("Inside on click.");
    	console.log("crs_id");
    	console.log(crs_id);
    	jQuery.ajax(
                {
                    url: "/activate_course/",
                    type: "POST",
                    data: {'crs_id' : crs_id},
                    success: function (data) 
                    {
                    	console.log("Course activation successful!");
                    },
                  
                    error: function(data) 
                    {
                        console.log("There was an error submitting your form.");
                    }
                });

    
    });
	
});