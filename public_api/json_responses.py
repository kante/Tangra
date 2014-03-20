from django.http import HttpResponse

import json


class JsonResponse(HttpResponse):
    """
        A general class for returning JSON documents as HttpResponses
    """
    
    def __init__(self, obj):
        """Return a JsonResponse with the JSON representing obj.
        
        Reqiures: obj is parseable by json.dumps.
        """
        super(JsonResponse, self).__init__(json.dumps(obj), content_type="application/json")


class NumberResponse(JsonResponse):
    """
        The NumberResponse is a json response object that contains a single json encoded number.
    """
    
    
    def __init__(self, number):
        """Create a default HttpResponse subclass for communicating a Tangra failure."""
        super(NumberResponse, self).__init__(number)


class FailureResponse(JsonResponse):
    """
        The FailureResponse is a json response object that contains the single json string 'SUCCESS'
    """
    failure_string = "FAILURE"
    
    
    def __init__(self):
        """Create a default HttpResponse subclass for communicating a Tangra failure."""
        super(FailureResponse, self).__init__(self.failure_string)


class SuccessResponse(JsonResponse):
    """
        The SuccessResponse is a json response object that contains the single json string 'SUCCESS'
    """
    success_string = "SUCCESS"
    
    
    def __init__(self):
        """Create a default HttpResponse subclass for communicating a Tangra success."""
        super(SuccessResponse, self).__init__(self.success_string)


# TODO: list response? 


    