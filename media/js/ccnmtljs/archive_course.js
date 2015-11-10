jQuery(function() {
    var crs_id = jQuery('input[name="crs-id"]').val();
    jQuery('.archive-course').on('click', function() {
        jQuery.ajax({
            url: '/archive_course/' + crs_id + '/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                window.location.href = '/';
            },
            error: function(data) {
                alert('Something went wrong, please try again');
            }
        });// end ajax
    });//end onclick
});// end jQuery(function()
