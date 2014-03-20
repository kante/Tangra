from django.test import TestCase, Client

from Tangra.studies.models import User

from ..json_responses import *


class LoginTestCase(TestCase):
    """
        A class for testing the login/logout system.
    """
    
    
    def setUp(self):
        self.client = Client()
        User.objects.create(username="spungo", password="jibblies")
    
    
    def test_nothing(self):
        pass