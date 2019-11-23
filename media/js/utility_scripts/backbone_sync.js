// need to send csrf token with requests

  Backbone._sync = Backbone.sync;

  Backbone.sync = function(method, model, options) {
      //from django docs
      function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie != '') {
              var cookies = document.cookie.split(';');
              for (var i = 0; i < cookies.length; i++) {
                  var cookie = jQuery.trim(cookies[i]);
                  // Does this cookie string begin with the name we want?
                  if (cookie.substring(0, name.length + 1) == (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }

      /* only need a token for non-get requests */
      if (method == 'create' || method == 'update' || method == 'delete') {
          const token = $('meta[name="csrf-token"]').attr('content');

          options.beforeSend = function(xhr){
              xhr.setRequestHeader('X-CSRFToken', token);
          };
      }

      return Backbone._sync(method, model, options);
  };
