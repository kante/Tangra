
from django.test import TestCase, Client

from Tangra.studies.models import User

from ..json_responses import *
from tangra_test_case import *


class KeyedDataTestCase(TangraTestCase):
    """Contains the general setUp function for testing the keyless data saving functionality."""
    
    
    def setUp(self):
        self.client = Client()
        # first create a study to test things out
        self.response = self.client.post('/study_builder/build_study', {'study':'unit_test_study'})
        
        self.credentials = {'username': 'participant_1', 'password': 'participant_1'}
        self.perform_and_verify_query('/public_api/login', SuccessResponse.success_string, "POST", self.credentials)
        
        self.participant = User.objects.get(username=self.credentials['username'])
        self.assertIsNotNone(self.participant)


class MultipleStageTestCase(KeyedDataTestCase):
    """
        Tests:
            /public_api/save_data_with_key
            /public_api/get_data_for_key
            /public_api/get_data_for_stage_and_key
    """


    def test_single_string_in_current_stage(self):
        data_to_save = {"data" : "This is a string I am saving", "key" : "elephants"}
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save)
        
        expected_data = data_to_save["data"]
        good_key_data = {"key" : "elephants"}
        bad_key_data = {"key" : "giraffes"}
        self.perform_and_verify_query('/public_api/get_data_for_key', expected_data, "POST", good_key_data)
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", bad_key_data)






