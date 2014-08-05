App.Views.Course = Backbone.View.extend({
  template: _.template($('#template-course').html()),
  $container: null,

  initialize: function(options) {
    _.bindAll(this, 'render', 'insert');

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
  }
});

App.Views.CourseList = Backbone.View.extend({
	  initialize: function() {
	    _.bindAll(this, 'render');
	  },

	  render: function() {
	    var $container = this.$('.listing').empty();

	    App.Courses.each(function(course) {
	      new App.Views.Course({
	        model: course,
	        $container: $container
	      }).render();
	    });

	    return this;
	  }
	});