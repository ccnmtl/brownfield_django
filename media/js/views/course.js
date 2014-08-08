App.Views.Course = Backbone.View.extend({
  template: _.template($('#template-course').html()),
  $container: null,

  events: {
	    'click .delete': 'remove'
  },

  
  initialize: function(options) {
    _.bindAll(this, 'render', 'insert', 'remove');

   this.$container = options.$container;

    this.listenTo(this.model, 'change', this.render);
    this.insert();
  },

  render: function() {
    this.$el.html(this.template(this.model.attributes));

    return this;
  },

  insert: function() {
    this.$container.append(this.$el);
  },
  
  remove: function() {
	    this.model.destroy();
  }

});
