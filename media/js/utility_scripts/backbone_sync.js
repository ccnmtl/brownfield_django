// need to send csrf token with requests

  Backbone._sync = Backbone.sync;

  Backbone.sync = function(method, model, options) {
      /* only need a token for non-get requests */
      if (method == 'create' || method == 'update' || method == 'delete') {
          const token = $('meta[name="csrf-token"]').attr('content');

          options.beforeSend = function(xhr){
              const token = $('meta[name="csrf-token"]').attr('content');
              xhr.setRequestHeader('X-CSRFToken', token);
          };
      }

      return Backbone._sync(method, model, options);
  };
