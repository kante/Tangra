from django.test import TestCase
import json


class TangraTestCase(TestCase):
    """
        TangraTestCase contains useful stuff for testing a Tangra instance.
    """
    
    
    def perform_and_verify_query(self, url, expected_response, request_type="GET", data={}):
        """Perform the selected query and assert that the response is as expected."""
        if request_type == "GET":
            response = self.client.get(url, data=data)
        else:
            response = self.client.post(url, data=data)
        
        actual_response = json.loads(response.content)
        self.assertEqual(actual_response, expected_response)
    
    
    def assert_user_is_logged_in(self, user, session):
        """Asserts that the supplied user is logged in based on the supplied session."""
        self.assertIn('_auth_user_id', session)   
        self.assertEqual(session['_auth_user_id'], user.pk)
    
    
    def assert_user_is_logged_out(self, user, session):
        """Asserts that the supplied user is logged out based on the supplied session."""
        if '_auth_user_id' in session:
            self.assertEqual(session['_auth_user_id'], user.pk)
        else:
            self.assertTrue(True)



