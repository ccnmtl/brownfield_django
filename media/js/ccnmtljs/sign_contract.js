jQuery(function() {
	
    jQuery('.sign-contract').on('click', function(e){
		
    	jQuery.ajax(
    	{
    	    url: "/team/sign_contract/",
    	    type: "POST",
    	    dataType: 'json',
    	    success: function (data)
    	    {
    	    	jQuery('.show-game').attr("style", "");
    	    	jQuery('.contract-btn').attr("style", "display:none");
    	    	jQuery('.team-div .contract-status').html("True");
    	    },
    	    error: function(data) 
    	    {
    	        alert('Something went wrong, please try again');
    	    }
        });// end ajax
        
    });

});