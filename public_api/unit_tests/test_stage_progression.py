from django.test import TestCase, Client

from Tangra.studies.models import User

from ..json_responses import *
from tangra_test_case import *


class StudyProgressionTestCase(TangraTestCase):
    """
        Tests:
            /public_api/get_current_stage
            /public_api/finish_current_stage
    """
    
    
    def verify_participants(self):
        """Ensure that the participants were added properly by the study_builder/build_stidy app"""
        self.participant_1 = User.objects.get(username="participant_1")
        self.participant_2 = User.objects.get(username="participant_2")
        self.participant_3 = User.objects.get(username="participant_3")
        
        self.assertIsNotNone(self.participant_1)
        self.assertIsNotNone(self.participant_2)
        self.assertIsNotNone(self.participant_3)
    
    
    def setUp(self):
        self.client = Client()
        # first create a study to test things out
        self.response = self.client.post('/study_builder/build_study', {'study':'unit_test_study'})
        
        # log participant_1 in to the Tangra server
        response = self.client.post('/public_api/login', {'username': 'participant_1', 'password': 'participant_1'})
        
        self.assertEqual(json.loads(response.content), json.loads(SuccessResponse(None).content))
    
    
    def test_appropriate_starting_stage(self):
        """Ensure that participants are starting on the appropriate stage."""
        
        response = self.client.get('/public_api/get_current_stage')
        actual_json_response = json.loads(response.content)
        expected_json_response = json.loads(SuccessResponse(1).content)
        self.assertEqual(actual_json_response, expected_json_response)
    
    
    def test_normal_stage_progression(self):
        """Ensure that participants can move through stages."""
        
        # See if participant_1 is able to move through the study
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(1))
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse(None))
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(2))
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse(None))
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(3))
        
        #ensure no other participant was moved inappropriately
        self.perform_and_verify_query('/public_api/logout', SuccessResponse(None))
        p2_data = {'username': 'participant_2', 'password': 'participant_2'}
        self.perform_and_verify_query('/public_api/login', SuccessResponse(None), "POST", p2_data)
        self.perform_and_verify_query('/public_api/get_current_stage', SuccessResponse(1))
        
        
    def test_excessive_stage_progression(self):
         """Ensure that participants can't move past the last stage in a study."""
         
         # Make sure participant can move through the whole study first
         self.perform_and_verify_query('/public_api/get_current_stage', 1)
         self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse.success_string)
         self.perform_and_verify_query('/public_api/get_current_stage', 2)
         self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse.success_string)
         self.perform_and_verify_query('/public_api/get_current_stage', 3)
         self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse.success_string)
         
         #shouldn't be able to get stages or finish stages if the participant is finished the study
         self.perform_and_verify_query('/public_api/get_current_stage', FailureResponse.failure_string)
         self.perform_and_verify_query('/public_api/finish_current_stage', FailureResponse.failure_string)
         
         #ensure no other participant was moved inappropriately
         self.perform_and_verify_query('/public_api/logout', SuccessResponse.success_string)
         p2_data = {'username': 'participant_2', 'password': 'participant_2'}
         self.perform_and_verify_query('/public_api/login', SuccessResponse.success_string, "POST", p2_data)
         self.perform_and_verify_query('/public_api/get_current_stage', 1)








