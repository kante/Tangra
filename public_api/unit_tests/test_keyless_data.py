from django.test import TestCase, Client

from Tangra.studies.models import User

from json_responses import *


class LoginTestCase(TestCase):
    """
        A class for testing the login/logout system.
    """
    
    
    def setUp(self):
        self.client = Client()
        User.objects.create(username="spungo", password="jibblies")
    
    
    def assert_user_is_logged_in(self, user, session):
        """Asserts that the supplied user is logged in based on the supplied session."""
        self.assertIn('_auth_user_id', session)   
        self.assertEqual(session['_auth_user_id'], user.pk)
