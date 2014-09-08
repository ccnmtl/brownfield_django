jQuery(document).ready(function () {
	
    // handle hash tag navigation
    var hash = window.location.hash;
    hash && jQuery('.instructor-nav a[href="' + hash + '"]').tab('show');
    
    // when the nav item is selected update the page hash
    jQuery('.instructor-nav a').on('shown', function (e) {
        window.location.hash = e.target.hash;
        scrollTo(0,0);
    })
    
    var frm = jQuery('#create_course');
    var course_list = jQuery('#course_list');
    frm.submit(
      function () {
        jQuery.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                jQuery(".modal-body").html("Course added!</br>");
            },
            error: function(data) {
                jQuery(".modal-body").html("Something went wrong!");
            }
        }

        );
        return false;
    });

    var refresh_bttn = jQuery('#refresh');
    refresh_bttn.click(
      function(){

        location.reload();

    });

    
//    var frm = jQuery('#create_team');
//    var course_list = jQuery('#course_list');
//    frm.submit(
//      function () {
//        jQuery.ajax({
//            type: frm.attr('method'),
//            url: frm.attr('action'),
//            data: frm.serialize(),
//            success: function (data) {
//                jQuery(".modal-body").html("Course added!</br>");
//            },
//            error: function(data) {
//                jQuery(".modal-body").html("Something went wrong!");
//            }
//        }
//
//        );
//        return false;
//    });
//
//    var refresh_bttn = jQuery('#refresh');
//    refresh_bttn.click(
//      function(){
//
//        location.reload();
//
//    });    
//    
//    var frm = jQuery('#create_student');
//    var course_list = jQuery('#course_list');
//    frm.submit(
//      function () {
//        jQuery.ajax({
//            type: frm.attr('method'),
//            url: frm.attr('action'),
//            data: frm.serialize(),
//            success: function (data) {
//                jQuery(".modal-body").html("Course added!</br>");
//            },
//            error: function(data) {
//                jQuery(".modal-body").html("Something went wrong!");
//            }
//        }
//
//        );
//        return false;
//    });
//
//    var refresh_bttn = jQuery('#refresh');
//    refresh_bttn.click(
//      function(){
//
//        location.reload();
//
//
//
//    });   
}