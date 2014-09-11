var UserView = Backbone.View.extend({
    render: function() {
        var html = "<h3>Backbone.js rocks!</h3>";
        this.$el.html(html);
        return this;
    }
});

var userView = new UserView();

// new UserView().render();

//$(document.body).append(userView.render().el);
jQuery('#container').append(userView.render().el);