jQuery(function() {
    var crsId = jQuery('input[name="crs-id"]').val();
    jQuery('.archive-course').on('click', function() {
        jQuery.ajax({
            url: '/archive_course/' + crsId + '/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                window.location.href = '/';
            },
            error: function(data) {
                alert('Something went wrong, please try again');
            }
        });
    });
});
