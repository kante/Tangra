
from django.test import TestCase, Client

from Tangra.studies.models import User

from json_responses import *


class BasicLoginTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="spungo", password="jibblies")
    
    
    def test_login(self):
        """Tests that login succeeds with correct credentials, and fails otherwise."""
        client = Client()
        
        response = client.post('/public_api/login', {'username': 'john', 'password': 'smith'})
        response_string = json.loads(response.content)
        self.assertEqual(response_string, FailureResponse.failure_string)
        
        
        response = client.get('/public_api/logout')
        response_string = json.loads(response.content)
        self.assertEqual(response_string, SuccessResponse.success_string)







        