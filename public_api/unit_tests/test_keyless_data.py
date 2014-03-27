from django.test import TestCase, Client

from Tangra.studies.models import User

from ..json_responses import *
from tangra_test_case import *


class KeylessDataTestCase(TangraTestCase):
    """Contains the general setUp function for testing the keyless data saving functionality."""
    
    
    def setUp(self):
        self.client = Client()
        # first create a study to test things out
        self.response = self.client.post('/study_builder/build_study', {'study':'unit_test_study'})
        
        self.credentials = {'username': 'participant_1', 'password': 'participant_1'}
        self.perform_and_verify_query('/public_api/login', SuccessResponse(None), "POST", self.credentials)
        
        self.participant = User.objects.get(username=self.credentials['username'])
        self.assertIsNotNone(self.participant)


class MultipleStageTestCase(KeylessDataTestCase):
    """
        Tests:
            /public_api/save_data
            /public_api/get_data_for_stage
    """
    
    
    def test_single_string_in_past_stage(self):
        data_to_save = {"data" : "This is a string I am saving"}
        self.perform_and_verify_query('/public_api/save_data', SuccessResponse(None), "POST", data_to_save)
        
        expected_data = [data_to_save["data"]]
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse(expected_data))
        
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(1))
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse(None))
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(2))
        
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse(expected_data), "POST", {"stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":2})


    def test_single_string_in_current_stage_none_in_past(self):
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse([]))
        
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(1))
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse(None))
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(2))
        
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":2})

        data_to_save = {"data" : "This is a string I am saving"}
        self.perform_and_verify_query('/public_api/save_data', SuccessResponse(None), "POST", data_to_save)
        expected_data = [data_to_save["data"]]
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse(expected_data))
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse(expected_data), "POST", {"stage":2})


    def test_mupltiple_strings_in_current_stage_none_in_past(self):
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse([]))
        
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(1))
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse(None))
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(2))
        
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":2})

        data_to_save = {"data" : "This is a string I am saving"}
        expected_data = []
        for i in range(10):
            self.perform_and_verify_query('/public_api/save_data', SuccessResponse(None), "POST", data_to_save)
            expected_data.append(data_to_save["data"])

        self.perform_and_verify_query('/public_api/get_data', SuccessResponse(expected_data))
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse(expected_data), "POST", {"stage":2})


    def test_mupltiple_strings_in_past_stage_none_in_current(self):
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse([]))
        
        data_to_save = {"data" : "This is a string I am saving"}
        expected_data = []
        for i in range(10):
            self.perform_and_verify_query('/public_api/save_data', SuccessResponse(None), "POST", data_to_save)
            expected_data.append(data_to_save["data"])
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse(expected_data), "POST", {"stage":1})
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse(expected_data))

        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(1))
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse(None))
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(2))
        
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse([]))
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse(expected_data), "POST", {"stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":2})


    def test_multiple_strings_in_middle_stage(self):
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse(None))
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(2))

        data_to_save = {"data" : "This is a string I am saving"}
        expected_data = []
        for i in range(10):
            self.perform_and_verify_query('/public_api/save_data', SuccessResponse(None), "POST", data_to_save)
            expected_data.append(data_to_save["data"])
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse(None))
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(3))

        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse(expected_data), "POST", {"stage":2})
        self.perform_and_verify_query('/public_api/get_data_for_stage', SuccessResponse([]), "POST", {"stage":3})


class SingleStageTestCase(KeylessDataTestCase):
    """
        Tests:
            /public_api/save_data
            /public_api/get_data
    """
    
    
    def test_retrieve_with_no_data(self):
        expected_data = []
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse(expected_data))
    
    
    def test_saving_single_string(self):
        data_to_save = {"data" : "This is a string I am saving"}
        self.perform_and_verify_query('/public_api/save_data', SuccessResponse(None), "POST", data_to_save)
        
        expected_data = [data_to_save["data"]]
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse(expected_data))
    
    
    def test_saving_multiple_strings(self):
        data_to_save = {"data" : "This is a string I am saving"}
        self.perform_and_verify_query('/public_api/save_data', SuccessResponse(None), "POST", data_to_save)
        
        more_data = {"data" : "ERUJSADFNN848349534%#$%3453450912=0--09234][]"}
        self.perform_and_verify_query('/public_api/save_data', SuccessResponse(None), "POST", more_data)
        
        expected_data = [data_to_save["data"], more_data["data"]]
        self.perform_and_verify_query('/public_api/get_data', SuccessResponse(expected_data))











