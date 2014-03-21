
from django.test import TestCase, Client

from Tangra.studies.models import User

import os

from ..json_responses import *
from tangra_test_case import *


class FileUploadTestCase(TangraTestCase):
    """Contains the general setUp function for testing the keyless data saving functionality."""
    
    
    def setUp(self):
        self.client = Client()
        # first create a study to test things out
        self.response = self.client.post('/study_builder/build_study', {'study':'unit_test_study'})
        
        self.credentials = {'username': 'participant_1', 'password': 'participant_1'}
        self.perform_and_verify_query('/public_api/login', SuccessResponse.success_string, "POST", self.credentials)
        
        self.participant = User.objects.get(username=self.credentials['username'])
        self.assertIsNotNone(self.participant)




class SimpleFileUploadTest(FileUploadTestCase):
    """
        Tests:
            /public_api/upload_file
    """


    def test_simple_text_file(self):

        # create a temporary file and try to upload it.
        test_file_path = os.path.join(os.path.dirname(__file__), "test_files/simple_text_file.txt")
        with open(test_file_path) as fp:
            self.perform_and_verify_query('/public_api/upload_file', SuccessResponse.success_string, "POST", {'file':fp})

        
        # check to see if the file exists in the user directory

        # check to see if the file is the same as the one we uploaded


        assert False




