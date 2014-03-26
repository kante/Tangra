from django.test import TestCase, Client

from Tangra.studies.models import User

from ..json_responses import *
from tangra_test_case import *
from public_api.tangra_error_codes import TangraErrorCodes


class LoginTestCase(TangraTestCase):
    """
        Tests:
            /public_api/login
            /public_api/logout
    """
    
    
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="spungo", email="spungo@jibblies.com", password="jibblies")
    
    
    def test_login_invalid_user(self):
        """Tests that login fails with bad credentials."""        
        response = self.client.post('/public_api/login', {'username': 'john', 'password': 'smith'})
        response_string = json.loads(response.content)
        expected_string = json.loads(FailureResponse(TangraErrorCodes.INVALID_CREDENTIALS).content)
        self.assertEqual(response_string, expected_string)
        
        spungo = User.objects.get(username="spungo")
        self.assert_user_is_logged_out(spungo, self.client.session)
        
        response = self.client.get('/public_api/logout')
        response_string = json.loads(response.content)
        expected_string = json.loads(SuccessResponse(None).content)
        self.assertEqual(response_string, expected_string)
    
    
    def test_login_valid_user_bad_pass(self):
        response = self.client.post('/public_api/login', {'username': 'spungo', 'password': 'smith'})
        response_string = json.loads(response.content)
        expected_string = json.loads(FailureResponse(TangraErrorCodes.INVALID_CREDENTIALS).content)
        self.assertEqual(response_string, expected_string)
        
        spungo = User.objects.get(username="spungo")
        self.assert_user_is_logged_out(spungo, self.client.session)
        
        response = self.client.get('/public_api/logout')
        response_string = json.loads(response.content)
        expected_string = json.loads(SuccessResponse(None).content)
        self.assertEqual(response_string, expected_string)
    
    
    def test_login_valid_user_valid_pass(self):
        response = self.client.post('/public_api/login', {'username': 'spungo', 'password': 'jibblies'})
        response_string = json.loads(response.content)
        expected_string = json.loads(SuccessResponse(None).content)
        self.assertEqual(response_string, expected_string)
        
        spungo = User.objects.get(username="spungo")
        self.assert_user_is_logged_in(spungo, self.client.session)
        
        response = self.client.get('/public_api/logout')
        response_string = json.loads(response.content)
        expected_string = json.loads(SuccessResponse(None).content)
        self.assertEqual(response_string, expected_string)
        self.assert_user_is_logged_out(spungo, self.client.session)






        