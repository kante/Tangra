from django.test import TestCase, Client

from Tangra.studies.models import User


class BasicStudyTestCase(TestCase):
    """
        Test the setup of a basic study with one group, three participants and three stages.
        
        TODO: Some real testing of the study builder...
    """
    
    
    def setUp(self):
        self.client = Client()
        self.response = self.client.post('/study_builder/build_study', {'study':'unit_test_study'})
        
        self.participant_1 = User.objects.get(username="participant_1")
        self.participant_2 = User.objects.get(username="participant_2")
        self.participant_3 = User.objects.get(username="participant_3")
        
    
    
    def test_user_creation(self):
        """Tests that login fails with bad credentials."""
        
        self.assertIsNotNone(self.participant_1)
        self.assertIsNotNone(self.participant_2)
        self.assertIsNotNone(self.participant_3)