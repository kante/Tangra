from django.test import TestCase, Client

from Tangra.studies.models import User

from ..json_responses import *


class SingleStageTestCase(TestCase):
    """
        Tests:
            /public_api/save_data
            /public_api/get_data
            /public_api/get_data_for_stage
    """
    
    
    def setUp(self):
        self.client = Client()
        # first create a study to test things out
        self.response = self.client.post('/study_builder/build_study', {'study':'unit_test_study'})
    
    
    
    def test_nothing(self):
        pass
