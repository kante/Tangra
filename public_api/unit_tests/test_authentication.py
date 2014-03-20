from django.test import TestCase, Client

from Tangra.studies.models import User

from ..json_responses import *


class LoginTestCase(TestCase):
    """
        Tests:
            /public_api/login
            /public_api/logout
    """
    
    
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="spungo", email="spungo@jibblies.com", password="jibblies")
        
    
    
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
    
    
    def test_login_invalid_user(self):
        """Tests that login fails with bad credentials."""        
        response = self.client.post('/public_api/login', {'username': 'john', 'password': 'smith'})
        response_string = json.loads(response.content)
        self.assertEqual(response_string, FailureResponse.failure_string)
        
        spungo = User.objects.get(username="spungo")
        self.assert_user_is_logged_out(spungo, self.client.session)
        
        response = self.client.get('/public_api/logout')
        response_string = json.loads(response.content)
        self.assertEqual(response_string, SuccessResponse.success_string)
    
    
    def test_login_valid_user_bad_pass(self):
        response = self.client.post('/public_api/login', {'username': 'spungo', 'password': 'smith'})
        response_string = json.loads(response.content)
        self.assertEqual(response_string, FailureResponse.failure_string)
        
        spungo = User.objects.get(username="spungo")
        self.assert_user_is_logged_out(spungo, self.client.session)
        
        response = self.client.get('/public_api/logout')
        response_string = json.loads(response.content)
        self.assertEqual(response_string, SuccessResponse.success_string)
    
    
    def test_login_valid_user_valid_pass(self):
        response = self.client.post('/public_api/login', {'username': 'spungo', 'password': 'jibblies'})
        response_string = json.loads(response.content)
        self.assertEqual(response_string, SuccessResponse.success_string)
        
        spungo = User.objects.get(username="spungo")
        self.assert_user_is_logged_in(spungo, self.client.session)
        
        response = self.client.get('/public_api/logout')
        response_string = json.loads(response.content)
        self.assertEqual(response_string, SuccessResponse.success_string)
        self.assert_user_is_logged_out(spungo, self.client.session)






        