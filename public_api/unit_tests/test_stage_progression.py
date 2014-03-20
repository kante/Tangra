from django.test import TestCase, Client

from Tangra.studies.models import User

from ..json_responses import *


class StudyProgressionTestCase(TestCase):
    """
        Tests:
            /public_api/get_current_stage
            /public_api/finish_current_stage
    """
    
    
    def setUp(self):
        self.client = Client()
        # first create a study to test things out
        self.response = self.client.post('/study_builder/build_study', {'study':'unit_test_study'})
        
        self.participant = User.objects.get(username="participant_1")
        self.assertIsNotNone(self.participant)
        
        # log participant_1 in to the Tangra server
        response = self.client.post('/public_api/login', {'username': 'participant_1', 'password': 'participant_1'})
        
        self.assertEqual(json.loads(response.content), SuccessResponse.success_string)
        
    
    
    def test_appropriate_starting_stage(self):
        """Ensure that participants are starting on the appropriate stage."""
        
        response = self.client.get('/public_api/get_current_stage')
        stage_num = json.loads(response.content)
        self.assertEqual(stage_num, 1)


