
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
        """Ensure basic saving of data with key works as expected"""
        data_to_save = {"data" : "This is a string I am saving", "key" : "elephants"}
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save)
        
        expected_data = data_to_save["data"]
        good_key_data = {"key" : "elephants"}
        bad_key_data = {"key" : "giraffes"}
        self.perform_and_verify_query('/public_api/get_data_for_key', expected_data, "POST", good_key_data)
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", bad_key_data)


    def test_overwriting_string_in_current_stage(self):
        """Make sure we overwrite old data when saving with a key"""
        data_to_clobber = {"data" : "Clobbered data had better not show up!@!@#!$$$%_+_)//;;.,,", "key" : "elephants"}
        data_to_save = {"data" : "This is a string I am saving", "key" : "elephants"}
        good_key_data = {"key" : "elephants"}
        bad_key_data = {"key" : "giraffes"}

        # first, see if the data is saved appropriately.
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_clobber)
        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_clobber["data"], "POST", good_key_data)
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", bad_key_data)

        # now see if it is clobbered appropriately
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save)
        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_save["data"], "POST", good_key_data)
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", bad_key_data)


    def test_saving_string_in_past_stages(self):
        """Make sure we can access data from a previous stage"""
        data_to_save_stage_1 = {"data" : "This is a 1111 1111 111string I am saving", "key" : "elephants"}
        data_to_save_stage_2 = {"data" : "This is a  222 2 222 2 2 2 string I am saving", "key" : "elephants"}
        data_to_save_stage_3 = {"data" : "333 3 3 3 33 This is a string I am saving", "key" : "elephants"}

        good_key_data = {"key" : "elephants"}
        bad_key_data = {"key" : "giraffes"}
        good_key_data_with_stage = {"key" : "elephants", "stage": 1}
        bad_key_data_with_stage = {"key" : "giraffes", "stage" : 1}

        # save the data for stage 1.
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save_stage_1)
        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_save_stage_1["data"], "POST", good_key_data)
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", bad_key_data)
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_1["data"], "POST", good_key_data_with_stage)
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", bad_key_data_with_stage)

        # move to the next stage
        self.perform_and_verify_query('/public_api/get_current_stage', 1)
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse.success_string)
        self.perform_and_verify_query('/public_api/get_current_stage', 2)

        # save the data for stage 2.
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save_stage_2)
        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_save_stage_2["data"], "POST", good_key_data)
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", bad_key_data)

        #check that old data is still retrievable
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_1["data"], "POST", good_key_data_with_stage)
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", bad_key_data_with_stage)

        # check that new data is retrievable
        good_key_data_with_stage["stage"] = 2
        bad_key_data_with_stage["stage"] = 2
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_2["data"], "POST", good_key_data_with_stage)
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", bad_key_data_with_stage)
        
        # move to the next stage
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse.success_string)
        self.perform_and_verify_query('/public_api/get_current_stage', 3)

        # save the data for stage 3.
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save_stage_3)
        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_save_stage_3["data"], "POST", good_key_data)
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", bad_key_data)

        #check that old data is still retrievable
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_2["data"], "POST", good_key_data_with_stage)
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", bad_key_data_with_stage)
        good_key_data_with_stage["stage"] = 1
        bad_key_data_with_stage["stage"] = 1
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_1["data"], "POST", good_key_data_with_stage)
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", bad_key_data_with_stage)

        # check that new data is retrievable
        good_key_data_with_stage["stage"] = 3
        bad_key_data_with_stage["stage"] = 3
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_3["data"], "POST", good_key_data_with_stage)
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", bad_key_data_with_stage)


    def test_multiple_keys_in_current_stage(self):
        """Ensure basic saving of data with key works as expected"""
        data_to_save1 = {"data" : "This is a string I am saving", "key" : "elephants"}
        data_to_save2 = {"data" : "ASDFRRHEHII$#$848 bloo bloo erouih", "key" : "pink"}
        good_key_data1 = {"key" : "elephants"}
        good_key_data2 = {"key" : "pink"}
        bad_key_data = {"key" : "giraffes"}

        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save1)
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save2)

        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_save1["data"], "POST", good_key_data1)
        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_save2["data"], "POST", good_key_data2)
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", bad_key_data)


    # TODO: test saving multiple keys in a past stage
    def test_saving_multiple_keys_in_past_stages(self):
        """Make sure we can access data with multiple keys from a previous stage"""
        data_to_save_stage_1 = {"data" : "This is a 1111 1111 111string I am saving", "key" : "elephants"}
        other_data_to_save_stage_1 = {"data" : "OTHER !!!!!11111111oneoneoneone ", "key" : "el guapo"}

        data_to_save_stage_2 = {"data" : "This is a  222 2 222 2 2 2 string I am saving", "key" : "elephants"}
        other_data_to_save_stage_2 = {"data" : "other 2 wut wut", "key" : "balloon"}


        # save the data for stage 1.
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save_stage_1)
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", other_data_to_save_stage_1)

        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_save_stage_1["data"], "POST", {"key":"elephants"})
        self.perform_and_verify_query('/public_api/get_data_for_key', other_data_to_save_stage_1["data"], "POST", {"key":"el guapo"})
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", {"key":""})

        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_1["data"], "POST", {"key":"elephants", "stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', other_data_to_save_stage_1["data"], "POST", {"key":"el guapo", "stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", {"key":"rere", "stage":1})

        # move to the next stage
        self.perform_and_verify_query('/public_api/get_current_stage', 1)
        self.perform_and_verify_query('/public_api/finish_current_stage', SuccessResponse.success_string)
        self.perform_and_verify_query('/public_api/get_current_stage', 2)

        # save the data for stage 2.
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", data_to_save_stage_2)
        self.perform_and_verify_query('/public_api/save_data_with_key', SuccessResponse.success_string, "POST", other_data_to_save_stage_2)
        self.perform_and_verify_query('/public_api/get_data_for_key', data_to_save_stage_2["data"], "POST", {"key":"elephants"})
        self.perform_and_verify_query('/public_api/get_data_for_key', other_data_to_save_stage_2["data"], "POST", {"key":"balloon"})
        self.perform_and_verify_query('/public_api/get_data_for_key', FailureResponse.failure_string, "POST", {"key":""})

        # make sure old data was not clobbered
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_1["data"], "POST", {"key":"elephants", "stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', other_data_to_save_stage_1["data"], "POST", {"key":"el guapo", "stage":1})
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", {"key":"rere", "stage":1})

        # make sure new data is still there
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', data_to_save_stage_2["data"], "POST", {"key":"elephants", "stage":2})
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', other_data_to_save_stage_2["data"], "POST", {"key":"balloon", "stage":2})
        self.perform_and_verify_query('/public_api/get_data_for_stage_and_key', FailureResponse.failure_string, "POST", {"key":"rere", "stage":2})



    # TODO: test for bad inputs
    # TODO: test for corner cases
