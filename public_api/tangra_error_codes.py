
class TangraErrorCodes:
    """Defines all the error codes returned by a FailureResponse
    """
    
    
    # Returned for bad username or password combinations.
    INVALID_CREDENTIALS = "100 Invalid username or passord."
    
    
    # Returned when requesting a stage/stage completion for a participant who has finished all stages.
    INVALID_STAGE_REQUEST = "110 Participant has finished all stages."
    
    
    # Returned when a non POST request was sent to a view requiring POST
    REQUIRES_POST = "120 Request was not a POST request."
    
    
    # Returned when we have an unexpected exception (and don't want to dump the exception info to users)
    SERVER_ERROR = "500 Server error."
    
    
    # Returned when we were unable to save something to the database
    DATABASE_ERROR = "510 There was an error saving the data."
    
    def __init__(self):
        """Doesn't really need to do something this is a purely static class right now."""
        pass