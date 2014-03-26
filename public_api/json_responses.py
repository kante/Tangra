from django.http import HttpResponse

import json


class JsonResponse(HttpResponse):
    """
        A general class for returning JSON documents as HttpResponses
    """
    failure_string = "FAILURE"
    success_string = "SUCCESS"
    
    def __init__(self, is_failure, data_or_message):
        """Return a JsonResponse with a success/failure indicator, a failure message if required, and a data
        field for returning information to the client
        
        Keyword Aruments:
            is_failure - A Boolean value indicating whether the request was successful or not.
            data_or_message - A failure message or a string with data to return depending on the value of is_failure
        """
        
        response_object =   { 
                                "status" : self.failure_string if is_failure else self.success_string,
                                "error_message" : data_or_message if is_failure else None,
                                "data" : None if is_failure else data_or_message
                            }
        
        super(JsonResponse, self).__init__(json.dumps(response_object), content_type="application/json")


class FailureResponse(JsonResponse):
    """
        The FailureResponse is a json response object that contains the single json string 'SUCCESS'
    """
    
    
    def __init__(self, failure_message):
        """Create a default HttpResponse subclass for communicating a Tangra failure."""
        super(FailureResponse, self).__init__(True, failure_message)


class SuccessResponse(JsonResponse):
    """
        The SuccessResponse is a json response object that contains the single json string 'SUCCESS'
    """    
    
    def __init__(self, data):
        """Create a default HttpResponse subclass for communicating a Tangra success."""
        super(SuccessResponse, self).__init__(False, data)


# TODO: list response? 


    