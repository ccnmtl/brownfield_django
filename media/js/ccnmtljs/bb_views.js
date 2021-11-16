/* global DocumentCollection: true, StudentCollection: true */
/* global TeamCollection: true, InstructorCollection: true */
/* global CourseCollection: true */

/* Experimenting with suggestions from Backbone best practices
 * for reducing duplicate code */

/* Might be good to pull out show edit form and remove */

/* All List Element Views have the same render function -
 * creating base class with the render method. */
var BaseItemView = Backbone.View.extend({

    tagName: 'li',

    render: function() {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },

    hideEditForm: function(e) {
        e.preventDefault();
        this.render();
    },

    showEditForm: function(e) {
        var editForm = this.editForm(this.model.toJSON());
        this.$el.html(editForm);
    },

    isEmpty: function(selectorString, errorElement, errorMsg) {
        var check = jQuery(this.el).find(selectorString).val();
        if (check === null || check === '') {
            if ((jQuery(errorElement).has('.is-empty').length) === 0) {
                jQuery(errorElement).append(
                    '<b class="error-msg is-empty" style="color:red">' +
                    String(errorMsg) + '</b>');
            }
            return true;
        }
        return false;
    },

    confirmArchival: function(evt) {
        var current = jQuery(this.el);
        current.find('.conf-del').show();
        current.find('.conf-del').css({
            'display': 'inline',
            'color': 'red',
            'font-weight': 'bold'
        });
        current.find('.reg-btn').hide();
    },

    cancelArchive: function(evt) {
        var current = jQuery(this.el);
        current.find('.reg-btn').show();
        current.find('.conf-del').hide();
    }
});

var DeletableItemView = BaseItemView.extend({
    removeItem: function() {
        this.model.destroy();
    }

});

/* Start with Single Element Views */
var DocumentView = BaseItemView.extend({

    initialize: function(options) {
        _.bindAll(this, 'changeDocument');
        this.listenTo(this.model, 'change', this.render);
        this.template = _.template(jQuery('#document-list-template').html());
    },

    events: {
        'click .chng-dct': 'changeDocument'
    },

    changeDocument: function() {
        if (this.model.attributes.visible === true) {
            this.model.set('visible', false);
            this.model.save({
                success: function(model, response) {
                },
                error: function(model, response) {
                    alert('An error occurred!');
                },
                wait: true
            });
        } else if (this.model.attributes.visible === false) {
            this.model.set('visible', true);
            this.model.save({
                success: function(model, response) {
                },
                error: function(model, response) {
                    alert('An error occured!');
                },
                wait: true
            });
        }
    },
});

var CourseView = BaseItemView.extend({

    initialize: function() {
        this.listenTo(this.model, 'change', this.render);
        this.template = _.template(jQuery('#course-list-template').html());
        this.editForm = _.template(jQuery('#course-edit-template').html());
        /*
         * As of now cannot think of solution for having the list of professors
         * available to the CourseView view and the main ControlView
         */
    },

    events: {
        'click .course_name': 'courseDetails',
        'click .edit-crs': 'showEditForm',
        'click .save-edit-course': 'editCourse',
        'click .cncl-edit-crs': 'hideEditForm',
        'click .conf-archive-course': 'confirmArchival',
        'click .cancel-arch': 'cancelArchive',
        'click .conf-arch': 'clear'
    },

    render: function() {
        if (this.model.get('archive') === true) {
            this.$el.remove();
        } else {
            BaseItemView.prototype.render.apply(this, arguments);
        }
        return this;
    },

    clear: function() {
        this.model.set('archive', true);
        this.model.save();
    },

    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var isValid = true;

        if (this.isEmpty('input#edit_course_name', '.course-name-block',
            'Please enter a valid course name.')) {
            isValid = false;
        }

        if (this.isEmpty(
            'input#edit_course_startingBudget', '.course-budget-block',
            'Please enter a valid starting budget for your course.')) {
            isValid = false;
        }
        if (this.isEmpty('textarea#edit_course_message',
            '.course-message-block',
            'Please enter a valid course message.')) {
            isValid = false;
        }

        return isValid;
    },

    editCourse: function(evt) {
        evt.preventDefault();

        if (this.validEditForm()) {
            var name = jQuery(this.el).find('input#edit_course_name').val();
            var startingBudget = jQuery(this.el).find(
                'input#edit_course_startingBudget').val();
            var message = jQuery(this.el).find('textarea#edit_course_message')
                .val();

            this.model.set('name', name);
            this.model.set('startingBudget', startingBudget);
            this.model.set('message', message);
            this.model.save({
                success: function(model, response) {
                },
                error: function(model, response) {
                    alert('An error occured!');
                },
                wait: true
            });// end save
        }// end if
    },// end editCourse

    courseDetails: function() {
        window.location.href = '/course_details/' + this.model.get('id') + '/';
    }
});// End CourseView

var InstructorView = BaseItemView.extend({

    initialize: function(options) {
        _.bindAll(this, 'editInstructor');
        this.template = _.template(jQuery('#instructor-list-template').html());
        this.editForm = _.template(jQuery('#instructor-edit-template').html());
        // need to bind the edit form to the model - when change made to
        // form change model
        this.listenTo(this.model, 'change', this.render);
    },

    events: {
        'click .ed-inst': 'showEditForm',
        'click .save-edit-instructor': 'editInstructor',
        'click .cncl-edit-inst': 'hideEditForm',
        'click .conf-archive-inst': 'confirmArchival',
        'click .cancel-arch-inst': 'cancelArchive',
        'click .conf-arch': 'clear'
    },

    render: function() {
        var prof = this.model.get('profile');
        if (prof && prof.archive === true) {
            this.$el.remove();
        } else {
            BaseItemView.prototype.render.apply(this, arguments);
        }
        return this;
    },

    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var isValid = true;

        if (this.isEmpty('input.edt-frst-name',
            '.inst-edt-first-name', 'Please enter a first name.')) {
            isValid = false;
        }
        if (this.isEmpty('input.edt-last-name', '.inst-edt-last-name',
            'Please enter a last name.')) {
            isValid = false;
        }
        if (this.isEmpty('input.edt-email', '.inst-edt-email',
            'Please enter a email address.')) {
            isValid = false;
        }

        return isValid;
    },

    editInstructor: function(e) {
        e.preventDefault();

        if (this.validEditForm()) {
            var current = jQuery(this.el);
            var instFname = current.find('input.edt-frst-name').val();
            var instLname = current.find('input.edt-last-name').val();
            var instEmail = current.find('input.edt-email').val();
            /*
             * For some reason setting the attributes below only sets
             * correctly if you edit email, pulling the varibles here
             * because here they are correct and then passing.
             */
            this.model.set('first_name', instFname);
            this.model.set('last_name', instLname);
            this.model.set('email', instEmail);
            this.model.save({
                success: function(model, response) {
                },
                error: function(model, response) {
                    alert('An error occured!');
                },
                wait: true
            });// end save
        }
    },

    clear: function() {
        this.model.get('profile').archive = true;
        this.model.save({
            wait: true
        });
    }

});

var TeamView = DeletableItemView.extend({

    initialize: function(options) {
        this.template = _.template(jQuery('#team-list-template').html());
        this.editForm = _.template(jQuery('#team-edit-template').html());
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.remove);
    },

    events: {
        'click .rm-team': 'removeItem',
        'click .edit-team': 'showEditForm',
        'click .save-edit-team': 'editTeam',
        'click .cncl-edit-team': 'hideEditForm',
        'click .hist-team': 'teamHistory'
    },

    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var isValid = true;

        if (this.isEmpty('input.edt-team-name', '.div-edt-team-name',
            'Please enter a team name.')) {
            isValid = false;
        }

        return isValid;
    },

    editTeam: function(e) {
        e.preventDefault();

        if (this.validEditForm()) {

            var firstName = jQuery(this.el).find('input.edt-team-name').val();

            this.model.set('first_name', firstName);
            this.model.save({
                success: function(model, response) {
                },
                error: function(model, response) {
                    alert('An error occured!');
                },
                wait: true
            });// end save
        }
    },

    teamHistory: function() {
        // eslint-disable-next-line security/detect-non-literal-fs-filename
        window.open('/team_csv/' + this.model.get('id') + '/');
    }
});// End Team View

var StudentView = DeletableItemView.extend({

    initialize: function(options) {
        _.bindAll(this, 'editStudent', 'hideEditForm', 'showEditForm');
        this.template = _.template(jQuery('#student-list-template').html());
        this.editForm = _.template(jQuery('#student-edit-template').html());
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.remove);
    },

    events: {
        'click .ed-st': 'showEditForm',
        'click .save-edit-student': 'editStudent',
        'click .cncl-edit-std': 'hideEditForm',
        'click .rm-st': 'removeItem'
    },
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var isValid = true;

        if (this.isEmpty('input.edt-frst-name', '.sedt-first-name',
            'Please enter a first name.')) {
            isValid = false;
        }

        if (this.isEmpty('input.edt-last-name', '.sedt-last-name',
            'Please enter a last name.')) {
            isValid = false;
        }
        if (this.isEmpty('input.edt-email', '.sedt-email',
            'Please enter a email address.')) {
            isValid = false;
        }

        return isValid;
    },
    editStudent: function(e) {
        e.preventDefault();

        if (this.validEditForm()) {
            var stdFname = jQuery(this.el).find('input.edt-frst-name').val();
            var stdLname = jQuery(this.el).find('input.edt-last-name').val();
            var stdEmail = jQuery(this.el).find('input.edt-email').val();
            /*
             * For some reason setting the attributes below only sets correctly
             * if you edit email, pulling the varibles here because here they
             * are correct and then passing.
             */
            this.model.set('first_name', stdFname);
            this.model.set('last_name', stdLname);
            this.model.set('email', stdEmail);
            this.model.save({
                success: function(model, response) {
                },
                error: function(model, response) {
                    alert('An error occured!');
                },
                wait: true
            });// end save
        }
    }

});

/* Now the Collection Views */
var BaseListView = Backbone.View.extend({

    renderCollection: function() {
        this.$el.html('');
        this.collection.each(function(model) {
            this.$el.append(new this.itemView({
                model: model
            }).render().el);
        }, this);
        return this;
    },

    addItem: function(model, collection, options) {
        this.$el.append(new this.itemView({
            model: model
        }).render().el);
    }
});

// eslint-disable-next-line no-unused-vars
var InstructorListView = BaseListView.extend({

    initialize: function(options) {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new InstructorCollection(options);
        this.collection.fetch({
            processData: true,
            reset: true
        });
        this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.itemView = InstructorView;
    }
});

// eslint-disable-next-line no-unused-vars
var CourseListView = BaseListView.extend({

    initialize: function(options) {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new CourseCollection(options);
        this.collection.fetch({
            processData: true,
            reset: true
        });
        this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.itemView = CourseView;
    }

});

// eslint-disable-next-line no-unused-vars
var DocumentListView = BaseListView.extend({

    initialize: function(options) {
        _.bindAll(this, 'renderCollection');

        this.collection = new DocumentCollection(options);
        this.collection.fetch({
            processData: true,
            reset: true
        });
        this.collection.on('reset', this.renderCollection);
        this.itemView = DocumentView;
    }
});

// eslint-disable-next-line no-unused-vars
var StudentListView = BaseListView.extend({

    initialize: function(options) {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new StudentCollection(options);
        this.collection.fetch({
            processData: true,
            reset: true
        });
        this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.itemView = StudentView;
    }

});

// eslint-disable-next-line no-unused-vars
var TeamListView = BaseListView.extend({

    initialize: function(options) {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new TeamCollection(options);
        this.collection.fetch({
            processData: true,
            reset: true
        });
        this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.itemView = TeamView;
    }

});
