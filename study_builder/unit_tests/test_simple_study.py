from django.test import TestCase, Client


class BasicStudyTestCase(TestCase):
    """
        Test the setup of a basic study with one group, three participants and three stages.
    """
    
    
    def setUp(self):
        self.client = Client()
        self.response = self.client.post('/study_builder/build_study', {'study':'unit_test_study'})
    
    
    def test_user_creation(self):
        """Tests that login fails with bad credentials."""        
        print "ASDFSADF", self.response