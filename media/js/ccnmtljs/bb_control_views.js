/* global User: true, InstructorCollection: true */
/* global CourseListView: true, InstructorListView: true */
/* global StudentListView: true, TeamListView: true  */
/* eslint-disable no-unused-vars */
//jscs:disable requireCamelCaseOrUpperCaseIdentifiers

var BaseManagementView = Backbone.View.extend({

    showAddItemForm: function(e) {
        e.preventDefault();
        this.addForm.show();
        this.addBtn.hide();
    },

    hideAddItemForm: function(e) {
        // assume its probably good practice to remove form errors here while
        // were at it
        this.addForm.find('.error-msg').remove();
        this.addForm.hide();
        this.addBtn.show();
    },

    showFormError: function(formSelector) {
        if ((jQuery(formSelector).has('.form_error').length) === 0) {
            this.addForm.append(
                '<p class=".form-error"><b>Something went wrong, ' +
                'please try again.</b></p>');
        }
    },

    removeFormError: function(formSelector) {
        /*
         * upon successful submission we want to remove any form errors if there
         * are any
         */
        if (jQuery(formSelector).has('.form_error').length > 0) {
            this.addForm.remove('<p class=".form-error"><b>Something went ' +
                'wrong, please try again.</b></p>');
        }
    },

    onlyLetters: function(selectorString, errorElement) {
        var check = jQuery(selectorString).val();
        if (/[^a-zA-Z]/.test(check)) {
            if ((jQuery(errorElement).has('.chars-only').length) === 0) {
                jQuery(errorElement).append(
                    '<b class="error-msg chars-only" style="color:red"> ' +
                    'Please only use letters of the alphabet</b>');
            }
            return false;
        }
        return true;
    },

    isEmpty: function(selectorString, errorElement, errorMsg) {
        var check = jQuery(selectorString).val();
        if (check === null || check === '') {
            if ((jQuery(errorElement).has('.is-empty').length) === 0) {
                jQuery(errorElement).append(
                    '<b class="error-msg is-empty" ' +
                    'style="color:red; display: block">' +
                    String(errorMsg) + '</b>');
            }
            return true;
        }
        return false;
    },

    clearFormErrors: function(selectorString) {
        jQuery(selectorString + ' .error-msg').remove();
    }
});

var ManageCoursesView = Backbone.View.extend({
    events: {
        'click .add-crs': 'showCourseForm',
        'click .cncl-add-crs': 'hideAddForm',
        'click .submit': 'addCourse'
    },

    initialize: function(options) {
        _.bindAll(this, 'addCourse', 'showCourseForm',
            'hideAddForm', 'validateForm');
        this.options = options;
        this.currentUser = new User({id: options.user_id});

        this.courseListView = new CourseListView({el: this.options.listEl});
        this.courseListView.collection.fetch({wait: true});
        this.userList = new InstructorCollection();
        this.userList.fetch({wait: true});
    },

    showCourseForm: function(e) {
        jQuery('.add-crs').hide();
        // how to bind this/make it wait for results from server
        this.userList.fetch({wait: true});
        this.userList.forEach(function(model) {

            jQuery('#id_professor').append(
                '<option value="' + String(model.attributes.id) +
                '">' + String(model.attributes.first_name) +
                ' ' + String(model.attributes.last_name)  +
                '</option>');
        });

        jQuery('#create-course-form').show();
    },

    hideAddForm: function() {
        if (jQuery('#create-course-form').has('.error-msg').length !== 0) {
            jQuery('#create-course-form .error-msg').remove();
        }
        if (jQuery('#create-course-form').has('.form-error').length !== 0) {
            jQuery('#create-course-form .form-error').remove();
        }
        this.$('#create-course-form').css('display', 'none');
        jQuery('.add-crs').show();
    },

    validateForm: function() {
        var isValid = true;
        var $elt;
        var courseName = jQuery('#id_course_name').val();
        var startingBudget = jQuery('#id_course_startingBudget').val();
        var courseMessage = jQuery('#id_course_message').val();

        if (courseName === null || courseName === '') {
            isValid = false;
            $elt = jQuery('.course-name-block');
            if ($elt.has('.error-msg').length === 0) {
                $elt.append('<p class="error-msg" style="color:#ff0000">' +
                'Please enter a valid course name.</p>');
            }
        }
        if (startingBudget === null || startingBudget === '') {
            isValid = false;
            $elt = jQuery('.course-budget-block');
            if ($elt.has('.error-msg').length === 0) {
                $elt.append('<p class="error-msg" style="color:#ff0000">' +
                        'Please enter a valid starting budget ' +
                'for your course.</p>');
            }
        }
        if (courseMessage === null || courseMessage === '') {
            isValid = false;
            $elt = jQuery('.course-message-block');
            if ($elt.has('.error-msg').length === 0) {
                $elt.append('<p class="error-msg" style="color:#ff0000">' +
                'Please enter a valid course message.</p>');
            }
        }
        return isValid;
    },

    addCourse: function(evt) {
        evt.preventDefault();
        var professor = jQuery('#id_professor').find('option:selected').val();

        /* TODO: change this no url anymore */
        if (professor === null || professor === undefined) {
            /*
             * Seems this needs to be user url - maybe if I changed to model
             * instead of hyperlink serializer ID will be acceptable?
             */
            professor = this.currentUser.get('id');
        }

        if (this.validateForm()) {
            this.courseListView.collection.create({
                name: jQuery('#id_course_name').val(),
                startingBudget: jQuery('#id_course_startingBudget').val(),
                message: jQuery('#id_course_message').val(),
                professor: professor,
                archive: false
            }, {
                success: function(model, response) {
                    jQuery('#id_course_name').val('');
                    jQuery('#id_course_startingBudget').val('');
                    jQuery('#id_course_message').val('');
                    jQuery('#create-course-form').hide();
                    jQuery('.add-crs').show();
                    if (jQuery('#create-course-form')
                        .has('.error-msg').length !== 0) {
                        jQuery('#create-course-form .error-msg').remove();
                    }
                    if (jQuery('#create-course-form')
                        .has('.form-error').length !== 0) {
                        jQuery('#create-course-form .form-error').remove();
                    }
                },
                error: function(model, response) {
                    if ((jQuery('#create-course-form')
                        .has('.form-error').length) === 0) {
                        jQuery('#create-course-form')
                            .append('<p class="error-msg form-error">' +
                            'Something went wrong, please try again.' +
                            '</p>');
                    }
                },
                wait: true
            });
        }
        return false;
    }
});// End UserControlView

var ManageInstructorsView = BaseManagementView.extend({
    events: {
        'click .add-instructor-btn': 'showAddItemForm',
        'click .cncl-add-inst': 'hideAddItemForm',
        'click .save-instructor': 'addInstructor'
    },

    initialize: function(options) {
        _.bindAll(this, 'addInstructor', 'showAddItemForm',
            'hideAddItemForm', 'isEmpty');
        this.instructorCollectionView = new InstructorListView({
            el: jQuery('.instructor-list'),
        });
        this.addForm = jQuery('.add-instructor-frm');
        this.addBtn = jQuery('.add-instructor-btn');
    },
    findInstructor: function(email) {
        var attr = {'email': email};
        return this.instructorCollectionView.collection.findWhere(attr);
    },
    validAddForm: function() {
        var isValid = true;
        this.$el.find('b.error-msg').remove();

        if (this.isEmpty('.add-instructor-frm input.instructor-frst-name',
            '.inst-first-name', 'Please enter a first name.')) {
            isValid = false;
        }
        if (this.isEmpty('.add-instructor-frm input.instructor-last-name',
            '.inst-last-name', 'Please enter a last name.')) {
            isValid = false;
        }

        var email = jQuery('.add-instructor-frm input.instructor-email').val();
        if (this.isEmpty('.add-instructor-frm input.instructor-email',
            '.inst-email', 'Please enter a email address.')) {
            isValid = false;
        } else if (email.indexOf('@') === -1 || email.indexOf('.') === -1) {
            isValid = false;
            jQuery('.inst-email')
                .append('<b class="error-msg" style="color:red">' +
                'Please enter a valid email.</b>');
        } else if (this.findInstructor(email) !== undefined) {
            isValid = false;
            jQuery('.instructor-form-area')
                .append('<b class="error-msg" style="color:red">' +
                'An instructor with this email already exists.</b>');
        }
        return isValid;
    },
    addInstructor: function(e) {
        e.stopPropagation();

        if (!this.validAddForm()) {
            return false;
        }

        this.instructorCollectionView.collection.create({
            first_name: jQuery('.instructor-frst-name').val(),
            last_name: jQuery('.instructor-last-name').val(),
            email: jQuery('.instructor-email').val()
        }, {
            success: function(model, response) {
                jQuery('.add-instructor-frm').hide();
                jQuery('.add-instructor-btn').show();
                jQuery('.instructor-frst-name').val('');
                jQuery('.instructor-last-name').val('');
                jQuery('.instructor-email').val('');
                if (jQuery('.add-instructor-frm')
                    .has('.error-msg').length !== 0) {
                    jQuery('.add-instructor-frm .error-msg').remove();
                }
                if (jQuery('.add-instructor-frm')
                    .has('.form-error').length !== 0) {
                    jQuery('.add-instructor-frm .form-error').remove();
                }

            },
            error: function(model, response) {
                if ((jQuery('.add-instructor-frm')
                    .has('.form-error').length) === 0) {
                    jQuery('.add-instructor-frm')
                        .append('<p class="error-msg form-error">' +
                            'Something went wrong, ' +
                    'please try again.</p>');
                }
            },
            wait: true
        }); // end create

        return false;
    }
});

var StudentControlView = BaseManagementView.extend({

    events: {
        'click .add-std-btn': 'showAddItemForm',
        'click .cncl-add-std': 'hideAddItemForm',
        'click .student_submit': 'addStudent'
    },

    initialize: function(options) {
        _.bindAll(this, 'addStudent', 'hideAddItemForm', 'showAddItemForm');

        this.studentCollectionView = new StudentListView({
            el: jQuery('.student-list'),
            course: options.course
        });
        this.addForm = jQuery('.add-std-frm');
        this.addBtn = jQuery('.add-std-btn');
    },
    addStudent: function(e) {
        e.preventDefault();
        var $elt;

        if (this.validAddForm()) {
            this.studentCollectionView.collection.create({
                first_name: jQuery('.frst-name').val(),
                last_name: jQuery('.last-name').val(),
                email: jQuery('.email').val()
            }, {
                success: function(model, response) {
                    /* seems you cannot access outer function from here... */
                    jQuery('.add-std-frm').hide();
                    jQuery('.add-std-btn').show();
                    jQuery('.frst-name').val('');
                    jQuery('.last-name').val('');
                    jQuery('.email').val('');
                    $elt = jQuery('.add-std-frm');
                    if ($elt.has('.error-msg').length !== 0) {
                        jQuery('.add-std-frm .error-msg').remove();
                    }
                    if ($elt.has('.form-error').length !== 0) {
                        jQuery('.add-std-frm .form-error').remove();
                    }
                },
                error: function(model, response) {
                    $elt = jQuery('.add-std-frm');
                    if ($elt.has('.form-error').length === 0) {
                        $elt.append('<p class="error-msg form-error">' +
                                'Something went wrong, please try again.' +
                        '</p>');
                    }
                },
                wait: true,
                url: this.studentCollectionView.collection.url()
            });
        }
        return false;
    },

    validAddForm: function() {
        var isValid = true;

        if (this.isEmpty('.add-std-frm input.frst-name',
            '.first-name-box', 'Please enter a first name.')) {
            isValid = false;
        }
        if (this.isEmpty('.add-std-frm input.last-name',
            '.last-name-box', 'Please enter a last name.')) {
            isValid = false;
        }
        if (this.isEmpty('.add-std-frm input.email',
            '.email-box', 'Please enter a email.')) {
            isValid = false;
        } else if ((jQuery('.add-std-frm input.email').val().length) !== 0) {
            // check whatever they put for email looks something like an actual
            // address
            var $elt = jQuery('.add-std-frm input.email');
            if ($elt.val().indexOf('@')  === -1 &&
                    $elt.val().indexOf('.') === -1) {
                isValid = false;
                if ((jQuery('.email-box').has('b').length) === 0) {
                    jQuery('.email-box')
                        .append('<b class="error-msg" style="color:red">' +
                        'Please enter a valid email.</b>');
                }
            }
        }

        return isValid;
    }
});

var TeamControlView = BaseManagementView.extend({
    events: {
        'click .add-team-btn': 'showAddItemForm',
        'click .cncl-add-team': 'hideAddItemForm',
        'click .team_submit': 'addTeam'
    },

    initialize: function(options) {
        this.teamCollectionView = new TeamListView({
            el: jQuery('.team-list'),
            course: options.course
        });
        this.addForm = jQuery('.add-team-frm');
        this.addBtn = jQuery('.add-team-btn');
    },

    validAddForm: function() {
        var isValid = true;

        if ((jQuery('.add-team-frm input.team-name').val().length) === 0) {
            isValid = false;
            var $elt = jQuery('.add-team-frm .team-name-box');
            if ($elt.has('b').length === 0) {
                $elt.append('<b class="error-msg" style="color:red">' +
                'Please enter a team name.</b>');
            }
        }
        return isValid;
    },

    addTeam: function(evt) {
        evt.preventDefault();
        var $elt = jQuery('.add-team-frm');

        if (this.validAddForm()) {
            this.teamCollectionView.collection.create({
                team_name: jQuery('.team-name').val()
            }, {
                success: function(model, response) {
                    if ($elt.has('.error-msg').length !== 0) {
                        jQuery('.add-team-frm .error-msg').remove();
                    }
                    if ($elt.has('.form-error').length !== 0) {
                        jQuery('.add-team-frm .form-error').remove();
                    }
                    jQuery('.team-name').val('');
                    jQuery('.add-team-frm').hide();
                    jQuery('.add-team-btn').show();
                },
                error: function(model, response) {
                    if ($elt.has('.form-error').length === 0) {
                        $elt.append('<p class="error-msg form-error">' +
                                'Something went wrong, please try again.' +
                        '</p>');
                    }
                },
                wait: true,
                url: this.teamCollectionView.collection.url()
            });
        }
        return false;
    }
});
