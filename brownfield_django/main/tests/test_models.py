# from datetime import date

from django.test import TestCase

from factories import UserFactory, UserProfileFactory, TeacherProfileFactory, \
    CourseFactory, HistoryFactory, TeamFactory, \
    PerformedTestFactory, DocumentFactory, AdminProfileFactory, \
    StudentProfileFactoryOne, StudentProfileFactoryTwo, InformationTestFactory


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
        team = TeamFactory()
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


class TestAdminProfileFactory(TestCase):

    def test_unicode(self):
        admin = AdminProfileFactory()
        self.assertEqual(str(admin), admin.user.username)
        self.assertEqual(admin.role(), "administrator")
        self.assertEqual(admin.is_admin(), True)
        self.assertEqual(admin.is_student(), False)


class TestTeacherProfileFactory(TestCase):

    def test_unicode(self):
        teach = TeacherProfileFactory()
        self.assertEqual(str(teach), teach.user.username)
        self.assertEqual(teach.role(), "faculty")
        self.assertEqual(teach.is_teacher(), True)
        self.assertEqual(teach.is_student(), False)


class TestStudentProfileFactory(TestCase):
    '''The UserProfile Factory is a student so we will test that.'''
    def test_unicode(self):
        student = UserProfileFactory()
        self.assertEqual(str(student), student.user.username)
        self.assertEqual(student.role(), "student")
        self.assertEqual(student.is_student(), True)
        self.assertEqual(student.is_admin(), False)


class TestCourseMethods(TestCase):
    '''
    Course model has several helper methods to assist
    in retrieving data for the dashboard.
    '''

    def test_course_get_students(self):
        '''
        Create some students, add to course. Make sure
        students are returned when get_students
        is called on course.
        '''
        student_one = StudentProfileFactoryOne()
        student_two = StudentProfileFactoryTwo()
        course = CourseFactory()
        course.userprofile_set.add(student_one, student_two)
        self.assertTrue(student_one in course.get_students())
        self.assertTrue(student_two in course.get_students())

    def test_course_get_documents(self):
        '''Right now the documents are added in the view,
        so we must add them here manually.'''
        document1 = DocumentFactory()
        document2 = DocumentFactory()
        document3 = DocumentFactory()
        course = CourseFactory()
        course.document_set.add(document1)
        course.document_set.add(document2)
        course.document_set.add(document3)
        self.assertTrue(document1 in course.get_documents())
        self.assertTrue(document2 in course.get_documents())
        self.assertTrue(document3 in course.get_documents())


class TestTeamMethods(TestCase):

    def setUp(self):
        '''Adding student profiles, and history records for testing here'''
        self.student_1 = StudentProfileFactoryOne()
        self.student_2 = StudentProfileFactoryTwo()
        self.team = TeamFactory()

    def test_get_team_members(self):
        self.team.userprofile_set.add(self.student_1)
        self.team.userprofile_set.add(self.student_2)
        self.assertTrue(self.student_1 in self.team.get_team_members())
        self.assertTrue(self.student_2 in self.team.get_team_members())
