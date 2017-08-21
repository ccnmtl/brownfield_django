jQuery(function() {
    var crsId = jQuery('input[name="crs-id"]').val();
    jQuery('.archive-course').on('click', function() {
        jQuery.ajax({
            url: '/archive_course/' + crsId + '/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                // eslint-disable-next-line scanjs-rules/assign_to_href
                window.location.href = '/';
            },
            error: function(data) {
                alert('Something went wrong, please try again');
            }
        });
    });
});
