from django.test import TestCase

from factories import UserFactory, UserProfileFactory, \
    CourseFactory, HistoryFactory, TeamFactory, \
    PerformedTestFactory, InformationTestFactory


'''Very basic model tests...'''


class TestUserFactory(TestCase):

    def test_unicode(self):
        user = UserFactory()
        self.assertEqual(str(user), user.username)


class TestCourseFactory(TestCase):

    def test_unicode(self):
        course = CourseFactory()
        self.assertEqual(str(course), course.name)

    def test_get_student_users_empty(self):
        course = CourseFactory()
        r = course.get_student_users()
        self.assertEqual(r.count(), 0)


class TestTeamFactory(TestCase):

    def test_unicode(self):
        team = TeamFactory(user=UserFactory())
        self.assertEqual(str(team), team.user.username)


class TestHistoryFactory(TestCase):

    def test_unicode(self):
        his = HistoryFactory()
        self.assertEqual(str(his), '%s - %s' % (his.description, his.team))


class TestPerformedTestFactory(TestCase):

    def test_unicode(self):
        pt = PerformedTestFactory()
        self.assertEqual(str(pt), '%s - %s' % (pt.testDetails, pt.paramString))


class TestInformationTestFactory(TestCase):

    def test_unicode(self):
        inf_t = InformationTestFactory()
        self.assertEqual(str(inf_t),
                         '%s - %s' % (inf_t.infoType, inf_t.internalName))


class TestUserProfileFactory(TestCase):

    def test_unicode(self):
        up = UserProfileFactory()
        self.assertEqual(str(up), up.user.username)


class TestAdminProfile(TestCase):

    def test_unicode(self):
        admin = UserProfileFactory(user=UserFactory(username='admin',
                                                    first_name='admin',
                                                    last_name='admin'),
                                   profile_type='AD')
        self.assertEqual(str(admin), admin.user.username)
        self.assertEqual(admin.role(), "administrator")
        self.assertEqual(admin.is_admin(), True)
        self.assertEqual(admin.is_student(), False)
        self.assertEqual(admin.display_name(), "admin - admin")


class TestTeacherProfile(TestCase):

    def test_unicode(self):
        teach = UserProfileFactory(user=UserFactory(username='teacher',
                                                    first_name='teacher',
                                                    last_name='teacher'),
                                   profile_type='TE')
        self.assertEqual(str(teach), teach.user.username)
        self.assertEqual(teach.role(), "faculty")
        self.assertEqual(teach.is_teacher(), True)
        self.assertEqual(teach.is_student(), False)
        self.assertEqual(teach.is_admin(), False)
        self.assertEqual(teach.display_name(), "teacher - teacher")


class TestStudentProfile(TestCase):
    '''The UserProfile Factory is a student so we will test that.'''
    def test_unicode(self):
        student = UserProfileFactory(user=UserFactory(username='student',
                                                      first_name='student',
                                                      last_name='student'),
                                     profile_type='ST')
        self.assertEqual(str(student), student.user.username)
        self.assertEqual(student.role(), "student")
        self.assertEqual(student.is_student(), True)
        self.assertEqual(student.is_admin(), False)
        self.assertEqual(student.display_name(), "student - student")


class TestCourseMethods(TestCase):
    '''
    Course model has several helper methods to assist
    in retrieving data for the dashboard.
    '''

    def setUp(self):
        self.course = CourseFactory(name="Course Methods")
        self.student1 = UserProfileFactory(
            user=UserFactory(username='student1'),
            profile_type='ST', course=self.course)
        self.student2 = UserProfileFactory(
            user=UserFactory(username='student2'),
            profile_type='ST', course=self.course)
        self.student3 = UserProfileFactory(
            user=UserFactory(username='student3'),
            profile_type='ST', course=self.course)
        self.student4 = UserProfileFactory(
            user=UserFactory(username='student4'),
            profile_type='ST', course=self.course)

    def test_course_get_students(self):
        '''
        Make sure students are returned when get_students
        is called on course.
        '''
        self.assertTrue(self.student1 in self.course.get_students())
        self.assertTrue(self.student2 in self.course.get_students())
        self.assertTrue(self.student3 in self.course.get_students())
        self.assertTrue(self.student4 in self.course.get_students())

    def test_course_get_documents(self):
        '''Updated the Course model to add the documents when created
        instead of adding them in the view. Should have 8 documents.'''
        self.assertEqual(len(self.course.get_documents()), 8)


class TestTeamMethods(TestCase):

    def setUp(self):
        '''Adding student profiles, and history records for testing here'''
        self.team = TeamFactory(user=UserFactory())
        self.student1 = UserProfileFactory(
            user=UserFactory(username='student1'),
            profile_type='ST', team=self.team)
        self.student2 = UserProfileFactory(
            user=UserFactory(username='student2'),
            profile_type='ST', team=self.team)
        self.history_record_one = HistoryFactory(team=self.team)
        self.history_record_two = HistoryFactory(team=self.team)

    def test_get_team_members(self):
        self.assertTrue(self.student1 in self.team.get_team_members())
        self.assertTrue(self.student2 in self.team.get_team_members())

    def test_get_team_history(self):
        self.assertTrue(
            self.history_record_one in self.team.get_team_history())
        self.assertTrue(
            self.history_record_two in self.team.get_team_history())


class TestHistoryMethods(TestCase):

    def setUp(self):
        '''Adding performed tests and information records to test
        history objects here'''
        self.team = TeamFactory(user=UserFactory())
        self.history = HistoryFactory(team=self.team)
        self.first_test_performed = PerformedTestFactory(history=self.history)
        self.second_test_performed = PerformedTestFactory(history=self.history)
        self.first_informtion_record = InformationTestFactory(
            history=self.history)
        self.second_information_record = InformationTestFactory(
            history=self.history)

    def test_get_tests_performed(self):
        self.assertTrue(
            self.first_test_performed in self.history.get_tests_performed())
        self.assertTrue(
            self.second_test_performed in self.history.get_tests_performed())

    def test_get_information(self):
        self.assertTrue(
            self.first_informtion_record in self.history.get_information())
        self.assertTrue(
            self.second_information_record in self.history.get_information())
