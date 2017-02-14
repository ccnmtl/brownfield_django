from django.test.testcases import TestCase

from brownfield_django.main.tests.factories import UserFactory,\
    UserProfileFactory
from brownfield_django.mixins import instructor_or_admin, user_is_admin


class MixinsTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.student = UserProfileFactory().user
        self.teacher = UserProfileFactory(profile_type='TE').user
        self.admin = UserProfileFactory(profile_type='AD').user

    def test_instructor_or_admin(self):
        self.assertFalse(instructor_or_admin(self.user))
        self.assertFalse(instructor_or_admin(self.student))
        self.assertTrue(instructor_or_admin(self.teacher))
        self.assertTrue(instructor_or_admin(self.admin))

    def test_user_is_admin(self):
        self.assertFalse(user_is_admin(self.user))
        self.assertFalse(user_is_admin(self.student))
        self.assertFalse(user_is_admin(self.teacher))
        self.assertTrue(user_is_admin(self.admin))
