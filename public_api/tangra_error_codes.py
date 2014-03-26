
class TangraErrorCodes:
    """Defines all the error codes returned by a FailureResponse
    """
    
    # Returned for bad username or password combinations.
    INVALID_CREDENTIALS = "Invalid username or passord."
    
    
    # Returned when requesting a stage/stage completion for a participant who has finished all stages.
    INVALID_STAGE_REQUEST = "Participant has finished all stages."
    
    
    # Returned when a non POST request was sent to a view requiring POST
    REQUIRES_POST = "Request was not a POST request."
    
    # Returned when we have an unexpected exception (and don't want to dump the exception info to users)
    SERVER_ERROR = "500 Server error."
    
    
    def __init__(self):
        """Doesn't really need to do something this is a purely static class right now."""
        pass